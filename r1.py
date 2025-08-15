# Definição das métricas iniciais para R1


def atualizar_metricas(respostas_aluno, metricas):

    r = respostas_aluno["respostas"]

    # Exames iniciais
    if "Quais exames de imagem você já tem contato na prática ou vai ter nesse início de R1?" in r:
        for exame in r["Quais exames de imagem você já tem contato na prática ou vai ter nesse início de R1?"]:
            if exame == "RX":
                metricas["exame_rx"] += 2
            elif exame == "USG":
                metricas["exame_usg"] += 2
            elif exame == "Densitometria":
                metricas["exame_densitometria"] += 2
            elif exame == "Mamografia":
                metricas["exame_mamografia"] += 2
            elif exame == "TC":
                metricas["exame_tc"] += 2
            elif exame == "RM":
                metricas["exame_rm"] += 2

    # Subespecialidades
    if "Quais subespecialidades você vai ter mais contato na Residência?" in r:
        for subesp in r["Quais subespecialidades você vai ter mais contato na Residência?"]:
            if subesp == "Neuro":
                metricas["subespecialidade_neuro"] += 2
            elif subesp == "Tórax":
                metricas["subespecialidade_torax"] += 2
            elif subesp == "Abdome":
                metricas["subespecialidade_abdome"] += 2
            elif subesp == "Mama":
                metricas["subespecialidade_mama"] += 2
            elif subesp == "Musculoesquelético":
                metricas["subespecialidade_musculoesqueletico"] += 2
            elif subesp == "Cabeça e Pescoço":
                metricas["subespecialidade_cabeca_pescoco"] += 2
            elif subesp == "Pediatria":
                metricas["subespecialidade_pediatria"] += 2
            elif subesp == "Gineco/Obstetrícia":
                metricas["subespecialidade_gineco"] += 2
            elif subesp == "Urologia":
                metricas["subespecialidade_urologia"] += 2
            elif subesp == "Oncologia":
                metricas["subespecialidade_oncologia"] += 2

    return metricas
