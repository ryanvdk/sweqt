from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('<slug:organization>/',
         views.OrganizationView.as_view(), name="organization"),
    path('<slug:organization>/contributors/<slug:contributor>/',
         views.ContributorView.as_view(), name="contributor"),
    path('<slug:organization>/projects/<slug:project>/',
         views.ProjectView.as_view(), name="project"),
    path('<slug:organization>/contributions/<int:pk>/',
         views.ContributionView.as_view(), name="contribution"),
    path('<slug:organization>/revenue/<int:pk>/',
         views.RevenueItemView.as_view(), name="revenue_item")

]
