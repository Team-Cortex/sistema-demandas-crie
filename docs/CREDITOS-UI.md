# Créditos da interface

## Identidade do CRIE

O logo do CRIE usado no login e no menu foi copiado de `public/brand/crie-logo-oficial.png` do repositório `site-crie`, projeto do Miguel Vaz para o CRIE (não é manual de marca oficial da instituição). A interface usa a imagem sem alteração, em `frontend/public/crie-logo-oficial.png`. A marca pertence ao CRIE; a autorização de uso neste sistema não está registrada por escrito. [Repositório de origem](https://github.com/miguelvzs/site-crie)

## Archivo

Archivo é uma família da Omnibus-Type, distribuída sob SIL Open Font License 1.1. O navegador a carrega pelo Google Fonts em `frontend/index.html`. Os tamanhos, pesos e alternativas de sistema são definidos em `frontend/src/index.css`. Quando a fonte externa está indisponível, o navegador usa a fonte local. [Família no Google Fonts](https://fonts.google.com/specimen/Archivo) · [Licença da família](https://github.com/google/fonts/blob/main/ofl/archivo/OFL.txt)

## Como falar na apresentação

O logotipo identifica a instituição no acesso e na navegação. No painel, cada cartão recebe uma demanda por props e mostra o prazo por escrito. Na ficha, o componente de confirmação recebe o resumo por `children` e usa o diálogo nativo do navegador para manter o foco e permitir o fechamento com Esc. As páginas, os componentes de interface e os CSS Modules foram desenvolvidos para este projeto.
