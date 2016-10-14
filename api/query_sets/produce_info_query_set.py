from django.utils.translation import ugettext_lazy as _

from api.query_sets.fake_query_set_with_subquery import FakeQuerySetFlat


class AnimalsQuerySet(FakeQuerySetFlat):
    # TODO: these queries are heinous. Fix the data, so we don't have to check
    # for empty strings
    FIELDS = [
        ('name', 'animal.name'),
        ('size', 'SUM(COALESCE(CASE WHEN animals.value2 ~ E\'^\\d+$\' THEN animals.value2::integer ELSE 0 END, a.deal_size))'),
    ]
    ADDITIONAL_JOINS = [
        "LEFT JOIN landmatrix_activityattribute         AS animals          ON a.id = animals.fk_activity_id AND animals.name = 'animals'",
        "LEFT JOIN landmatrix_animal                    AS animal           ON CAST(animals.value AS NUMERIC) = animal.id",
    ]
    GROUP_BY = [
        'animal.name',
    ]
    ORDER_BY = [
        'size',
    ]

class MineralsQuerySet(FakeQuerySetFlat):
    FIELDS = [
        ('name', 'mineral.name'),
        ('size', 'SUM(COALESCE(CASE WHEN minerals.value2 ~ E\'^\\d+$\' THEN minerals.value2::integer ELSE 0 END, a.deal_size))'),
    ]
    ADDITIONAL_JOINS = [
        "LEFT JOIN landmatrix_activityattribute         AS minerals         ON a.id = minerals.fk_activity_id AND minerals.name = 'minerals'",
        "LEFT JOIN landmatrix_mineral                   AS mineral          ON CAST(minerals.value AS NUMERIC) = mineral.id",
    ]
    GROUP_BY = [
        'mineral.name',
    ]
    ORDER_BY = [
        'size',
    ]

class CropsQuerySet(FakeQuerySetFlat):
    FIELDS = [
        ('name', 'crop.name'),
        ('size', 'SUM(COALESCE(CASE WHEN crops.value2 ~ E\'^\\d+$\' THEN crops.value2::integer ELSE 0 END, a.deal_size))'),
    ]
    ADDITIONAL_JOINS = [
        "LEFT JOIN landmatrix_activityattribute         AS crops            ON a.id = crops.fk_activity_id AND crops.name = 'crops'",
        "LEFT JOIN landmatrix_crop                      AS crop             ON CAST(crops.value AS NUMERIC) = crop.id",
    ]
    GROUP_BY = [
        'crop.name',
    ]
    ORDER_BY = [
        'size',
    ]

class ProduceInfoQuerySet(FakeQuerySetFlat):
    """
    Returns: {
        "animals": [
            {"name": "Birds", "size": 3938},
            {"name": "Apes", "size": 3812},
            {"name": "Sheep", "size": 6714},
            {"name": "Mules", "size": 743}
        ],
        "minerals": [
            {"name": "Iron", "size": 17010},
            {"name": "Aluminium", "size": 5842},
            {"name": "Titanium", "size": 1041},
            {"name": "Gold", "size": 5176}
        ],
        "crops": [
            {"name": "Salad", "size": 721},
            {"name": "Carrots", "size": 4294},
            {"name": "Peas", "size": 9800},
            {"name": "Cabbage", "size": 1314},
            {"name": "Radish", "size": 2220}
        ]
    }
    """
    def __init__(self, request):
        self.request = request

    def all(self):
        response = {}
        animals = AnimalsQuerySet(self.request).all()#[:20]
        minerals = MineralsQuerySet(self.request).all()#[:20]
        crops = CropsQuerySet(self.request).all()#[:20]
        response = {
            "animals": animals,
            "minerals": minerals,
            "crops": crops
        }
        return response
