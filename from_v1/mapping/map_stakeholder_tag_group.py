from migrate import V1, V2
from mapping.map_tag_groups import MapTagGroups

from mapping.aux_functions import stakeholder_ids
from landmatrix.models.language import Language
from landmatrix.models.country import Country

if V1 == 'v1_my':
    from editor.models import Comment, SH_Tag_Group, SH_Tag



class MapStakeholderTagGroup(MapTagGroups):

    # prevent error if postgres branch of landmatrix 1 is checked out
    if V1 == 'v1_my':
        old_class = SH_Tag_Group
        tag_groups = SH_Tag_Group.objects.using(V1).select_related('fk_stakeholder').filter(
            fk_stakeholder__pk__in=stakeholder_ids()
        )

    @classmethod
    def relevant_tag_sets(cls, tag_group):
        return [
            [tag_group.fk_sh_tag],
            SH_Tag.objects.using(V1).filter(fk_sh_tag_group=tag_group).select_related('fk_sh_key', 'fk_sh_value'),
        ]

    @classmethod
    def migrate_tags(cls, relevant_tags, tag_group):
        attrs = {}
        for tag in relevant_tags:
            key = tag.fk_sh_key.key
            value = tag.fk_sh_value.value
            if key in attrs:
                cls.write_stakeholder_attribute_group(attrs, tag_group)
            attrs[key] = value
        if attrs:
            cls.write_stakeholder_attribute_group(attrs, tag_group)

    @classmethod
    def write_stakeholder_attribute_group(cls, attrs, tag_group):
        attrs = resolve_country(attrs)
        sag = StakeholderAttributeGroup(
            fk_stakeholder_id=tag_group.fk_stakeholder.id, fk_language=Language.objects.get(pk=1),
            attributes=attrs, name=attrs.get('name')
        )

        comments = cls.get_comments(tag_group)
        if comments:
            sag.attributes.update({
                tag_group.fk_sh_tag.fk_sh_value.value + '_comment': '\n'.join(comments)
            })

        if cls._save:
            sag.save(using=V2)

    @classmethod
    def get_comments(cls, tag_group):
        queryset = Comment.objects.using(V1).filter(fk_sh_tag_group=tag_group)
        return set([comment.comment.strip() for comment in queryset if comment.comment.strip()])

def resolve_country(attrs):
    if 'country' in attrs:
        attrs['country'] = Country.objects.using(V2).get(name=attrs['country']).id
    return attrs