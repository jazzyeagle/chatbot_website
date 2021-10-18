from django.shortcuts import render, redirect

from result import Result, ResultFlag
from sounds import data

# Create your views here.
def sounds(request):
    page_data = data.sounds(request)
    if page_data.isOk():
        print(f'Page Data: {page_data.get()}')
        return render(request, 'sounds/sound/sounds.html', page_data.get())


def sound(request, sound_code):
    print('sound')
    page_data = data.sound(request, sound_code)
    if page_data.isOk():
        return render(request, 'sounds/sound/sound.html', page_data.get())


def sound_search(request):
    print('sound_search')
    query = data.sound_search(request)
    if query.isOk():
        print(f'Query result: {query.get()}')
        request.session['search'] = query.get()
    return redirect('sounds')
