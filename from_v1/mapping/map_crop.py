from mapping.map_model import MapModel
import landmatrix.models
import old_editor.models

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


def map_crop_name(name):
    return name


def map_crop_code(code):
    return code


def map_crop_slug(slug):
    return slug


class MapCrop(MapModel):
    old_class = old_editor.models.Crop
    new_class = landmatrix.models.Crop
    attributes = {
        'agricultural_produce': 'fk_agricultural_produce',
        'name': ('name', map_crop_name),
        'code': ('code', map_crop_code),
        'slug': ('slug', map_crop_slug)
    }
    depends = [MapAgriculturalProduce]


class MapAgriculturalProduce(MapModel):
    old_class = old_editor.models.AgriculturalProduce
    new_class = landmatrix.models.AgriculturalProduce


class MapAnimal(MapModel):
    old_class = old_editor.models.Animal
    new_class = landmatrix.models.Animal


class MapMineral(MapModel):
    old_class = old_editor.models.Mineral
    new_class = landmatrix.models.Mineral
