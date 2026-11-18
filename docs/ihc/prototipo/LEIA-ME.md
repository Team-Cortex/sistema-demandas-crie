# Protótipo de IHC · Demandas CRIE

Abra [index.html](index.html) com dois cliques e selecione **Entrar**. O e-mail e a senha fictícios já estão preenchidos. O arquivo inclui a fonte Archivo, os ícones e o logo. Funciona offline, inclusive se for copiado sozinho para outro computador. A cópia do logo em PNG serve de referência para o design.

## Conduzir uma sessão

Abra **Roteiro de fluxos** no topo da página ou acrescente `#fluxos` ao endereço do arquivo. **Iniciar T1** a **Iniciar T7** abrem a tarefa com o perfil previsto. O roteiro traz os passos para o moderador. Use **Reiniciar dados** antes de cada participante. Entre tarefas da mesma sessão, volte ao roteiro sem recarregar a página.

| Tarefa | O que conferir na carga inicial |
| --- | --- |
| T1 · Ver vencidas | O painel mostra duas vencidas. A Demanda nº 3, de avaliação fonoaudiológica, tem o prazo mais antigo. |
| T2 · Buscar histórico | Buscar “material adaptado” localiza a Demanda nº 2. O histórico informa que Carlos encaminhou o pedido à equipe pedagógica. |
| T3 · Registrar demanda | Registrar “Solicitar ao CAPSi vaga para avaliação” na reunião de Saúde mais recente, com prioridade alta, Bruna e prazo de sete dias. A confirmação abre a Demanda nº 9. |
| T4 · Aguardar o CRAS | Na Demanda nº 1, mudar para Aguardando terceiros e anotar a ligação. As duas ações aparecem no histórico. |
| T5 · Concluir e sair | Na Demanda nº 2, passar de Aberta para Em andamento e depois para Concluída. **Sair** retorna à tela Entrar. |
| T6 · Trocar responsável | Na Demanda nº 3, trocar Bruna por Carlos. A ficha e o histórico identificam a troca. |
| T7 · Lançar evolução | Na ficha do Assistido Fictício A, lançar a evolução da oficina de música. A descrição aparece na ficha com a data e o autor. |

Os prazos são relativos ao dia de abertura. A simulação começa com o CRAS em andamento, o material adaptado aberto e perto do prazo de Carlos e uma reunião de Saúde no dia. Assim, o mesmo roteiro pode ser usado em datas diferentes.

## Telas disponíveis

- **Entrar e Painel** com aviso de prazo, demandas vencidas e quadro por estado.
- **Minhas demandas e Demandas** com busca e filtros, cadastro com confirmação e ficha com histórico, anotação, mudança de estado e troca de responsável.
- **Reuniões e Assistidos** com listas, fichas, cadastro e edição. A reunião dá acesso ao registro de demanda. A ficha do assistido permite lançar evolução e consultar os registros.
- **Encaminhamentos** com pendentes, consulta de todos, registro e confirmação de desfecho.
- **Direção** com administração de usuários, emissão e impressão de relatórios e consulta à auditoria. O seletor **Perfil de simulação** permite explorar os três menus.

## Limites

O protótipo demonstra a navegação e guarda as alterações apenas na memória da aba. Recarregar a página restaura a carga inicial. **Sair** encerra a sessão simulada e preserva os registros para o próximo perfil enquanto a página continuar aberta. Use somente informações fictícias.

## Créditos

Fonte [Archivo](https://github.com/Omnibus-Type/Archivo), da Omnibus-Type, sob a SIL Open Font License 1.1, embutida no arquivo. Ícones do [Lucide](https://lucide.dev) (ISC; os derivados do Feather, MIT), com a licença no próprio arquivo. O logo do CRIE tem a mesma origem descrita em `docs/CREDITOS-UI.md` (PR #15).

O sistema real usa autenticação, permissões de acesso, API e banco de dados. A simulação dispensa esses serviços. A auditoria é demonstrativa, a impressão usa o navegador e a ficha de evolução cobre lançamento e consulta. Retificação, histórico de versões e acesso simultâneo de vários usuários ficam no sistema real.
