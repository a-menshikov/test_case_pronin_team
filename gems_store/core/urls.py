from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

admin.site.site_header = 'Store Admin'
admin.site.site_title = 'gems_store'
admin.site.index_title = 'Панель администратора'
