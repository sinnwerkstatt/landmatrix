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
    def map_record(cls, record, save=False, verbose=False):
        old_activity = Activity.objects.using(cls.DB).get(
            pk=record['fk_activity'])
        old_stakeholder = Stakeholder.objects.using(cls.DB).get(
            pk=record['fk_stakeholder'])

        # Grab the first match in case of duplicate data here
        new_investor_queryset = new_models.Investor.objects.using(V2).filter(
            comment__contains=old_stakeholder.stakeholder_identifier)
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
            cls._log_object_missing(
                new_models.Investor.__name__,
                old_stakeholder.stakeholder_identifier)

    @classmethod
    def _map_primary_investor(cls, old_activity):
        new_record = None
        aag_lookup = {
            'landobservatory_uuid': str(old_activity.activity_identifier),
        }
        new_activity_queryset = new_models.Activity.objects.using(V2).filter(
            activityattributegroup__attributes__contains=aag_lookup)
        new_activity = new_activity_queryset.first()
        if new_activity:
            new_record = new_models.InvestorActivityInvolvement(
                fk_activity=new_activity)
        else:
            cls._log_object_missing(
                new_models.Activity.__name__,
                old_activity.activity_identifier)

        return new_record

    @classmethod
    def _map_secondary_investor(cls, old_record):
        new_record = None

        parent_involvement = cls.old_class.objects.using(cls.DB).filter(
            fk_stakeholder_role=cls.PRIMARY_INVESTOR_ROLE_ID,
            fk_activity=old_record['fk_activity']).first()

        if parent_involvement:
            try:
                parent_stakeholder = Stakeholder.objects.using(cls.DB).get(
                    pk=parent_involvement.fk_stakeholder)
            except Stakeholder.DoesNotExist:
                pass
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
                    cls._log_object_missing(
                        new_models.Investor.__name__,
                        parent_investor.stakeholder_identifier)
        else:
            cls._log_object_missing(
                cls.old_class.__name__, old_record['fk_activity'])
        return new_record

    @classmethod
    def _log_object_missing(cls, type, id):
        message = "{type} with identifier '{id}' has not been imported yet. Skipping."
        print(message.format(type=type, id=id))
