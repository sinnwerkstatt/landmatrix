from celery import shared_task
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl.signals import BaseSignalProcessor


@shared_task
def task_handle_save(pk, content_type):
    ct_model = ContentType.objects.get_by_natural_key(*content_type)
    instance = ct_model.get_object_for_this_type(pk=pk)

    registry.update(instance)
    registry.update_related(instance)


# # TODO: This is broken as we can not retrieve the instance anymore when it's actually gone.
# @shared_task
# def task_handle_pre_delete(pk, content_type):
#     ct_model = ContentType.objects.get_by_natural_key(*content_type)
#     instance = ct_model.get_object_for_this_type(pk=pk)
#
#     registry.delete_related(instance)
#
# @shared_task
# def task_handle_delete(pk, content_type):
#     ct_model = ContentType.objects.get_by_natural_key(*content_type)
#     instance = ct_model.get_object_for_this_type(pk=pk)
#
#     registry.delete(instance, raise_on_error=False)


class CelerySignalProcessor(BaseSignalProcessor):
    def setup(self):
        for m in registry._models.keys():
            models.signals.post_save.connect(self.handle_save, sender=m)
            models.signals.post_delete.connect(self.handle_delete, sender=m)
            models.signals.m2m_changed.connect(self.handle_m2m_changed, sender=m)
            models.signals.pre_delete.connect(self.handle_pre_delete, sender=m)

    def teardown(self):
        for m in registry._models.keys():
            models.signals.post_save.disconnect(self.handle_save, sender=m)
            models.signals.post_delete.disconnect(self.handle_delete, sender=m)
            models.signals.m2m_changed.disconnect(self.handle_m2m_changed, sender=m)
            models.signals.pre_delete.disconnect(self.handle_pre_delete, sender=m)

    def handle_save(self, sender, instance, **kwargs):
        ct = ContentType.objects.get_for_model(instance)
        task_handle_save.delay(instance.pk, ct.natural_key())

    # TODO: This can't handle like this because we can't access the instance anymore in the task
    # def handle_pre_delete(self, sender, instance, **kwargs):
    #     ct = ContentType.objects.get_for_model(instance)
    #     task_handle_pre_delete.delay(instance.pk, ct.natural_key())
    #
    # def handle_delete(self, sender, instance, **kwargs):
    #     ct = ContentType.objects.get_for_model(instance)
    #     task_handle_delete.delay(instance.pk, ct.natural_key())


class DoNothingProcessor(BaseSignalProcessor):
    pass
