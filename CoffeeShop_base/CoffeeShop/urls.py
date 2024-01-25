from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from skripsi.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', home, name='home'),
    path('Beranda/', beranda, name='beranda'),
    path('Search/', search, name='search'),
    path('Detail/<int:id>/', detail, name='detail'),
    path('favorite/<int:favorite_id>', favorite, name='favorite'),
    path('delete-riwayat/<int:riwayat_id>/', delete_riwayat, name='delete_riwayat'),
    path('hapus-favorite/', delete_favorite, name='delete_favorite'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
