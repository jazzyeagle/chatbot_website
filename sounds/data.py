from django.core.exceptions import ObjectDoesNotExist
from django.db.models       import Q, Avg, Count, Max

from users.models           import User
from show.models            import *
from sounds.models          import *
from result                 import ResultFlag, Result


def sounds(request):
    if 'search' in request.session:
        search = request.session['search']
        if search['search_category']:
            category = Category.objects.get(text=search['search_category'])
            sounds = Sound.objects.filter(Q(name__icontains=search['text_filter']) |
                                          Q(code__icontains=search['text_filter']),
                                          category=category)
        else:
            sounds = Sound.objects.filter(Q(name__icontains=search['text_filter']) |
                                          Q(code__icontains=search['text_filter']))
        ratings = {}
        request.session.pop('search')
    else:
        sounds = Sound.objects.all().annotate(avg_rating=Avg('ratings__rating'))
        
    sounds = sounds.annotate(avg_rating=Avg('ratings__rating'),
                             num_times_used = Count('requests'),
                             last_used      = Max('requests__used_on_track__venue__date')).order_by('name')[:10]
    
    for s in sounds:
        print(f'{s.name} [{s.code}]: {s.avg_rating} {s.num_times_used} {s.last_used}')
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
    else:
        user = None
    return Result(
                   ResultFlag.Ok,
                   {
                     'categories':    Category.objects.all(),
                     'subcategories': SubCategory.objects.all(),
                     'sounds':        sounds,
                     'user':          user
                   }
                 )


def sound(request, sound_code):
    sound = Sound.objects.get(code=sound_code)
    requests = Request.objects.filter(sound=sound)
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
    else:
        user = None
    return Result(
                   ResultFlag.Ok,
                   {
                     'sound':    sound,
                     'requests': requests,
                     'user':     user
                   }
                 )


# The search field needs to be able to return results that match either the sound code or part of the sound
#     name.
def sound_search(request):
    return Result(
                   ResultFlag.Ok,
                   {
                     'text_filter':     request.POST['search_text'],
                     'search_category': request.POST['search_category'],
                   }

                 )



def sound_rate(request, sound_code):
    if 'user_id' not in request.session:
            return Result(ResultFlag.Error, 'You must be logged in if you wish to rate a song.')

    user = User.objects.get(id=request.session['user_id'])
    sound = Sound.objects.get(code=sound_code)
    rating = request.POST['rating']

    # We create the rating without the rating being added to ensure that matching for get_or_create will get_or_create
    #    a rating for the same user & sound, in case user is changing their rating.
    sound_rating, _ = SoundRating.objects.get_or_create(user=user, sound=sound)
    sound_rating.rating = rating
    sound_rating.save()

    return Result(ResultFlag.Ok, None)
