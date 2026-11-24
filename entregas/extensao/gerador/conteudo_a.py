"""Pré-textuais, seção 1 (Introdução) e seção 2 (Contato com a comunidade)."""
from docx.enum.text import WD_ALIGN_PARAGRAPH

AUTORES = ["GABRIEL BORBA", "HENRY CLARO", "INÁCIO FONTES", "MIGUEL VAZ DE SOUZA", "VINÍCIUS MARROCOS"]
TITULO = "SISTEMA DE GESTÃO DE DEMANDAS DE ARTICULAÇÃO"

SIGLAS = [
    ("ABNT", "Associação Brasileira de Normas Técnicas"),
    ("API", "Interface de programação de aplicação (Application Programming Interface)"),
    ("APAE", "Associação de Pais e Amigos dos Excepcionais"),
    ("BRABCD1", "Banco de Dados 1"),
    ("BRADWFR", "Desenvolvimento Web Front End"),
    ("BRAENSO", "Engenharia de Software"),
    ("BRAEXT2", "Extensão como Metodologia de Ensino 2"),
    ("BRAINHC", "Interface Humano-Computador"),
    ("BRAPROB", "Programação Orientada a Objetos"),
    ("CAPSi", "Centro de Atenção Psicossocial Infantojuvenil"),
    ("CI", "Integração contínua (Continuous Integration)"),
    ("CRAS", "Centro de Referência de Assistência Social"),
    ("CRIE", "Centro de Integração Especial"),
    ("DER", "Diagrama Entidade-Relacionamento"),
    ("EXPOEX", "Mostra de Extensão"),
    ("HTTPS", "Protocolo de transferência de hipertexto seguro"),
    ("IFSP", "Instituto Federal de Educação, Ciência e Tecnologia de São Paulo"),
    ("JSON", "JavaScript Object Notation"),
    ("JWT", "JSON Web Token"),
    ("LGPD", "Lei Geral de Proteção de Dados Pessoais"),
    ("ORM", "Mapeamento objeto-relacional (Object-Relational Mapping)"),
    ("PR", "Pull request (pedido de integração de código)"),
    ("RF", "Requisito funcional"),
    ("RNF", "Requisito não funcional"),
    ("SQL", "Structured Query Language"),
    ("WCAG", "Web Content Accessibility Guidelines"),
]


def capa(d):
    d.linha_centro("INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DE SÃO PAULO", negrito=True)
    d.linha_centro("CÂMPUS BRAGANÇA PAULISTA", negrito=True)
    d.linha_centro("TECNOLOGIA EM ANÁLISE E DESENVOLVIMENTO DE SISTEMAS", negrito=True)
    for i, nome in enumerate(AUTORES):
        d.linha_centro(nome, espaco_antes=90 if i == 0 else 0)
    d.linha_centro(TITULO, negrito=True, espaco_antes=110)
    d.linha_centro("Projeto de extensão em parceria com o CRIE — Centro de Integração Especial, Extrema/MG")
    d.linha_centro("Relatório de Projeto — Versão 5 (final)", espaco_antes=6)
    d.linha_centro("BRAGANÇA PAULISTA", espaco_antes=150)
    d.linha_centro("2026")


def folha_de_rosto(d):
    for nome in AUTORES:
        d.linha_centro(nome)
    d.linha_centro(TITULO, negrito=True, espaco_antes=120)
    d.natureza(
        "Relatório de projeto apresentado à unidade curricular Extensão como Metodologia de Ensino 2 "
        "(BRAEXT2) do curso de Tecnologia em Análise e Desenvolvimento de Sistemas do Instituto Federal "
        "de São Paulo — Câmpus Bragança Paulista, como parte dos requisitos de avaliação. Versão 5, "
        "referente à entrega final de 26/11/2026.", espaco_antes=70)
    d.natureza("Orientador: Prof. Luiz Gustavo Diniz de Oliveira Véras", espaco_antes=24)
    d.linha_centro("BRAGANÇA PAULISTA", espaco_antes=170)
    d.linha_centro("2026")


