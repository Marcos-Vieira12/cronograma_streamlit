# Definição das métricas iniciais para R1


def atualizar_metricas(respostas_aluno, metricas):
    #ajuste das métricas com base no nivel

    r = respostas_aluno["respostas"]

    # Exames iniciais
    q_exames = "Quais exames você tem mais contato hoje na residência e gostaria de aprofundar?"
    if q_exames in r:
        for exame in r[q_exames]:
            if exame == "RX":
                metricas["exame_rx"] += 2
            elif exame == "USG Geral":
                metricas["exame_usg"] += 2
            elif exame == "Densitometria Óssea":
                metricas["exame_densitometria"] += 2
            elif exame == "Mamografia":
                metricas["exame_mamografia"] += 2
            elif exame == "TC":
                metricas["exame_tc"] += 2
            elif exame == "RM":
                metricas["exame_rm"] += 2
            elif exame == "Doppler":
                metricas["exame_doppler"] += 2
            elif exame == "AngioTC / AngioRM":
                metricas["exame_angiotc"] += 2
            elif exame == "Fluoroscopia":
                metricas["exame_fluoroscopia"] += 2
            elif exame == "Contrastados":
                metricas["exame_contrastados"] += 2
            elif exame == "PET-CT":
                metricas["exame_petct"] += 2
            elif exame == "HSG":
                metricas["exame_hsg"] += 2
            # Ignora "Outros"

    # Subespecialidades no R3
    q_subs = "Quais subespecialidades você mais tem contato na Residência e gostaria de aprofundar?"
    if q_subs in r:
        for subesp in r[q_subs]:
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
