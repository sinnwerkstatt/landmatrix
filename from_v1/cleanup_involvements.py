__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

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

BASE_PATH = '/home/lene/workspace/landmatrix'

load_project(BASE_PATH+'/land-matrix-2', 'landmatrix')

from landmatrix.models import InvestorVentureInvolvement, InvestorActivityInvolvement

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

