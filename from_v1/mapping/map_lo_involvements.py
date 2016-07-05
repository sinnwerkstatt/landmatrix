from landmatrix import models as new_models
from migrate import V2
from .land_observatory_objects.activity import Activity
from .land_observatory_objects.involvement import Involvement
from .land_observatory_objects.stakeholder import Stakeholder

from .map_lo_model import MapLOModel


class MapLOInvolvements(MapLOModel):

    PRIMARY_INVESTOR_ROLE_ID = 6
    IMPORT_STATUS_ID = 2  # Set everything to approved

    old_class = Involvement

    @classmethod
    def all_records(cls):
        return super().all_records()

    @classmethod
    def map_record(cls, record, save=False, verbose=False):
        old_activity = Activity.objects.using(cls.DB).get(
            pk=record['fk_activity'])
        old_stakeholder = Stakeholder.objects.using(cls.DB).get(
            pk=record['fk_stakeholder'])

        # Grab the first match in case of duplicate data here
        uuid_match = 'UUID: {}'.format(old_stakeholder.stakeholder_identifier)
        new_investor_queryset = new_models.Investor.objects.using(V2).filter(
            comment__contains=uuid_match)
        new_investor = new_investor_queryset.first()
        if new_investor:
            # Investors are now operational companies
            if record['fk_stakeholder_role'] == cls.PRIMARY_INVESTOR_ROLE_ID:
                new_record = cls._map_primary_investor(old_activity)
            else:
                new_record = cls._map_secondary_investor(record)

            if new_record:
                new_record.fk_investor = new_investor
                new_record.fk_status_id = cls.IMPORT_STATUS_ID

                cls.save_record(new_record, save=save)
        else:
            print(
                "Couldn't find an imported investor with a UUID matching",
                '{}'.format(old_stakeholder.stakeholder_identifier))

    @classmethod
    def _map_primary_investor(cls, old_activity, verbose=False):
        new_record = None
        uuid = str(old_activity.activity_identifier)

        attr_model = new_models.HistoricalActivityAttribute
        new_activity_attr_queryset = attr_model.objects.using(V2).filter(
            name='landobservatory_uuid', value__contains=uuid)
        new_activity_attr = new_activity_attr_queryset.first()
        if new_activity_attr:
            try:
                new_activity = new_activity_attr.fk_activity
            except new_models.HistoricalActivity.DoesNotExist:
                pass
            else:
                new_record = new_models.InvestorActivityInvolvement(
                    fk_activity=new_activity)
        else:
            print(
                "Counldn't find an imported activity with an attribute group",
                "containing the UUID {}".format(uuid))

        return new_record

    @classmethod
    def _map_secondary_investor(cls, old_record, verbose=False):
        new_record = None

        parent_involvement = cls.old_class.objects.using(cls.DB).filter(
            fk_stakeholder_role=cls.PRIMARY_INVESTOR_ROLE_ID,
            fk_activity=old_record['fk_activity']).first()

        if parent_involvement:
            try:
                parent_stakeholder = Stakeholder.objects.using(cls.DB).get(
                    pk=parent_involvement.fk_stakeholder)
            except Stakeholder.DoesNotExist:
                print(
                    'Bad foreign key in lo data - Stakeholder with id',
                    '{}'.format(parent_involvement.fk_stakeholder),
                    'not found')
            else:
                parent_stakeholder_id = str(
                    parent_stakeholder.stakeholder_identifier)
                new_investor_queryset = new_models.Investor.objects.using(V2)
                new_investor_queryset = new_investor_queryset.filter(
                    comment__contains=parent_stakeholder_id)
                new_parent_investor = new_investor_queryset.first()

                if new_parent_investor:
                    new_record = new_models.InvestorVentureInvolvement(
                        fk_venture=new_parent_investor)
                else:
                    print(
                        "Couldn't find a previously imported Investor with"
                        "UUID {}".format(parent_stakeholder_id))

        else:
            # Without a parent involvement, we create a new operational
            # stakeholder
            new_parent_investor = new_models.Investor.objects.using(V2).create(
                name='', fk_status_id=cls.IMPORT_STATUS_ID)
            new_record = new_models.InvestorVentureInvolvement(
                fk_venture=new_parent_investor)

        return new_record
