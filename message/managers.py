from django.db import models


class MessageManager(models.Manager):

    def active(self):
        """
        Returns active messages
        :return:
        """
        return self.filter(is_active=True)
