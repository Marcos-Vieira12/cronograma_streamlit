# common.py
from typing import Dict, Any, List

def _to_list(value: Any) -> List[str]:
    """Garante lista de strings (aceita lista ou string separada por vírgulas)."""
    if value is None:
        return []
    if isinstance(value, list):
        return [str(x).strip() for x in value]
    return [p.strip() for p in str(value).split(",") if p.strip()]

def configurar_metricas_comuns(metricas: Dict[str, float], respostas_aluno: Dict[str, Any]) -> None:
    """
    Aplica ajustes gerais de métricas:
    - Peso base do nível
    - Objetivos (comum a todos os níveis)
    """

    r = respostas_aluno.get("respostas", {})
    nivel = respostas_aluno.get("nivel")
    num_semanas = r.get("numero_semanas")
    if isinstance(num_semanas, (int, float)) and num_semanas > 0:
        metricas["semanas"] = int(num_semanas)
    # Peso base por nível
    if nivel == "R1":
        metricas["fundamentos_basicos"] += 1.2
        metricas["conteudo_intermediario"] += 0.3
        metricas["casos_clinicos_simples"] += 1.2

    elif nivel == "R2":
        metricas["fundamentos_basicos"] += 1
        metricas["conteudo_intermediario"] += 0.5
        metricas["casos_clinicos_simples"] += 0.8
        metricas["casos_clinicos_complexos"] += 0.4

    elif nivel == "R3":
        metricas["fundamentos_basicos"] += 0.7
        metricas["conteudo_intermediario"] += 0.6
        metricas["conteudo_avancado"] += 0.2
        metricas["casos_clinicos_simples"] += 0.6
        metricas["casos_clinicos_complexos"] += 0.6

    elif nivel == "R4 / medico radiologista":
        metricas["fundamentos_basicos"] += 0.51
        metricas["conteudo_intermediario"] += 0.50
        metricas["conteudo_avancado"] += 0.49
        metricas["casos_clinicos_simples"] += 0.4
        metricas["casos_clinicos_complexos"] += 0.8


    # Objetivos (comum a todos os níveis)
    objetivos = _to_list(r.get("Quais os seus objetivos com o curso RadioClub?"))

    if "Aprofundar conhecimentos na minha subespecialidade atual" in objetivos:
        metricas["foco_subespecialidade"] += 0.5
    if "Expandir para novas subespecialidades da radiologia" in objetivos:
        metricas["multi_subspecialidades"] += 0.51
        metricas["fundamentos_basicos"] += 0.51

    if "Melhorar interpretação de exames no dia a dia" in objetivos:
        metricas["casos_clinicos_simples"] += 0.5
        metricas["casos_clinicos_complexos"] += 0.5
        metricas["conteudo_intermediario"] += 0.2
        metricas["conteudo_avancado"] += 0.1
        metricas["protocolo_fluxo"] += 0.2


    if "Desenvolver skills para ensino/supervisão de residentes" in objetivos:
        metricas["multi_subspecialidades"] += 0.2
        metricas["multi_exames"] += 0.2   
        metricas["conteudo_avancado"] += 0.1          
        metricas["revisao_conteudo_antigo"] += 0.1
        metricas["subespecialidade_ensino_radiologia"] += 2.5  

    if "Complementar minha formação como residente de radiologia" in objetivos:
        metricas["fundamentos_basicos"] += 0.7
        metricas["multi_subspecialidades"] += 0.2
        metricas["multi_exames"] += 0.2   

    if "Me atualizar com as inovações e protocolos mais recentes" in objetivos:
        metricas["atualizacoes_novos_protocolos"] += 1.5
        metricas["protocolo_fluxo"] += 0.5
        metricas["subespecialidade_inteligencia_artificial"] += 1
        metricas["subespecialidade_workstation"] += 1

    if "Participar ativamente da comunidade profissional" in objetivos:
        metricas["multi_subspecialidades"] += 0.2
        metricas["multi_exames"] += 0.2 
        metricas["abrangencia_geral"] += 1
        metricas["subespecialidade_gestao_radiologia"] += 2

    if "Praticar com casos reais e discussões clínicas" in objetivos:
        metricas["casos_clinicos_simples"] += 0.7
        metricas["casos_clinicos_complexos"] += 0.7
        metricas["casos_clinicos_reais"] += 2
        metricas["erros_pitfalls"] += 0.2


    if "Quanto tempo, por semana, você consegue dedicar aos estudos com o RadioClub?" in r:
        tempo = r["Quanto tempo, por semana, você consegue dedicar aos estudos com o RadioClub?"]

        if tempo == "Até 1h":
            metricas["carga_horaria_min"] = 30
            metricas["carga_horaria_max"] = 60
        elif tempo == "1h a 2h":
            metricas["carga_horaria_min"] = 60
            metricas["carga_horaria_max"] = 120
        elif tempo == "2h a 3h":
            metricas["carga_horaria_min"] = 120
            metricas["carga_horaria_max"] = 180
        elif tempo == "3h a 4h":
            metricas["carga_horaria_min"] = 180
            metricas["carga_horaria_max"] = 240
        elif tempo == "Mais de 4h":
            metricas["carga_horaria_min"] = 240
            metricas["carga_horaria_max"] = 360

    