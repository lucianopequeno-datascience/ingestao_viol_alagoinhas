# Ingestão de Dados SINAN - Violência Interpessoal e Autoprovocada (Alagoinhas-BA)

Este repositório contém o pipeline de extração e ingestão de dados epidemiológicos referentes à **Violência Interpessoal e Autoprovocada** (agravo `VIOL`) registrados no SINAN (DATASUS). 

O script realiza uma varredura histórica (de 2000 a 2030), filtra os registros exclusivos para residentes do município de Alagoinhas - BA (Código IBGE: `290070`) e armazena os dados brutos na camada Bronze de um Data Lake no Google Cloud Storage, otimizados no formato `.parquet`.

---

## 🏗️ Arquitetura e Tecnologias

* **Fonte de Dados:** FTP DATASUS / SINAN (via biblioteca `PySUS`)
* **Processamento:** Python 3.10, Pandas
* **Otimização de Arquivos:** Fastparquet, PyArrow
* **Armazenamento:** Google Cloud Storage (GCS)
* **Containerização e Deploy:** Docker, Google Cloud Build

---

## 📂 Estrutura do Projeto

| Arquivo | Descrição |
| :--- | :--- |
| `main.py` | Script principal responsável pelo download, filtragem, conversão para parquet e upload dos dados. |
| `requirements.txt` | Lista de dependências Python, com o PySUS fixado em sua versão estável (`1.0.1`). |
| `Dockerfile` | Receita para a construção da imagem do container, incluindo as dependências de sistema (C, GCC, Libmagic). |
| `cloudbuild.yaml` | Arquivo de orquestração de CI/CD para o Cloud Build, com logs restritos ao Cloud Logging. |
| `README.md` | Documentação principal do repositório. |

---

## ⚙️ Configurações do Pipeline

As variáveis principais estão definidas no escopo da função `run_oda_pipeline()` no `main.py`. Caso necessite reaproveitar o código para outros cenários, altere os parâmetros abaixo:

* `BUCKET_NAME`: Nome do bucket de destino no GCS (Padrão: `dados_alagoinhas_bronze`).
* `DESTINATION_FOLDER`: Caminho das pastas no bucket (Padrão: `saude/violencia`).
* `COD_ALAGOINHAS`: Código do município para filtro residencial (Padrão: `290070`).

---

## 🚀 Pré-requisitos

Antes de executar, certifique-se de ter:
1. **Docker** instalado em sua máquina local (para testes).
2. **Google Cloud SDK (`gcloud`)** instalado e autenticado em um projeto GCP.
3. Permissão de escrita (`roles/storage.objectAdmin` ou similar) na Service Account que executará a rotina.

Para rodar localmente utilizando suas próprias credenciais do GCP, autentique-se via:
```bash
gcloud auth application-default login
