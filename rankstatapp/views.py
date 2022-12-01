from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

# lolwatcher
from funcs.account_info import *
# Create your views here.

def hello_world(request):
    return render(request, 'rankstatapp/ranksearch.html')

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
            'region':my_region
        }
        return HttpResponse(template.render(context, request))
    except:
        context = {
            'error':'소환사가 없습니다'
        }
        return HttpResponse(template.render(context, request))
    
    
    ##################진행중 게임######################
    
    
def rolematch(champions, a):
    from funcs.position_match.pull_data import pull_data
    from funcs.position_match.get_roles import get_roles
    # from roleidentification import get_roles,pull_data
    champion_roles = pull_data()
    if a == []:
        pass
    else:
        for i in a:
            champion_roles[i]['JUNGLE']=10 

    return get_roles(champion_roles, champions)

def champcode2name(code):
    from urllib.request import urlopen
    import json
    url = "http://ddragon.leagueoflegends.com/cdn/12.22.1/data/en_US/champion.json"
    response = urlopen(url)
    rawchampiondata = json.loads(response.read())
    championdata = rawchampiondata['data']
    championdict = list(championdata.values())
    for i in championdict:
        if i['key'] == f'{code}':
            return i['id']
    


def Current_game_Participants(request):
    template = loader.get_template('rankstatapp/currentgame.html')
    try:
        my_region = request.GET.get('region')
        myid = request.GET.get('name')
        me = watcher.summoner.by_name(my_region, myid)
        gamenow = watcher.spectator.by_summoner(my_region, me['id'])
        #블루팀 정보
        blueteam_info = [ x for x in gamenow['participants'] if x['teamId']== 100 ]
        blue_team_champs = [x['championId'] for x in blueteam_info]
        smite_champ = []
        for x in blueteam_info:
            if x['spell1Id']==11 or x['spell2Id'] ==11:
                smite_champ.append(x['championId'])
        positions=rolematch(blue_team_champs, smite_champ)
        for x in blueteam_info:
            x['position'] = [i for i in positions if positions[i] == x['championId']][0]
        blue_datas = []
        for x in blueteam_info:
            blue_datas.append({'position':x['position'], 'name':x['summonerName'], 'champion':x['championId']})
        for x in blue_datas:
            x['championName'] = champcode2name(x['champion'])
        #소환사 스펠 데이터에 추가
        for x in blue_datas:
            x['spell1'] = list(i['spell1Id'] for i in blueteam_info if i['summonerName'] == x['name'])[0]
            x['spell2'] = list(i['spell2Id'] for i in blueteam_info if i['summonerName'] == x['name'])[0]
            
        #레드팀 정보
        redteam_info = [ x for x in gamenow['participants'] if x['teamId']== 200 ]
        red_team_champs = [x['championId'] for x in redteam_info]
        smite_champ = []
        for x in redteam_info:
            if x['spell1Id']==11 or x['spell2Id'] ==11:
                smite_champ.append(x['championId'])
        positions=rolematch(red_team_champs, smite_champ)
        for x in redteam_info:
            x['position'] = [i for i in positions if positions[i] == x['championId']][0]
        red_datas = []
        for x in redteam_info:
            red_datas.append({'position':x['position'], 'name':x['summonerName'], 'champion':x['championId']})
        for x in red_datas:
            x['championName'] = champcode2name(x['champion'])
        #소환사 스펠 데이터에 추가
        for x in red_datas:
            x['spell1'] = list(i['spell1Id'] for i in redteam_info if i['summonerName'] == x['name'])[0]
            x['spell2'] = list(i['spell2Id'] for i in redteam_info if i['summonerName'] == x['name'])[0]
        #블루팀 플레이어 정보 분류
        blue_top = list(x for x in blue_datas if x['position']=='TOP')[0]
        blue_jungle = list(x for x in blue_datas if x['position']=='JUNGLE')[0]
        blue_middle = list(x for x in blue_datas if x['position']=='MIDDLE')[0]
        blue_bottom = list(x for x in blue_datas if x['position']=='BOTTOM')[0]
        blue_utility = list(x for x in blue_datas if x['position']=='UTILITY')[0]
        #레드팀 플레이어 정보 분류
        red_top = list(x for x in red_datas if x['position']=='TOP')[0]
        red_jungle = list(x for x in red_datas if x['position']=='JUNGLE')[0]
        red_middle = list(x for x in red_datas if x['position']=='MIDDLE')[0]
        red_bottom = list(x for x in red_datas if x['position']=='BOTTOM')[0]
        red_utility = list(x for x in red_datas if x['position']=='UTILITY')[0]
                
        # 데이터 전송
        context = {
            'name' : myid,
            'blue_datas' : blue_datas,
            'region' : my_region,
            'blue_top' : blue_top,
            'blue_jungle' : blue_jungle,
            'blue_middle' : blue_middle,
            'blue_bottom' : blue_bottom,
            'blue_utility' : blue_utility,
            'red_top' : red_top,
            'red_jungle' : red_jungle,
            'red_middle' : red_middle,
            'red_bottom' : red_bottom,
            'red_utility' : red_utility,
        }
        
        return HttpResponse(template.render(context, request))
    except:
        context = {
            'error':'진행중 게임이 없습니다.',
            'name' : myid,
            'region' : my_region,
        }
        return HttpResponse(template.render(context, request))
