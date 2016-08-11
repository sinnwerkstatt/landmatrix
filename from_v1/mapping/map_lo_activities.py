from django.db.models.aggregates import Max
from functools import lru_cache

from .land_observatory_objects.tags import A_Value
from .land_observatory_objects.activity import Activity
from .land_observatory_objects.tag_groups import A_Tag_Group
from .map_lo_model import MapLOModel
from .map_activity import calculate_history_date, get_history_user
from django.utils import timezone
from migrate import V2

import landmatrix.models

from django.db import connections

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

def map_status_id(id):
    return id


class MapLOActivities(MapLOModel):

    _save = False

    old_class = Activity
    new_class = landmatrix.models.Activity
    attributes = {
        'fk_status': ('fk_status_id', map_status_id),
    }

    @classmethod
    def all_records(cls):
        ids = cls.all_ids()
        # exclude the deals that have been imported from landmatrix and not changed
        # ...

        all_deals = Activity.objects.using(cls.DB).filter(pk__in=ids)
        deals = [
            deal
            for deal in all_deals
            if get_deal_country(deal) not in ['China', 'Myanmar', 'Tanzania, United Republic of', 'Viet Nam']
            if not is_unchanged_imported_deal(deal)
        ]
        cls._count = len(deals)

        return Activity.objects.using(cls.DB).filter(pk__in=[deal.id for deal in deals]).values()

    @classmethod
    def all_ids(cls):
        cursor = connections[cls.DB].cursor()
        cursor.execute("""
    SELECT id
    FROM activities AS a
    WHERE version = (SELECT MAX(version) FROM activities WHERE activity_identifier = a.activity_identifier)
    ORDER BY activity_identifier
            """)
        return [id[0] for id in cursor.fetchall()]

    tag_group_to_attribute_group_ids = {}

    @classmethod
    def save_activity_record(cls, new, save, imported=False):
        latest_historical_activity = None
        activity_identifier = cls.get_deal_id(new)
        if save:
            new.id = None  # Don't assume that ids line up
            new.activity_identifier = activity_identifier
            new.fk_status = landmatrix.models.Status.objects.get(
                name="pending")
            new.save(using=V2)

        #if not imported:
        versions = cls.get_activity_versions(new)
        for i, version in enumerate(versions):
            # Only save newest version
            if i+1 == len(version):
                historical_activity = landmatrix.models.HistoricalActivity(
                    id=new.id,
                    activity_identifier=activity_identifier,
                    availability=version['reliability'],
                    fk_status_id=version['fk_status'],
                    fully_updated=False,
                    history_date=calculate_history_date(versions, i),
                    history_user=get_history_user(version))
                changeset = landmatrix.models.ActivityChangeset(
                    comment='Imported from Land Observatory',
                    fk_activity=historical_activity)

                if save:
                    historical_activity.save(using=V2)
                    changeset.save(using=V2)



        return new

    @classmethod
    def save_record(cls, new, save):
        """Save all versions of an activity as HistoricalActivity records."""
        lo_record_id = new.id
        cls._save = save
        tag_groups = A_Tag_Group.objects.using(cls.DB).filter(fk_activity=lo_record_id)

        imported = is_imported_deal_groups(tag_groups)
        if imported:
            # set activity identifier to Tag "Original reference number"
            original_refnos = get_group_tags(tag_groups, "Original reference number")
            new.activity_identifier = original_refnos[0]

        new = cls.save_activity_record(new, save, imported)

        cls.write_standard_tag_groups(new, tag_groups)

        group_proxy = type('MockTagGroup', (object,), {"fk_activity": new.id, 'id': None})
        cls.write_activity_attribute_group(
            {'not_public_reason': 'Land Observatory Import (new)' if not imported else 'Land Observatory Import (duplicate)'},
            group_proxy,
            None,
            'not_public', None
        )

        uuid = Activity.objects.using(cls.DB).filter(id=lo_record_id).values_list('activity_identifier', flat=True).first()
        cls.write_activity_attribute_group(
            {'type': 'Land Observatory Import', 'landobservatory_uuid': str(uuid)},
            group_proxy,
            None,
            'data_source_1', None
        )

    @classmethod
    def write_standard_tag_groups(cls, new, tag_groups):
        for tag_group in tag_groups:
            attrs = {}
            polygon = None
            group_name = cls.tag_group_name(tag_group)

            # set location - stored in activity in LO, but tag group in LM
            if group_name == 'location_1':
                attrs['point_lat'] = new.point.get_y()
                attrs['point_lon'] = new.point.get_x()

            # area boundaries.
            if tag_group.geometry is not None:
                polygon = tag_group.geometry

            for tag in cls.relevant_tags(tag_group):
                key = tag.key.key
                value = tag.value.value

                if key in attrs and value != attrs[key]:
                    cls.write_activity_attribute_group_with_comments(attrs, tag_group, None,
                                                                     group_name, polygon)
                    attrs = {}
                    polygon = None

                attrs[key] = value

            if attrs:
                cls.write_activity_attribute_group_with_comments(attrs, tag_group, None,
                                                                 group_name, polygon)

    @classmethod
    def tag_group_name(cls, tag_group):
        map_to_name = {
            'Animals': 'crop_animal_mineral',
            'Annual leasing fee area (ha)': 'leasing_fees',
            'Announced amount of investement': '',
            'Announced amount of investment': '',
            'Area (ha)': '',
            'Benefits for local communities': 'community_compensation',
            'Consultation of local community': 'community_reaction',
            'Contract area (ha)': 'contract_farming',
            'Contract date': 'contract_farming',
            'Contract farming': 'contract_farming',
            'Contract Number': 'contract_farming',
            'Country': 'location_1',
            'Crop': 'crop_animal_mineral',
            'Current area in operation (ha)': 'production_size',
            'Current Number of daily/seasonal workers': 'total_number_of_jobs_created',
            'Current number of employees': 'total_number_of_jobs_created',
            'Current total number of jobs': 'total_number_of_jobs_created',
            'Data source': 'data_source_1',
            'Date': '',
            'Duration of Agreement (years)': 'agreement_duration',
            'Files': 'data_source_1',
            'Former predominant land cover': 'land_cover',
            'Former predominant land owner': 'land_owner',
            'Former predominant land use': 'land_use',
            'How did community react': 'community_reaction',
            'How much do investors pay for water': 'water_extraction_amount',
            'How much water is extracted (m3/year)': 'water_extraction_amount',
            'Implementation status': 'implementation_status',
            'Intended area (ha)': 'land_area',
            'Intention of Investment': 'intention',
            'Leasing fee (per year)': 'leasing_fees',
            'Mineral': 'crop_animal_mineral',
            'Name': '',
            'Nature of the deal': 'nature',
            'Negotiation Status': 'negotiation_status',
            'Number of farmers': '',
            'Number of people actually displaced': 'number_of_displaced_people',
            'Original reference number': '',
            'Percentage': '',
            'Planned Number of daily/seasonal workers': 'total_number_of_jobs_created',
            'Planned number of employees': 'total_number_of_jobs_created',
            'Planned total number of jobs': 'total_number_of_jobs_created',
            'Promised or received compensation': 'community_compensation',
            'Purchase price': 'purchase_price',
            'Purchase price area (ha)': 'purchase_price',
            'Remark': 'data_source_1',
            'Scope of agriculture': '',
            'Scope of forestry': '',
            'Spatial Accuracy': 'location_1',
            'URL / Web': 'data_source_1',
            'Use of produce': 'use_of_produce',
            'Water extraction': 'water_extraction_envisaged',
            'Year': '',
        }

        try:
            for key, value in map_to_name.items():
                if key in tag_group.tag.key.key:
                    return value
            print(tag_group, tag_group.tag)
            return A_Value.objects.using(cls.DB).get(pk=tag_group.tag.fk_a_value).value
        except Exception:
            return None

    @classmethod
    def tag_group_key(cls, tag_group):
        try:
            return tag_group.tag.key.key
        except Exception:
            return None

    @classmethod
    def relevant_tags(cls, tag_group):
        return tag_group.tags

    @classmethod
    def write_activity_attribute_group_with_comments(cls, attrs, tag_group, year, name, polygon):
        if (len(attrs) == 1) and attrs.get('name'):
            return

        attrs = transform_attributes(attrs)
        aag = cls.write_activity_attribute_group(
            attrs, tag_group, year, name, polygon
        )

    @classmethod
    def write_activity_attribute_group(cls, attrs, tag_group, year, name, polygon):
        activity_id = cls.matching_activity_id(tag_group)
        if 'YEAR' in attrs:
            year = attrs['YEAR']
            del attrs['YEAR']

        save = cls._save and cls.is_current_version(tag_group)
        aag = landmatrix.models.ActivityAttributeGroup(name=name)
        english = landmatrix.models.Language.objects.get(pk=1)
        if save:
            aag.save(using=V2)
            raise IOError("ok")

        if activity_id:
            for key, value in attrs.items():
                aa = landmatrix.models.ActivityAttribute(
                    fk_activity_id=activity_id,
                    fk_language=english,
                    name=key,
                    value=value,
                    date=year,
                    polygon=polygon
                )
                aa = landmatrix.models.HistoricalActivityAttribute(
                    fk_activity_id=activity_id,
                    fk_language=english,
                    name=key,
                    value=value,
                    date=year,
                    polygon=polygon,
                )
                if save:
                    aa.save(using=V2)

        # No need to import LO history
        #if cls._save:
        #    if not cls.is_current_version(tag_group):
        #        
        #        aag = landmatrix.models.HistoricalActivityAttribute.objects.create(
        #            history_date=cls.get_history_date(tag_group),
        #            fk_activity_id=activity_id,
        #            fk_language=landmatrix.models.Language.objects.get(pk=1),
        #            date=year,
        #            attributes=attrs,
        #            name=name,
        #            polygon=polygon
        #        )
