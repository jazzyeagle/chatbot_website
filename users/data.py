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
    for rt in Command.objects.all():
        data[rt.text.replace(' ', '_')] = user.requested_by.filter(command=rt).order_by('used_on_track').distinct('used_on_track')
        total += data[rt.text.replace(' ', '_')].count()
    data['Tours']  = Tour.objects.filter(named_by=user).distinct()
    data['Venues'] = Venue.objects.filter(named_by=user).distinct()
    data['Songs']  = Song.objects.filter(named_by=user).distinct()
    data['Sounds_Named'] = Sound.objects.filter(renamed_by=user).distinct()
    data['Covers'] = VenueArt.objects.filter(found_by=user).distinct()
    total += data['Tours'].count() + data['Venues'].count() + data['Songs'].count() + data['Sounds_Named'].count() + data['Covers'].count()
    data['total'] = total
    print(data.keys())
    return Result(ResultFlag.Ok, data)
