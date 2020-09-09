from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.create, name = "create"),
    path("categories/", views.categories, name ="category"),
    path("listing/<int:listing_id>", views.listing, name = "listing"),
    path("category/<int:category_id>", views.category, name = "view_category"),
    path("<int:listing_id>/comment", views.comment, name  = "comment"),
    path("watchlist", views.watchlist, name = "watchlist"),
    path("add/<int:listing_id>", views.add_watchlist, name = "add_watchlist"),
    path("remove/<int:listing_id>", views.remove_watchlist, name = "remove_watchlist"),
    path("check/<int:listing_id>", views.check),
    path("close/<int:listing_id>", views.close, name = "close"),
    path("bid/<int:listing_id>", views.place_bid, name = "bid")
]
