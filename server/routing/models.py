from django.db import models

# Create your models here.


class Routes(models.Model):
    id = models.AutoField(primary_key=True)
    identifier = models.CharField(max_length=50)
    link = models.CharField(max_length=200)
