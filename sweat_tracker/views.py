from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Organization

# Create your views here.


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
