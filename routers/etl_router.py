from fastapi import APIRouter
from etl import etl_run

router = APIRouter(prefix="/etl", tags=["ETL"])

@router.post("/run")
def run_etl():
    """Executa o processo ETL manualmente."""
    result = etl_run()
    return result