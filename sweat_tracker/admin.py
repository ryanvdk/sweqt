from django.contrib import admin
from .models import Organization, Contributor, Project, Team, Contribution, Role, Currency, Revenue
# Register your models here.


class ContributorAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("first_name", "last_name")}


class OrganizationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class ContributionAdmin(admin.ModelAdmin):
    list_filter = ("contribution_type", "project",
                   "contributor", "date_completed")
    list_display = ("project", "contributor", "contribution_type", "work_hours", "work_units",
                    "contribution_value", "date_completed")


class RevenueAdmin(admin.ModelAdmin):
    list_filter = ("source_name", "project", "date_received")
    list_display = ("project", "source_name",
                    "gross_amount", "net_amount", "date_received")


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Team)
admin.site.register(Contribution, ContributionAdmin)
admin.site.register(Role)
admin.site.register(Currency)
admin.site.register(Revenue, RevenueAdmin)
