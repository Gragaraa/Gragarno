from django.shortcuts import render
from . import models
def page(request):
    list_event = models.Event.objects.all()
    data = {
        'list_event': [[i.data, i.description] for i in list_event],
    }
    return render(request, 'Papp/htmll.html', data)
