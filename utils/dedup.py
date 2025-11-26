def ignore_duplicates(db, model, data_list):
    """
    Insere dados no banco ignorando registros cujo ID já exista.
    """
    if not data_list:
        print(f"[WARN] Nenhum dado recebido para {model.__tablename__}")
        return

    existing_ids = {
        item.id for item in db.query(model.id).all()
    }

    inserts = []

    for item in data_list:
        if item["id"] not in existing_ids:
            inserts.append(model(**item))

    if inserts:
        db.bulk_save_objects(inserts)
        print(f"[OK] Inseridos {len(inserts)} itens em {model.__tablename__}")
    else:
        print(f"[SKIP] Nenhum novo item para {model.__tablename__}")
