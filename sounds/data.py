from django.core.exceptions import ObjectDoesNotExist
from django.db.models       import Q

from login.models           import User
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
        request.session.pop('search')
    else:
        sounds = Sound.objects.all()[:500]
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
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
    else:
        user = None
    return Result(
                   ResultFlag.Ok,
                   {
                     'text_filter':     request.POST['search_text'],
                     'search_category': request.POST['search_category'],
                     'user':            user
                   }

                 )
