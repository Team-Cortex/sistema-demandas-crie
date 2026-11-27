# Deck do seminário de BD1 (equipe Cortex)

38 slides para 20 minutos e 5 integrantes, na identidade visual do CRIE.

## Arquivos

| Arquivo | O que é |
|---|---|
| `index.html` | O deck. Arquivo único, abre offline em qualquer navegador. |
| `Seminario_BD1_Equipe_Cortex.pdf` | Os mesmos slides em PDF (1920×1080), para reserva. |
| `notas.py` | Notas do apresentador (tecla N): o que falar, conceitos das aulas, passo a passo das consultas e perguntas prováveis. |
| `gerar_deck.py` | Gera o `index.html` (e o PDF com `--pdf`) a partir dos scripts e dos resultados. |
| `qa_deck.py` | Confere o deck e, com `--prints`, salva um PNG por slide em `prints/`. |
| `assets/` | Fontes com licença, logos e a tela do protótipo. |

## Como apresentar

**F** tela cheia · **seta direita, espaço ou clique** avança · **seta esquerda** volta · **Home/End** · **N** abre e fecha as notas de quem fala (seta para baixo e para cima rolam as notas) · **P** abre a janela do apresentador (notas e cronômetro), que acompanha a janela projetada.

O roteiro de fala, com quem apresenta cada slide, está no `GUIA_APRESENTACAO.md` da pasta do BD1.

## Como gerar de novo

```
python gerar_deck.py --pdf
python qa_deck.py --prints
```

Requisitos: Python 3, Microsoft Edge (gera o PDF e roda a checagem), PyMuPDF e Pillow (só para os prints). O gerador lê:
- `../ferramentas/`: equipe, relacionamentos e resultados das consultas;
- o `01_criacao_banco.sql`, em `../entrega/` ou, no repositório do sistema, em `docs/modelagem/sql/`.

## O que a checagem confere

Em todos os slides, a 1920×1080:
- texto com pelo menos 24 px;
- contraste AA (4,5:1; 3:1 em texto grande);
- nada fora do slide nem encostado no rodapé;
- nenhum texto cortado;
- nenhum travessão.

## Origem de cada coisa

- **Identidade:** handoff do site do CRIE (`site-crie/docs/handoff/README.md`, seção Design Tokens):
  - tinta `#0E1013` e `#16181C`, papel `#F6F5F2`;
  - acentos magenta, amarelo, roxo, ciano e verde;
  - barra de quatro cores;
  - cantos vivos, sem sombras e sem ícones.
- **Fontes** (SIL OFL 1.1, licença ao lado de cada uma em `assets/fontes/` e, no site publicado, em `licencas/`): Bricolage Grotesque (títulos), Archivo (texto) e IBM Plex Mono (SQL e rótulos).
- **Logo do CRIE:** recriado em vetor a partir de `crie-logo-oficial.png` (150×70, `site-crie/public/brand`), com as cinco cores do original.
- **Logo do IFSP:** marca horizontal de 2015.
- **Tela do slide 36:** trecho do painel da direção no protótipo do sistema (`entregas/engenharia-de-software/telas/T-02.png`), com dados fictícios.
- **Dados:**
  - dicionário lido do `01_criacao_banco.sql`;
  - contagem por tabela feita com `COUNT(*)` depois do `02`;
  - as 17 consultas e os resultados vêm de `ferramentas/resultados.json`, rodadas no MySQL 8.4 com `SET TIMESTAMP` de 30/11/2026, 19:00.
- Todos os dados são fictícios.

## Escolhas de conteúdo

- O DER do slide 7 mostra entidades, relacionamentos e cardinalidades em tamanho de telão, na notação (mín, máx) da Aula 02 (Elmasri, Figura 7.15), com o quadro "Como ler". Os atributos ficam:
  - na notação textual (slide 9);
  - no dicionário (slide 11);
  - no documento ABNT, que tem o DER completo.
- Os títulos das consultas são curtos. O enunciado completo de cada uma fica nas notas (tecla N).
- O SQL aparece sem o alinhamento largo do script: só os espaços mudam. A Q16 tem uma quebra de linha a mais, para caber.
- Cada slide de consulta usa a maior letra (até 30 px) em que tudo cabe. Quando o resultado tem muitas linhas, aparecem as primeiras e a contagem do resto.
