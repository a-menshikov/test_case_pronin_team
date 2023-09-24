from django.urls import path

from api.v1.views import add_deals, get_top_customers

urlpatterns = [
    path('add-deals', add_deals),
    path('get-top', get_top_customers),
]
