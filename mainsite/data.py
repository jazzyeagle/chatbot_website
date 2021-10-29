from django.db.models.functions import Lower

from mainsite.models import *
from show.models     import *
from users           import data

from result import ResultFlag, Result


def index(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
    else:
        user = None
    # Uses the user page as default, so pull same data
    page_data = data.user(request, user.username)
    if page_data.isOk:
        return Result(ResultFlag.Ok, page_data.get() )
    else:
        return Result(ResultFlag.Error, 'Could not get User data')


def tours(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
    else:
        user = None
    return Result(ResultFlag.Ok, { 'tours': Tour.objects.all().order_by('month'),
                                   'user':  user
                                 })


def venues(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
    else:
        user = None
    return Result(ResultFlag.Ok, { 'venues': Venue.objects.all().order_by('date'),
                                   'user':   user
                                 })


def songs(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
    else:
        user = None
    return Result(ResultFlag.Ok, { 'songs': Song.objects.all().order_by(Lower('title')),
                                   'user':  user
                                 })




def tour(request, tour_name):
    tour   = Tour.objects.get(name=tour_name)
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
    else:
        user = None
    return Result(ResultFlag.Ok, {
                                   'tour':   tour,
                                   'venues': tour.venue_set.order_by('date'),
                                   'user':   user
                                 })


def venue(request, tour_name, venue_name):
    venue  = Venue.objects.get(name=venue_name)
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
    else:
        user = None
    return Result(ResultFlag.Ok, {
                                   'venue': venue,
                                   'songs': venue.song_set.order_by('track_number'),
                                   'user':  user
                                 })


def song(request, tour_name, venue_name, song_title):
    song   = Song.objects.get(title=song_title)
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
    else:
        user = None
    data = { 'song': song,
             'user': user
           }
    for rt in RequestType.objects.all():
        data[rt.text.replace(' ', '_')] = song.request_set.filter(request_type=rt)
    return  Result(ResultFlag.Ok, data)
