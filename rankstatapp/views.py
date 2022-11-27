from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

# lolwatcher
from funcs.account_info import *
# Create your views here.

def hello_world(request):
    return render(request, 'rankstatapp/rankstat.html')

def rankinfo(request):
    template = loader.get_template('rankstatapp/ranksearch.html')
    return HttpResponse(template.render({},request))

def ranksearch(request):
    template = loader.get_template('rankstatapp/ranksearch.html')
    try:
        my_region = request.GET.get('region')
        myid = request.GET.get('name')
        me = watcher.summoner.by_name(my_region, myid)
        my_ranked_stats = watcher.league.by_summoner(my_region, me['id'])

        my_solo_stats = list(filter(lambda my_solo_stats: my_solo_stats['queueType'] =='RANKED_SOLO_5x5' , my_ranked_stats)) 

        my_flex_stats = list(filter(lambda my_flex_stats: my_flex_stats['queueType'] =='RANKED_FLEX_SR' , my_ranked_stats)) 
        if my_solo_stats != []:
            my_solo_tier = f"{my_solo_stats[0]['tier']} {my_solo_stats[0]['rank']} {my_solo_stats[0]['leaguePoints']}"
            my_solo_winlose = f"{my_solo_stats[0]['wins']}승 {my_solo_stats[0]['losses']}패 ({my_solo_stats[0]['wins']/(my_solo_stats[0]['wins']+my_solo_stats[0]['losses'])*100:.2f}%) "
        else:
            my_solo_tier = '솔로랭크 전적없음'
            my_solo_winlose = '0승 0패'
            
            
        if my_flex_stats !=[]:
            my_flex_tier = f"{my_flex_stats[0]['tier']} {my_flex_stats[0]['rank']} {my_flex_stats[0]['leaguePoints']}"
            my_flex_winlose = f"{my_flex_stats[0]['wins']}승 {my_flex_stats[0]['losses']}패 ({my_flex_stats[0]['wins']/(my_flex_stats[0]['wins']+my_flex_stats[0]['losses'])*100:.2f}%) "
        else:
            my_flex_tier = '자유랭크 전적없음'
            my_flex_winlose = '0승 0패'

        context = {
            'name':myid,
            'my_solo_tier':my_solo_tier,
            'my_flex_tier':my_flex_tier,
            'my_solo_winlose':my_solo_winlose,
            'my_flex_winlose':my_flex_winlose,
        }
        return HttpResponse(template.render(context, request))
    except:
        context = {
            'error':'소환사가 없습니다'
        }
        return HttpResponse(template.render(context, request))
    
    
