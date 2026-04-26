from django.urls import path
from . import views

urlpatterns = [

    path("price/add/", views.add_service_price, name="add_service_price"),
    path("price/list/", views.service_price_list, name="service_price_list"),
    path('price/edit/<int:id>/', views.edit_price, name='edit_price'),
    path('price/delete/<int:id>/', views.delete_price, name='delete_price'),
    path("tyre/add/", views.add_tyre_service, name="add_tyre_service"),
    path("tyre/list/", views.tyre_list, name="tyre_list"),
    path("tyre/receipt/<int:pk>/", views.tyre_receipt, name="tyre_receipt"),
    path("battery/add/", views.add_battery_service, name="add_battery_service"),
    path("battery/list/", views.battery_list, name="battery_list"),
    path("battery/receipt/<int:pk>/", views.battery_receipt, name="battery_receipt"),
    path('battery/edit/<int:id>/', views.edit_battery, name='edit_battery'),
    path('battery/delete/<int:id>/', views.delete_battery, name='delete_battery'),
    path('battery/<int:id>/', views.battery_detail, name='battery_detail'),
    path('tyre/<int:id>/', views.tyre_detail, name='tyre_detail'),
    path('tyre/edit/<int:id>/', views.edit_tyre, name='edit_tyre'),
    path('tyre/delete/<int:id>/', views.delete_tyre, name='delete_tyre'),
    
]