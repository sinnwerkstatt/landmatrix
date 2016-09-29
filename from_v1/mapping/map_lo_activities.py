from functools import lru_cache

from django.db import connections
from django.utils import timezone

import landmatrix.models
from .land_observatory_objects.tags import A_Value
from .land_observatory_objects.activity import Activity
from .land_observatory_objects.tag_groups import A_Tag_Group
from .map_lo_model import MapLOModel
from .map_activity import calculate_history_date
from migrate import V2


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class MapLOActivities(MapLOModel):
    '''
    Activities should be mapped to an existing record where there is one.
    '''
    _save = False

    old_class = Activity
    new_class = landmatrix.models.Activity
    attributes = {
        'fk_status': ('fk_status_id', lambda id: id),
    }

    @classmethod
    def cleanup_previously_imported_rejected_deals(
            cls, save=False, verbose=False):
        '''
        Previously, LO import would import deals that had only one, rejected
        version. Clean these up.
        '''
        # use a list here so Django doesn't try to make a subquery
        rejects = Activity.objects.using(cls.DB).filter(
            fk_status__in=(4, 5), version=1)

        rejected_ids = list(rejects.values_list(
            'activity_identifier', flat=True))

        previous_imports = landmatrix.models.HistoricalActivity.objects.using(
            V2).filter(
            attributes__fk_group__name='imported', attributes__name='id',
            attributes__value__in=rejected_ids)

        if verbose:
            print('Found {} previous LO imports that were rejected.'.format(
                previous_imports.count()))

        for rejected_activity in previous_imports:
            if verbose:
                print('Deleting rejected deal with id {}'.format(
                    rejected_activity.activity_identifier))
            if rejected_activity.public_version:
                if save:
                    rejected_activity.public_version.delete()
            if save:
                rejected_activity.delete()

    @classmethod
    def all_records(cls):
        latest_version_ids = cls.all_ids()
        deals = Activity.objects.using(cls.DB).filter(
            pk__in=latest_version_ids)

        # exclude deals for various reasons
        excluded_country_deal_ids = list([
            deal.pk for deal in deals
            if get_deal_country(deal) in (
                'China', 'Myanmar', 'Tanzania, United Republic of', 'Viet Nam',
            )
        ])
        excluded_lm_import_deal_ids = list([
            deal.pk for deal in deals
            if 'http://www.landmatrix.org' in get_deal_tags(deal, 'URL / Web')
        ])
        excluded_unreviewed_deal_ids = list([
            deal.pk for deal in deals
            if deal.timestamp_review is None
        ])

        deals = deals.exclude(pk__in=excluded_country_deal_ids)
        deals = deals.exclude(pk__in=excluded_lm_import_deal_ids)
        deals = deals.exclude(pk__in=excluded_unreviewed_deal_ids)

        cls._count = deals.count()

        return deals.values()

    @classmethod
    def get_existing_record(cls, record):
        already_imported = cls.new_class.objects.using(V2)
        already_imported = already_imported.filter(
            attributes__fk_group__name='imported', attributes__name='id',
            attributes__value=record['activity_identifier']).first()

        return already_imported

    @classmethod
    def all_ids(cls):
        cursor = connections[cls.DB].cursor()
        cursor.execute("""
    SELECT id
    FROM activities AS a
    WHERE version = (
        SELECT MAX(version) FROM activities
        WHERE activity_identifier = a.activity_identifier
        AND fk_status NOT IN (4, 5)
    )
    ORDER BY activity_identifier
            """)
        return [id[0] for id in cursor.fetchall()]

    tag_group_to_attribute_group_ids = {}

    @classmethod
    def save_activity_record(
            cls, new, save, activity_identifier, imported=False):
        versions = cls.get_activity_versions(new)
        if len(versions) > 0:
            i = len(versions) - 1
        else:
            i = 0

        if not hasattr(cls, '_pending_status'):
            # Don't need to query this every time
            cls._pending_status = landmatrix.models.Status.objects.using(
                V2).get(name="pending")

        new.activity_identifier = activity_identifier
        new.fk_status = cls._pending_status

        if save:
            new.save(using=V2)

        # existing records already have a historical version
        if new.historical_version:
            historical_activity = new.historical_version
        else:
            historical_activity = landmatrix.models.HistoricalActivity(
                public_version=new)

        historical_activity.activity_identifier = new.activity_identifier
        historical_activity.fk_status = cls._pending_status
        historical_activity.history_date = calculate_history_date(versions, i)
        historical_activity.history_user_id = 75

        if save:
            historical_activity.save(using=V2)

        changeset = landmatrix.models.ActivityChangeset(
            comment='Imported from Land Observatory',
            fk_activity=historical_activity)

        if save:
            # Clear out old import changesets to reset the timestamp
            historical_activity.changesets.filter(
                comment='Imported from Land Observatory').delete()
            changeset.save(using=V2)

        return new, historical_activity

    @classmethod
    def save_record(cls, new, old, save):
        """Save all versions of an activity as HistoricalActivity records."""
        lo_record_id = old['id']

        # If the polygon is valid, use it, otherwise ask postgres to try
        # and fix it.
        tag_groups = A_Tag_Group.objects.using(cls.DB).raw('''
            SELECT *,
            CASE
                WHEN a_tag_groups.geometry != '' THEN
                    CASE
                        WHEN ST_IsValid(a_tag_groups.geometry) = FALSE
                            THEN ST_MakeValid(a_tag_groups.geometry)
                        ELSE a_tag_groups.geometry
                    END
                ELSE NULL
            END AS clean_geometry
            FROM a_tag_groups
            WHERE fk_activity = %s
            ''', [lo_record_id])

        activity_identifier = None
        imported = is_imported_deal_groups(tag_groups)
        if imported:
            # set activity identifier to Tag "Original reference number"
            original_refnos = get_group_tags(tag_groups, "Original reference number")
            activity_identifier = original_refnos[0]

        new, historical_activity = cls.save_activity_record(
            new, save, activity_identifier, imported)

        # Clear any existing attrs for imported deals (we're going to write
        # them again)
        landmatrix.models.ActivityAttribute.objects.using(V2).filter(
            fk_activity=new).delete()
        landmatrix.models.HistoricalActivityAttribute.objects.using(V2).filter(
            fk_activity=historical_activity).delete()

        group_proxy = type(
            'MockTagGroup', (object,),
            {"fk_activity": new.id, 'id': None})
        historical_group_proxy = type(
            'MockTagGroup', (object,),
            {"fk_activity": historical_activity.id, 'id': None})
        not_public_attrs = {
            'not_public_reason': 'Land Observatory Import (new)' if not imported else 'Land Observatory Import (duplicate)',
        }
        imported_attrs = {
            'source': 'Land Observatory',
            'id': str(old['activity_identifier']),
            'timestamp': timezone.now().isoformat(),
        }

        # Write both new and historical
        cls.write_standard_tag_groups(
            new, tag_groups, point=getattr(new, 'point'), save=save)
        cls.write_activity_attribute_group(
            new, not_public_attrs, group_proxy, None, 'not_public', None,
            save=save)
        cls.write_activity_attribute_group(
            new, imported_attrs, group_proxy, None, 'imported', None,
            save=save)

        cls.write_standard_tag_groups(
            historical_activity, tag_groups, point=getattr(new, 'point'),
            save=save)
        cls.write_activity_attribute_group(
            historical_activity, not_public_attrs, historical_group_proxy,
            None, 'not_public', None, save=save)
        cls.write_activity_attribute_group(
            historical_activity, imported_attrs, historical_group_proxy, None,
            'imported', None, save=save)

    @classmethod
    def write_standard_tag_groups(
        cls, activity, tag_groups, point=None, save=False):
        location_set = False
        data_source_counter = 0
        for tag_group in tag_groups:
            attrs = {}
            polygon = None
            group_name = cls.tag_group_name(tag_group)

            # Add all data sources, not just the last one
            if group_name == 'data_source':
                group_name = 'data_source_{}'.format(data_source_counter)
                data_source_counter += 1

            # set location - stored in activity in LO, but tag group in LM
            if group_name == 'location_0' and not location_set:
                attrs['point_lat'] = point.get_y()
                attrs['point_lon'] = point.get_x()
                location_set = True

            # area boundaries.
            if tag_group.clean_geometry is not None:
                polygon = tag_group.clean_geometry

            for tag in cls.relevant_tags(tag_group):
                key = tag.key.key
                value = tag.value.value

                # Not sure if this is required, but it doesn't hurt
                if key in attrs and value != attrs[key]:
                    cls.write_activity_attribute_group_with_comments(
                        activity, attrs, tag_group, None, group_name, polygon,
                        save=save)
                    attrs = {}
                    polygon = None

                attrs[key] = value

            if attrs:
                cls.write_activity_attribute_group_with_comments(
                    activity, attrs, tag_group, None, group_name, polygon,
                    save=save)

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
            'Country': 'location_0',
            'Crop': 'crop_animal_mineral',
            'Current area in operation (ha)': 'production_area',
            'Current Number of daily/seasonal workers': 'total_number_of_jobs_created',
            'Current number of employees': 'total_number_of_jobs_created',
            'Current total number of jobs': 'total_number_of_jobs_created',
            'Data source': 'data_source',
            'Date': '',
            'Duration of Agreement (years)': 'agreement_duration',
            'Files': 'data_source',
            'Former predominant land cover': 'land_cover',
            'Former predominant land owner': 'land_owner',
            'Former predominant land use': 'land_use',
            'How did community react': 'community_reaction',
            'How much do investors pay for water': 'water_extraction_amount',
            'How much water is extracted (m3/year)': 'water_extraction_amount',
            'Implementation status': 'implementation_status',
            'Intended area (ha)': 'intended_area',
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
            'Remark': 'data_source',
            'Scope of agriculture': '',
            'Scope of forestry': '',
            'Spatial Accuracy': 'location_0',
            'URL / Web': 'data_source',
            'Use of produce': 'use_of_produce',
            'Water extraction': 'source_of_water_extraction',
            'Year': '',
        }

        try:
            for key, value in map_to_name.items():
                if key in tag_group.tag.key.key:
                    return value
            return A_Value.objects.using(cls.DB).get(pk=tag_group.tag.fk_a_value).value
        except (AttributeError, A_Value.DoesNotExist):
            return None

    @classmethod
    def tag_group_key(cls, tag_group):
        try:
            return tag_group.tag.key.key
        except AttributeError:
            return None

    @classmethod
    def relevant_tags(cls, tag_group):
        return tag_group.tags

    @classmethod
    def write_activity_attribute_group_with_comments(cls, activity, attrs, tag_group, year, name, polygon, save=False):
        if (len(attrs) == 1) and attrs.get('name'):
            return

        attrs = transform_attributes(attrs, group_name=name or '')
        aag = cls.write_activity_attribute_group(
            activity, attrs, tag_group, year, name, polygon, save=save)

    @classmethod
    def write_activity_attribute_group(cls, activity, attrs, tag_group, year, name, polygon, save=False):
        # Depending on the activity type, save the write kind of attrs
        if type(activity) == landmatrix.models.HistoricalActivity:
            attr_model = landmatrix.models.HistoricalActivityAttribute
        else:
            attr_model = landmatrix.models.ActivityAttribute

        if 'YEAR' in attrs:
            year = attrs['YEAR']
            del attrs['YEAR']

        # I think aags should be distinct, but they aren't, so just go with it
        try:
            aag = landmatrix.models.ActivityAttributeGroup.objects.using(
                V2).get(name=name)
        except landmatrix.models.ActivityAttributeGroup.MultipleObjectsReturned:
            aag = landmatrix.models.ActivityAttributeGroup.objects.using(
                V2).filter(name=name).last()
        except landmatrix.models.ActivityAttributeGroup.DoesNotExist:
            aag = landmatrix.models.ActivityAttributeGroup(name=name)
            if save:
                aag.save(using=V2)

        for key, value in attrs.items():
            if '#' in str(value):
                values = value.split('#')
                if len(values) == 2 and len(values[1]) <= 10:
                    value, year = values
            attr = attr_model(
                fk_activity_id=activity.pk,
                fk_language_id=1,
                fk_group=aag,
                name=key,
                value=value,
                date=year,
                polygon=polygon
            )
            if save:
                attr.save(using=V2)

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
    def get_activity_versions(cls, activity):
        return Activity.objects.using(cls.DB).filter(
            activity_identifier=activity.activity_identifier).order_by(
            'version').values()


