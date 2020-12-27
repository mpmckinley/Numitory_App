from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # ITEMS
    path('', views.inventory, name='inventory'),
    path('item/create/', views.itemcreate, name='itemcreate'),
    path('item/<int:item_pk>', views.itemdetail, name='itemdetail'),

    # TYPES
    path('type/', views.typeinv, name='typeinv'),
    path('type/items/<int:type_pk>', views.typeitems, name='typeitems'),
    path('type/create/', views.typecreate, name='typecreate'),
    path('type/<int:type_pk>/', views.typedetail, name='typedetail'),

    # COLLECTIONS
    path('collection/', views.collinv, name='collinv'),
    path('collection/items/<int:coll_pk>', views.collitems, name='collitems'),
    path('collection/create/', views.collcreate, name='collcreate'),
    path('collection/<int:coll_pk>/', views.colldetail, name='colldetail'),
]