#
        if hasattr(aag, 'id'):
            cls.tag_group_to_attribute_group_ids[tag_group.id] = aag.id

        return aag

    @classmethod
    def is_current_version(cls, tag_group):
        return tag_group.fk_activity == cls.matching_activity_id(tag_group)

    @classmethod
    @lru_cache(maxsize=128, typed=True)
    def matching_activity_id(cls, tag_group):
        activity_identifier = landmatrix.models.HistoricalActivity.objects.filter(
            id=tag_group.fk_activity
        ).values_list(
            'activity_identifier', flat=True
        ).distinct().first()
        current_activity = landmatrix.models.Activity.objects.using(V2).filter(
            activity_identifier=activity_identifier
        ).values_list('id', flat=True).distinct().first()

        return current_activity

    @classmethod
    def get_deal_id(cls, activity):
        # if activity already in DB, return its ID
        return landmatrix.models.Activity.objects.using(V2).values().\
            aggregate(Max('activity_identifier'))['activity_identifier__max']+1

    @classmethod
    def get_activity_versions(cls, activity):
        cursor = connections[cls.DB].cursor()
        cursor.execute(
            """SELECT id FROM activities AS a WHERE activity_identifier = {}
            ORDER BY version """.format(activity.activity_identifier)
        )
        ids = [id[0] for id in cursor.fetchall()]
        return Activity.objects.using(cls.DB).filter(
            pk__in=ids).order_by('pk').values()