def is_imported_deal_groups(groups):
    for group in groups:
        for tag in group.tags:
            if tag.key.key == 'URL / Web' and tag.value.value == 'http://www.landmatrix.org':
                return True
    return False


def transform_attributes(attrs, group_name=''):
    clean_attrs = {}
    for key, value in attrs.items():
        key, value = clean_attribute(key, value)
        # Don't use anything we couldn't clean
        if key and str(value):
            clean_attrs[key] = value
    attrs = clean_attrs
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
        remark = attrs.pop('REMARK')

        if attrs.get('url') == 'http://www.landmatrix.org':
            pass
        elif 'implementation_status' in attrs:
            attrs['tg_implementation_status_comment'] = remark
        elif group_name.startswith('data_source'):
            attrs['tg_data_source_comment'] = remark
        elif 'intended_area' in attrs:
            attrs['tg_intended_area_comment'] = remark
        elif group_name.startswith('location') or 'point_lat' in attrs:
            attrs['tg_location_comment'] = remark
        elif 'community_consultation' in attrs:
            attrs['tg_community_consultation_comment'] = remark
        elif 'community_reaction' in attrs:
            attrs['tg_community_reaction_comment'] = remark
        elif 'contract_farming' in attrs:
            attrs['tg_contract_farming_comment'] = remark
        elif 'annual_leasing_fee' in attrs:
            attrs['tg_leasing_fees_comment'] = remark
        elif 'purchase_price' in attrs:
            attrs['tg_purchase_price_comment'] = remark
        elif 'source_of_water_extraction' in attrs:
            attrs['tg_source_of_water_extraction_comment'] = remark
        elif 'number_of_displaced_people' in attrs:
            attrs['tg_number_of_displaced_people_comment'] = remark
        elif 'use_of_produce' in attrs or 'use_of_produce_comment' in attrs:
            attrs['tg_use_of_produce_comment'] = remark
        elif 'benefits' in remark:
            attrs['tg_materialized_benefits_comment'] = remark

    # If we got any jobs created attrs, also set the boolean for that
    # section
    jobs_created_attrs = {
        'total_jobs_current_daily_workers', 'total_jobs_current_employees',
        'total_jobs_current', 'total_jobs_planned_daily_workers',
        'total_jobs_planned_employees', 'total_jobs_planned',
    }
    if jobs_created_attrs.intersection(set(attrs.keys())):
        attrs['total_jobs_created'] = 'True'

    return attrs


