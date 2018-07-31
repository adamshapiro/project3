from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cart", views.view_cart, name="cart"),
    path("confirm", views.confirm_cart, name="confirm"),
    path("orders", views.orders, name="orders"),
    path("all_orders", views.all_orders, name="all_orders"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("ajax/add_item", views.add_item, name="add_item"),
    path("ajax/confirm_order", views.confirm_order, name="confirm_order")
]
