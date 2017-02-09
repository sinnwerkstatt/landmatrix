
def load_project(proj_path, app_name):

    import os, sys

    # This is so Django knows where to find stuff.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", app_name + ".settings")
    sys.path.append(proj_path)

    # This is so my local_settings.py gets loaded.
    os.chdir(proj_path)

    # This is so models get loaded.
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

BASE_PATH = '/Users/Simon/Sites'
load_project(BASE_PATH+'/landmatrix', 'landmatrix')

from landmatrix.models.investor import InvestorVentureInvolvement, InvestorActivityInvolvement

if False:
    pairs = InvestorVentureInvolvement.objects.values_list('fk_venture_id', 'fk_investor_id').distinct()

    for venture, investor in pairs:
        involvements = InvestorVentureInvolvement.objects.filter(fk_venture_id=venture).filter(fk_investor_id=investor).order_by('id')
        if len(involvements) > 1:
            keep = involvements.last()
            print('KEEP:  ', keep)
            delete = involvements[:len(involvements)-1]
            for involvement in delete:
                print('DELETE:', involvement)
                involvement.delete()

    pairs = InvestorActivityInvolvement.objects.values_list('fk_activity_id', 'fk_investor_id').distinct()

    for activity, investor in pairs:
        involvements = InvestorActivityInvolvement.objects.filter(fk_activity_id=activity).filter(fk_investor_id=investor).order_by('id')
        if len(involvements) > 1:
            keep = involvements.last()
            print('KEEP:  ', keep)
            delete = involvements[:len(involvements)-1]
            for involvement in delete:
                print('DELETE:', involvement)
                involvement.delete()

from landmatrix.models.activity import Activity

deal_ids = Activity.objects.values_list('activity_identifier', flat=True).distinct()
for id in deal_ids:
    activities = Activity.objects.filter(activity_identifier=id).order_by('id')
    if len(activities) > 1:
        keep = activities.last()
        print('KEEP:', keep.id, keep.activity_identifier, keep.fk_status.name)
        delete = activities[:len(activities)-1]
        for activity in delete:
            print('DELETE:', activity.id, activity.activity_identifier, activity.fk_status.name)
            activity.delete()