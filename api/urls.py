from django.urls import path
from .views import CompanyView

urlpatterns = [
  path('companies/', CompanyView.as_view(), name='companies'),
  path('companies/<int:nit>', CompanyView.as_view(), name='companiesNIT')
]