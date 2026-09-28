import telebot
from core import *
import propreg as pr
from parties import generate_voting_results

@bot.message_handler(commands=["startreg"])
def start_reg(message):
    if message.from_user.id not in [pr.KESLI_ID, pr.BOTADMIN_ID]:
        bot.send_message(message.chat.id, "Вы не обладаете полномочиями для данной команды")
        return
    if not pr.REG_PROCESS:
        pr.REG_PROCESS = True
        bot.send_message(message.chat.id, "Вы открыли регистрацию")
        pr.global_message("РЕГИСТРАЦИЯ ИЗБИРАТЕЛЕЙ ОТКРЫТА.\nВВЕДИТЕ /reg для регистрации")
        
@bot.message_handler(commands=["stopreg"])
def stop_reg(message):
    if message.from_user.id not in [pr.KESLI_ID, pr.BOTADMIN_ID]:
        bot.send_message(message.chat.id, "Вы не обладаете полномочиями для данной команды")
        return
    if pr.REG_PROCESS:
        pr.REG_PROCESS = False
        bot.send_message(message.chat.id, "Вы закрыли регистрацию")
        pr.global_message("РЕГИСТРАЦИЯ ИЗБИРАТЕЛЕЙ ОКОНЧЕНА. ЖДИТЕ ВЫБОРОВ")

@bot.message_handler(commands=["startvote"])
def start_vote(message):
    if message.from_user.id not in [pr.KESLI_ID, pr.BOTADMIN_ID]:
        bot.send_message(message.chat.id, "Вы не обладаете полномочиями для данной команды")
        return
    if not pr.VOTE_PROCESS:
        pr.VOTE_PROCESS = True
        bot.send_message(message.chat.id, "Вы открыли голосование")
        pr.global_message("ВЫБОРЫ ОБЪЯВЛЯЮТСЯ ОТКРЫТЫМИ. НАПИШИТЕ КОМАНДУ /vote ДЛЯ ПОЛУЧЕНИЯ БЮЛЛЕТЕНЯ\nВВЕДИТЕ /parties ДЛЯ ПОЛУЧЕНИЯ ИНФОРМАЦИИ О ПАРТИЯХ")
        
@bot.message_handler(commands=["stopvote"])
def stop_vote(message):
    if message.from_user.id not in [pr.KESLI_ID, pr.BOTADMIN_ID]:
        bot.send_message(message.chat.id, "Вы не обладаете полномочиями для данной команды")
        return
    if pr.VOTE_PROCESS:
        pr.VOTE_PROCESS = False
        bot.send_message(message.chat.id, "Вы закрыли голосование")
        pr.global_message(f"ВЫБОРЫ ОБЪЯВЛЯЮТСЯ ОКОНЧЕННЫМИ\nПРЕДВАРИТЕЛЬНЫЕ РЕЗУЛЬТАТЫ:\n{generate_voting_results()}")