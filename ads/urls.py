from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_ads, name='list_ads'),
    path('ads/create/', views.create_ad, name='create_ad'),
    path('ads/<int:ad_id>/', views.ad_detail, name='ad_detail'),
    path('ads/<int:ad_id>/edit/', views.edit_ad, name='edit_ad'),
    path('ads/<int:ad_id>/delete/', views.delete_ad, name='delete_ad'),
    path('ads/<int:ad_id>/proposal/', views.send_proposal, name='send_proposal'),
    path('ads/proposal/<int:proposal_id>/<str:status>/', views.update_proposal_status, name='update_proposal_status'),
    path('register/', views.register, name='register'),
]
