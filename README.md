# Consinco ETL API

Projeto desenvolvido para realizar um processo ETL (Extract, Transform, Load) consumindo dados de uma API fonte e armazenando-os em um banco PostgreSQL.  
A aplicação utiliza FastAPI como interface REST para execução manual do ETL.

---

## 1. Tecnologias utilizadas

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL (Docker)
- Uvicorn
- Requests

---

## 2. Pré-requisitos

- Python 3.10+
- Docker e Docker Compose
- Pip ou pipenv
- Acesso à API fonte (URL definida no .env)

---

## 3. Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto contendo:

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=consinco
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

SOURCE_API_URL=http://localhost:8000/api/v1


A variável `SOURCE_API_URL` define o endereço da API origem dos dados.

---

## 4. Subindo o banco de dados (Docker)

O banco PostgreSQL deve estar rodando em um container.  
Exemplo de comando para criação do container:

```bash
docker run --name consinco-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=consinco -p 5432:5432 -d postgres

```
## 5. Para acessar o banco:

```bash
docker exec -it consinco-postgres psql -U postgres -d consinco
```
## 6. instalar dependencias e rodar projeto:

```bash
pip install -r requirements.txt

uvicorn main:app --reload --port 5000
```
A documentação automática estará disponível em:
```bash

http://localhost:5000/docs
```


## 7. O ETL pode ser acionado via endpoint:
```bash

POST /etl/run ou curl -X POST http://localhost:5000/etl/run
```


## 8. Ao executar, o serviço:

Busca todos os dados paginados da API fonte

Insere ou atualiza registros sem duplicação

Grava os dados nas tabelas SQLAlchemy mapeadas

Retorna um JSON de status

## 9. Estrutura do banco (tabelas)

Tabelas criadas automaticamente:

produtos

fornecedores

estoque_atual

estoque_historico

vendas

O models.py contém o mapeamento completo das colunas conforme a API fonte.

