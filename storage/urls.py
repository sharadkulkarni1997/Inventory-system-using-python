from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add/", views.add_box, name="add_box"),
    path("in-use/", views.move_to_in_use, name="move_to_in_use"),
    path("consume/", views.consume_box, name="consume_box"),
]