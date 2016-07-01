from django.conf.urls import url

from fishingcontest import views, main

urlpatterns = [
   url(r'^$', views.index, name='index'),
   url(r'^main/$', main.main, name='main'),
   url(r'^main/fishlist/(\d+)/$', main.fishlist, name='fishlist'), # Takes a contestant and renders list of all caught fish
   url(r'^main/addcontestant/$', main.addcontestant, name='addcontestant'), # addcontestant (first,last,age,gender)
   url(r'^main/deletecontestant/$', main.deletecontestant, name='deletecontestant'),
   url(r'^main/addfish/$', main.addfish, name='addfish'), # addfish/(contestantid,fishweight)
   url(r'^main/deletefish/$', main.deletefish, name='deletefish'),
   url(r'^leaderboard/$', views.leaderboard, name='leaderboard'),
   url(r'^leaderboard_long/$', views.leaderboard_long, name='leaderboard_long')
]