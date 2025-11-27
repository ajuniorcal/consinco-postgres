def ignore_duplicates(db, model, data_list):
    """
    Insere dados no banco ignorando registros cujo ID já exista.
    Retorna estatísticas para logging.
    """
    if not data_list:
        print(f"[WARN] Nenhum dado recebido para {model.__tablename__}")
        return {
            "processados": 0,
            "novos": 0,
            "atualizados": 0,
            "erros": 0
        }

    # IDs já existentes no banco
    existing_ids = {
        row[0] for row in db.query(model.id).all()
    }

    inserts = []
    novos = 0
    atualizados = 0
    erros = 0

    for item in data_list:
        try:
            if item["id"] not in existing_ids:
                inserts.append(model(**item))
                novos += 1
            else:
                atualizados += 1
        except Exception:
            erros += 1

    if inserts:
        db.bulk_save_objects(inserts)
        print(f"[OK] Inseridos {novos} itens em {model.__tablename__}")
    else:
        print(f"[SKIP] Nenhum novo item para {model.__tablename__}")

    return {
        "processados": len(data_list),
        "novos": novos,
        "atualizados": atualizados,
        "erros": erros
    }
