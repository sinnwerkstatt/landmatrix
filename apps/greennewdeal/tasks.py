from celery import shared_task

from apps.greennewdeal.synchronization.deal import histivity_to_deal
from apps.greennewdeal.synchronization.investor import histvestor_to_investor


@shared_task
def task_propagate_save_to_gnd_deal(hist_deal_pk):
    histivity_to_deal(activity_pk=hist_deal_pk)


@shared_task
def task_propagate_save_to_gnd_investor(histvestor_id):
    histvestor_to_investor(investor_pk=histvestor_id)


@shared_task
def task_propagate_save_to_gnd_involvement(involvement_id):
    pass
