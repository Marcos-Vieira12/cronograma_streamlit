# parte1.py
import streamlit as st # type: ignore

OBJETIVOS = [
    "Aprofundar conhecimentos na minha subespecialidade atual",
    "Expandir para novas subespecialidades da radiologia",
    "Melhorar interpretação de exames no dia a dia",
    "Desenvolver skills para ensino/supervisão de residentes",
    "Complementar minha formação como residente de radiologia",
    "Me atualizar com as inovações e protocolos mais recentes",
    "Participar ativamente da comunidade profissional",
    "Praticar com casos reais e discussões clínicas",
]

NIVEIS = ["R1", "R2", "R3", "R4 / medico radiologista"]

def render_parte1(form_state: dict):
    st.header("Parte 1 – Dados básicos")

    email = st.text_input("Email", value=form_state.get("email", ""))
    nivel = st.selectbox("Nível", options=NIVEIS, index=(
        NIVEIS.index(form_state.get("nivel")) if form_state.get("nivel") in NIVEIS else 0
    ))
    objetivos = st.multiselect(
        "Quais os seus objetivos com o curso RadioClub?",
        options=OBJETIVOS,
        default=form_state["respostas"].get(
            "Quais os seus objetivos com o curso RadioClub?", []
        ),
        key="p1_objetivos"  # <<< key estável
    )
    hosp = st.text_input(
        "Em qual hospital você faz/fez a residência?",
        value=form_state["respostas"].get(
            "Em qual hospital você faz/fez a residência?", ""
        )
    )

    if st.button("Próximo ➡️"):
        form_state["email"] = email.strip()
        form_state["nivel"] = nivel
        form_state["respostas"]["Quais os seus objetivos com o curso RadioClub?"] = objetivos
        form_state["respostas"]["Em qual hospital você faz/fez a residência?"] = hosp.strip()
        st.session_state.step = 2
        st.rerun()