def clean_attribute(key, value):
    # Check key
    key = LM_ATTRIBUTES.get(key, key)
    if key == 'contract_farming':
        if value == 'On the lease':
            key = 'on_the_lease'
            value = 't'
        elif value == 'Off the lease':
            key = 'off_the_lease'
            value = 't'

    if key == 'nature':
        if 'Lease/Concession' in value:
            value = value.replace('Lease/Concession', 'Lease')
        elif 'Exploitation License' in value:
            value = value.replace('Exploitation License', 'Resource exploitation license / concession')
    elif key == 'implementation_status':
        if 'Startup phase' in value:
            value = value.replace('Startup phase', 'Startup phase (no production)')
        elif 'In operation' in value:
            value = value.replace('In operation', 'In operation (production)')
    elif key == 'intention':
        if value == 'Mining':
            value = value.replace('Mining', 'Resource extraction')
        elif value == 'carbon sequestration':
            value = value.replace('carbon sequestration', 'For carbon sequestration/REDD')
        elif value == 'wood and fibre':
            value = value.replace('wood and fibre', 'For wood and fibre')
        elif value == 'Renewable energy':
            value = value.replace('Renewable energy', 'Renewable Energy')
        elif value == 'Agrofuels':
            value = value.replace('Agrofuels', 'Biofuels')
    elif key == 'level_of_accuracy':
        if value == "worse than 100km":
            value = 'Country'
        elif value == "10km to 100km":
            value = 'Administrative region'
        elif value == "1km to 10km":
            value = 'Approximate location'
        elif value == "100m to 1km":
            value = 'Exact location'
        elif value == "better than 100m":
            value = 'Coordinates'
    elif key == 'target_country':
        if value == "Lao People's Democratic Republic":
            value = 'Lao PDR'
        try:
            value = landmatrix.models.Country.objects.get(name=value).id
        except Country.DoesNotExist:
            value = ''
    elif key == 'type':
        if value == 'Research paper':
             value = 'Research Paper / Policy Report'
    elif key == 'community_consultation':
        if value not in ("Not consulted", "Limited consultation",
            "Free, Prior and Informed Consent (FPIC)",
            "Certified Free, Prior and Informed Consent (FPIC)", "Other"):
            key = 'tg_community_consultation_comment'
    elif key == 'community_reaction':
        if value not in ("Consent", "Mixed reaction", "Rejection"):
            key = 'tg_community_reaction_comment'
    elif key == 'promised_benefits':
        if value == 'Financial support':
            value = 'Financial Support'
        elif value == 'Water supply':
            value = 'Other'
        elif value == 'Capacity building':
            value = 'Capacity Building'
    elif key == 'land_use':
        if value == 'Pastoralists':
            value = 'Pastoralism'
    elif key == 'land_cover':
        if value == 'Grassland':
            value = 'Shrub land/Grassland'
    elif key == 'source_of_water_extraction':
        if value == 'Ground water':
            value = 'Groundwater'
    # Crops, minerals and animals need to be converted to ids
    elif key == 'crops':
        value = get_crop_id(value) or ''
    elif key == 'minerals':
        value = get_mineral_id(value) or ''
    elif key == 'animals':
        value = get_animal_id(value) or ''

    return key, value


