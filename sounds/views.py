from django.shortcuts import render, redirect

from result import Result, ResultFlag
from sounds import data

# Create your views here.
def sounds(request):
    page_data = data.sounds(request)
    if page_data.isOk():
        return render(request, 'sounds/sound/sounds.html', page_data.get())


def sound(request, sound_code):
    page_data = data.sound(request, sound_code)
    for r in page_data.get()['requests']:
        print(r.serialize())
    if page_data.isOk():
        return render(request, 'sounds/sound/sound.html', page_data.get())


def sound_search(request):
    query = data.sound_search(request)
    if query.isOk():
        request.session['search'] = query.get()
    return redirect('sounds')