def resumo(d):
    d.quebra()
    d.titulo_sem_numero("RESUMO", sumario=False)
    d.p("Este relatório apresenta a quinta e última versão da documentação do projeto integrado de "
        "extensão desenvolvido pelos estudantes do 2º módulo do curso de Tecnologia em Análise e "
        "Desenvolvimento de Sistemas do IFSP — Câmpus Bragança Paulista, no âmbito da unidade curricular "
        "Extensão como Metodologia de Ensino 2 (BRAEXT2). O projeto é realizado em parceria com o CRIE — "
        "Centro de Integração Especial, organização da sociedade civil sem fins lucrativos sediada em "
        "Extrema (MG) e filiada à Federação das APAEs, e resultou em um sistema web para o registro, o "
        "acompanhamento e a consulta das demandas levantadas nas reuniões semanais de equipe que exigem "
        "articulação com a rede de serviços públicos. Em relação à versão 3, esta versão registra a "
        "conclusão do modelo relacional e sua implementação em PostgreSQL por migrações, com histórico e "
        "auditoria que só admitem inserção; a implementação da API em Flask, orientada a objetos, guiada "
        "por nove especificações de comportamento e verificada por 570 testes automatizados; o projeto de "
        "banco de dados da disciplina de Banco de Dados 1, com scripts e dezessete consultas; os artefatos "
        "de interação — cenários de uso, arquitetura da informação, fluxos, especificação de telas, "
        "protótipo clicável e plano de testes de usabilidade; a interface em React integrada à API; e a "
        "publicação do sistema na Vercel, com banco de dados no Neon. Registra também o que permanece "
        "pendente: a execução dos testes de usabilidade com oito participantes, a criação da primeira "
        "conta da direção no ambiente publicado e as decisões que dependem da instituição. "
        "[[Atualizar este resumo após os testes de usabilidade e o registro do retorno da EXPOEX.]]",
        recuo=False, entrelinha=1.0)
    d.p("**Palavras-chave:** extensão universitária; terceiro setor; articulação de rede; sistema web; "
        "orientação a objetos; usabilidade.", recuo=False, entrelinha=1.0).paragraph_format.space_before = 12


def historico(d, R):
    d.quebra()
    d.titulo_sem_numero("HISTÓRICO DE VERSÕES DO RELATÓRIO", sumario=False)
    d.quadro("q-historico", "Histórico de versões deste relatório",
             ["Versão", "Entrega", "Conteúdo principal"],
             [["1", "03/09/2026", "Contextualização, relato de contato com a comunidade externa, levantamento "
               "de requisitos e decisões estruturais de cada disciplina."],
              ["2", "02/10/2026", "Minimundo e DER concluídos; início do modelo relacional; personas e protótipo "
               "inicial em construção; estrutura do projeto React; registro do quadro Kanban e planejamento do "
               "backlog."],
              ["3", "22/10/2026", "Personas concluídas; servidor Flask estruturado, com testes automatizados e "
               "banco local; especificações do servidor e proposta do contrato da API; repositório separado em "
               "cliente e servidor; revisão do quadro Kanban, das decisões em aberto e do backlog."],
              ["4", "05/11/2026", "[[a preencher pela equipe: conteúdo da versão 4, apresentada na ET4; o "
               "arquivo não está versionado em docs/relatorios]]"],
              ["5", "26/11/2026", "Versão final: modelo relacional e banco implementados; API e interface "
               "concluídas, integradas e publicadas; artefatos de IHC e protótipo clicável; projeto de BD1; "
               "verificação automatizada e integração contínua; estrutura da avaliação de usabilidade; "
               "comparação entre o planejado na versão 3 e o realizado; pendências."]],
             "elaborado pelos autores (2026).", larguras=[1.6, 2.4, 12.0])