def is_unchanged_imported_deal(deal):
    if not is_imported_deal(deal):
        return False
    return deal.timestamp_review is None


def is_imported_deal(deal):
    return 'http://www.landmatrix.org' in get_deal_tags(deal, 'URL / Web')


def is_imported_deal_groups(groups):
    for group in groups:
        for tag in group.tags:
            if tag.key.key == 'URL / Web' and tag.value.value == 'http://www.landmatrix.org':
                return True
    return False


def transform_attributes(attrs):
    try:
        attrs = {
            rename_key(key): clean_attribute(key, value) for key, value in attrs.items()
        }
        if 'NUMBER_OF_FARMERS' in attrs:
            if attrs.get('contract_farming', '') == 'On the lease':
                attrs['on_the_lease_farmers'] = attrs['NUMBER_OF_FARMERS']
            else:
                attrs['off_the_lease_farmers'] = attrs['NUMBER_OF_FARMERS']
            del attrs['NUMBER_OF_FARMERS']
        if 'NAME' in attrs:
            del attrs['NAME']
        if 'YEAR' in attrs:
            attrs = {
                key: value+'#'+attrs['YEAR']+'-01-01' if isinstance(value, str) else value
                for key, value in attrs.items()
                if key != 'YEAR'
            }
            # don't delete from attrs, that is done in write_activity_attribute_group() above
        if 'REMARK' in attrs:
            if attrs.get('url') == 'http://www.landmatrix.org':
                pass
            elif 'implementation_status' in attrs:
                attrs['implementation_status_comment'] = attrs['REMARK']
            elif 'data_source' in attrs:
                attrs['data_source_1_comment'] = attrs['REMARK']
            elif 'intended_size' in attrs:
                attrs['land_area_comment'] = attrs['REMARK']
            elif 'point_lat' in attrs:
                attrs['location_1_comment'] = attrs['REMARK']
            elif 'community_consultation' in attrs:
                attrs['community_consultation_comment'] = attrs['REMARK']
            elif 'community_reaction' in attrs:
                attrs['community_reaction_comment'] = attrs['REMARK']
            elif 'contract_farming' in attrs:
                attrs['contract_farming_comment'] = attrs['REMARK']
            elif 'annual_leasing_fee' in attrs:
                attrs['leasing_fees_comment'] = attrs['REMARK']
            elif 'purchase_price' in attrs:
                attrs['purchase_price_comment'] = attrs['REMARK']
            elif 'water_extraction_envisaged' in attrs:
                attrs['water_extraction_envisaged_comment'] = attrs['REMARK']
            elif 'number_of_displaced_people' in attrs:
                attrs['number_of_displaced_people_comment'] = attrs['REMARK']

            elif 'use_of_produce' in attrs or 'use_of_produce_comment' in attrs:
                attrs['use_of_produce_comment'] += attrs['REMARK']

            elif 'benefits' in attrs['REMARK']:
                attrs['materialized_benefits_comment'] = attrs['REMARK']

            del attrs['REMARK']

    except TypeError:
        print(attrs)
        raise Exception

    return attrs


