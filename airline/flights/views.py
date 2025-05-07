from django.shortcuts import render
from .models import Flight, Passenger
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })

def flight(request, flight_id):
    flight = Flight.objects.get(pk=flight_id)
    passengers = flight.passengers.all()
    non_passengers = Passenger.objects.exclude(flights=flight)
    
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": passengers,
        "non_passengers": non_passengers
    })

@login_required
def book(request, flight_id):
    flight = Flight.objects.get(pk=flight_id)
    
    if request.method == "POST":
        passenger_id = int(request.POST["passenger"])
        
        passenger = Passenger.objects.get(pk=passenger_id)
        
        passenger.flights.add(flight)
        
        return HttpResponseRedirect(reverse("flight", args=(flight.id,)))

    non_passengers = Passenger.objects.exclude(flights=flight)
    
    return render(request, "flights/book.html", {
        "flight": flight,
        "non_passengers": non_passengers
    })

@login_required
def dashboard(request):
    return render(request, "flights/dashboard.html")
