from django.shortcuts import render, redirect
from sounds.models    import *

# Create your views here.
def sounds(request):
    num_results = Sound.objects.count() / 10
    page_data = {
                  'categories': Category.objects.all(),
                  'subcategories': SubCategory.objects.all(),
                  'sounds': Sound.objects.all()
                }
    return render(request, 'sounds/sounds.html', page_data)


def sound(request, sound_code):
    sound = Sound.objects.get(code=sound_code)
    page_data = {
                  'sound': sound
                }
    return render(request, 'sounds/sound.html', page_data)


def search_sounds(request):
    pass
