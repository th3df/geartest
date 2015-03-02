from django.db import models

# Create your models here.

class Experiment(models.Model):
    pass

class Memloadstat(models.Model):
    gearID = models.TextField(default="")
    memload = models.BigIntegerField(default=0)
    availdelta = models.BigIntegerField(default=0)
    availmem = models.BigIntegerField(default=0)
    exp = models.ForeignKey(Experiment, default=0)
    
