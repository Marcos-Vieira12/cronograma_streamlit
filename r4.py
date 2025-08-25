# Definição das métricas iniciais para R1


def atualizar_metricas(respostas_aluno, metricas):
    r = respostas_aluno["respostas"]

    # Exames iniciais
    q_exames = "Quais exames você realiza na sua prática atual e gostaria de revisar ou de se atualizar?"
    if q_exames in r:
        for exame in r[q_exames]:
            if exame == "RX Geral":
                metricas["exame_rx"] += 4
            elif exame == "USG Geral":
                metricas["exame_usg"] += 4
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
                metricas["exame_angio"] += 2
            elif exame == "Fluoroscopia":
                metricas["exame_fluoroscopia"] += 2
            elif exame == "Contrastados":
                metricas["exame_contrastados"] += 2
            elif exame == "PET-CT":
                metricas["exame_petct"] += 2
            elif exame == "HSG":
                metricas["exame_hsg"] += 2
            # Ignora "Outros. Quais?"

    # Subespecialidades no R4
    q_subs = "Em quais subespecialidades você tem mais interesse revisar ou se aprofundar agora?"
    if q_subs in r:
        for subesp in r[q_subs]:
            if subesp == "Neuro":
                metricas["subespecialidade_neuro"] += 4
            elif subesp == "Tórax":
                metricas["subespecialidade_torax"] += 4
            elif subesp == "Abdome":
                metricas["subespecialidade_abdome"] += 4
            elif subesp == "Mama":
                metricas["subesatualizacoes_mama"] += 4
            elif subesp == "Musculoesquelético":
                metricas["subespecialidade_musculoesqueletico"] += 4
            elif subesp == "Cabeça e Pescoço":
                metricas["subespecialidade_cabeca_pescoco"] += 4
            elif subesp == "Pediatria":
                metricas["subespecialidade_pediatria"] += 4
            elif subesp == "Gineco/Obstetrícia":
                metricas["subespecialidade_gineco"] += 4
            elif subesp == "Urologia":
                metricas["subespecialidade_urologia"] += 4
            elif subesp == "Oncologia":
                metricas["subespecialidade_oncologia"] += 4
            elif subesp == "Intervenção":
                metricas["subespecialidade_intervencao"] += 4
            elif subesp == "Cardiovascular":
                metricas["subespecialidade_cardiovascular"] += 4

    # ==== R4 — Pergunta: "Há quanto tempo terminou a residência?" ====
    tempo_pos_resid = r.get("Há quanto tempo terminou a residência?")
    if tempo_pos_resid == "Menos de 1 ano":
        metricas["atualizacoes_novos_protocolos"] += 0.1
        metricas["conteudo_avancado"] += 0.1
        # recém-egresso: foco em protocolos atuais e refinamento avançado

    elif tempo_pos_resid == "Entre 1 e 3 anos":
        metricas["atualizacoes_novos_protocolos"] += 0.2
        metricas["conteudo_avancado"] += 0.1
        # ainda próximo da residência, mas já pede revisões pontuais

    elif tempo_pos_resid == "Entre 3 e 5 anos":
        metricas["atualizacoes_novos_protocolos"] += 0.2
        metricas["fundamentos_basicos"] += 0.1
        # reforço de base + atualização em blocos relevantes

    elif tempo_pos_resid == "Há mais de 5 anos":
        metricas["revisao_conteudo_antigo"] += 0.3
        metricas["atualizacoes_novos_protocolos"] += 0.2
        metricas["fundamentos_basicos"] += 0.1
        # reciclagem estruturada + diretrizes atuais


    # # ==== R4 — Pergunta: "No RadioClub, você pretende:" ====
    # pretende = r.get("No RadioClub, você pretende:")
    # if pretende:
    #     if isinstance(pretende, str):
    #         pretende_list = [p.strip() for p in pretende.split(",") if p.strip()]
    #     else:
    #         pretende_list = pretende

    #     for opc in pretende_list:
    #         if opc == "Revisar conteúdos que não pratica há um tempo":
    #             metricas["fundamentos_basicos"] += 0.8
    #             metricas["foco_subespecialidade"] += 0.2

    #         elif opc == "Se atualizar com temas novos na Radiologia":
    #             metricas["atualizacoes_novos_protocolos"] += 1

    #         elif opc == "Aprimorar uma nova subespecialidade de interesse":
    #             metricas["foco_subespecialidade"] += 0.3

    #         elif opc == "Ganhar mais segurança em exames e temas específicos":


    #         elif opc == "Ter uma rotina organizada de estudos":
    #             metricas["urgencia_praticidade"] += 0

    return metricas
