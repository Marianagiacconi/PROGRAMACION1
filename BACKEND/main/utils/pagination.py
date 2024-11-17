def generalPagination(request):
    pageConfig = {"page": 1, "per_page": 20}  # Comienza en 1 para la primera página

    # Obtener el JSON del request si está disponible
    data = request.get_json(silent=True)
    
    if data:  # Solo procede si hay datos en JSON
        filters = data.items()
        for key, value in filters:
            if key == 'page':
                pageConfig["page"] = max(1, int(value))  # Asegura que page sea al menos 1
            elif key == 'per_page':
                pageConfig["per_page"] = max(1, int(value))  # Asegura que per_page sea al menos 1

    return pageConfig
