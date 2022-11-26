from pprint import pprint
from funcs.account_info import *

myid = 'cuzz'
me = watcher.summoner.by_name(my_region, myid)
my_ranked_stats = watcher.league.by_summoner(my_region, me['id'])

my_solo_stats = list(filter(lambda my_solo_stats: my_solo_stats['queueType'] =='RANKED_SOLO_5x5' , my_ranked_stats)) 

my_flex_stats = list(filter(lambda my_flex_stats: my_flex_stats['queueType'] =='RANKED_FLEX_SR' , my_ranked_stats)) 
if my_solo_stats != []:
    my_solo_tier = f"{my_solo_stats[0]['tier']}{my_solo_stats[0]['rank']} {my_solo_stats[0]['leaguePoints']}"
    my_solo_winlose = f"{my_solo_stats[0]['wins']}승 {my_solo_stats[0]['losses']}패 ({my_solo_stats[0]['wins']/(my_solo_stats[0]['wins']+my_solo_stats[0]['losses'])*100:.2f}%) "
else:
    my_solo_tier = '솔로랭크 전적없음'
    
    
if my_flex_stats !=[]:
    my_flex_tier = f"{my_flex_stats[0]['tier']}{my_flex_stats[0]['rank']} {my_flex_stats[0]['leaguePoints']}"
    my_flex_winlose = f"{my_flex_stats[0]['wins']}승 {my_flex_stats[0]['losses']}패 ({my_flex_stats[0]['wins']/(my_flex_stats[0]['wins']+my_flex_stats[0]['losses'])*100:.2f}%) "
else:
    my_flex_tier = '자유랭크 전적없음'

context = {
    'my_solo_tier':my_solo_tier,
    'my_flex_tier':my_flex_tier,
    'my_solo_winlose':my_solo_winlose,
    'my_flex_winlose':my_flex_winlose,
}
pprint(my_solo_tier)