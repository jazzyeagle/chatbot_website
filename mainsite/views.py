from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'mainsite/index.html')


def tours(request):
    return render(request, 'mainsite/tours.html')


def venues(request):
    pass


def songs(request):
    pass


def tour(request):
    return render(request, 'mainsite/tour.html')


def venue(request):
    return render(request, 'mainsite/venue.html')


def song(request):
    return render(request, 'mainsite/song.html')
