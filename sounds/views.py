from django.contrib   import messages
from django.shortcuts import render, redirect

from result import Result, ResultFlag
from sounds import data


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


def sound_rate(request, sound_code):
    page_data = data.sound_rate(request, sound_code)
    if page_data.hasErrors():
        for err in page_data.getErrors():
            messages.error(request, err)
            return redirect(reverse('sounds')) # We don't want to use bookmarking, because want the user to see the error
                                               # messages at the top of the page.

    # Not using the name here because we want to use the bookmarking capabilities of the URL
    return redirect('/sounds/#' + sound_code)
