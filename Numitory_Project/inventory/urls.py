from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # ITEMS
    path('', views.inventory, name='inventory'),
    path('item/create/', views.itemcreate, name='itemcreate'),
    path('item/<int:item_pk>', views.itemdetail, name='itemdetail'),
    path('type/create/', views.typecreate, name='typecreate'),
    path('collection/create/', views.collectioncreate, name='collectioncreate'),

    # TYPES


    # COLLECTIONS
    # path('<int:blog_id>/', views.detail, name='detail'),
]