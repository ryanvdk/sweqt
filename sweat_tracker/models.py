from django.db import models

# Create your models here.


class Contributor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)


class Organization(models.Model):
    """
    An organization is the highest level entity, for example a company.
    """
    name = models.CharField(max_length=100)
    projects = models.one
    members = models.ManyToManyField(Contributor, related_name="organizations")


class Project(models.Model):
    """
    A project is a product, service, website, game etc. that contributors make contributions to.
    """
    name = models.CharField(max_length=50)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="projects")


class Team(models.Model):
    """
    Teams belong to an organization. 
    """
    name = models.CharField(max_length=50)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="teams")
    members = models.ManyToManyField(Contributor, related_name="teams")


class Currency(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=3, unique=True)
    symbol = models.CharField(max_length=5, default="$")
    decimal_places = models.PositiveSmallIntegerField(default=2)


class Role(models.Model):
    """
    A role describes the activity of a contributor. One contributor can take on many roles. 
    The same role can be held by multiple contributors.
    Roles exist within Organizations, Projects or Teams. 
    """
    name = models.CharField(max_length=100)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="roles")
    projects = models.ManyToManyField(Project, related_name="roles")
    teams = models.ManyToManyField(Team, related_name="roles")
    contributors = models.ManyToManyField(Contributor, related_name="roles")
    hourly_rate = models.DecimalField(max_digits=9, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)


class Contribution(models.Model):
    """
    Types of contribution: hourly work, paying an expense, buying materials, investing money.
    """
    class ContributionType(models.TextChoices):
        HOURLY_WORK = "hourly_work", "Hourly Work"
        EXPENSE = "expense", "Expense"
        WORK_PACKAGE = "work_package", "Work Package"
    contribution_type = models.CharField(
        max_length=20, choices=ContributionType.choices, default=ContributionType.HOURLY_WORK)
    description = models.TextField()
    work_hours = models.FloatField()
    work_units = models.FloatField()
    contribution_value = models.DecimalField(max_digits=9, decimal_places=2)
    contributor = models.ForeignKey(
        Contributor, on_delete=models.CASCADE, related_name="contributions")
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="contributions")
    is_approved = models.BooleanField(default=False)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)


class Revenue(models.Model):
    source_name = models.CharField(max_length=100)
    source_description = models.TextField()