def listas(d, paginas):
    """Lista de figuras, quadros, tabelas e siglas; paginas: chave -> página."""
    for tipo, titulo in (("Figura", "LISTA DE FIGURAS"), ("Quadro", "LISTA DE QUADROS"),
                         ("Tabela", "LISTA DE TABELAS")):
        d.quebra()
        d.titulo_sem_numero(titulo, sumario=False)
        entradas = [("TOC 4", f"{t} {n} — {tit}", paginas.get(f"{t} {n}", "?"))
                    for (t, n, tit) in paginas.get("_ilustracoes", []) if t == tipo]
        if entradas:
            d.indice(rf'TOC \h \z \t "Legenda {tipo},4"', entradas)
    d.quebra()
    d.titulo_sem_numero("LISTA DE ABREVIATURAS E SIGLAS", sumario=False)
    for sigla, sig in SIGLAS:
        par = d.doc.add_paragraph()
        pf = par.paragraph_format
        from docx.shared import Cm
        pf.first_line_indent = Cm(0)
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf.tab_stops.add_tab_stop(Cm(3))
        par.add_run(f"{sigla}\t{sig}")


def sumario(d, paginas):
    d.quebra()
    d.titulo_sem_numero("SUMÁRIO", sumario=False)
    entradas = [(f"TOC {max(nivel, 1)}", texto, paginas.get("T:" + texto, "?"))
                for nivel, texto in paginas.get("_titulos", [])]
    if entradas:
        d.indice(r'TOC \o "1-3" \h \z \u', entradas)


