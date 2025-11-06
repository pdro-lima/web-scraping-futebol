# Web Scraping Artilheiros Futebol Brasileiro

Este projeto tem como objetivo **coletar dados dos 25 artilheiros do futebol brasileiro de cada ano da série 2000-2025** e **analisar estatísticas dos jogadores**.

O pipeline automatiza todo o fluxo de:
1. Coleta dos dados do site [Transfermarkt](https://www.transfermarkt.com.br/);

---

## Arquitetura do Projeto

```bash
.
├── src/
│   ├── dados_artilheiros.py          # Script principal: coleta, tradução e resumo
├── requirements.txt                  # Dependências do projeto
└── README.md

```