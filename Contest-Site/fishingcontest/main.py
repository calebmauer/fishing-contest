from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import RequestContext, loader

from fishingcontest.models import Contestant, Fish

def main(request):
	""" A main page which contains a list of users. Can click on a contestant to view
	and edit the list of fish they caught. """
	template = loader.get_template('fishingcontest/main.html')
	context = RequestContext(request, {
		'contestants': list(sorted(Contestant.objects.all(), key=lambda x: x.last_name+x.first_name))
    })
	return HttpResponse(template.render(context))
	
def contestantlist(request):
	contestantList = {'contestants': [{'first_name':c.first_name,'last_name':c.last_name,'age':c.age,'id':c.id}
						for c in sorted(Contestant.objects.all(), key=lambda x: x.last_name+x.first_name)]}
	
	return JsonResponse(contestantList)

def addcontestant(request):

	firstname = request.GET.get('firstName')
	lastname = request.GET.get('lastName')
	age = request.GET.get('age')
	gender = request.GET.get('gender')

	if len(firstname) == 0:
		raise ValueError('First name supplied to addcontestant is empty.')
	elif len(lastname) == 0:
		raise ValueError('Last name supplied to addcontestant is empty.')
	elif len(gender) != 1 and not (gender == 'M' or gender == 'F'):
		raise ValueError('Gender supplied to addcontestant is not M or F.')

	# Add new contestant and save it to the database
	contestant = Contestant.objects.create(first_name=firstname,last_name=lastname,age=int(age),gender=gender)
	contestant.save()
	
	# return HTML rendering of the new contestant
	template = loader.get_template('fishingcontest/contestantentry.html')
	context = RequestContext(request, {
		'contestant': contestant
    })
	return HttpResponse(template.render(context))
	
def addfish(request):

	contestantid = request.GET.get('contestantid')
	new_fish_weight = request.GET.get('weight')

	contestant = Contestant.objects.get(id=int(contestantid))
	newFish = Fish.objects.create(weight=float(new_fish_weight),contestant=contestant)
	newFish.save()

	template = loader.get_template('fishingcontest/fishentry.html')
	context = RequestContext(request, {
		'fish': newFish
    })
	return HttpResponse(template.render(context))
	
def deletecontestant(request):
	contestantid = request.GET.get('contestantid')
	Contestant.objects.get(id=int(contestantid)).delete()
	return HttpResponse('true')
	
def deletefish(request):
	fishid = request.GET.get('fishid')
	Fish.objects.get(id=int(fishid)).delete()
	return HttpResponse('true')
	
def fishlist(request,contestantid):
	template = loader.get_template('fishingcontest/fishlist.html')
	context = RequestContext(request, {
		'fishes': list(sorted(Contestant.objects.get(id=int(contestantid)).fish_set.all(),key=lambda x: x.weigh_time)),
		'contestantid': contestantid
    })
	return HttpResponse(template.render(context))