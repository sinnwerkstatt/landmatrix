from types import new_class

from landmatrix.models.activity_attribute_group import ActivityAttributeGroup
from landmatrix.models.investor import Investor
from .land_observatory_objects.tag_groups import A_Tag_Group, SH_Tag_Group
from .land_observatory_objects.stakeholder import Stakeholder
from .land_observatory_objects.changeset import Changeset
from .land_observatory_objects.involvement import Involvement
from .map_lo_model import MapLOModel
from .map_lo_activities import MapLOActivities

from migrate import V1, V2

from django.db import transaction

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class MapLandObservatory:
    """
    Preparing the land observatory data:
    cat cdelokp-unibe-ch_data_20160510.backup | sed s/lokpeditor/<db_user>/g > cdelokp-unibe-ch_data_20160510.backup.lm
    pg_restore -c cdelokp-unibe-ch_data_20160510.backup.lm
    psql -U<db_user> -c 'ALTER USER <db_user> SET SEARCH_PATH = data, public;'
    """

    @classmethod
    @transaction.atomic(using=V2)
    def map_all(cls, save=False, verbose=False):
        MapLOActivities.map_all(save, verbose)
        MapLOATagGroups.map_all(save, verbose)
        MapLOStakeholders.map_all(save, verbose)
        MapLOSTagGroups.map_all(save, verbose)
        MapLOChangesets.map_all(save, verbose)
        MapLOInvolvements.map_all(save, verbose)


class MapLOATagGroups(MapLOModel):

    old_class = A_Tag_Group
    new_class = ActivityAttributeGroup

    map_attributes = {
        'Animals':                                  'animals',
        'Annual leasing fee area (ha)':             'annual_leasing_fee_area',
        'Announced amount of investement':          '',
        'Announced amount of investment':           '',
        'Area (ha)':                                '',
        'Benefits for local communities':           'promised_benefits',
        'Consultation of local community':          'community_consultation',
        'Contract area (ha)':                       'contract_size',
        'Contract date':                            'contract_date',
        'Contract farming':                         'contract_farming',
        'Contract Number':                          'contract_number',
        'Country':                                  'target_country',
        'Crop':                                     'crops',
        'Current area in operation (ha)':           'production_size',
        'Current Number of daily/seasonal workers': 'total_jobs_current_daily_workers',
        'Current number of employees':              'total_jobs_current_employees',
        'Current total number of jobs':             'total_jobs_current',
        'Data source':                              'data_source',
        'Date':                                     'date',
        'Duration of Agreement (years)':            'agreement_duration',
        'Files':                                    'file',
        'Former predominant land cover':            'land_cover',
        'Former predominant land owner':            'land_owner',
        'Former predominant land use':              'land_use',
        'How did community react':                  'community_reaction',
        'How much do investors pay for water':      'how_much_do_investors_pay_comment',
        'How much water is extracted (m3/year)':    'water_extraction_amount',
        'Implementation status':                    'implementation_status',
        'Intended area (ha)':                       '',
        'Intention of Investment':                  '',
        'Leasing fee (per year)':                   'annual_leasing_fee',
        'Mineral':                                  'minerals',
        'Name':                                     '',
        'Nature of the deal':                       'nature',
        'Negotiation Status':                       'negotiation_status',
        'Number of farmers':                        '',
        'Number of people actually displaced':      'number_of_displaced_people',
        'Original reference number':                '',
        'Percentage':                               '',
        'Planned Number of daily/seasonal workers': 'total_jobs_planned_daily_workers',
        'Planned number of employees':              'total_jobs_planned_employees',
        'Planned total number of jobs':             'total_jobs_planned',
        'Promised or received compensation':        'promised_compensation',
        'Purchase price':                           'purchase_price',
        'Purchase price area (ha)':                 'purchase_price_area',
        'Remark':                                   '',
        'Scope of agriculture':                     '',
        'Scope of forestry':                        '',
        'Spatial Accuracy':                         'level_of_accuracy',
        'URL / Web':                                'url',
        'Use of produce':                           'use_of_produce_comment',
        'Water extraction':                         'water_extraction_envisaged',
        'Year':                                     '',
    }
    @classmethod
    def all_records(cls):
        return A_Tag_Group.objects.using('lo').all().values()

    @classmethod
    def save_record(cls, new, save):
        print(new)


class MapLOStakeholders(MapLOModel):

    old_class = Stakeholder
    new_class = Investor

    @classmethod
    def all_records(cls):
        return Stakeholder.objects.using('lo').all().values()

    @classmethod
    def save_record(cls, new, save):
        print(new)


class MapLOSTagGroups(MapLOModel):

    old_class = SH_Tag_Group
    new_class = Investor

    @classmethod
    def all_records(cls):
        return SH_Tag_Group.objects.using('lo').all().values()

    @classmethod
    def save_record(cls, new, save):
        print(new)


class MapLOChangesets(MapLOModel):

    old_class = Changeset

    @classmethod
    def all_records(cls):
        return Changeset.objects.using('lo').all().values()

    @classmethod
    def save_record(cls, new, save):
        print(new)


class MapLOInvolvements(MapLOModel):

    old_class = Involvement

    @classmethod
    def all_records(cls):
        return Involvement.objects.using('lo').all().values()

    @classmethod
    def save_record(cls, new, save):
        print(new)
