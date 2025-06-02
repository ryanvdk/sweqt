from django.db import models
from django.utils import timezone

# Create your models here.


class BaseModel():
    def gross_revenue(self):
        return self.revenue_items.aggregate(total=models.Sum("gross_amount"))["total"] or 0

    def net_revenue(self):
        return self.revenue_items.aggregate(total=models.Sum("net_amount"))["total"] or 0

    def total_contribution_value(self):
        return self.contributions.aggregate(total=models.Sum("contribution_value"))["total"] or 0


class Contributor(models.Model, BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def projects(self):
        result = []
        for contribution in self.contributions.all():
            if contribution.project not in result:
                result.append(contribution.project)
        return result


class Organization(models.Model, BaseModel):
    """
    An organization is the highest level entity, for example a company.
    """
    name = models.CharField(max_length=100)
    organization_url = models.URLField(blank=True)
    members = models.ManyToManyField(Contributor, related_name="organizations")
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Project(models.Model, BaseModel):
    """
    A project is a product, service, website, game etc. that contributors make contributions to.
    """
    name = models.CharField(max_length=50)
    project_url = models.URLField(blank=True)
    slug = models.SlugField(blank=True, null=True)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="projects")

    def __str__(self):
        return f"{self.name}"


class Team(models.Model):
    """
    Teams belong to an organization. 
    """
    name = models.CharField(max_length=50)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="teams")
    members = models.ManyToManyField(Contributor, related_name="teams")

    def __str__(self):
        return f"{self.organization}: {self.name} ({self.members.count()} Members)"


class Currency(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=3, unique=True)
    symbol = models.CharField(max_length=5, default="$")
    decimal_places = models.PositiveSmallIntegerField(default=2)

    def __str__(self):
        return f"{self.code} ({self.symbol})"

    class Meta:
        verbose_name_plural = "Currencies"


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

    def __str__(self):
        return f"{self.organization} - {self.name}: {self.currency.symbol}{self.hourly_rate}/hour | {self.contributors.count()} People"


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
    work_hours = models.FloatField(blank=True, null=True)
    work_units = models.FloatField(blank=True, null=True)
    date_completed = models.DateTimeField(default=timezone.now, null=True)
    contribution_value = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, null=True)
    contributor = models.ForeignKey(
        Contributor, on_delete=models.CASCADE, related_name="contributions")
    contributor_role = models.ForeignKey(
        Role, on_delete=models.PROTECT, related_name="contributions", blank=True, null=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="contributions")
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="contributions", blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.date_completed.strftime('%Y-%m-%d %H:%M')} - {self.project}: {self.description}"


class Revenue(models.Model):
    """
    A model for tracking revenue earned by the organizationn.
    """
    source_name = models.CharField(max_length=100)
    source_description = models.TextField(blank=True)
    source_url = models.URLField(blank=True)
    date_received = models.DateTimeField(default=timezone.now, null=True)
    gross_amount = models.DecimalField(
        max_digits=9, decimal_places=2, default=0)
    net_amount = models.DecimalField(
        max_digits=9, decimal_places=2, default=0)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, null=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="revenue_items", null=True)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="revenue_items", null=True)

    def __str__(self):
        return f"{self.date_received.strftime('%Y-%m-%d %H:%M')} - {self.source_name}: {self.currency.symbol}{self.gross_amount} ({self.currency.symbol}{self.net_amount})"

    class Meta:
        verbose_name = "Revenue Item"
        verbose_name_plural = "Revenue Items"

# class Payouts
