from django.contrib import admin
from django.urls import path
from chat import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    path('send_message/', views.send_message, name='send_message'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
