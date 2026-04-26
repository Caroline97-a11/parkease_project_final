from django.urls import path
from . import views

urlpatterns = [
    path("category/add/", views.vehicle_category, name="vehicle_category"),
    path("category/list/", views.vehicle_category_list, name="vehicle_category_list"),
    path('category/edit/<int:id>/', views.edit_category, name='edit_category'),
    path('category/delete/<int:id>/', views.delete_category, name='delete_category'),
    path('vehicle/register/', views.register_vehicle, name="register_vehicle"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("checkout/<int:pk>/", views.checkout_vehicle, name="checkout_vehicle"),
    path("receipt/print/<int:pk>/", views.vehicle_receipt, name="vehicle_receipt"),
    path('vehicle/edit/<int:id>/', views.edit_vehicle, name='edit_vehicle'),
]