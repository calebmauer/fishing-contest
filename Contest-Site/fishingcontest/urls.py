from django.conf.urls import url

from fishingcontest import views, main

urlpatterns = [
   url(r'^$', main.main, name='main'),

   
   # Leaderboard pages for viewing how the contest is going
   url(r'^leaderboard/$', views.leaderboard, name='leaderboard'),
   url(r'^leaderboard_long/$', views.leaderboard_long, name='leaderboard_long'),
   
   # The following are all REST API URLS - not intended to be called by the user directly
   
   # Get list of all contestants
   url(r'^contestantlist/$', main.contestantlist, name='contestantlist'),
   
    # Takes a contestant and renders list of all caught fish
   url(r'^fishlist/$', main.fishlist, name='fishlist'),
   
   # addcontestant (first,last,age,gender)
   url(r'^addcontestant/$', main.addcontestant, name='addcontestant'), 
   url(r'^deletecontestant/$', main.deletecontestant, name='deletecontestant'),
   
   # addfish (contestantid,fishweight)
   url(r'^addfish/$', main.addfish, name='addfish'), 
   
   
   url(r'^deletefish/$', main.deletefish, name='deletefish'),
]