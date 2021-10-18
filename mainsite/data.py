from mainsite.models import *
from show.models     import *

from result import ResultFlag, Result


def tours(request):
    return Result(ResultFlag.Ok, { 'tours': Tour.objects.all() })


def tour(request, tour_name):
    tour   = Tour.objects.get(name=tour_name)
    return Result(ResultFlag.Ok, {
                                   'tour':   tour,
                                   'venues': tour.venue_set.order_by('date')
                                 })


def venue(request, tour_name, venue_name):
    venue  = Venue.objects.get(name=venue_name)
    return Result(ResultFlag.Ok, {
                                   'venue': venue,
                                   'songs': venue.song_set.order_by('track_number')
                                 })


def song(request, tour_name, venue_name, song_title):
    song   = Song.objects.get(title=song_title)
    data = { 'song': song }
    for rt in RequestType.objects.all():
        data[rt.text.replace(' ', '_')] = song.request_set.filter(request_type=rt)
    return  Result(ResultFlag.Ok, data)
