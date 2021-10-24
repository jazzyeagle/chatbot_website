from django.shortcuts import render

from mainsite import data

# Create your views here.
def index(request):
    page_data = data.index(request)
    if page_data.isOk():
        return render(request, 'mainsite/index.html', page_data.get())


def tours(request):
    page_data = data.tours(request)
    if page_data.isOk():
        return render(request, 'mainsite/tour/tours.html', page_data.get())


def venues(request):
    pass


def songs(request):
    pass


def tour(request, tour_name):
    page_data = data.tour(request, tour_name)
    if page_data.isOk():
        return render(request, 'mainsite/tour/tour.html', page_data.get())


def venue(request, tour_name, venue_name):
    page_data = data.venue(request, tour_name, venue_name)
    if page_data.isOk():
        return render(request, 'mainsite/venue/venue.html', page_data.get())


def song(request, tour_name, venue_name, song_name):
    page_data = data.song(request, tour_name, venue_name, song_name)
    if page_data.isOk():
        return render(request, 'mainsite/song/song.html', page_data.get())


def song_rate(request, tour_name, venue_name, song_name):
    pass
