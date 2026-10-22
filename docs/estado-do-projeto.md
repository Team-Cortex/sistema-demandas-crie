# Estado do projeto

Mapa geral do sistema, para quem abre o repositório sem a conversa anterior. Atualizado em 13/10/2026.

Quem mantém este arquivo é a frente de back-end. A atualização acompanha os commits dessa frente quando um fato daqui muda ([`documentacao.md`](documentacao.md)). Não é diário de commits e não é obrigação das outras frentes manterem este texto em tempo real.

---

## 1. O que é

Sistema web para registrar, acompanhar e consultar as **demandas de articulação de rede** do CRIE — Centro de Integração Especial / APAE de Extrema. São situações que a equipe não resolve internamente e que exigem a rede pública (assistência social, saúde, educação).

Há três reuniões semanais, uma por setor: pedagógico, saúde e serviço de convivência. O histórico é consultável e não se apaga. Dados no repositório e na demonstração são fictícios. Parte das pessoas atendidas é menor de idade.

A direção optou por visibilidade aberta a todo profissional cadastrado. A auditoria (autor, data e hora, inclusive na consulta) é o controle. A alternativa restritiva permanece prevista no código, desligada.

Parceiro: CRIE. Curso: ADS, IFSP Câmpus Bragança Paulista, BRAEXT2, orientação do Prof. Luiz Gustavo Diniz de Oliveira Véras. Entrega final: 26/11/2026. A ET3, em que o back-end começa a responder, é 22/10/2026.

O relato acadêmico da versão 2 (02/10/2026) é a referência de escopo quando divergir dos Markdown de agosto.

## 2. Como está desenhado

Cliente-servidor. O navegador não fala com o PostgreSQL.

| Parte | Onde | Quem preenche |
| --- | --- | --- |
| Cliente React | `frontend/` | os arquivos do Gabriel, apenas movidos da raiz para esta pasta |
| Servidor Flask | `backend/` | Miguel Vaz |
| Camadas do servidor | `schemas/`, `routes/`, `services/`, `models/` | back-end; os arquivos das specs 01 a 04 estão reservados e sem rota |
| Banco | PostgreSQL via `docker-compose.yml`; scripts em `docs/modelagem/sql/` | Henry Claro |
| Requisitos e plano | `docs/requisitos.md`, `docs/plano-de-projeto.md` | Vinícius Marrocos |
| Interface | Figma, fora deste repositório | Inácio Fontes |

Contrato HTTP: [`contrato-api.md`](contrato-api.md). Comportamento do servidor: [`specs/`](specs/).

## 3. O que responde hoje

| Método | Caminho | Resposta |
| --- | --- | --- |
| GET | `/api/saude` | `{"ok": true, "status": "ok"}` |
| GET | `/api/teste` | `Hello World` |

Login, usuários, demandas, assistidos e reuniões estão especificados e ainda não têm rota. Não há tabela de domínio no servidor: o modelo relacional segue com o Henry.

## 4. Decisões abertas

| # | Decisão | Enquanto não fecha |
| --- | --- | --- |
| A1 | Destino do encaminhamento | sem rota de encaminhamento |
| A2 | Categorias de demanda | campo opcional, texto de até 80 caracteres, sem catálogo |
| A3 | Campos do assistido | o servidor só aceitará `nome_tratamento` |
| A4 | Perfil coordenação de setor | não há classe própria |
| A5 | Trocar JWT em `sessionStorage` por cookie | permanece o JWT de 30 minutos |

Fora das quatro specs atuais: encaminhamento, serviço da rede, retorno de acompanhamento, evolução lançada, relatório e notificação.

## 5. Como rodar

Está no [`README.md`](../README.md). Servidor em `backend/` (`flask run`, porta 5000). Cliente em `frontend/` (`npm run dev`, porta 5173). Banco local com `docker compose up -d`.
