from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,  Http404
from django.shortcuts import render
from django.urls import reverse
from .models import *

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(close = False)
    })

@login_required
def create(request):
    Categories = Category.objects.all()
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        start = request.POST["start"]
        link = request.POST["link"]
        category = Category.objects.get(pk=int(request.POST["Category"]))
        creator = request.user
        listing = Listing(title = title, description = description, start = start, url = link, category = category, creator = creator)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html", {
            "category": Categories
        })

def place_bid(request, listing_id):
    w = check(request, listing_id)
    if request.method =="POST":
        user = request.user
        item = Listing.objects.get(pk = listing_id)
        price = request.POST["price"]
        if int(price)>item.start:
            bid = Bid(price = price, item = item, bidder= user)
            item.start = price
            item.winner = user
            item.save()
            bid.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponse("Error")
    else:
        return render(request, "auctions/listing.html",{
            "listing": listing,
            "comments": comments,
            "message": not w,
            "trial" : w
        })


def categories(request):
    Categories = Category.objects.all()
    return render(request, "auctions/category.html",{
        "category": Categories
    })

def category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        raise Http404("Category not found.")
    return render(request, "auctions/view_category.html", {
        "category": category,
        "items": category.items.all()
    })

def listing(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
        comments = listing.comments.all()
        w = check(request, listing_id)
    except Listing.DoesNotExist:
        raise Http404("Listing not found.")
    user = request.user
    if listing.close == True:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": comments,
            "closed": True,
            "winner": listing.winner
        })
    if listing in user.created_listings.all():
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": comments,
            "created": True
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": comments,
            "message": not w,
            "trial": w
        })


def close(request, listing_id):
    Item = Listing.objects.get(pk = listing_id)
    Item.close = True
    Item.save()
    return HttpResponseRedirect(reverse("index"))

@login_required
def comment(request, listing_id):
    if request.method == "POST":
        content = request.POST["comment"]
        listing = Listing.objects.get(pk = listing_id)
        comment = Comment(item = listing, comment = content)
        comment.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required
def watchlist(request):
    current_user = request.user
    watchlist = Watchlist.objects.get(creator = current_user)
    return render(request, "auctions/watchlist.html",{
        "list":watchlist.items.all()
    })

@login_required
def check(request, listing_id):
    listing = Listing.objects.get(pk = listing_id)
    user = request.user
    w = user.Watchlist.get()
    test = listing in w.items.all()
    return test

def add_watchlist(request, listing_id):
    listing = Listing.objects.get(pk = listing_id)
    user = request.user
    w = user.Watchlist.get()
    w.items.add(listing)
    return HttpResponseRedirect(reverse("watchlist"))

def remove_watchlist(request, listing_id):
    listing = Listing.objects.get(pk = listing_id)
    user = request.user
    w = user.Watchlist.get()
    w.items.remove(listing)
    return HttpResponseRedirect(reverse("watchlist"))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
