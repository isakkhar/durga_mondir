from django.urls import path
from . import views

app_name = 'durga'

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.events, name='events'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('album/<int:album_id>/', views.album_detail, name='album_detail'),
    path('committee/', views.committee, name='committee'),
    path('durga-sangha/', views.durga_sangha, name='durga_sangha'),
    path('contact/', views.contact, name='contact'),
    path('page/<slug:slug>/', views.page_detail, name='page_detail'),
]