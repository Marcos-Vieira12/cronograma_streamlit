import json
from metricas_base import METRICAS
from common import configurar_metricas_comuns
from r1 import atualizar_metricas as atualizar_metricas_r1
from r2 import atualizar_metricas as atualizar_metricicas_r2  # (mantém nome original do seu projeto)
from r3 import atualizar_metricas as atualizar_metricas_r3
from r4 import atualizar_metricas as atualizar_metricas_r4

from reportlab.lib.pagesizes import A4 # type: ignore
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak # type: ignore
from reportlab.lib import colors # type: ignore
from reportlab.lib.styles import getSampleStyleSheet # type: ignore

JSON_PATH = "json/catalogo_certo.json"
OUTPUT_PATH = "json/catalogo/catalogo_pesos_aulas.json"
PDF_OUTPUT = "cronograma.pdf"


def carregar_catalogo(path=JSON_PATH):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def calcular_pesos_aulas(catalogo, metricas_aluno):
    subespecialidades = [m for m in metricas_aluno if m.startswith("subespecialidade_")]
    exames = [m for m in metricas_aluno if m.startswith("exame_")]

    foco_subesp = metricas_aluno.get("foco_subespecialidade", 0)
    foco_exames = metricas_aluno.get("foco_exames", 0)

    resultado = []
    for aula in catalogo:
        score = 0
        for metrica, valor_aula in aula.get("metrics", {}).items():
            valor_aluno = metricas_aluno.get(metrica, 0)
            if metrica in subespecialidades:
                valor_aluno *= (1 + foco_subesp)
            elif metrica in exames:
                valor_aluno *= (1 + foco_exames)
            score += valor_aula * valor_aluno

        resultado.append({
            "module_name": aula["module_name"],
            "lesson_theme": aula["lesson_theme"],
            "duration_min": aula["duration_min"],
            "peso": round(score, 4),
        })
    return resultado


def salvar_catalogo_pesos(pesos_aulas, output_path=OUTPUT_PATH):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(pesos_aulas, f, ensure_ascii=False, indent=2)
    print(f"Catálogo salvo em: {output_path}")


def gerar_cronograma(
    pesos_aulas,
    tempo_max_semana,
    numero_semanas,
    tempo_min_semana=0,
    frac_limite_max=0.90,
    peso_min_intermediario=1.0,
):
    aulas_ordenadas = sorted(pesos_aulas, key=lambda x: x["peso"], reverse=True)
    cronograma = [[] for _ in range(numero_semanas)]
    limite_90 = tempo_max_semana * frac_limite_max

    for semana_idx in range(numero_semanas):
        if not aulas_ordenadas:
            break

        total_semana = 0

        while aulas_ordenadas:
            if total_semana >= limite_90:
                break

            if total_semana < tempo_min_semana:
                def cabe(a):
                    return a["duration_min"] + total_semana <= tempo_max_semana
            else:
                def cabe(a):
                    return (
                        a["peso"] >= peso_min_intermediario
                        and a["duration_min"] + total_semana <= tempo_max_semana
                    )

            candidato = None
            for aula in aulas_ordenadas:
                if cabe(aula):
                    candidato = aula
                    break

            if candidato is None:
                break

            cronograma[semana_idx].append(candidato)
            total_semana += candidato["duration_min"]
            aulas_ordenadas.remove(candidato)

    return cronograma


def salvar_pdf(cronograma, output_path=PDF_OUTPUT):
    doc = SimpleDocTemplate(output_path, pagesize=A4)
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
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        elementos.append(tabela)
        elementos.append(Spacer(1, 24))
        elementos.append(Paragraph(f"Tempo total da semana: {total_semana} minutos", styles["Normal"]))

        if i < len(cronograma):
            elementos.append(PageBreak())

    doc.build(elementos)
    print(f"PDF gerado: {output_path}")