LM_ATTRIBUTES = {
    'Animals':                          'animals',
    "Animales":                          'animals',
    'Annual leasing fee area (ha)':     'annual_leasing_fee_area',
    "Área de la cuota anual de arrendamiento (ha)":     'annual_leasing_fee_area',
    'Announced amount of investement':  'purchase_price_comment',
    'Announced amount of investment':   'purchase_price_comment',
    'Area (ha)':                        'intended_area',
    "Área pretendida (ha)":                        'intended_area',
    'Benefits for local communities':   'promised_benefits',
    'Consultation of local community':  'community_consultation',
    "Contreparties pour les populations locales":  'community_consultation',
    "Consulta a las comunidades locales":  'community_consultation',
    "Consultations tenues au niveau local ":  'community_consultation',
    'Contract area (ha)':               'contract_area',
    "Área del contrato (ha)":               'contract_area',
    "Superficie sous contrat (ha)":               'contract_area',
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
    'Current area in operation (ha)':   'production_area',
    "Área actual en operación (ha)":   'production_area',
    "Superficie exploitée (ha) ":   'production_area',
    'Current Number of daily/seasonal workers': 'total_jobs_current_daily_workers',
    "Emplois temporaires créés (nombre)": 'total_jobs_current_daily_workers',
    "Número actual de trabajadores por día o por temporada": 'total_jobs_current_daily_workers',
    'Current number of employees':      'total_jobs_current_employees',
    "Emplois permanents créés (nombre)":      'total_jobs_current_employees',
    "Número actual de empleados":      'total_jobs_current_employees',
    'Current total number of jobs':     'total_jobs_current',
    "Número total de empleos actual":     'total_jobs_current',
    "Emplois total créés":     'total_jobs_current',
    'Data source':                      'type',
    "Source des données":                      'type',
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
    'How much do investors pay for water': 'tg_how_much_do_investors_pay_comment',
    "Cuánto paga el inversor por el agua": 'tg_how_much_do_investors_pay_comment',
    "Redevances hydrauliques en AR/m3": 'tg_how_much_do_investors_pay_comment',
    'How much water is extracted (m3/year)': 'water_extraction_amount',
    "Cuánta agua es extraida (m3/año)": 'water_extraction_amount',
    "Volume d'eau prélevé en m3/année": 'water_extraction_amount',
    'Implementation status':            'implementation_status',
    "Estado de aplicación":            'implementation_status',
    "Etat d'avancement":            'implementation_status',
    'Intended area (ha)':               'intended_area',
    "Superficie visée (ha)":               'intended_area',
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
    'Use of produce':                   'tg_use_of_produce_comment',
    "Uso de los productos":                   'tg_use_of_produce_comment',
    'Water extraction':                 'source_of_water_extraction',
    "Extracción de agua":                 'source_of_water_extraction',
    "Utilisation d'eau ":                 'source_of_water_extraction',
    'Year':                             'YEAR',
    "Année":                             'YEAR',
    "Año":                             'YEAR',
    "Remark (Negotiation Status)":  'tg_negotiation_status_comment',
    "Remark (Intention of Investment)": 'tg_intention_comment',
}


