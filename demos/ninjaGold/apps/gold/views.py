from django.shortcuts import render, redirect
from random import randint
from datetime import datetime
from django.utils import formats

# Create your views here.
def index(request):
    if 'gold' not in request.session:
        request.session['gold'] = 0
        request.session['activities'] = []

    return render(request, 'gold/index.html')

def process_money(request):
    if request.method == 'POST':
        building = request.POST['building']

        buildings = {
            'farm': randint(10, 20),
            'cave': randint(5, 10),
            'house': randint(2, 5),
            'casino': randint(-50, 50)
        }

        if building in buildings:
            gold = buildings[building]
            request.session['gold'] += gold

            gain_lost = 'gain' if gold > 0 else 'lost'
            if gain_lost is 'gain':
                activity = 'Earned {} golds from the {}! ({})'.format(gold, building, formats.date_format(datetime.now(), "SHORT_DATETIME_FORMAT"))
            else:
                activity = 'You entered a {}, and lost {} golds...Ouch... ({})'.format(building, abs(gold), formats.date_format(datetime.now(), "SHORT_DATETIME_FORMAT"))

            activity = {'class': gain_lost, 'activity': activity}
            print activity
            request.session['activities'].insert(0, activity)


    return redirect('/')
