# PropSelectAI - Backend

Bem-vindo ao repositório do Backend do projeto PropSelectAI, responsável pelo sistema inteligente de seleção de hélices aeronáuticas.

## Estrutura de Pastas e Arquivos

O projeto está organizado da seguinte forma para facilitar a manutenção e escalabilidade:

### Raiz
- `main.py`: Ponto de entrada da API. Inicializa o servidor FastAPI e registra as rotas.
- `Dockerfile`: Configuração de imagem do Docker para a construção isolada do backend, utilizando `uv` como gerenciador de pacotes.
- `pyproject.toml` / `uv.lock`: Arquivos de declaração das dependências Python utilizadas na API.

### `api/`
Armazena a definição das rotas e endpoints (controllers).
- `router.py`: Roteador principal do FastAPI que define o endpoint `POST /api/recommend`. Responsável por orquestrar a recomendação, justificativa (RAG) e a geração de relatório PDR.

### `models/`
Definição dos contratos de dados (Schemas).
- `schemas.py`: Classes do Pydantic (`PropellerRequest`, `PropellerResponse`, `RecommendationResponse`) que validam o formato da requisição e das respostas trafegadas entre o Frontend e o Backend.

### `services/`
Contém as lógicas de negócio core, isoladas da API.
- `database.py`: Estabelece conexão com o PostgreSQL usando `SQLAlchemy` e realiza a consulta/pesquisa das hélices com base nos filtros do usuário e expressões regulares de tratamento de texto.
- `filters.py`: Lógica heurística e algoritmos de cálculo. Avalia o peso, a potência e a velocidade exigida para definir o requisito mínimo de empuxo.
- `rag.py`: Responsável pela conexão com a IA utilizando LangChain e OpenAI. Faz a busca semântica na base vetorial (ChromaDB) e constrói o prompt de solicitação para a justificativa de escolha.
- `report.py`: Responsável pela formatação técnica e geração do documento PDF (Preliminary Design Review - PDR), exportando as referências no padrão ABNT.

### `scripts/`
Contém os utilitários de linha de comando (*one-offs*) focados em ingestão e análise off-line.
- `ingestion.py`: Lê arquivos PDF salvos na pasta `data/artigos/`, realiza o *chunking* de texto e constrói a base vetorial do RAG no ChromaDB. **(Deve ser rodado uma vez no setup da infraestrutura)**.
- `migrate_db.py`: Migra todas as planilhas Excel da pasta `data/planilhas/` convertendo-as para a tabela `propeller_data` dentro do PostgreSQL.
- `analyze_sheets.py`: Script simples (scratch) que exibe no terminal as colunas extraídas do Excel, utilizado apenas para mapeamento e diagnóstico da base de dados local.

## Execução

Para iniciar o Backend localmente através do Docker (recomendado):
```bash
docker compose up --build -d
```
Para inicializar scripts de forma avulsa pelo container:
```bash
docker compose exec backend uv run python scripts/ingestion.py
```