def secao1(d, R):
    d.h1("1 INTRODUÇÃO", nova_pagina=False)
    d.h2("1.1 Contextualização")
    d.p("A curricularização da extensão, prevista na Resolução CNE/CES nº 7/2018, estabelece que ao menos "
        "dez por cento da carga horária dos cursos de graduação seja destinada a atividades de extensão, "
        "compreendidas como processo interdisciplinar que promove interação transformadora entre a "
        "instituição de ensino e a sociedade (BRASIL, 2018b). No curso de Tecnologia em Análise e "
        "Desenvolvimento de Sistemas do IFSP — Câmpus Bragança Paulista, essa exigência se materializa em "
        "três unidades curriculares distribuídas ao longo do curso, das quais o presente relatório se "
        "refere à segunda, Extensão como Metodologia de Ensino 2 (BRAEXT2).")
    d.p("O projeto de extensão do câmpus, denominado \"Sistemas em Ação: Desenvolvimento de Soluções "
        "Digitais para Demandas Comunitárias\", propõe que as equipes de estudantes identifiquem uma "
        "organização da região com necessidade real de solução digital, realizem o levantamento dessa "
        "necessidade em diálogo com a comunidade e desenvolvam um sistema web que integre os conhecimentos "
        "das cinco disciplinas do 2º módulo (INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DE SÃO "
        "PAULO, 2026).")
    d.h2("1.2 A instituição parceira")
    d.p("O CRIE — Centro de Integração Especial é uma organização da sociedade civil sem fins lucrativos, "
        "fundada em 1991 no município de Extrema, no sul de Minas Gerais. Sua criação partiu de um grupo de "
        "cidadãos da própria cidade, diante da ausência de atendimento especializado a pessoas com "
        "deficiência no município. Em 2005 a instituição filiou-se à Federação das APAEs, e em 2016 obteve "
        "autorização de funcionamento para seu Centro de Atendimento Educacional Especializado, além do "
        "Certificado de Entidade Beneficente de Assistência Social.")
    d.p("A instituição organiza-se em setores que atendem de forma complementar as pessoas assistidas e "
        "suas famílias: atendimento educacional especializado, saúde, assistência social, oficinas para "
        "jovens e adultos e programas voltados às famílias.")
    d.p("A escolha do CRIE como parceiro decorreu da decisão da equipe de direcionar o projeto ao terceiro "
        "setor, buscando impacto social concreto, somada ao fato de um dos integrantes residir em Extrema, "
        "o que facilitou a aproximação inicial e o vínculo com o território.")
    d.h2("1.3 Problema identificado")
    d.p("A instituição realiza três reuniões semanais de equipe, uma para cada setor: pedagógico, saúde e "
        "serviço de convivência. Nessas reuniões são discutidos os casos que a equipe não consegue resolver "
        "com os recursos internos e que, portanto, exigem articulação com a rede de serviços públicos — "
        "assistência social, saúde e educação — para a garantia de direitos da pessoa atendida.")
    d.p("Segundo a direção da instituição, o fluxo típico de uma dessas demandas percorre as seguintes "
        "etapas: identifica-se uma situação que a equipe não compreende ou não resolve internamente; o caso "
        "é levado à reunião do setor correspondente; a equipe define as ações cabíveis, que podem incluir o "
        "encaminhamento a profissional interno, a convocação da família e a verificação de referenciamento "
        "da pessoa atendida junto a serviços da assistência social; designa-se um responsável pela "
        "articulação; e, ao final, registra-se o desfecho, frequentemente o encaminhamento a um serviço da "
        "rede, seguido de acompanhamento continuado.")
    d.p("Todo esse processo era registrado em papel, sem controle centralizado do andamento. A direção "
        "relatou três consequências desse modelo:")
    d.alineas([
        "a) tempo despendido para retomar demandas anteriores, dada a ausência de histórico organizado;",
        "b) ocorrência de demandas esquecidas, que permanecem sem conclusão porque nada sinaliza que estão "
        "paradas;",
        "c) dificuldade de consultar o que já foi realizado quando uma demanda se repete — situação descrita "
        "como frequente, cuja resposta é por vezes solicitada pela família da pessoa atendida ou pela "
        "própria rede de serviços."])
    d.h2("1.4 Objetivos")
    d.p("**Objetivo geral.** Desenvolver um sistema web para o registro, o acompanhamento e a consulta das "
        "demandas de articulação de rede levantadas nas reuniões de equipe do CRIE, desde a identificação "
        "do caso até o desfecho, preservando histórico consultável.")
    d.p("**Objetivos específicos.**")
    d.alineas([
        "a) realizar o levantamento de requisitos junto à direção e à equipe da instituição, aplicando a "
        "extensão como metodologia de ensino;",
        "b) especificar os requisitos funcionais e não funcionais do sistema, com rastreabilidade em relação "
        "às necessidades levantadas;",
        "c) modelar e implementar banco de dados relacional adequado ao domínio;",
        "d) projetar interface centrada no usuário, considerando o perfil de familiaridade tecnológica da "
        "equipe da instituição, e validá-la por meio de testes de usabilidade;",
        "e) implementar o back-end da aplicação segundo o paradigma de orientação a objetos, em linguagem "
        "Python;",
        "f) implementar o front-end da aplicação com framework web, organizado em componentes reutilizáveis;",
        "g) validar a solução junto à instituição parceira, verificando sua aderência às necessidades "
        "identificadas."])
    d.p(f"Ao final do projeto, os objetivos (a) a (c), (e) e (f) foram cumpridos; o objetivo (d) foi "
        f"cumprido na etapa de projeto da interface, e sua validação depende dos testes de usabilidade; o "
        f"objetivo (g) depende da mesma etapa e do retorno da instituição (seções 5.3 e 6).")
    d.h2("1.5 Relevância")
    d.p("A relevância do projeto se manifesta em três dimensões. Para a instituição parceira, o sistema "
        "responde a uma necessidade operacional concreta, sem custo, em um contexto de recursos escassos "
        "característico do terceiro setor. Para as pessoas atendidas pelo CRIE e suas famílias, a "
        "organização do acompanhamento das demandas de articulação contribui indiretamente para a "
        "efetividade da garantia de direitos, ao reduzir a probabilidade de que uma providência necessária "
        "seja esquecida. Para os estudantes, o projeto proporciona experiência de desenvolvimento em "
        "contexto real, com interlocutor externo, restrições concretas e necessidade de negociação de "
        "escopo.")
    d.h2("1.6 Situação ao final do projeto e organização do relatório")
    d.p("Esta é a versão final do relatório, referente à entrega de 26/11/2026. Ela mantém a estrutura das "
        "versões anteriores e atualiza cada seção com o que foi produzido entre a versão 3, de 22/10/2026, "
        "e a data de fechamento deste texto, 23/11/2026. No período, a equipe concluiu o banco de dados, "
        "implementou a API e a interface, publicou o sistema e preparou a avaliação de usabilidade. A seção "
        "4.4 compara, item por item, o planejamento registrado na versão 3 com o que foi realizado.")
    d.p("A seção 2 relata o contato com a comunidade externa; a seção 3 descreve o trabalho de cada "
        "disciplina; a seção 4 trata da gestão do projeto; a seção 5 apresenta o sistema desenvolvido e sua "
        "correspondência com os requisitos; a seção 6 reúne a verificação automatizada, os critérios de "
        "aceitação e a avaliação de usabilidade; e a seção 7 apresenta a conclusão. Todos os nomes, "
        "registros e telas mostrados neste relatório são fictícios: nenhum dado de pessoa atendida pela "
        "instituição foi usado no desenvolvimento, nos testes ou nas demonstrações.")
    d.p("A apresentação segue as normas da ABNT para trabalhos acadêmicos (ASSOCIAÇÃO BRASILEIRA DE NORMAS "
        "TÉCNICAS, 2011), numeração progressiva das seções (ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS, "
        "2012a), sumário (ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS, 2012b), citações (ASSOCIAÇÃO BRASILEIRA "
        "DE NORMAS TÉCNICAS, 2023) e referências (ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS, 2018).")


