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
        investors = list(filter(None, [
            new_models.HistoricalInvestor.objects.using(V2).filter(comment__contains=uuid_match)
                                .order_by('-id').first(),
            new_models.Investor.objects.using(V2).filter(comment__contains=uuid_match)
                                .order_by('-id').first(),
        ]))

        is_primary = (
            record['fk_stakeholder_role'] == cls.PRIMARY_INVESTOR_ROLE_ID
        )

        if investors:
            # Primary investors are now operating companies
            if is_primary:
                new_records = cls._map_primary_investor(
                    old_activity, investors, save=save, verbose=verbose)
            else:
                new_records = cls._map_secondary_investor(
                    record, investors, old_activity, save=save,
                    verbose=verbose)

            if new_records:
                for new_record in new_records:
                    new_record.fk_status_id = cls.IMPORT_STATUS_ID
                    cls.save_record(new_record, record, save)

        elif verbose:
            print('No investor found for record')

    @classmethod
    def _get_new_activity(cls, activity_identifier):
        return list(filter(None, [
            new_models.HistoricalActivity.objects.using(V2) \
                .filter(
                attributes__fk_group__name='imported',
                attributes__name='id',
                attributes__value=str(activity_identifier)) \
                .distinct().order_by('-id').first(),
            new_models.Activity.objects.using(V2) \
                           .filter(
                attributes__fk_group__name='imported',
                attributes__name='id',
                attributes__value=str(activity_identifier)) \
                           .distinct().order_by('-id').first(),
        ]))

    @classmethod
    def _get_new_activity_involvement(cls, activities, investors):
        involvements = list(filter(None, [
            new_models.HistoricalInvestorActivityInvolvement.objects.using(V2)\
                .filter(fk_activity=activities[0],
                        fk_investor=investors[0]).order_by('-id').first(),
            new_models.InvestorActivityInvolvement.objects.using(V2)\
                .filter(fk_activity=activities[1],
                        fk_investor=investors[1]).order_by('-id').first(),
        ]))
        if not involvements:
            involvements = [
                new_models.HistoricalInvestorActivityInvolvement(fk_activity=activities[0],
                                                                 fk_investor=investors[0]),
                new_models.InvestorActivityInvolvement(fk_activity=activities[1],
                                                       fk_investor=investors[1]),
            ]
        return involvements

    @classmethod
    def _get_new_venture_involvement(cls, ventures, investors, role):
        involvements = list(filter(None, [
            new_models.HistoricalInvestorVentureInvolvement.objects.using(V2)\
                .filter(fk_venture=ventures[0], role=role,
                        fk_investor=investors[0]).order_by('-id').first(),
            new_models.InvestorVentureInvolvement.objects.using(V2)\
                .filter(fk_venture=ventures[1], role=role,
                        fk_investor=investors[1]).order_by('-id').first(),
        ]))
        if not involvements:
            involvements = [
                new_models.HistoricalInvestorVentureInvolvement(fk_venture=ventures[0], role=role,
                                                                fk_investor=investors[0]),
                new_models.InvestorVentureInvolvement(fk_venture=ventures[1], role=role,
                                                      fk_investor=investors[1]),
            ]
        return involvements

    @classmethod
    def _get_new_venture_involvement_by_activity(cls, activities, investors, role):
        involvements = []
        if activities:
            involvements = list(filter(None, [
                new_models.HistoricalInvestorVentureInvolvement.objects.using(V2)\
                    .filter(fk_venture__involvements__fk_activity=activities[0], role=role,
                            fk_investor=investors[1]).order_by('-id').first(),
                new_models.InvestorVentureInvolvement.objects.using(V2)\
                    .filter(fk_venture__involvements__fk_activity=activities[1], role=role,
                            fk_investor=investors[0]).order_by('-id').first(),
            ]))
        return involvements

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
    def _map_primary_investor(cls, old_activity, investors, save=False, verbose=False):
        involvements = []
        activities = cls._get_new_activity(old_activity.activity_identifier)

        if activities:
            involvements = cls._get_new_activity_involvement(activities=activities,
                                                             investors=investors)
            if verbose:
                print('Mapping primary investor to activity {}'.format(
                    involvements[0].__dict__))

        elif verbose:
            print('Missing imported activity with ID {}'.format(
                old_activity.activity_identifier))

        return involvements

    @classmethod
    def _map_secondary_investor(cls, old_record, investors, old_activity, save=False,
                                verbose=False):
        involvements = []
        role = new_models.InvestorVentureInvolvement.STAKEHOLDER_ROLE

        parent_stakeholder = cls._get_old_primary_investor(old_record['fk_activity'])

        if parent_stakeholder:
            involvements = cls._map_secondary_investor_with_parent(parent_stakeholder, investors,
                                                                   role, save=save,
                                                                   verbose=verbose)
        else:
            involvements = cls._map_secondary_investor_without_parent(investors, role,
                                                                      old_activity, save=save,
                                                                      verbose=verbose)

        return involvements

    @classmethod
    def _map_secondary_investor_with_parent(cls, parent_stakeholder, investors, role, save=False,
            verbose=False):
        involvements = []
        uuid = str(parent_stakeholder.stakeholder_identifier)
        new_parent_investors = list(filter(None, [
            new_models.HistoricalInvestor.objects.using(V2).filter(comment__contains=uuid)
                .order_by('-id').first(),
            new_models.Investor.objects.using(V2).filter(comment__contains=uuid)
                .order_by('-id').first(),
        ]))

        if new_parent_investors:
            involvements = cls._get_new_venture_involvement(
                ventures=new_parent_investors,
                investors=investors,
                role=role)

            if verbose:
                print('Mapping secondary investor to venture {}'.format(
                    involvements[0].__dict__))

        elif verbose:
            print(
                "Couldn't find a previously imported Investor with"
                "UUID {}".format(uuid))

        return involvements

    @classmethod
    def _map_secondary_investor_without_parent(
            cls, investors, role, old_activity, save=False, verbose=False):
        # Check if the investor already has an operational stakeholder
        # connecting it to this activity
        activities = cls._get_new_activity(old_activity.activity_identifier)
        involvements = cls._get_new_venture_involvement_by_activity(activities=activities,
                                                        investors=investors, role=role)

        if involvements and verbose:
            print(
                'Found existing venture involvement {}'.format(
                    involvements[0].__dict__))
        elif not activities and verbose:
            print(
                'No imported activity with identifier {}'.format(
                    old_activity.activity_identifier))
        elif activities and not involvements:
            # Without a parent involvement, we create a new blank
            # operational stakeholder AND link it to the activity
            new_parent_hinvestor = new_models.HistoricalInvestor(name='',
                                                                 fk_status_id=cls.IMPORT_STATUS_ID)
            if save:
                new_parent_hinvestor.save(using=V2)
            new_hactivity_involvement = new_models.InvestorActivityInvolvement(
                fk_activity=activities[0],
                fk_investor=new_parent_hinvestor,
                fk_status_id=cls.IMPORT_STATUS_ID)
            if save:
                new_hactivity_involvement.save(using=V2)

            new_parent_investor = new_models.Investor(name='', fk_status_id=cls.IMPORT_STATUS_ID)
            if save:
                new_parent_investor.investor_identifier = new_parent_hinvestor.investor_identifier
                new_parent_investor.save(using=V2)
            new_activity_involvement = new_models.InvestorActivityInvolvement(
                fk_activity=activities[1],
                fk_investor=new_parent_investor,
                fk_status_id=cls.IMPORT_STATUS_ID)
            if save:
                new_activity_involvement.save(using=V2)

            if verbose:
                print('Created new operational stakeholder {}'.format(
                    new_parent_investor.__dict__))
                print('Created new activity involvement {}'.format(
                    new_activity_involvement.__dict__))

            involvements = [
                new_models.HistoricalInvestorVentureInvolvement(fk_venture=new_parent_hinvestor,
                                                                fk_investor=investors[0],
                                                                role=role),
                new_models.InvestorVentureInvolvement(fk_venture=new_parent_investor,
                                                      fk_investor=investors[1],
                                                      role=role)
            ]

            if verbose:
                print(
                    'Mapping secondary investor to venture (no parent)'
                    ' {}'.format(involvements[0].__dict__))

        return involvements
