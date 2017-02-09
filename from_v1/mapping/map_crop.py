from django.db.models.aggregates import Max
from django.utils.text import slugify
from mapping.map_model import MapModel
import landmatrix.models
import old_editor.models
from migrate import V1, V2
from django.db import transaction



class MapAgriculturalProduce(MapModel):
    old_class = old_editor.models.AgriculturalProduce
    new_class = landmatrix.models.AgriculturalProduce


CHANGED_CROPS = {
    'Algae': 'Seaweed / Macroalgae(unspecified)',
    'Aquaculture': 'Aquaculture (unspecified crops)',
    'Cereals (no specification)': 'Cereals (unspecified)',
    'Chert': None,
    'Citrus Fruits': 'Citrus Fruits (unspecified)',
    'Flowers': 'Flowers (unspecified)',
    'Fodder Plants': 'Fodder Plants (unspecified)',
    'Food crops (no specification)': 'Food crops (unspecified)',
    'Fruit': 'Fruit (unspecified)',
    'Glucose Syrup': None,
    'Grains': 'Grains (unspecified)',
    'Herbs (no specification)': 'Herbs (unspecified)',
    'Mariculture': None,
    'Oil Seeds': 'Oil Seeds (unspecified)',
    'Peanut': 'Peanut (groundnut)',
    'Pulses': 'Pulses (unspecified)',
    'Rubber': 'Rubber tree',
    'Sea Cucumber': None,
    'Seed Production': 'Seeds Production (unspecified)',
    'Starch': None,
    'Sugar (no specification)': 'Sugar (unspecified)',
    'Trees': 'Trees (unspecified)',
    'Vegetables': 'Vegetables (unspecified)',
}
NEW_CROPS = ['Oats', 'Spices (unspecified)', 'Other crops (please specify)']


def add_new_crops_if_not_present():
    for crop_name in NEW_CROPS:
        if not landmatrix.models.Crop.objects.using(V2).filter(name=crop_name).exists():
            # create() somehow does not set a correct pk so i have to find out a free one myself
            last_id = landmatrix.models.Crop.objects.using(V2).values().aggregate(Max('id'))['id__max']
            landmatrix.models.Crop.objects.using(V2).create(
                name=crop_name, slug=slugify(crop_name), code=crop_name[:3].upper(), id=last_id+1
            )


def map_crop_name(name):
    return CHANGED_CROPS.get(name, name)


def map_crop_slug(slug):
    for potential_new_name in CHANGED_CROPS.keys():
        if slug == slugify(potential_new_name):
            return slugify(CHANGED_CROPS[potential_new_name])
    return slug


class MapCrop(MapModel):
    old_class = old_editor.models.Crop
    new_class = landmatrix.models.Crop
    attributes = {
        'agricultural_produce': 'fk_agricultural_produce',
        'name': ('name', map_crop_name),
        'slug': ('slug', map_crop_slug)
    }
    depends = [MapAgriculturalProduce]

    @classmethod
    @transaction.atomic(using=V2)
    def map_all(cls, save=False, verbose=False):
        cls._check_dependencies()
        cls._start_timer()

        for index, record in enumerate(cls.all_records()):
            cls.map_record(record, save, verbose)
            cls._print_status(record, index)

        add_new_crops_if_not_present()

        cls._done = True
        cls._print_summary()

    @classmethod
    def all_records(cls):
        to_delete = [
            key for key, value in CHANGED_CROPS.items() if value is None or isinstance(value, tuple)
        ]
        return old_editor.models.Crop.objects.using(V1).exclude(name__in=to_delete).values()


CHANGED_ANIMALS = {
    'Abalone': None,
    'Aquaculture': 'Aquaculture (animals)',
    'Chicken': None,
    'Cows': None,
    'Mariculture': None,
    'Tilapia Fish': None,
}
NEW_ANIMALS = ['Beef Cattle', 'Shrimp', 'Other crops (please specify)']


def add_new_animals_if_not_present():
    for animal_name in NEW_ANIMALS:
        if not landmatrix.models.Animal.objects.using(V2).filter(name=animal_name).exists():
            # create() somehow does not set a correct pk so i have to find out a free one myself
            last_id = landmatrix.models.Animal.objects.using(V2).values().aggregate(Max('id'))['id__max']
            landmatrix.models.Animal.objects.using(V2).create(
                name=animal_name, code=animal_name[:3].upper(), id=last_id+1
            )


def map_animal_name(name):
    return CHANGED_ANIMALS.get(name, name)

class MapAnimal(MapModel):
    old_class = old_editor.models.Animal
    new_class = landmatrix.models.Animal
    attributes = {'name': ('name', map_animal_name)}

    @classmethod
    @transaction.atomic(using=V2)
    def map_all(cls, save=False, verbose=False):
        cls._check_dependencies()
        cls._start_timer()

        for index, record in enumerate(cls.all_records()):
            cls.map_record(record, save, verbose)
            cls._print_status(record, index)

        add_new_animals_if_not_present()

        cls._done = True
        cls._print_summary()

    @classmethod
    def all_records(cls):
        to_delete = [
            key for key, value in CHANGED_ANIMALS.items() if value is None or isinstance(value, tuple)
            ]
        return old_editor.models.Animal.objects.using(V1).exclude(name__in=to_delete).values()


CHANGED_MINERALS = {
    'Diamond mining': 'Diamonds',
    'Petroleum': 'Hydrocarbons (e.g. crude oil)',
    'Iron': 'Iron ore',
    'Pyrolisis Plant': None,
}
NEW_MINERALS = [
    'Aluminum', 'Bentonite', 'Chromite', 'Heavy Mineral Sands', 'Lithium', 'Magnetite', 'Rutile',
    'Tin', 'Other minerals (please specify)'
]


def add_new_minerals_if_not_present():
    for mineral_name in NEW_MINERALS:
        if not landmatrix.models.Mineral.objects.using(V2).filter(name=mineral_name).exists():
            # create() somehow does not set a correct pk so i have to find out a free one myself
            last_id = landmatrix.models.Mineral.objects.using(V2).values().aggregate(Max('id'))['id__max']
            landmatrix.models.Mineral.objects.using(V2).create(
                name=mineral_name, code=mineral_name[:3].upper(), id=last_id+1
            )


def map_mineral_name(name):
    return CHANGED_MINERALS.get(name, name)


class MapMineral(MapModel):
    old_class = old_editor.models.Mineral
    new_class = landmatrix.models.Mineral
    attributes = {'name': ('name', map_mineral_name)}

    @classmethod
    def all_records(cls):
        to_delete = [
            key for key, value in CHANGED_MINERALS.items() if value is None or isinstance(value, tuple)
            ]
        return old_editor.models.Mineral.objects.using(V1).exclude(name__in=to_delete).values()


    @classmethod
    @transaction.atomic(using=V2)
    def map_all(cls, save=False, verbose=False):
        cls._check_dependencies()
        cls._start_timer()

        for index, record in enumerate(cls.all_records()):
            cls.map_record(record, save, verbose)
            cls._print_status(record, index)

        add_new_minerals_if_not_present()

        cls._done = True
        cls._print_summary()
