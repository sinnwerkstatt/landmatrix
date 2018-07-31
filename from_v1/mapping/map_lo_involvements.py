from landmatrix import models as new_models
from from_v1.migrate import V2
from .land_observatory_objects.activity import Activity
from .land_observatory_objects.involvement import Involvement
from .land_observatory_objects.stakeholder import Stakeholder
from .map_lo_model import MapLOModel
from .map_lo_activities import MapLOActivities


class MapLOInvolvements(MapLOModel):

    PRIMARY_INVESTOR_ROLE_ID = 6
    IMPORT_STATUS_ID = 2  # Set everything to approved

    old_class = Involvement

    @classmethod
    def all_records(cls):
        records = cls.old_class.objects.using(cls.DB).all()

        # gets only the most recent versions
        activity_ids = MapLOActivities.all_ids()
        records = records.filter(fk_activity__in=activity_ids)

        # Remove duplicates here
        records = records.distinct(
            'fk_activity', 'fk_stakeholder', 'fk_stakeholder_role')
        records = records.order_by(
            'fk_activity', 'fk_stakeholder', 'fk_stakeholder_role')

        # Make sure that we cannot have something be both primary and
        # secondary
        primary_rels = records.filter(
            fk_stakeholder_role=cls.PRIMARY_INVESTOR_ROLE_ID)
        secondary_rels = records.exclude(
            fk_stakeholder_role=cls.PRIMARY_INVESTOR_ROLE_ID)

        primary_rel_set = {
            (rel.fk_activity, rel.fk_stakeholder) for rel in primary_rels
        }
        values = list(primary_rels.values())
        for rel in secondary_rels.values():
            rel_tuple = (rel['fk_activity'], rel['fk_stakeholder'])
            if rel_tuple not in primary_rel_set:
                values.append(rel)

        cls._count = len(values)

        return values

    @classmethod
    def cleanup_previously_imported_involvements(
            cls, save=False, verbose=False):
        # Venture involvements between two imported investors can be cleared
        ivis = new_models.InvestorVentureInvolvement.objects.filter(
            fk_venture__comment__contains='Imported from Land Observatory',
            fk_investor__comment__contains='Imported from Land Observatory')
        hivis = new_models.HistoricalInvestorVentureInvolvement.objects.filter(
            fk_venture__comment__contains='Imported from Land Observatory',
            fk_investor__comment__contains='Imported from Land Observatory')

        # Activity involvements between imported activity and investor
        # can be cleared
        iais = new_models.InvestorActivityInvolvement.objects.filter(
            fk_activity__attributes__fk_group__name='imported',
            fk_activity__attributes__name='source',
            fk_activity__attributes__value='Land Observatory',
            fk_investor__comment__contains='Imported from Land Observatory')
        hiais = new_models.HistoricalInvestorActivityInvolvement.objects.filter(
            fk_activity__attributes__fk_group__name='imported',
            fk_activity__attributes__name='source',
            fk_activity__attributes__value='Land Observatory',
            fk_investor__comment__contains='Imported from Land Observatory')

        if save:
            iais.delete()
            hiais.delete()
            ivis.delete()
            hivis.delete()

    @classmethod
    def map_record(cls, record, save=False, verbose=False):
        if verbose:
            print('Mapping involvement record {}'.format(record))

        old_activity = Activity.objects.using(cls.DB).get(
            pk=record['fk_activity'])
        old_stakeholder = Stakeholder.objects.using(cls.DB).get(
            pk=record['fk_stakeholder'])
        # Grab the first match in case of duplicate data here
        uuid_match = 'UUID: {}'.format(old_stakeholder.stakeholder_identifier)
        new_investor = new_models.Investor.objects.using(V2) \
            .filter(comment__contains=uuid_match).order_by('id').first()

        is_primary = (
            record['fk_stakeholder_role'] == cls.PRIMARY_INVESTOR_ROLE_ID
        )

        if new_investor:
            # Primary investors are now operating companies
            if is_primary:
                new_record = cls._map_primary_investor(
                    old_activity, new_investor, save=save, verbose=verbose)
            else:
                new_record = cls._map_secondary_investor(
                    record, new_investor, old_activity, save=save,
                    verbose=verbose)

            if new_record:
                new_record.fk_status_id = cls.IMPORT_STATUS_ID
                cls.save_record(new_record, record, save)

        elif verbose:
            print('No investor found for record')

    @classmethod
    def _get_new_activity(cls, activity_identifier):
        return new_models.Activity.objects.using(V2) \
            .filter(
                attributes__fk_group__name='imported',
                attributes__name='id',
                attributes__value=str(activity_identifier)) \
            .distinct().order_by('id').first()

    @classmethod
    def _get_new_activity_involvement(cls, **filters):
        return new_models.InvestorActivityInvolvement.objects \
            .using(V2).filter(**filters).order_by('id').first()

    @classmethod
    def _get_new_venture_involvement(cls, **filters):
        return new_models.InvestorVentureInvolvement.objects \
            .using(V2).filter(**filters).order_by('id').first()

    @classmethod
    def _get_old_primary_investor(cls, activity_id):
        involvement = cls.old_class.objects.using(cls.DB) \
            .filter(
                fk_stakeholder_role=cls.PRIMARY_INVESTOR_ROLE_ID,
                fk_activity=activity_id) \
            .order_by('-id').first()

        if involvement:
            stakeholder = Stakeholder.objects.using(cls.DB).get(
                pk=involvement.fk_stakeholder)
        else:
            stakeholder = None

        return stakeholder

    @classmethod
    def _map_primary_investor(
            cls, old_activity, new_investor, save=False, verbose=False):
        involvement = None
        new_activity = cls._get_new_activity(old_activity.activity_identifier)

        if new_activity:
            involvement = cls._get_new_activity_involvement(
                fk_activity=new_activity, fk_investor=new_investor)
            if not involvement:
                involvement = new_models.InvestorActivityInvolvement(
                    fk_activity=new_activity, fk_investor=new_investor)
            if verbose:
                print('Mapping primary investor to activity {}'.format(
                    involvement.__dict__))

        elif verbose:
            print('Missing imported activity with ID {}'.format(
                old_activity.activity_identifier))

        return involvement

    @classmethod
    def _map_secondary_investor(
            cls, old_record, new_investor, old_activity, save=False,
            verbose=False):
        involvement = None
        role = new_models.InvestorVentureInvolvement.STAKEHOLDER_ROLE

        parent_stakeholder = cls._get_old_primary_investor(
            old_record['fk_activity'])

        if parent_stakeholder:
            involvement = cls._map_secondary_investor_with_parent(
                parent_stakeholder, new_investor, role, save=save,
                verbose=verbose)
        else:
            involvement = cls._map_secondary_investor_without_parent(
                new_investor, role, old_activity, save=save, verbose=verbose)

        return involvement

    @classmethod
    def _map_secondary_investor_with_parent(
            cls, parent_stakeholder, new_investor, role, save=False,
            verbose=False):
        involvement = None
        uuid = str(parent_stakeholder.stakeholder_identifier)
        new_parent_investor = new_models.Investor.objects.using(V2) \
            .filter(comment__contains=uuid).order_by('id').first()

        if new_parent_investor:
            involvement = cls._get_new_venture_involvement(
                fk_venture=new_parent_investor,
                fk_investor=new_investor,
                role=role)
            if not involvement:
                involvement = new_models.InvestorVentureInvolvement(
                    fk_venture=new_parent_investor,
                    fk_investor=new_investor,
                    role=role)

            if verbose:
                print('Mapping secondary investor to venture {}'.format(
                    involvement.__dict__))

        elif verbose:
            print(
                "Couldn't find a previously imported Investor with"
                "UUID {}".format(uuid))

        return involvement

    @classmethod
    def _map_secondary_investor_without_parent(
            cls, new_investor, role, old_activity, save=False, verbose=False):
        # Check if the investor already has an operational stakeholder
        # connecting it to this activity
        new_activity = cls._get_new_activity(old_activity.activity_identifier)
        involvement = cls._get_new_venture_involvement(
            fk_investor=new_investor, role=role,
            fk_venture__involvements__fk_activity=new_activity)

        if involvement and verbose:
            print(
                'Found existing venture involvement {}'.format(
                    involvement.__dict__))
        elif not new_activity and verbose:
            print(
                'No imported activity with identifier {}'.format(
                    old_activity.activity_identifier))
        elif new_activity and involvement is None:
            # Without a parent involvement, we create a new blank
            # operational stakeholder AND link it to the activity

            new_parent_investor = new_models.Investor(name='', fk_status_id=cls.IMPORT_STATUS_ID)
            if save:
                new_parent_investor.save(using=V2)

            new_activity_involvement = new_models.InvestorActivityInvolvement(
                fk_activity=new_activity,
                fk_investor=new_parent_investor,
                fk_status_id=cls.IMPORT_STATUS_ID)
            if save:
                new_activity_involvement.save(using=V2)

            if verbose:
                print('Created new operational stakeholder {}'.format(
                    new_parent_investor.__dict__))
                print('Created new activity involvement {}'.format(
                    new_activity_involvement.__dict__))

            involvement = new_models.InvestorVentureInvolvement(
                fk_venture=new_parent_investor, fk_investor=new_investor,
                role=role)

            if verbose:
                print(
                    'Mapping secondary investor to venture (no parent)'
                    ' {}'.format(involvement.__dict__))

        return involvement
