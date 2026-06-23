# Documentação de Arquitetura - PropSelectAI

## Visão Geral
O PropSelectAI é um sistema inteligente focado em auxiliar o processo de seleção de hélices para aeronaves (como VANTs, drones e aeronaves de transporte/acrobáticas). O sistema avalia parâmetros de missão e características aerodinâmicas para gerar recomendações embasadas, contando com inteligência artificial para argumentação técnica.

## Stack Tecnológico
O sistema é dividido em duas frentes principais:
- **Backend**:
  - **Linguagem**: Python
  - **Framework Web**: FastAPI, utilizado para criar endpoints rápidos e eficientes.
  - **Inteligência Artificial & RAG**: LangChain e ChromaDB (banco de dados vetorial) acoplados ao OpenAI Embeddings/LLM. Eles realizam a Busca Aumentada por Recuperação (RAG) para fundamentar as decisões com catálogos e referências da engenharia aeronáutica.
  - **Geração de Relatórios**: ReportLab, utilizado para a construção de PDFs (Relatórios PDR) no padrão ABNT.
- **Frontend**:
  - **Framework Web**: Streamlit, provendo uma interface amigável e reativa para o usuário inserir parâmetros do projeto (peso, potência do motor, velocidade e missão) e visualizar as hélices recomendadas.
- **Orquestração e Deploy**: Docker e Docker Compose, organizando os serviços (backend, frontend e chromadb) em containers.

## Técnicas Utilizadas
- **Modelagem Física Simplificada**: O backend implementa regras heurísticas preliminares para pré-filtrar as hélices disponíveis num banco de dados (JSON), baseando-se no requisito mínimo de empuxo e eficiência da hélice.
- **RAG (Retrieval-Augmented Generation)**: Para gerar as justificativas técnicas, o sistema busca textos de referências bibliográficas (via ChromaDB) que detalham o comportamento aerodinâmico da hélice em determinada missão, fornecendo este contexto para um LLM (ChatGPT). O modelo então elabora um parágrafo estritamente técnico citando as fontes.
- **Geração de PDF Dinâmico**: Utilizando ReportLab, um relatório de revisão preliminar de design (PDR) é dinamicamente gerado e formatado com margens ABNT, incluindo as recomendações e a justificativa técnica.

## Fórmulas e Cálculos Aerodinâmicos
O sistema calcula os requisitos usando um modelo físico simplificado presente no motor de heurística (`backend/services/filters.py`):

1. **Conversão de Potência**:
   A potência do motor é convertida de HP para Watts:
   `power_watts = engine_power_hp * 745.7`

2. **Empuxo Estimado**:
   Uma estimativa aproximada da capacidade de empuxo (em Newtons) baseada na eficiência assumida do conjunto propulsor (70%):
   `estimated_thrust = (power_watts / speed) * 0.7`

3. **Requisito Mínimo de Empuxo**:
   O sistema estipula o empuxo mínimo considerando o arrasto induzido, adotando uma aproximação genérica de eficiência aerodinâmica (Lift-to-Drag ratio L/D ≈ 17):
   `min_thrust = weight_kg * 9.81 * (1 / 17)`

4. **Filtro de Eficiência Mínima**:
   A eficiência requerida da hélice no catálogo considera a proporção da potência e velocidade de cruzeiro:
   `min_efficiency = (estimated_thrust * speed) / power_watts`

A recomendação cruza as exigências (`min_thrust`) com os dados das hélices, filtrando e enviando os melhores candidatos para a análise do LLM.
