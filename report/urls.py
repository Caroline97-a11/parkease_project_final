from django.urls import path
from . import views

urlpatterns = [
    path("report/", views.report_dashboard, name="report_dashboard"),
    path('vehicle/delete/<int:id>/', views.delete_vehicle, name='delete_vehicle'),

]
