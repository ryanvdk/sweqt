from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('<slug:organization>/',
         views.OrganizationView.as_view(), name="organization"),
    path('<slug:organization>/contributors/<slug:contributor>/',
         views.OrganizationView.as_view(), name="organization")
]
