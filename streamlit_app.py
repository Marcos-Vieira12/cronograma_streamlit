import streamlit as st
import io
from main import (
    carregar_catalogo,
    configurar_metricas_comuns,
    atualizar_metricas_r1,
    atualizar_metricas_r2,
    atualizar_metricas_r3,
    atualizar_metricas_r4,
    calcular_pesos_aulas,
    gerar_cronograma,
    METRICAS
)
from parte1 import render_parte1
from parte2 import render_parte2
from parte3 import render_parte3

# ==================== Configuração inicial ====================
st.set_page_config(page_title="RadioClub - Gerar Cronograma", layout="wide")

if "step" not in st.session_state:
    st.session_state.step = 1
if "form" not in st.session_state:
    st.session_state.form = {"email": "", "nivel": "", "respostas": {}}

json_saida = st.session_state.form

# ==================== Título e navegação ====================
st.title("RadioClub – Gerador de Cronograma")
st.markdown("Preencha as partes na sequência. O cronograma será gerado no final.")

col1, col2, col3 = st.columns(3)
with col1:
    st.button("Parte 1", on_click=lambda: st.session_state.update({"step": 1}))
with col2:
    st.button("Parte 2", on_click=lambda: st.session_state.update({"step": 2}),
              disabled=not st.session_state.form.get("nivel"))
with col3:
    st.button("Parte 3", on_click=lambda: st.session_state.update({"step": 3}),
              disabled=not st.session_state.form.get("nivel"))

st.divider()

# ==================== Renderização por etapa ====================
if st.session_state.step == 1:
    render_parte1(st.session_state.form)
elif st.session_state.step == 2:
    if not st.session_state.form.get("nivel"):
        st.warning("Defina o nível na Parte 1 antes de avançar.")
    else:
        render_parte2(st.session_state.form)
elif st.session_state.step == 3:
    if not st.session_state.form.get("nivel"):
        st.warning("Defina o nível na Parte 1 antes de avançar.")
    else:
        render_parte3(st.session_state.form)

st.divider()

# ==================== Botão para gerar cronograma ====================
st.subheader("Gerar Cronograma")
col_a, col_b = st.columns([1, 2])
with col_a:
    gerar = st.button("Gerar usando meu pipeline", type="primary")

# ==================== Execução do pipeline ====================
if gerar:
    erros = []
    if not json_saida["email"]:
        erros.append("Email não informado (Parte 1).")
    if not json_saida["nivel"]:
        erros.append("Nível não informado (Parte 1).")
    if "Quanto tempo, por semana, você consegue dedicar aos estudos com o RadioClub?" not in json_saida["respostas"]:
        erros.append("Carga horária semanal não informada (Parte 3).")
    if "numero_semanas" not in json_saida["respostas"]:
        erros.append("Número de semanas não informado (Parte 3).")

    if erros:
        st.error("Corrija antes de gerar:\n- " + "\n- ".join(erros))
    else:
        catalogo = carregar_catalogo()
        respostas_aluno = json_saida
        nivel = respostas_aluno.get("nivel")
        metricas = METRICAS.copy()

        configurar_metricas_comuns(metricas, respostas_aluno)
        if nivel == "R1":
            atualizar_metricas_r1(respostas_aluno, metricas)
        elif nivel == "R2":
            atualizar_metricas_r2(respostas_aluno, metricas)
        elif nivel == "R3":
            atualizar_metricas_r3(respostas_aluno, metricas)
        elif nivel == "R4 / medico radiologista":
            atualizar_metricas_r4(respostas_aluno, metricas)

        pesos_aulas = calcular_pesos_aulas(catalogo, metricas)

        numero_semanas = int(metricas.get("semanas", respostas_aluno["respostas"].get("numero_semanas", 12)))
        tempo_max_semana = int(metricas.get("carga_horaria_max", 0))
        if tempo_max_semana <= 0:
            carga_txt = respostas_aluno["respostas"].get(
                "Quanto tempo, por semana, você consegue dedicar aos estudos com o RadioClub?"
            )
            mapa = {
                "Até 1h": 60,
                "1h a 2h": 120,
                "2h a 3h": 180,
                "3h a 4h": 240,
                "Mais de 4h": 300,
            }
            tempo_max_semana = mapa.get(carga_txt, 180)

        cronograma = gerar_cronograma(pesos_aulas, tempo_max_semana, numero_semanas)

        st.success("Cronograma gerado com sucesso.")
        for i, semana in enumerate(cronograma, start=1):
            st.markdown(f"### Semana {i}")
            if not semana:
                st.info("Sem aulas alocadas nesta semana.")
                continue
            st.dataframe(
                [{"#": idx + 1, "Módulo": a["module_name"], "Tema": a["lesson_theme"], "Min": a["duration_min"]}
                 for idx, a in enumerate(semana)]
            )

        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet

            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            elementos = []

            for i, semana in enumerate(cronograma, 1):
                elementos.append(Paragraph(f"Semana {i}", styles["Heading2"]))
                data = [["#", "Módulo", "Tema", "Minutos"]]
                total_semana = 0
                for idx, aula in enumerate(semana, 1):
                    data.append([idx, aula["module_name"], aula["lesson_theme"], aula["duration_min"]])
                    total_semana += aula["duration_min"]

                tabela = Table(data, repeatRows=1)
                tabela.setStyle(TableStyle([
                    ("BACKGROUND", (0,0), (-1,0), colors.grey),
                    ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
                    ("ALIGN", (0,0), (-1,-1), "LEFT"),
                    ("GRID", (0,0), (-1,-1), 0.5, colors.black)
                ]))
                elementos.append(tabela)
                elementos.append(Spacer(1, 24))
                elementos.append(Paragraph(f"Tempo total da semana: {total_semana} minutos", styles["Normal"]))

                if i < len(cronograma):
                    elementos.append(PageBreak())

            doc.build(elementos)
            pdf_bytes = buffer.getvalue()
            buffer.close()

            st.download_button(
                label="Baixar PDF do Cronograma",
                data=pdf_bytes,
                file_name="cronograma.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.warning(f"Não foi possível gerar o PDF para download no Streamlit ({e}). "
                       f"O cronograma foi gerado e exibido acima normalmente.")
