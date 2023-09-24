from django.urls import path

from api.v1.views import add_deals

urlpatterns = [
    path('add-deals', add_deals),
]
