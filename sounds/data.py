from django.core.exceptions import ObjectDoesNotExist
from django.db.models       import Q

from sounds.models          import *
from result                 import ResultFlag, Result


def sounds(request):
    if 'search' in request.session:
        search = request.session['search']
        category = Category.objects.get(text=search['search_category'])
        sounds = Sound.objects.filter(Q(name__icontains=search['text_filter']) |
                                      Q(code__icontains=search['text_filter']),
                                      category=category)
        request.session.pop('search')
    else:
        sounds = Sound.objects.all()[:500]
    return Result(
                   ResultFlag.Ok,
                   {
                     'categories':    Category.objects.all(),
                     'subcategories': SubCategory.objects.all(),
                     'sounds':        sounds
                   }
                 )


def sound(request, sound_code):
    print(f'Sound Code: {sound_code}')
    return Result(
                   ResultFlag.Ok,
                   {
                     'sound': Sound.objects.get(code=sound_code)
                   }
                 )


# The search field needs to be able to return results that match either the sound code or part of the sound
#     name.
def sound_search(request):
    return Result(
                   ResultFlag.Ok,
                   {
                     'text_filter':     request.POST['search_text'],
                     'search_category': request.POST['search_category']
                   }

                 )
