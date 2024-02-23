public_paths = [
    "/api/countries/",
    "/api/regions/",
    "/api/currencies/",
    "/api/deals/",
    "/api/deals/{pk}/",
    "/api/deals/{pk}/{version_id}/",
    "/api/investors/",
    "/api/investors/{pk}/",
    "/api/investors/{pk}/{version_id}/",
    "/api/field_choices/",
    "/api/schema/",
]


def preprocessing_filter_spec(endpoints):
    filtered = []

    for path, path_regex, method, callback in endpoints:
        if path in public_paths and method.lower() == "get":
            filtered.append((path, path_regex, method, callback))

    return filtered
