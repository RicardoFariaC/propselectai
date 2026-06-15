# Guia de Configuração, Execução e Inicialização do Projeto

Este documento detalha os passos necessários para configurar o ambiente, executar o sistema (via Docker) e utilizar os scripts de inicialização de dados presentes no backend.

---

## 1. Pré-requisitos

Para rodar o projeto localmente da forma recomendada, você precisará ter:
- **Docker** e **Docker Compose** instalados na sua máquina.
- Os arquivos fonte de dados devem estar posicionados nas pastas corretas:
  - Planilhas de hélices (`.xlsx`) devem estar em `data/planilhas/`
  - Artigos/manuais em PDF (`.pdf`) devem estar em `data/artigos/`

## 2. Configurando o Ambiente (.env)

Antes de rodar o projeto, é necessário configurar as variáveis de ambiente. Na raiz do projeto, existe um arquivo `.env.template`. 

1. Crie uma cópia ou renomeie este arquivo para `.env`.
2. Certifique-se de preencher a chave da API da OpenAI, necessária para a funcionalidade de RAG (Geração de texto e embeddings).

Exemplo de configuração básica do `.env`:
```env
OPENAI_API_KEY=sua_chave_da_openai_aqui
DATABASE_URL=postgresql://propselect:propselect@db:5432/propselect
CHROMA_HOST=chromadb
CHROMA_PORT=8000
```
*(Nota: as configurações de banco geralmente já vêm ajustadas para a rede interna do Docker).*

## 3. Subindo os Serviços (Execução do Projeto)

O projeto é orquestrado através do Docker Compose, facilitando o levantamento de todos os serviços simultaneamente (Frontend, Backend, PostgreSQL, ChromaDB, etc).

Abra um terminal na **raiz do projeto** e execute:

```bash
docker compose up --build -d
```

Este comando fará o build das imagens (backend utilizando o gerenciador de pacotes `uv`) e iniciará os contêineres em modo desacoplado (*detached*).

---

## 4. Inicialização do Banco de Dados (Scripts de Ingestão e Migração)

Com os serviços rodando, os bancos de dados (PostgreSQL e ChromaDB) estarão vazios. Para que a aplicação tenha dados de consulta e contexto, é **obrigatório** rodar os scripts de inicialização localizados em `backend/scripts/`.

### A. Migração dos Dados Estruturados (`migrate_db.py`)
Este script carrega os dados brutos de hélices contidos nas planilhas Excel (da pasta `data/planilhas/`), limpa as colunas e os insere na tabela `propeller_data` do PostgreSQL.

**Para rodar a migração via Docker:**
```bash
docker compose exec backend uv run python scripts/migrate_db.py
```

### B. Ingestão da Base Vetorial RAG (`ingestion.py`)
Este script lê todos os PDFs da pasta `data/artigos/`, realiza o processo de *chunking* avançado (Parent Document Retrieval) e constrói a base vetorial dentro do banco de dados ChromaDB. Isso é essencial para gerar as "Justificativas de Escolha" com IA na interface.
*(Atenção: A chave da OpenAI precisa estar configurada no seu `.env`, ou o script falhará).*

**Para rodar a ingestão via Docker:**
```bash
docker compose exec backend uv run python scripts/ingestion.py
```

### C. Script Auxiliar de Diagnóstico (`analyze_sheets.py`)
Um utilitário simples em forma de script de teste (scratch). Ele pode ser rodado caso você deseje visualizar a estrutura (cabeçalhos e primeiras linhas) das planilhas que estão na sua pasta de dados antes de inseri-las no banco.

**Para rodar a visualização:**
```bash
docker compose exec backend uv run python scripts/analyze_sheets.py
```

---

## Dicas Adicionais

- Para parar e desligar os serviços do projeto:
  ```bash
  docker compose down
  ```
- Para reiniciar e recriar toda a infraestrutura zerando os volumes de dados dos bancos (reset total):
  ```bash
  docker compose down -v
  docker compose up --build -d
  ```
