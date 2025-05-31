from django.db import models

# Create your models here.


class Organizations(models.Model):
    name = models.CharField(max_length=100)


class Contributor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)


class Project(models.Model):
    name = models.CharField(max_length=50)


class Teams(models.Model):
    name = models.CharField(max_length=50)


class Contributions(models.Model):
    contribution_type = models.CharField(max_length=50)
    description = models.TextField()
    work_hours = models.FloatField()
    work_units = models.FloatField()
