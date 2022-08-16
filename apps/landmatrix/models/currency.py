from django.db import models


class Currency(models.Model):
    code = models.CharField("Code", max_length=3)
    name = models.CharField("Name", max_length=255)
    symbol = models.CharField("Symbol", max_length=255)
    country = models.CharField("Country", max_length=2)
    ranking = models.IntegerField("Ranking")

    def __str__(self):
        if self.symbol:
            return f"{self.name} ({self.symbol})"
        return self.name

    def to_dict(self):
        return {"id": self.id, "code": self.code, "name": self.name}