def get_crop_id(crop_name):
    crop_name = crop_name.replace('(no specification)', '(unspecified)')
    crop = _get_instance_with_name(crop_name, landmatrix.models.Crop)
    return crop.id if crop else None


def get_mineral_id(mineral_name):
    mineral = _get_instance_with_name(mineral_name, landmatrix.models.Mineral)
    return mineral.id if mineral else None


def get_animal_id(animal_name):
    animal = _get_instance_with_name(animal_name, landmatrix.models.Animal)
    return animal.id if animal else None


def _get_instance_with_name(name, model_class):
    '''
    Given a name, try to find the closest match or other.
    Works with Crop, Animal, Mineral.
    '''
    try:
        instance = model_class.objects.get(name=name)
    except model_class.DoesNotExist:
        try:
            instance = model_class.objects.get(name__istartswith=name)
        except (model_class.DoesNotExist, model_class.MultipleObjectsReturned):
            try:
                instance = model_class.objects.get(code='OTH')
            except model_class.DoesNotExist:
                instance = None

    return instance


def get_deal_country(deal):
    for group in deal.tag_groups:
        for tag in group.tags:
            if tag.key.key == 'Country':
                return tag.value.value


def get_deal_tags(deal, key):
    return [
        tag.value.value for group in deal.tag_groups
        for tag in group.tags
        if tag.key.key == key
    ]


def get_group_tags(groups, key):
    return [
        tag.value.value for group in groups
        for tag in group.tags
        if tag.key.key == key
    ]
