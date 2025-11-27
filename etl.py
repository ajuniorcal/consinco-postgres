import os
import time
import requests
from sqlalchemy.orm import Session
from database import SessionLocal
from models import (
    Produto, Fornecedor, EstoqueAtual, EstoqueHistorico, Venda, ETLLog
)
from utils.dedup import ignore_duplicates
from datetime import datetime

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
# FUNÇÃO PARA GRAVAR LOG POR ENTIDADE
# =============================================
def salvar_log(db, entidade, stats, maior_descricao, inicio, fim):
    duracao_ms = int((fim - inicio).total_seconds() * 1000)

    log = ETLLog(
        entidade=entidade,
        inicio=inicio,
        fim=fim,
        qt_processados=stats["processados"],
        qt_novos=stats["novos"],
        qt_atualizados=stats["atualizados"],
        qt_erros=stats["erros"],
        duracao_ms=duracao_ms,
        status="sucesso" if stats["erros"] == 0 else "parcial",
        maior_descricao=maior_descricao
    )

    db.add(log)


# =============================================
# ROTINA ETL PRINCIPAL
# =============================================
def etl_run():
    print("\n======= INICIANDO ETL =======")

    db: Session = SessionLocal()

    entidades = [
        ("produtos", Produto),
        ("fornecedores", Fornecedor),
        ("estoque-atual", EstoqueAtual),
        ("estoque-historico", EstoqueHistorico),
        ("vendas", Venda),
    ]

    for endpoint, model in entidades:
        inicio = datetime.now()

        dados = fetch_all(endpoint)
        stats = ignore_duplicates(db, model, dados)

        # Maior descrição 
        if endpoint == "produtos":
            maior = max((x.get("descricao", "") for x in dados), key=len, default="")
        elif endpoint == "fornecedores":
            maior = max((x.get("nome", "") for x in dados), key=len, default="")
        else:
            maior = ""

        fim = datetime.now()

        salvar_log(db, endpoint, stats, maior, inicio, fim)

    db.commit()
    db.close()

    print("\n======= ETL FINALIZADO =======")
    return {"status": "ETL completed successfully"}
