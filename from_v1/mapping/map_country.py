from django.utils.text import slugify
from mapping.map_model import MapModel
from mapping.map_region import MapRegion
import landmatrix.models
import old_editor.models

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


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


def old_country_name_to_new(name):
    return RENAMED_COUNTRIES.get(name, name)


def old_country_slug_to_new(slug):
    return RESLUGGED_COUNTRIES.get(slug, slug)


class MapCountry(MapModel):
    old_class = old_editor.models.Country
    new_class = landmatrix.models.Country
    attributes = {
        'region': 'fk_region',
        'name': ('name', old_country_name_to_new),
        'slug': ('slug', old_country_slug_to_new),
    }
    depends = [ MapRegion ]
