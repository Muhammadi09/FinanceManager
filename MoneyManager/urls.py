from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('home/', include('pages.urls')),
    path('banking/', include('banking.urls')),
]
