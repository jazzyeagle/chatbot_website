from django.db.models.functions import Lower

from show.models                import *
from users.models               import *
from result                     import *


def users(request):
    return Result(ResultFlag.Ok, {
                                   'users': User.objects.all().order_by(Lower('username'))
                                 })


def user(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        return Result(ResultFlag.Error, f'Username {username} does not exist.')
    data = { 'user': user }
    total = 0
    for rt in RequestType.objects.all():
        data[rt.text.replace(' ', '_')] = user.requested_by.filter(request_type=rt)
        total += data[rt.text.replace(' ', '_')].count()
    data['Tours']  = Tour.objects.filter(named_by=user)
    data['Venues'] = Venue.objects.filter(named_by=user)
    data['Songs']  = Song.objects.filter(named_by=user)
    data['Covers'] = VenueArt.objects.filter(found_by=user)
    total += data['Tours'].count() + data['Venues'].count() + data['Songs'].count()
    data['total'] = total
    print(data.keys())
    return Result(ResultFlag.Ok, data)
