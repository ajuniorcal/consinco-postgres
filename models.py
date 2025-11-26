from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base


# =========================
# PRODUTOS
# =========================
class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True)
    descricao = Column(String)             # ← Corrigido
    seq_product = Column(Integer, index=True)
    price_sale = Column(Float)
    quantity_available = Column(Float)


# =========================
# FORNECEDORES
# =========================
class Fornecedor(Base):
    __tablename__ = "fornecedores"

    id = Column(Integer, primary_key=True)
    nome = Column(String)                  # ← Corrigido
    cnpj = Column(String)
    status = Column(String)


# =========================
# ESTOQUE ATUAL
# =========================
class EstoqueAtual(Base):
    __tablename__ = "estoque_atual"

    id = Column(Integer, primary_key=True)
    seq_product = Column(Integer)
    id_loja = Column(Integer)
    quantity_available = Column(Float)
    quantity_reserved = Column(Float)


# =========================
# ESTOQUE HISTORICO
# =========================
class EstoqueHistorico(Base):
    __tablename__ = "estoque_historico"

    id = Column(Integer, primary_key=True)
    seq_product = Column(Integer)
    id_loja = Column(Integer)
    quantity_before = Column(Float)
    quantity_after = Column(Float)
    change_reason = Column(String)
    timestamp = Column(DateTime)


# =========================
# VENDAS
# =========================
class Venda(Base):
    __tablename__ = "vendas"

    id = Column(Integer, primary_key=True)
    seq_product = Column(Integer)
    id_loja = Column(Integer)
    quantidade = Column(Float)
    valor_unitario = Column(Float)
    data_venda = Column(DateTime)
