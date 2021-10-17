from django.shortcuts import render

from mainsite import data

# Create your views here.
def index(request):
    return render(request, 'mainsite/index.html')


def tours(request):
    return render(request, 'mainsite/tours.html', data.tours(request))


def venues(request):
    pass


def songs(request):
    pass


def tour(request, tour_name):
    return render(request, 'mainsite/tour.html', data.tour(request, tour_name))


def venue(request, tour_name, venue_name):
    return render(request, 'mainsite/venue.html', data.venue(request, tour_name, venue_name))


def song(request, tour_name, venue_name, song_name):
    return render(request, 'mainsite/song.html', data.song(request, tour_name, venue_name, song_name))


def song_rate(request, tour_name, venue_name, song_name):
    pass
