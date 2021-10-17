from django.db.models import Q

from sounds.models    import *
from result import ResultFlag, Result


def sounds(request):
    return Result(
                   ResultFlag.Ok,
                   {
                     'categories': Category.objects.all(),
                     'subcategories': SubCategory.objects.all(),
                     'sounds': Sound.objects.all()[:100]
                   }
                 )


def sound(request, sound_code):
    return Result(
                   ResultFlag.Ok,
                   {
                     'sound': Sound.objects.get(code=sound_code)
                   }
                 )


# The search field needs to be able to return results that match either the sound code or part of the sound
#     name.
def search_sounds(request):
    text_filter = request.POST['search_text']
    category = Category.objects.get(text=request.POST['search_category'])
    # subcategory = SubCategory.objects.get(text=request.POST['search_subcategory'])
    return Result(
                   ResultFlag.Ok,
                   Sound.objects.filter(
                                         Q(name__icontains=text_filter) | Q(code__icontains=text_filter),
                                         category=category,
                                         # subcategory=subcategory
                                       )
                 )

# Need to add JSON serialization to models
