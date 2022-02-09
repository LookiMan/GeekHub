from django.urls import path

from . import views


app_name = "store"

urlpatterns = [
    path("index/", views.index, name="index"),
    path("category/<int:pk>", views.category, name="category"),
    path("edit/<int:pk>", views.edit_product, name="edit"),
    path("delete/<int:pk>", views.delete_product, name="delete"),
    path("permission_denied/", views.permission_denied, name="permission_denied"),
    path("cart/", views.cart, name="cart"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("add_from_cart/<int:pk>",
         views.add_product_from_cart, name="add_from_cart"),
    path("remove_from_cart/<int:pk>",
         views.remove_product_from_cart, name="remove_from_cart"),
]
