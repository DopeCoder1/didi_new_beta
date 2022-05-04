from unicodedata import name

from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name = 'home'),
    path('account/', account, name = 'account'),
    path('details/<int:id>/', details, name = 'details'),
    path('show_category/<int:id>/', show_category, name = 'show_category'),
    path("searches/", searches, name="searches"),
    path("card_add/<int:bookid>/", cart_add, name="card_add"),


    path("card_remove/<int:bookid>/", cart_remove, name="card_remove"),
    path("card_details", cart_details, name="card_details"),
    path("exit/", LogoutView.as_view(), name="exit"),
    path("afterlogin_view/", afterlogin_view, name="afterlogin_view"),
    path("order_create/", order_create, name="order_create"),
    path("profile_report", profile_report ,name="profile_report"),
]
