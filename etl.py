import os
import requests
from sqlalchemy.orm import Session
from database import SessionLocal
from models import (
    Produto, Fornecedor, EstoqueAtual, EstoqueHistorico, Venda
)
from utils.dedup import ignore_duplicates

API_URL = os.getenv("SOURCE_API_URL")


# =============================================
# PAGINAÇÃO SAFE
# =============================================
def fetch_all(endpoint: str):
    page = 1
    size = 500
    results = []

    print(f"\n[FETCH] Coletando dados de: {endpoint}")

    while True:
        url = f"{API_URL}/{endpoint}/?page={page}&size={size}"
        print(f"  → GET {url}")

        resp = requests.get(url)
        data = resp.json()

        items = data.get("items", [])
        results.extend(items)

        print(f"    + Recebidos {len(items)} items (página {page})")

        if not data.get("hasNext"):
            break

        page += 1

    print(f"[DONE] Total recebido em {endpoint}: {len(results)}\n")

    return results


# =============================================
# ROTINA ETL PRINCIPAL
# =============================================
def etl_run():
    print("\n======= INICIANDO ETL =======")

    db: Session = SessionLocal()

    # 1 – Buscar dados da API fake
    produtos = fetch_all("produtos")
    fornecedores = fetch_all("fornecedores")
    estoque_atual = fetch_all("estoque-atual")
    estoque_hist = fetch_all("estoque-historico")
    vendas = fetch_all("vendas")

    # 2 – Inserir no banco
    ignore_duplicates(db, Produto, produtos)
    ignore_duplicates(db, Fornecedor, fornecedores)
    ignore_duplicates(db, EstoqueAtual, estoque_atual)
    ignore_duplicates(db, EstoqueHistorico, estoque_hist)
    ignore_duplicates(db, Venda, vendas)

    db.commit()
    db.close()

    print("\n======= ETL FINALIZADO =======")
    return {"status": "ETL completed successfully"}
