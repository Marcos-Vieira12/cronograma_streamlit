import streamlit as st

def render_parte3(form_state):
    st.header("Parte 3 - Finalização")

    tempo_semana = st.radio(
        "Quanto tempo, por semana, você consegue dedicar aos estudos com o RadioClub?",
        ["Até 1h", "1h a 2h", "2h a 3h", "3h a 4h", "Mais de 4h"],
        index=None
    )

    num_semanas = st.number_input("Número de semanas para o cronograma:", min_value=1, max_value=52, value=12)

    temas_extras = st.multiselect(
        "Além de conteúdo técnico, você se interessa por esses outros temas?",
        [
            "Inglês médico",
            "Como montar sua workstation",
            "Finanças médicas",
            "Trabalhos científicos",
            "Inteligência artificial",
            "Revalidação de diploma",
            "Prefiro focar no conteúdo técnico"
        ]
    )

    if st.button("Próximo ➡️"):
        form_state["respostas"]["Quanto tempo, por semana, você consegue dedicar aos estudos com o RadioClub?"] = tempo_semana
        form_state["respostas"]["numero_semanas"] = num_semanas
        form_state["respostas"]["temas_extras"] = temas_extras
        st.session_state.step = 3
        st.rerun()
