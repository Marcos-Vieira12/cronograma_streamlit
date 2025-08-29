import streamlit as st
from openai import OpenAI
import re

# Cliente da OpenAI (pega do secrets do Streamlit)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Listas de categorias
EXAMES = [
    "exame_rx",
    "exame_usg",
    "exame_densitometria",
    "exame_mamografia",
    "exame_tc",
    "exame_rm",
    "exame_doppler",
    "exame_angio",
    "exame_fluoroscopia",
    "exame_contrastados",
    "exame_petct",
    "exame_hsg",
    "exame_radiologia_geral",
]

SUBESPECIALIDADES = [
    "subespecialidade_neuro",
    "subespecialidade_torax",
    "subespecialidade_abdome",
    "subespecialidade_mama",
    "subespecialidade_musculoesqueletico",
    "subespecialidade_cabeca_pescoco",
    "subespecialidade_pediatria",
    "subespecialidade_gineco",
    "subespecialidade_intervencao",
    "subespecialidade_cardiovascular",
    "subespecialidade_financas",
    "subespecialidade_inteligencia_artificial",
    "subespecialidade_workstation",
    "subespecialidade_fisica_medica",
    "subespecialidade_ingles",
    "subespecialidade_gestao_radiologia",
    "subespecialidade_telemedicina",
    "subespecialidade_ensino_radiologia",
    "subespecialidade_pesquisa",
    "subespecialidade_anatomia",
    "subespecialidade_reumatolgia",
    "subespecialidade_geral",
    "subespecialidade_mediastino",
    "subespecialidade_pratica_cetrus",
]

def processar_resposta_aberta(pergunta: str, resposta: str, metricas: dict) -> dict:
    """Usa LLM para interpretar resposta aberta e atualizar métricas."""
    if not resposta or str(resposta).strip() == "":
        return metricas

    categorias = EXAMES + SUBESPECIALIDADES

    prompt = f"""
    Pergunta: "{pergunta}"
    Resposta do aluno: "{resposta}"

    Sua tarefa é mapear a resposta para UMA OU MAIS chaves do seguinte conjunto de categorias:
    {categorias}

    Regras:
    - Se não houver correspondência clara, responda "nenhuma".
    - Responda apenas com uma lista separada por vírgula das chaves encontradas (sem explicações).
    """

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um classificador de respostas abertas."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=200,
        )

        saida_raw = resp.choices[0].message.content.strip().lower()

        # limpeza básica
        saida = re.sub(r"[^a-z0-9_, ]", "", saida_raw)
        chaves = [s.strip() for s in saida.split(",") if s.strip()]

        # Log no Streamlit para debug
        st.write("#### [LLM Debug]")
        st.json({
            "pergunta": pergunta,
            "resposta_aluno": resposta,
            "saida_llm_raw": saida_raw,
            "saida_llm_parseada": chaves,
        })

        if not chaves or "nenhuma" in chaves:
            return metricas

        # Atualiza métricas
        for chave in chaves:
            if chave in EXAMES:
                metricas[chave] = metricas.get(chave, 0) + 2
            elif chave in SUBESPECIALIDADES:
                metricas[chave] = metricas.get(chave, 0) + 4

    except Exception as e:
        st.warning(f"[LLM] Erro ao processar resposta aberta: {e}")

    return metricas
