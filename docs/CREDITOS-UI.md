# Créditos da interface

## Identidade do CRIE

O CRIE forneceu a marca usada no login e no menu. O arquivo disponibilizado para este projeto veio de `public/brand/crie-logo-oficial.png` do site do CRIE. A interface conserva as cores e as proporções da imagem em `frontend/public/crie-logo-oficial.png`. A licença de redistribuição da marca não foi informada no briefing. [Repositório de origem](https://github.com/miguelvzs/site-crie)

## Archivo

Archivo é uma família da Omnibus-Type, distribuída sob SIL Open Font License 1.1. O navegador a carrega pelo Google Fonts em `frontend/index.html`. Os tamanhos, pesos e alternativas de sistema são definidos em `frontend/src/index.css`. Quando a fonte externa está indisponível, o navegador usa a fonte local. [Família no Google Fonts](https://fonts.google.com/specimen/Archivo) · [Licença da família](https://github.com/google/fonts/blob/main/ofl/archivo/OFL.txt)

## Ícones Lucide

Os desenhos vêm de Lucide Contributors, sob ISC, com ícones derivados de Feather, de Cole Bemis, sob MIT. Mantivemos os traços vetoriais do pacote `lucide-react`. Os componentes de `frontend/src/components/` e as telas de `frontend/src/pages/` ajustam tamanho e cor. Os ícones decorativos ficam ocultos dos leitores de tela, enquanto os controles têm nome acessível. [Projeto Lucide](https://lucide.dev/) · [Licenças originais](https://lucide.dev/license) · [Cópia distribuída no projeto](../frontend/public/licenses/lucide-react.txt)

## Como falar na apresentação

O logotipo identifica a instituição no acesso e na navegação. No painel, cada cartão recebe uma demanda por props e mostra o prazo com texto e ícone. Na ficha, o componente de confirmação recebe o resumo por `children` e usa o diálogo nativo do navegador para manter o foco e permitir o fechamento com Esc. As páginas, os componentes de interface e os CSS Modules foram desenvolvidos para este projeto.
