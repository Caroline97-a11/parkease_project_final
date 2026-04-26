from django.urls import path
from .import views
urlpatterns =[
    path('', views.loginPage, name = 'loginPage'),
    path('staff/', views.register, name='register'),
    path('user/', views.user_list, name="user_list"),
    path('edit-user/<int:pk>/', views.edit_user, name='edit_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('user/delete/<int:id>/', views.delete_user, name='delete_user'),

]