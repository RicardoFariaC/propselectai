# PropSelectAI

## Visão Geral (Overview)

O **PropSelectAI** é um sistema inteligente focado na otimização e auxílio da seleção de hélices aeronáuticas. A ferramenta facilita a escolha de propulsores através do cruzamento de parâmetros de voo (potência, RPM, entre outros) e enriquece a experiência utilizando Inteligência Artificial via RAG (*Retrieval-Augmented Generation*). 

Desta forma, o sistema não apenas filtra a melhor recomendação em um banco de dados estruturado, mas também elabora uma justificativa técnica embasada na literatura acadêmica e manuais do setor, podendo gerar um relatório técnico final detalhado (Preliminary Design Review - PDR).

### Arquitetura do Projeto
A arquitetura baseia-se em serviços independentes orquestrados via Docker Compose:
- **Frontend:** Interface do usuário (UI) focada na captura dos parâmetros da aeronave e apresentação das recomendações.
- **Backend:** Desenvolvido em Python (FastAPI), é a engine de regras. Cuida da filtragem técnica e da comunicação com as LLMs.
- **Bancos de Dados:**
  - **PostgreSQL:** Armazenamento relacional dos dados estruturados das hélices extraídos de planilhas de catálogo.
  - **ChromaDB:** Banco de dados vetorial utilizado para armazenar os embeddings dos PDFs acadêmicos (utilizados pelo RAG na justificativa).

---

## 📚 Documentações Importantes

A pasta `docs/` centraliza todo o conhecimento e instruções fundamentais sobre a plataforma. Listamos abaixo os pontos de partida:

- 🚀 **[Guia de Inicialização e Setup (SETUP.md)](docs/SETUP.md)**
  **Leitura Obrigatória para começar!** Detalha de forma prática como configurar as variáveis de ambiente (`.env`), como rodar todos os serviços usando Docker e como executar os scripts do backend (para migração dos dados pro PostgreSQL e vetorização dos arquivos pro ChromaDB).

- 📄 **[Artigo Principal (PropSelectAI_Intelligent_Propeller_Selection_PT-br.pdf)](docs/PropSelectAI_Intelligent_Propeller_Selection_PT-br.pdf)**
  Documento de especificação/artigo que aborda o referencial teórico da seleção de hélices, o problema enfrentado no design aerodinâmico e como a solução sistêmica resolve e simplifica essa escolha através da IA.

- 📊 **[Apresentação/Resumo (propselectai.pdf)](docs/propselectai.pdf)**
  Apresentação que traz um overview conceitual sobre o PropSelectAI, sua arquitetura e metodologias de análise.

---

## Estrutura do Repositório

```text
/
├── backend/            # API FastAPI, serviços (RAG, banco, regras heurísticas) e scripts locais
├── frontend/           # Aplicação frontend com a interface do sistema
├── docs/               # Manuais de setup e PDFs acadêmicos/teóricos
├── data/
│   ├── planilhas/      # Base de dados original (Excel) de catálogos e modelos de hélices
│   └── artigos/        # Manuais e artigos teóricos (PDFs) consumidos pela inteligência artificial
├── docker-compose.yml  # Orquestração local dos containers (DBs, back e front)
└── .env.template       # Template das variáveis de ambiente necessárias para o projeto (Ex: OPENAI_API_KEY)
```

## Como Começar?

Para rodar a aplicação imediatamente em seu computador local, leia o nosso **[Guia de Configuração (SETUP.md)](docs/SETUP.md)** e siga os passos descritos para montar os bancos de dados e inicializar o projeto.
