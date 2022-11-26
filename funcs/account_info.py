
from riotwatcher import LolWatcher, ApiError

from lolstatyong.settings import RIOT_API_KEY
api_key = RIOT_API_KEY
watcher = LolWatcher(api_key)
my_region = 'kr'
