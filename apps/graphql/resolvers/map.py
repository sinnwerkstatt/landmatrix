from apps.landmatrix.models.deal import Deal


# TODO: This resolver is for the old frontend
def resolve_markers(_obj, _info, region_id=None, country_id=None):
    return Deal.get_geo_markers(region_id, country_id)
