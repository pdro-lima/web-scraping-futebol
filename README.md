# Web Scraping Transfermarkt

Este projeto tem como objetivo de pesquisa e aprendizado **coletar dados dos principais artilheiros do futebol brasileiro** da série de anos - 2000-2025 - e **analisar estatísticas dos jogadores e gerar insights**.

---

## Coleta de Dados

Os dados foram coletados do site [Transfermarkt](https://www.transfermarkt.com.br/) com o uso das bibliotecas BeautifulSoup4 e Requests.

A coleta envolveu:

Requisições HTTP para a página de artilharia de cada ano do campeonato brasileiro;
Extração e parsing de cada HTML com o BeautifulSoup;
Estruturação e armazenamento dos dados em formato tabular com pandas.

---

## Tratamento dos Dados

Bibliotecas utilizadas: pandas, datetime

O tratamento dos dados trouxe padronização, limpeza e segurança aos dados, gerando possibilidade de análise e geração de insights confiáveis. Passou por etapas como:
- Tratamento de caracteres especiais no HTML coletado do site com replace e regex
- Tratamento de colunas com dados aninhados ou em listas com normalização
- Criação de novas colunas de dados quantitativos e qualitativos com iteração, funções, manipulação de tipo de dados, e etc...
- Renomeação e organização das colunas

## Analise dos Dados

Bibliotecas utilizadas: pandas, matplotlib

As análises buscaram entender o comportamento dos jogadores ao longo de todo período, possíveis tendências com base no histórico e o que pode ter motivado os cenários apresentados pelos dados. Para isso, alguns passos foram necessários:
- Criação de subconjuntos de dados através de cálculos de diversas agregações e armazenamento em dataframes auxiliares
- Filtragens, tabela dinâmica, agrupamentos, ordenações e geração de dados de suporte
- Calcular estatísticas descritivas, rankings e indicadores derivados
- Detectar e tratar outliers para análises sensíveis
- Geração de visualizações - gráficos de barras, linhas, dispersão, pizza - para apoiar as conclusões
- Realizar análises temporais e comparativas (tendências por década, posição, clube)
- Estruturação lógica de insights textuais

obs: pra visualização dos gráficos juntos as conclusões textuais das análises utilize um ambiente de desenvolvimento que permite a execução do código em células e imprima os gráficos no kernel do ambiente.


## Arquitetura do Projeto

```bash
.
├── src/
│   ├── dados_artilheiros.py          # Script de coleta dos dados
│   ├── processando_dados.py          # Script de tratamento dos dados
│   ├── analises.py                   # Script de análises estatísticas dos dados com geração de insights
│
├── data/                             # Armazenamento dos dados gerados
├── requirements.txt                  # Dependências do projeto
└── README.md

```

---

