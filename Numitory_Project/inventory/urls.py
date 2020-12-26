from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # ITEMS
    path('', views.inventory_home, name='inventory_home'),
    path('itemcreate/', views.itemcreate, name='itemcreate'),

    # TYPES


    # COLLECTIONS
    # path('<int:blog_id>/', views.detail, name='detail'),
]