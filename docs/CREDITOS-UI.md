# Créditos da interface

## Identidade do CRIE

O logo do CRIE usado no login e no menu foi copiado de `public/brand/crie-logo-oficial.png` do repositório `site-crie`, projeto do Miguel Vaz para o CRIE (não é manual de marca oficial da instituição). A interface usa a imagem sem alteração, em `frontend/public/crie-logo-oficial.png`. A marca pertence ao CRIE; a autorização de uso neste sistema não está registrada por escrito. [Repositório de origem](https://github.com/miguelvzs/site-crie)

## Archivo

Archivo é uma família da Omnibus-Type ("Copyright 2020 The Archivo Project Authors"), distribuída sob a SIL Open Font License 1.1, que permite usar, copiar e redistribuir a fonte junto com o software, desde que a licença vá junto.

- **Origem dos arquivos:** pacote `@fontsource/archivo` 5.3.0 (mesma fonte do Google Fonts, separada por peso e alfabeto), baixado de `https://cdn.jsdelivr.net/npm/@fontsource/archivo@5/files/`. [Página do pacote](https://fontsource.org/fonts/archivo) · [Família no Google Fonts](https://fonts.google.com/specimen/Archivo)
- **Arquivos no projeto:** `frontend/public/fonts/archivo-latin-400-normal.woff2`, `archivo-latin-600-normal.woff2` e `archivo-latin-700-normal.woff2` (alfabeto latino, que cobre o português) e a licença em `frontend/public/fonts/OFL.txt`, copiada de [google/fonts](https://github.com/google/fonts/blob/main/ofl/archivo/OFL.txt).
- **Mantido:** os arquivos `.woff2` sem alteração.
- **Adaptado:** só os pesos que as telas usam (400 texto, 600 rótulos e botões, 700 títulos e números). As regras `@font-face` ficam no começo de `frontend/src/index.css`; o `frontend/index.html` não chama mais o Google Fonts.
- **Por que local:** a internet do CRIE é instável; com a fonte no próprio site, a tela não depende de outro servidor para carregar o texto. Se o arquivo falhar, o navegador usa "Segoe UI" ou Arial.

## Como falar na apresentação

O logotipo identifica a instituição no acesso e na navegação. No painel, cada cartão recebe uma demanda por props e mostra o prazo por escrito. Na ficha, o componente de confirmação recebe o resumo por `children` e usa o diálogo nativo do navegador para manter o foco e permitir o fechamento com Esc. As páginas, os componentes de interface e os CSS Modules foram desenvolvidos para este projeto. A fonte Archivo é de terceiros, com licença aberta (OFL), e vem do próprio site, declarada com `@font-face` no `index.css`.
