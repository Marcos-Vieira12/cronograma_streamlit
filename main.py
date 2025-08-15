import json
import streamlit as st
from metricas_base import METRICAS
from common import configurar_metricas_comuns
from r1 import atualizar_metricas as atualizar_metricas_r1
from r2 import atualizar_metricas as atualizar_metricas_r2
from r3 import atualizar_metricas as atualizar_metricas_r3
from r4 import atualizar_metricas as atualizar_metricas_r4
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

JSON_PATH = "json/catalogo_ajustado.json"
JSON_ALUNOS_PATH = "json/alunos"
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
            "peso": round(score, 4)
        })
    return resultado

def gerar_cronograma(pesos_aulas, tempo_max_semana, numero_semanas):
    aulas_ordenadas = sorted(pesos_aulas, key=lambda x: x["peso"], reverse=True)
    cronograma = [[] for _ in range(numero_semanas)]

    semana_idx = 0
    while aulas_ordenadas and semana_idx < numero_semanas:
        total_semana = 0
        usadas = []
        for aula in list(aulas_ordenadas):
            if aula["duration_min"] + total_semana <= tempo_max_semana:
                cronograma[semana_idx].append(aula)
                usadas.append(aula)
                total_semana += aula["duration_min"]
        for usada in usadas:
            aulas_ordenadas.remove(usada)
        semana_idx += 1
    
    return cronograma

def salvar_pdf(cronograma):
    doc = SimpleDocTemplate(PDF_OUTPUT, pagesize=A4)
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
        elementos.append(Spacer(1, 24))  # duas linhas
        elementos.append(Paragraph(f"Tempo total da semana: {total_semana} minutos", styles["Normal"]))

        if i < len(cronograma):
            elementos.append(PageBreak())
    
    doc.build(elementos)
    print(f"PDF gerado: {PDF_OUTPUT}")

if __name__ == "__main__":

    
    catalogo = carregar_catalogo()
    respostas_aluno = 0
    if not respostas_aluno:
        exit()
    
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
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(pesos_aulas, f, ensure_ascii=False, indent=2)

    numero_semanas = int(metricas.get("semanas", 12))
    tempo_max_semana = int(metricas.get("carga_horaria_max", 0))
    if tempo_max_semana <= 0:
        tempo_max_semana = 180

    cronograma = gerar_cronograma(pesos_aulas, tempo_max_semana, numero_semanas)
    salvar_pdf(cronograma)
