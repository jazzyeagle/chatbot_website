from django.shortcuts import render, redirect

from result import Result, ResultFlag
from sounds import data

# Create your views here.
def sounds(request):
    if 'search' in request.session:
        page_data = Result(ResultFlag.Ok, request.session['search'])
    else:
        page_data = data.sounds(request)
    if request.method=='POST':
        page_data = request.POST['']
    if page_data.isOk:
        return render(request, 'sounds/sounds.html', page_data.get())


def sound(request, sound_code):
    page_data = data.sound(request, sound_code)
    if page_data.isOk:
        return render(request, 'sounds/sound.html', page_data.get())


def search_sounds(request):
    query = data.search_sounds(request)
    if query.isOk():
        request.session['search'] = query.get()
    return redirect('sounds')
