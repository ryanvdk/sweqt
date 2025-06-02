from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Organization, Contributor, Project, Contribution, Revenue

# Create your views here.


def calculateGrossRevenue():
    pass


class IndexView(TemplateView):
    template_name = "sweat_tracker/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["organizations"] = Organization.objects.all()
        return context


class OrganizationView(TemplateView):
    template_name = "sweat_tracker/organization.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        organization_slug = self.kwargs.get("organization")
        context["organization"] = Organization.objects.get(
            slug=organization_slug)
        return context


class ContributorView(TemplateView):
    template_name = "sweat_tracker/contributor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contributor_slug = self.kwargs.get("contributor")
        context["contributor"] = Contributor.objects.get(
            slug=contributor_slug)
        organization_slug = self.kwargs.get("organization")
        context["organization"] = Organization.objects.get(
            slug=organization_slug)
        return context


class ProjectView(TemplateView):
    template_name = "sweat_tracker/project.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_slug = self.kwargs.get("project")
        context["project"] = Project.objects.get(
            slug=project_slug)
        organization_slug = self.kwargs.get("organization")
        context["organization"] = Organization.objects.get(
            slug=organization_slug)
        return context


class ContributionView(TemplateView):
    template_name = "sweat_tracker/contribution.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contribution_pk = self.kwargs.get("pk")
        context["contribution"] = Contribution.objects.get(
            pk=contribution_pk)
        organization_slug = self.kwargs.get("organization")
        context["organization"] = Organization.objects.get(
            slug=organization_slug)
        return context


class RevenueItemView(TemplateView):
    template_name = "sweat_tracker/revenue_item.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        revenue_pk = self.kwargs.get("pk")
        context["revenue_item"] = Revenue.objects.get(
            pk=revenue_pk)
        organization_slug = self.kwargs.get("organization")
        context["organization"] = Organization.objects.get(
            slug=organization_slug)
        return context