def secao2(d, R):
    d.h1("2 RELATO DE CONTATO COM A COMUNIDADE EXTERNA")
    d.p("Esta seção descreve o processo de interação com a instituição parceira, demonstrando a aplicação "
        "da extensão como metodologia de ensino. O relato é apresentado em ordem cronológica, seguido da "
        "análise dos seus efeitos sobre as decisões do projeto.")
    d.h2("2.1 Abordagem inicial")
    d.p("O contato inicial foi realizado por mensagem eletrônica direta à instituição, apresentando a "
        "equipe, a natureza acadêmica do projeto, a ausência de custos para a organização e a proposta de "
        "uma conversa para compreender as necessidades do cotidiano institucional. Optou-se deliberadamente "
        "por não apresentar uma solução previamente concebida, de modo que a definição do problema "
        "decorresse da escuta e não de suposição da equipe.")
    d.p("A resposta foi obtida no mesmo dia, pela própria diretora da instituição, que manifestou "
        "disponibilidade para agendar conversa. Na sequência, a equipe expôs suas restrições de agenda e "
        "propôs alternativas de formato, tendo a instituição indicado preferência por interação por "
        "mensagens e áudios, formato compatível com a rotina de trabalho da direção.")
    d.h2("2.2 Levantamento estruturado")
    d.p("Definido o canal, elaborou-se um formulário de levantamento de requisitos organizado em dez "
        "seções, abrangendo: objetivo do sistema, situação atual, perfil dos usuários, funcionalidades "
        "necessárias, privacidade e sigilo das informações, ambiente de uso, ferramentas já utilizadas, "
        "prioridades e prazos, critérios de sucesso e observações finais.")
    d.p("O formulário foi respondido integralmente pela direção da instituição. Entre os resultados "
        "obtidos, destacam-se dois pontos determinantes para o projeto:")
    d.alineas([
        "a) foram levantadas duas necessidades distintas — o controle de entrada e saída de materiais de "
        "consumo e a organização das demandas levantadas nas reuniões de equipe. Questionada sobre a "
        "prioridade, a direção indicou a segunda;",
        "b) a direção informou que o sistema trataria dados sensíveis das pessoas atendidas e declarou "
        "desconhecer as exigências legais aplicáveis, o que transferiu à equipe a responsabilidade de "
        "propor as salvaguardas cabíveis."])
    d.h2("2.3 Aprofundamento e correção de hipóteses")
    d.p("A análise das respostas ao formulário revelou ambiguidades que exigiram novas rodadas de "
        "perguntas. Elaboraram-se blocos temáticos curtos, com alternativas fechadas sempre que possível, "
        "respeitando a rotina da interlocutora. As respostas foram obtidas por texto e por mensagens de "
        "áudio.")
    d.p(f"Este aprofundamento produziu o resultado metodologicamente mais significativo do processo: a "
        f"hipótese inicial da equipe estava incorreta em três aspectos estruturais, e apenas a escuta "
        f"continuada permitiu corrigi-la (Quadro {R('q-hipoteses')}).")
    d.quadro("q-hipoteses", "Correção de hipóteses a partir do contato com a instituição",
             ["Aspecto", "Hipótese inicial da equipe", "Realidade informada pela instituição"],
             [["Reuniões", "Uma reunião semanal de equipe",
               "Três reuniões semanais, uma por setor: pedagógico, saúde e serviço de convivência"],
              ["Natureza da demanda", "Tarefa ou pendência interna a ser executada por um profissional",
               "Situação que excede a capacidade interna e exige articulação com a rede de serviços públicos"],
              ["Visibilidade dos registros", "Acesso restrito a cada profissional segundo os assistidos que "
               "acompanha", "Acesso aberto a todos os profissionais cadastrados, por decisão da direção"]],
             "elaborado pelos autores (2026).", larguras=[3.4, 6.0, 6.6])
    d.p("Cada uma dessas correções alterou decisões técnicas já tomadas. A primeira introduziu o conceito "
        "de setor nas entidades de reunião e demanda. A segunda reorientou o escopo do sistema, tornando o "
        "encaminhamento à rede uma peça central, e não acessória. A terceira modificou a implementação do "
        "controle de acesso, que no sistema final mantém a regra restritiva no código, desligada, e usa a "
        "auditoria como controle (seção 3.1.3).")
    d.h2("2.4 Detalhamento do fluxo de trabalho")
    d.p("Solicitou-se à direção a descrição detalhada do funcionamento de uma reunião de equipe. A "
        "resposta, obtida por áudio, forneceu o exemplo que passou a orientar a modelagem: identificada uma "
        "alteração de comportamento em uma criança atendida, sem compreensão imediata por parte da equipe, "
        "o caso é levado à reunião; discutem-se as ações — encaminhamento à psicóloga da instituição, "
        "convocação dos responsáveis, verificação de referenciamento em serviço da assistência social; "
        "designa-se o responsável pela articulação; e registra-se a conclusão, que pode ser o "
        "encaminhamento ao Centro de Referência de Assistência Social (CRAS), com acompanhamento posterior "
        "em reunião mensal de rede.")
    d.p("Duas informações adicionais foram obtidas nesta etapa e alteraram o escopo:")
    d.alineas([
        "a) **Sobre a repetição de demandas.** A direção informou que determinadas demandas se repetem ao "
        "longo do tempo, sendo necessário consultar o que já foi realizado anteriormente, informação por "
        "vezes solicitada pela família ou pela rede. Essa constatação elevou a consulta ao histórico da "
        "pessoa atendida à condição de funcionalidade central do sistema, hoje atendida pela ficha da "
        "pessoa assistida e pela busca de demandas;",
        "b) **Sobre o relatório encaminhado ao poder público.** A direção esclareceu que o relatório "
        "periódico enviado à Prefeitura não possui modelo padronizado, é elaborado individualmente por cada "
        "profissional e consiste em resumo de atendimento, não abrangendo as demandas de articulação "
        "tratadas por este sistema. O requisito correspondente foi, em consequência, retirado do escopo; os "
        "relatórios do sistema final são de uso interno da direção."])
    d.h2("2.5 Formalização da parceria")
    d.p("A parceria foi formalizada por meio do Formulário de Manifestação de Interesse em Participação em "
        "Projeto de Extensão, disponibilizado pela Pró-Reitoria de Extensão do IFSP, encaminhado à "
        "instituição e devolvido devidamente assinado pela direção. O documento consta dos Anexos deste "
        "relatório.")
    d.h2("2.6 Análise do processo")
    d.p("O contato com a comunidade externa não se limitou à coleta de informações: alterou "
        "substantivamente as decisões de projeto. Três decisões técnicas que a equipe havia tomado com base "
        "em suposição foram revistas após a escuta, e um requisito considerado essencial foi eliminado do "
        "escopo por não corresponder à realidade da instituição.")
    d.p("Registre-se ainda um aprendizado metodológico. A primeira formulação da pergunta sobre "
        "visibilidade dos registros ofereceu alternativas de modo insuficientemente explícito, e obteve "
        "como resposta uma afirmação genérica, sem valor informativo. A reformulação da mesma pergunta em "
        "alternativas fechadas e numeradas produziu resposta imediata e inequívoca. A qualidade do dado "
        "obtido em levantamento de requisitos depende diretamente da formulação da pergunta.")
    d.p("Nos ciclos seguintes, a interlocução alimentou diretamente a modelagem e a interface: o minimundo "
        "foi redigido a partir do fluxo descrito na seção 2.4; a persona da direção incorpora as dores e os "
        "desejos relatados pela diretora; e os cenários de uso e as tarefas do teste de usabilidade partem "
        "das situações descritas pela instituição, como a demanda que se repete e o contato com o CRAS "
        "(seção 3.2).")
    d.h2("2.7 Contato no período final e Mostra de Extensão")
    d.p(f"Entre a versão 3 e esta versão, a pendência principal com a instituição era o envio do bloco "
        f"único de perguntas fechadas e numeradas sobre as decisões em aberto, previsto no planejamento "
        f"anterior. [[a preencher pela equipe: se o bloco foi enviado, em que data, por qual canal e quais "
        f"respostas foram obtidas]]. Até 23/11/2026, as decisões que dependem da instituição — categorias de "
        f"demanda (A2), campos de identificação da pessoa assistida (A3), data considerada no período dos "
        f"filtros (A6), retenção da auditoria (A7), autoria da retificação de evolução (A9) e antecedência "
        f"do aviso de prazo (A10) — continuam registradas como abertas na documentação do repositório, com "
        f"a solução provisória descrita no Quadro {R('q-decisoes')}.")
    d.p(f"Conforme o cronograma da unidade curricular, a Mostra de Extensão (EXPOEX) ocorreu em 18/11/2026, "
        f"com apresentação dos projetos em banner (INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DE "
        f"SÃO PAULO, 2026). [[a preencher pela equipe: integrantes que apresentaram, público e principais "
        f"perguntas recebidas]]. A Figura {R('f-banner')} reproduz o banner apresentado.")
    d.figura_pendente("f-banner", "Banner do projeto apresentado na EXPOEX (18/11/2026)",
                      "arte final do banner apresentado na EXPOEX, exportada em PNG com largura de pelo menos "
                      "1280 px; foto da apresentação é opcional e só pode mostrar integrantes que autorizarem",
                      "entregas/extensao/prints/20-banner-expoex.png",
                      "[[elaborado pelos autores (2026); inserir a arte do banner]].")
    d.p("**Feedback recebido na EXPOEX:** [[a preencher pela equipe, com a origem de cada observação "
        "(avaliador, docente ou visitante) e o que foi dito, sem identificar visitantes]]. A seção 4.6 "
        "relaciona as alterações registradas no repositório depois da Mostra.")
    d.p("**Apresentação do sistema à instituição parceira:** [[a preencher pela equipe: se a versão "
        "publicada foi mostrada à direção do CRIE, em que data e com qual retorno]]. A validação com o "
        "público-alvo por meio dos testes de usabilidade, planejada desde a primeira versão, ainda não foi "
        "realizada (seção 6.3).")