def clean_attribute(key, value):
    if isinstance(value, str):
        # HSTORE attribute values can not take strings longer than that due to index constraints :-(
        return value[:3000]
    return value


def rename_key(key):
    return LM_ATTRIBUTES.get(key, key)


LM_ATTRIBUTES = {
    'Animals':                          'animals',
    "Animales":                          'animals',
    'Annual leasing fee area (ha)':     'annual_leasing_fee_area',
    "Área de la cuota anual de arrendamiento (ha)":     'annual_leasing_fee_area',
    'Announced amount of investement':  'purchase_price_comment',
    'Announced amount of investment':   'purchase_price_comment',
    'Area (ha)':                        'intended_size',
    "Área pretendida (ha)":                        'intended_size',
    'Benefits for local communities':   'promised_benefits',
    'Consultation of local community':  'community_consultation',
    "Contreparties pour les populations locales":  'community_consultation',
    "Consulta a las comunidades locales":  'community_consultation',
    "Consultations tenues au niveau local ":  'community_consultation',
    'Contract area (ha)':               'contract_size',
    "Área del contrato (ha)":               'contract_size',
    "Superficie sous contrat (ha)":               'contract_size',
    'Contract date':                    'contract_date',
    "Date de signature du contrat":                    'contract_date',
    'Contract farming':                 'contract_farming',
    "Agriculture contractuelle":                 'contract_farming',
    "Contrato de trabajo agrícola":                 'contract_farming',
    'Contract Number':                  'contract_number',
    "Número de contrato":                  'contract_number',
    'Country':                          'target_country',
    "País":                          'target_country',
    "Pays":                          'target_country',
    'Crop':                             'crops',
    "Cultivo":                             'crops',
    "Cultures":                             'crops',
    'Current area in operation (ha)':   'production_size',
    "Área actual en operación (ha)":   'production_size',
    "Superficie exploitée (ha) ":   'production_size',
    'Current Number of daily/seasonal workers': 'total_jobs_current_daily_workers',
    "Emplois temporaires créés (nombre)": 'total_jobs_current_daily_workers',
    "Número actual de trabajadores por día o por temporada": 'total_jobs_current_daily_workers',
    'Current number of employees':      'total_jobs_current_employees',
    "Emplois permanents créés (nombre)":      'total_jobs_current_employees',
    "Número actual de empleados":      'total_jobs_current_employees',
    'Current total number of jobs':     'total_jobs_current',
    "Número total de empleos actual":     'total_jobs_current',
    "Emplois total créés":     'total_jobs_current',
    'Data source':                      'data_source',
    "Source des données":                      'data_source',
    'Date':                             'date',
    'Duration of Agreement (years)':    'agreement_duration',
    "Duración del Contrato (años)":    'agreement_duration',
    "Durée du contrat (années)":    'agreement_duration',
    'Files':                            'file',
    "Fecha":                            'file',
    "Fichiers":                            'file',
    'Former predominant land cover':    'land_cover',
    "Couverture végétale dominante antérieure":    'land_cover',
    "Recubierta original predominante de la tierra":    'land_cover',
    'Former predominant land owner':    'land_owner',
    "Dueño original predominante de la tierra":    'land_owner',
    "Statuts juridiques antérieurs des terres ":    'land_owner',
    'Former predominant land use':      'land_use',
    "Usages antérieurs de la terre":      'land_use',
    "Uso original predominante de la tierra":      'land_use',
    'How did community react':          'community_reaction',
    '¿Cómo ha reaccionado la comunidad?':          'community_reaction',
    "Réactions des communautés locales":          'community_reaction',
    'How much do investors pay for water': 'how_much_do_investors_pay_comment',
    "Cuánto paga el inversor por el agua": 'how_much_do_investors_pay_comment',
    "Redevances hydrauliques en AR/m3": 'how_much_do_investors_pay_comment',
    'How much water is extracted (m3/year)': 'water_extraction_amount',
    "Cuánta agua es extraida (m3/año)": 'water_extraction_amount',
    "Volume d'eau prélevé en m3/année": 'water_extraction_amount',
    'Implementation status':            'implementation_status',
    "Estado de aplicación":            'implementation_status',
    "Etat d'avancement":            'implementation_status',
    'Intended area (ha)':               'intended_size',
    "Superficie visée (ha)":               'intended_size',
    'Intention of Investment':          'intention',
    "Intención de la inversión":          'intention',
    'Leasing fee (per year)':           'annual_leasing_fee',
    "Redevances foncières annuelles (total payé par année)":           'annual_leasing_fee',
    'Mineral':                          'minerals',
    "Minerales":                          'minerals',
    "Minéraux":                          'minerals',
    'Name':                             'NAME',
    'Nature of the deal':               'nature',
    "Carácter del acuerdo":               'nature',
    'Negotiation Status':               'negotiation_status',
    "Estado de la negociación":               'negotiation_status',
    'Number of farmers':                'NUMBER_OF_FARMERS',
    "Nombre d'agriculteurs ":                'NUMBER_OF_FARMERS',
    "Número de agricultores":                'NUMBER_OF_FARMERS',
    'Number of people actually displaced': 'number_of_displaced_people',
    "Nombre de personnes effectivement déplacées": 'number_of_displaced_people',
    "Número de personas desplazadas": 'number_of_displaced_people',
    'Original reference number':        'ORIGINAL_REFERENCE_NUMBER',
    "Número de referencia original":        'ORIGINAL_REFERENCE_NUMBER',
    'Planned Number of daily/seasonal workers': 'total_jobs_planned_daily_workers',
    "Emplois temporaires annoncés (nombre)": 'total_jobs_planned_daily_workers',
    "Número de trabajadores planeados diarios/o por temporada": 'total_jobs_planned_daily_workers',
    'Planned number of employees':      'total_jobs_planned_employees',
    "Emplois permanents annoncés (nombre)":      'total_jobs_planned_employees',
    'Planned total number of jobs':     'total_jobs_planned',
    "Emplois total annoncés":     'total_jobs_planned',
    "Total de empleos planeados":     'total_jobs_planned',
    'Promised or received compensation': 'promised_compensation',
    "Beneficios para las comunidades locales": 'promised_compensation',
    "Compensación prometidio o recibida": 'promised_compensation',
    'Purchase price':                   'purchase_price',
    "Prix d'achat total":                   'purchase_price',
    "Precio de compra":                   'purchase_price',
    'Purchase price area (ha)':         'purchase_price_area',
    "Prix d'achat par ha":         'purchase_price_area',
    "Área del precio de compra (ha)":         'purchase_price_area',
    'Remark':                           'REMARK',
    "Remarque":                           'REMARK',
    'Scope of agriculture':             'intention',
    "Ámbito Agrícola":             'intention',
    "Destination des produits agricoles":             'intention',
    'Scope of forestry':                'intention',
    "Ámbito Forestal":             'intention',
    "Destination des produits forestiers":             'intention',
    'Spatial Accuracy':                 'level_of_accuracy',
    "Precisión espacial":                 'level_of_accuracy',
    "Résolution spatiale ":                 'level_of_accuracy',
    'URL / Web':                        'url',
    "Página Web":                        'url',
    "URL : Web":                        'url',
    'Use of produce':                   'use_of_produce_comment',
    "Uso de los productos":                   'use_of_produce_comment',
    'Water extraction':                 'water_extraction_envisaged',
    "Extracción de agua":                 'water_extraction_envisaged',
    "Utilisation d'eau ":                 'water_extraction_envisaged',
    'Year':                             'YEAR',
    "Année":                             'YEAR',
    "Año":                             'YEAR',
}


def get_deal_country(deal):
    for group in deal.tag_groups:
        for tag in group.tags:
            if tag.key.key == 'Country':
                return tag.value.value


def get_deal_tags(deal, key):
    return [tag.value.value for group in deal.tag_groups for tag in group.tags if tag.key.key == key]


def get_group_tags(groups, key):
    return [tag.value.value for group in groups for tag in group.tags if tag.key.key == key]
