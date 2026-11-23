# Desenvolvimento Web Front End: projeto semestral

**Profa. Ana Paula Müller Giancoli.**
- **Envio:** até 04/12/2026, 23:59.
- **Valor:** 10,0 (Parte I 8,0 + Parte II 2,0). A média é (NetAcad + Prova + API + Projeto + ENADE) / 3 + Pesquisa.
- **Fonte:** tarefa "Entrega PROJETO SEMESTRAL: Entrega em EQUIPES [04-12-2026]" (Moodle de Front End).

## O que o enunciado pede

| Exigência | Situação | Onde |
|---|---|---|
| "aplicação REACT JS sob o paradigma de Orientação a Objetos" | em andamento | React 19 com Vite em `frontend/`. O PR de ajustes finais leva o cliente da API para a classe `ClienteApi` e cria a classe de domínio `Demanda`, explicadas em `docs/front-orientacao-a-objetos.md`. **Confirmar com a professora o que ela espera** |
| "consumir a API da aplicação Python desenvolvida no componente curricular BRAPROB" | ok | Todas as rotas do `docs/contrato-api.md` §2 são usadas pelas 14 telas |
| Interface "responsiva, acessível e interativa", "validações de formulário e requisições assíncronas", "componentes reutilizáveis" (Extensão §4.5) | ok | Ver `docs/ihc/telas.md` e a definição de pronto do PR #15 |
| README.md com instalação; "Indicar as bibliotecas utilizadas" | ok | `README.md`, seção de bibliotecas com versão, licença e motivo; créditos em `docs/CREDITOS-UI.md` |
| "Publicar na plataforma Vercel.com" | ok | https://sistema-demandas-crie.vercel.app ("verifique o link… em outro navegador em que você não esteja logado") |
| .zip "sem a pasta node_modules" | a gerar | Comando abaixo |
| Apresentação (2,0): até 20 min, todos apresentam, "Exibir o Front-end, Back-end e os dados registrados no banco de dados", divisão de tarefas, trecho de código | a preparar | Precisa da primeira direção em produção (PR #19) |

## Gerar o .zip do front (a partir da raiz, no commit entregue)

```bash
git archive --format=zip -o entregas/front-end/Front_CRIE_Equipe_Cortex.zip HEAD frontend README.md docs/CREDITOS-UI.md
```

## Pendências da equipe
- [ ] Perguntar à professora o que "sob o paradigma de Orientação a Objetos" exige no React.
- [ ] Criar a primeira direção em produção (PR #19) e cadastrar dados fictícios pela própria aplicação, para mostrar "os dados registrados no banco".
- [ ] Divisão da fala: cada integrante apresenta as telas e um trecho de código que domina. Os parágrafos "Como explicar" dos PRs #15, #16 e #18 servem de roteiro.
