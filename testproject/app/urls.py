from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.list_museums, name='index'),
    path('museum/<int:museum_id>', views.list_museum_paintings, name='paintings'),
    path('api/painting/<int:painting_id>', views.painting_info, name='painting_info'),
    path('search', views.search, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
