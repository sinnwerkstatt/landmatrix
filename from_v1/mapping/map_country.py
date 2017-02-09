from mapping.map_model import MapModel
import landmatrix.models
import old_editor.models

# from old_editor.models.region import Region as OldRegion
from landmatrix.models.region import Region

from migrate import V1, V2

from django.utils.text import slugify



RENAMED_COUNTRIES = {
    'Bolivia (Plurinational State of)': 'Bolivia',
    'Congo': 'Congo, Rep.',
    "Democratic People's Republic of Korea": "Korea, Dem. People's Rep.",
    'Democratic Republic of the Congo': 'Congo, Dem. Rep.',
    'Egypt': 'Egypt, Arab Rep.',
    'Gambia': 'Gambia, The',
    'Iran (Islamic Republic of)': 'Iran, Islamic Rep.',
    'Kyrgyzstan': 'Kyrgyz Republic',
    "Lao People's Democratic Republic": 'Lao PDR',
    'Micronesia (Federated States of)': 'Micronesia, Fed. Sts.',
    'Occupied Palestinian Territory': 'West Bank and Gaza',
    'Republic of Moldova': 'Moldova',
    'Saint Kitts and Nevis': 'St. Kitts and Nevis',
    'Saint Lucia': 'St. Lucia',
    'Saint Vincent and the Grenadines': 'St. Vincent and the Grenadines',
    'Sao Tome and Principe': 'São Tomé and Principe',
    'The former Yugoslav Republic of Macedonia': 'Macedonia, FYR',
    'United Republic of Tanzania': 'Tanzania',
    'Venezuela (Bolivarian Republic of)': 'Venezuela, RB',
    'Viet Nam': 'Vietnam',
    'Yemen': 'Yemen, Rep.',
}

RESLUGGED_COUNTRIES = {slugify(old_name): slugify(new_name) for (old_name, new_name) in RENAMED_COUNTRIES.items()}


REGIONS = {
    "Eastern Africa": (2, 'Africa'),
    "Central Africa": (2, 'Africa'),
    "Northern Africa": (2, 'Africa'),
    "Southern Africa": (2, 'Africa'),
    "Western Africa": (2, 'Africa'),
    "Caribbean": (419, "Latin America and the Caribbean"),
    "Central America": (419, "Latin America and the Caribbean"),
    "South America": (419, "Latin America and the Caribbean"),
    "Northern America": (21, "Northern America"),
    "Central Asia": (142, "Asia"),
    "Eastern Asia": (142, "Asia"),
    "South Asia": (142, "Asia"),
    "South-East Asia": (142, "Asia"),
    "Western Asia": (142, "Asia"),
    "Middle East": (142, "Asia"),
    "Eastern Europe": (150, "Europe"),
    "Northern Europe": (150, "Europe"),
    "Southern Europe": (150, "Europe"),
    "Western Europe": (150, "Europe"),
    "Australia and New Zealand": (9, "Oceania"),
    "Melanesia": (9, "Oceania"),
    "Micronesia": (9, "Oceania"),
    "Polynesia": (9, "Oceania"),
}


def old_country_name_to_new(name):
    return RENAMED_COUNTRIES.get(name, name)


def old_country_slug_to_new(slug):
    return RESLUGGED_COUNTRIES.get(slug, slug)


def old_region_to_new(fk_region_id):
    region = old_editor.models.Region.objects.using(V1).get(pk=fk_region_id)
    new_region = REGIONS[region.name]
    if not landmatrix.models.Region.objects.using(V2).filter(pk=new_region[0]).exists():
        landmatrix.models.Region(id=new_region[0], name=new_region[1]).save(using=V2)
    # print(region.name, '->', landmatrix.models.Region.objects.using(V2).get(pk=new_region[0]))
    return new_region[0]


class MapCountry(MapModel):
    old_class = old_editor.models.Country
    new_class = landmatrix.models.Country
    attributes = {
        'name': ('name', old_country_name_to_new),
        'slug': ('slug', old_country_slug_to_new),
        'region_id': ('fk_region_id', old_region_to_new),
    }
