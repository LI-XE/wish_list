from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('additem', views.additem),
    path('wish_items/<product_id>', views.wishitem),
    path('dashboard/<product_id>/delete', views.delete),
    path('dashboard/<product_id>/remove', views.remove),
    path('dashboard/<product_id>/add', views.add),
]