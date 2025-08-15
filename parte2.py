import streamlit as st
import re

def _slug(txt: str) -> str:
    s = re.sub(r"\W+", "_", txt.strip().lower())
    return re.sub(r"_+", "_", s).strip("_")

PERGUNTAS_R1 = {
    "Quais exames de imagem você já tem contato na prática ou vai ter nesse início de R1?": [
        "RX", "USG", "Densitometria", "Mamografia", "TC", "RM"
    ],
    "Quais exames de imagem sente mais dificuldade no momento?": "aberta",
    "Quais subespecialidades você vai ter mais contato na Residência?": [
        "Neuro", "Tórax", "Abdome", "Mama", "Musculoesquelético", "Cabeça e Pescoço",
        "Pediatria", "Gineco/Obstetrícia", "Urologia", "Oncologia", "Ainda não sei"
    ],
    "Quais temas você está vendo ou vai ver no primeiro ano de Residência?": "aberta",
}

PERGUNTAS_R2 = {
    "Quais exames você mais lauda/interpreta e tem contato no R2 atualmente?": [
        "RX", "USG", "Densitometria Óssea", "Mamografia", "TC", "RM",
        "Doppler", "AngioTC e AngioRM", "Fluoroscopia", "Contrastados"
    ],
    "Quais desses exames de imagem sente mais dificuldade no momento? Algo passou batido no R1?": "aberta",
    "Quais subespecialidades você tem mais contato na Residência?": [
        "Neuro", "Tórax", "Abdome", "Mama", "Musculoesquelético", "Cabeça e Pescoço",
        "Pediatria", "Gineco/Obstetrícia", "Urologia", "Oncologia"
    ],
    "Tem alguma subespecialidade que quer aprofundar mais ou revisar agora no R2?": "aberta",
}

PERGUNTAS_R3 = {
    "Já decidiu qual área quer seguir no R4/Fellow?": {
        "tipo": "single",
        "opcoes": ["ainda não tenho certeza", "sim, qual?"]
    },
    "Quais exames você tem mais contato hoje na residência e gostaria de aprofundar?": [
        "RX", "USG Geral", "Densitometria Óssea", "Mamografia", "TC", "RM",
        "Doppler", "AngioTC / AngioRM", "Fluoroscopia", "Contrastados",
        "PET-CT", "HSG"
    ],
    "Quais subespecialidades você mais tem contato na Residência e gostaria de aprofundar?": [
        "Neuro", "Tórax", "Abdome", "Mama", "Musculoesquelético", "Cabeça e Pescoço",
        "Pediatria", "Gineco/Obstetrícia", "Urologia", "Oncologia"
    ],
    "Tem algum exame de imagem ou subespecialidade específica que você quer dominar ou revisar agora no R3? Ou algo que você sente que ficou pra trás do R1/R2?": "aberta",
}

PERGUNTAS_R4 = {
    "Há quanto tempo terminou a residência?": {
        "tipo": "single",
        "opcoes": ["Menos de 1 ano", "Entre 1 e 3 anos", "Entre 3 e 5 anos", "Há mais de 5 anos"]
    },
    "Quais exames você realiza na sua prática atual e gostaria de revisar ou de se atualizar?": [
        "RX Geral", "USG Geral", "Densitometria Óssea", "Mamografia", "TC", "RM",
        "Doppler", "AngioTC / AngioRM", "Fluoroscopia", "Contrastados",
        "PET-CT", "HSG"
    ],
    "Em quais subespecialidades você tem mais interesse revisar ou se aprofundar agora?": [
        "Neuro", "Tórax", "Abdome", "Mama", "Musculoesquelético", "Cabeça e Pescoço",
        "Pediatria", "Gineco/Obstetrícia", "Urologia", "Oncologia", "Intervenção", "Cardiovascular"
    ],
    "No RadioClub, você pretende:": [
        "Revisar conteúdos que não pratica há um tempo",
        "Se atualizar com temas novos na Radiologia",
        "Aprimorar uma nova subespecialidade de interesse",
        "Ganhar mais segurança em exames e temas específicos",
        "Ter uma rotina organizada de estudos"
    ],
}

MAPA = {
    "R1": PERGUNTAS_R1,
    "R2": PERGUNTAS_R2,
    "R3": PERGUNTAS_R3,
    "R4 / medico radiologista": PERGUNTAS_R4,
}

def _render_field(pergunta: str, spec, respostas_dict: dict, nivel: str):
    slug = _slug(pergunta)

    if spec == "aberta":
        respostas_dict[pergunta] = st.text_area(
            pergunta,
            value=respostas_dict.get(pergunta, ""),
            height=90,
            key=f"ta_{nivel}_{slug}"
        ).strip()

    elif isinstance(spec, list):
        # Se já existe valor no st.session_state, não forçar default
        state_key = f"ms_{nivel}_{slug}"
        if state_key in st.session_state:
            default_val = st.session_state[state_key]
        else:
            defval = respostas_dict.get(pergunta, [])
            if isinstance(defval, str):
                defval = [defval] if defval else []
            default_val = [v for v in defval if v in spec]

        respostas_dict[pergunta] = st.multiselect(
            pergunta,
            options=spec,
            default=default_val,
            key=state_key
        )

    elif isinstance(spec, dict) and spec.get("tipo") == "single":
        opcoes = spec.get("opcoes", [])
        atual = respostas_dict.get(pergunta, None)
        if isinstance(atual, list):
            atual = next((x for x in atual if x in opcoes), None)
        selecionado = st.selectbox(
            pergunta,
            options=opcoes,
            index=(opcoes.index(atual) if atual in opcoes else 0),
            key=f"sb_{nivel}_{slug}"
        )
        respostas_dict[pergunta] = selecionado

def render_parte2(form_state: dict):
    st.header("Parte 2 – Conteúdo específico por nível")
    nivel = form_state.get("nivel")
    if nivel not in MAPA:
        st.error("Nível inválido. Volte à Parte 1.")
        return

    perguntas = MAPA[nivel]
    for pergunta, spec in perguntas.items():
        _render_field(pergunta, spec, form_state["respostas"], nivel)

    if st.button("Próximo ➡️", key=f"btn_next_{nivel}"):
        st.session_state.step = 3
        st.rerun()
