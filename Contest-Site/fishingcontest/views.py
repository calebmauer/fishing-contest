import sys
import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from operator import *

from fishingcontest.models import Contestant, Fish

# Age groups, inclusive. Specify min and max.
age_groups = ((3, 6), (7, 10), (11, 16))

# Max rows in a table per page
page_size = 16

def leaderboard_long(request):
    leader_lists, list_labels = getLeaderLists()
    leader_lists.insert(0, getLeaderList(Contestant.objects.all()))
    list_labels.insert(0, "All Contestants")
    
    leader_lists = zip(leader_lists, list_labels)
    
    template = loader.get_template('fishingcontest/leaderboard_long.html')
    context = RequestContext(request, {
        'leader_lists': leader_lists
    })
    return HttpResponse(template.render(context))

def leaderboard(request):
    
    list_page = 0
    if 'list_page' in request.GET:
        list_page = int(request.GET['list_page'])

    
    leader_lists, list_labels = getLeaderLists()

    all_last = True
    for i, leader_list in enumerate(leader_lists):
        page, last_page = getPage(leader_list, list_page)
        all_last = all_last and last_page
        leader_lists[i] = page

    new_row = [False, False, False, True, False, False]

    leader_lists = zip(leader_lists, list_labels, new_row)

    if all_last:
        list_page = 0
    else:
        list_page += 1
    
    template = loader.get_template('fishingcontest/leaderboard.html')
    context = RequestContext(request, {
        'leader_lists': leader_lists,
        'list_page' : list_page
    })
    return HttpResponse(template.render(context))

def getLeaderLists():
    leader_lists = []

    for gender in (Contestant.FEMALE, Contestant.MALE):
        leader_lists.extend([getLeaderList(Contestant.objects.filter(age__gte=min_age,
                                            age__lte=max_age,
                                            gender__exact=gender)) for
                        min_age, max_age in age_groups])

    list_labels = []
    for gender_label in ["Girls ", "Boys "]:
        list_labels.extend([gender_label + "Ages " + str(min_age)
                            + " to " + str(max_age) for
                        min_age, max_age in age_groups])

    return leader_lists, list_labels


def getLeaderList(objects):
    leader_list = list(objects)

    for contestant in leader_list:
        contestant.getBiggestFish()
        contestant.name = str(contestant)

    leader_list = sorted(sorted(leader_list,
                               key=fishSorterByWeighTime('biggest_fish')),
                        key=sortBiggestFish, reverse=True)

    addRanks(leader_list, [])

    addFishRanks(leader_list)

	# un-comment these lines to remove ranks from contestants who haven't caught fish
    #for c in leader_list:
    #    if c.biggest_fish is None:
    #        c.rank = ''

    return leader_list

def getPage(leader_list, page):
    last_page = False
    result = []
    page_start = page*page_size
    page_end = (page+1)*page_size

    if page_end >= len(leader_list):
        last_page = True

    if last_page:
        result = getLastPage(leader_list, page_size)
    else:
        result = leader_list[page_start:page_end]

    return result, last_page

def getLastPage(leader_list, page_size):
    last_page = False
    page_start = 0
    page_end = page_size
    while not last_page:
        if page_end >= len(leader_list):
            last_page = True
        else:
            page_start += page_size
            page_end += page_size

    return leader_list[-page_size:]
        

# Adds a rank field to each item in the list with value equal to the
# rank of the item in the list
def addRanks(olist, colors):
    for i, o in enumerate(olist):
        if o:
            o.rank = i+1
            if len(colors) > i:
                o.color = colors[i]
            
def addFishRanks(clist):
    by_biggest = sorted(sorted(clist,
                               key=fishSorterByWeighTime('biggest_fish')),
                        key=sortBiggestFish, reverse=True)
    
    addRanks(map(attrgetter('biggest_fish'), by_biggest), ["blue","red","green"])

# Key function for sorting contestants by their biggest_fish field
def sortBiggestFish(c):
    bf = c.biggest_fish
    if bf:
        return bf.weight
    else:
        return 0.0

def fishSorterByWeighTime(fish_attr):
    fish_getter = attrgetter(fish_attr)
    def sortFishByWeighTime(c):
        fish = fish_getter(c)
        t = sys.maxsize
        if fish:
            t = unix_time(fish.weigh_time)
        return t

    return sortFishByWeighTime

def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = datetime.datetime.utcfromtimestamp(dt) - epoch
    return delta.total_seconds()

def unix_time(dt):
    return dt.timestamp()
