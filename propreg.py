from core import *

KESLI_ID = 5828596306
BOTADMIN_ID = 5569778383
registered_voters = 0

users: dict[int,dict] = {}
spectators: list[int] = []

cbcheck_stat = {i:0 for i in range(1, 10)}
cbcheck_stat[-1] = 0

REG_PROCESS = False
VOTE_PROCESS = False

from datetime import datetime, timezone, timedelta
def time_convert(time) -> str:
    unix_time = time
    utc_date = datetime.fromtimestamp(unix_time, tz=timezone.utc)
    local_tz = timezone(timedelta(hours=3))
    local_date = utc_date.astimezone(local_tz)
    formatted_time = local_date.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time

from json import dump, load
def upload_voters():
    return
    global users
    with open(f"users/voters.json", "w", encoding="UTF-8") as f:
        dump(users, f, indent=4, ensure_ascii=False)
        
def download_voters():
    return
    global users
    with open(f"users/voters.json", "r", encoding="UTF-8") as f:
        users = {int(k): v for k, v in load(f).items()}

def upload_spectators():
    return
    global spectators
    with open(f"users/spectators.json", "w", encoding="UTF-8") as f:
        dump(spectators, f, indent=4, ensure_ascii=False)

def download_spectators():
    return
    global spectators
    with open(f"users/spectators.json", "r", encoding="UTF-8") as f:
        spectators = [int(usid) for usid in load(f)]
        
download_voters()
download_spectators()
        
def crypto_gen(id: str):
    key = ""
    numbers = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    hard = len(numbers)
    number = int(id)
    while number > 0: 
        key = f"{numbers[number % hard]}" + key
        number //= hard
    return key

def uncrypt_key(key: str):
    numbers = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    hard = len(numbers)
    usid = 0
    for numb in range(len(key)):
        n = key[numb]
        usid += numbers.find(n) * hard**(len(key)-1-numb)
    return usid

def unique_check(answer: int) -> float:
    if len(users) < 5:
        return 100
    unique = 100.0 - 100.0*(cbcheck_stat[answer]/cbcheck_stat[-1]-1.0/9)
    return float(round(unique, 2))

def activities_update(user_id):
    users[user_id]["activities_count"] += 1
    upload_voters()
    
def global_message(message_text):
    for user in users.keys():
        bot.send_message(user, message_text)
        
def global_spectators_mes(message_text):
    for id in spectators:
        bot.send_message(id, message_text)
        
def global_spectator_pict(picture, message_text):
    for id in spectators:
        picture = open(f"{picture}","rb")
        bot.send_photo(id, picture, message_text)
        
def global_picture(picture, message_text):
    for user in users.keys():
        bot.send_photo(user, picture, message_text)