from from_v1.mapping.map_model import MapModel
import landmatrix.models
import old_editor.models
from from_v1.mapping.aux_functions import get_first_stakeholder_tag_value, get_country_id_for_stakeholder, get_now
from from_v1.migrate import V1, V2
from django.db import connections


def get_stakeholder_id(stakeholder_id):
    return stakeholder_id + 50000


def get_name_for_stakeholder(stakeholder_id):
    investor_name = get_first_stakeholder_tag_value(stakeholder_id, 'investor_name')
    return '' if investor_name is None else investor_name


def get_classification_for_stakeholder(stakeholder_id):
    classification = get_first_stakeholder_tag_value(stakeholder_id, 'classification')
    return {
        'Private company': '10',
        'Stock-exchange listed company': '20',
        'Individual entrepreneur': '30',
        'Investment fund': '40',
        'Semi state-owned company': '50',
        'State-/government(owned)': '60',
        'State-/government(-owned)': '60',
        'Other (please specify in comment field)': '70'
    }.get(classification, None)


class MapStakeholderInvestor(MapModel):
    old_class = old_editor.models.Stakeholder
    new_class = landmatrix.models.Investor
    attributes = {
        'stakeholder_identifier': 'investor_identifier',
        'id': (
            ('id', get_stakeholder_id),
            ('name', get_name_for_stakeholder),
            ('fk_country_id', get_country_id_for_stakeholder),
            ('classification', get_classification_for_stakeholder)
        )
    }
    DEBUG = False

    @classmethod
    def save_record(cls, new, save):
        """Save all versions of an activity as HistoricalActivity records."""
        if not save:
            return

        versions = get_stakeholder_versions(new)
        for i, version in enumerate(versions):
            landmatrix.models.HistoricalInvestor.objects.create(
                id=get_stakeholder_id(version['id']),
                investor_identifier=version['stakeholder_identifier'],
                name=get_name_for_stakeholder(version['id']).strip(),
                fk_country_id=get_country_id_for_stakeholder(version['id']),
                classification=get_classification_for_stakeholder(version['id']),
                fk_status_id=version['fk_status_id'],
                history_date=get_now(version['id']),
                #parent_relation=version['parent_relation'],
                #homepage=version['homepage'],
                #opencorporates_link=version['opencorporates_link'],
                #comment=version['comment'],
                #history_date=version['timestamp'],
                #history_user=get_history_user(new)
            )

        new.save(using=V2)

    @classmethod
    def all_ids(cls):
        cursor = connections[V1].cursor()
        cursor.execute("""
SELECT id
FROM stakeholders s
WHERE s.version = (SELECT MAX(st.version) FROM stakeholders st WHERE 
                   st.stakeholder_identifier = s.stakeholder_identifier)
ORDER BY s.stakeholder_identifier
        """)
        return [id[0] for id in cursor.fetchall()]

    @classmethod
    def all_records(cls):
        return cls.old_class.objects.using(cls.DB).filter(id__in=cls.all_ids()).values()


def get_stakeholder_versions(investor):
    return MapStakeholderInvestor.old_class.objects.using(V1).filter(
        stakeholder_identifier=investor.investor_identifier).order_by(
        'version').values()
