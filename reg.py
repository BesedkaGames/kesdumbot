from core import *
import telebot
import telebot.types as tbtypes

import propreg as pr

START_MESSAGE = "Добро пожаловать в бот для голосования в КэсДуму. Для доступа к регистрации на выборы выберите любую кнопку из представленных ниже"
START_MESSAGE_AFTER = "Добро пожаловать в бот для голосования в КэсДуму. Для регистрации сохраните себе следующий криптокод: "
START_MESSAGE_REG = "Добро пожаловать в бот для голосования в КэсДуму. Благодарим за использование нашего бота"
@bot.message_handler(commands=["start","prereg"],chat_types=["private"])
def start_message(message):
    username = f"@{message.from_user.username}"
    user_id = f"{message.from_user.id}"
    print(f"USERNAME: {username}\nUSERID: {user_id}\n")
    if message.from_user.id in pr.users.keys():
        bot.send_message(message.chat.id, "Вы уже прошли идентификацию. Для регистрации введите /reg")
        return
    user = {
        "id": user_id,
        "username": username,
        "start_message_id": message.id,
        
        "is_created": False,
        
        "prereg_datetime": pr.time_convert(message.date),
        
        "activities_count": 1,
        "cbcheck": None,
        "unique": 0.0,
        "bot_analysis": not "-" in user_id,
        "cryptokey": None,
        
        "registration_datetime": None,
        "voteabilty": False,
        
        "wait_bul": False,
        "vote_id": None,
        "vote_datetime": None,
        "vote_option_name": None
    }
    pr.users[message.from_user.id] = user
    pr.upload_voters()
    
    print(f"USERNAME: {username} \n ID:{user_id} \n")
    markup = tbtypes.InlineKeyboardMarkup(row_width=3)
    markup.add(*[
        tbtypes.InlineKeyboardButton(" ", callback_data=f"cbcheck:{i}") for i in range(1,10)
    ])
    bot.send_message(
        message.chat.id,
        START_MESSAGE,
        reply_markup=markup,
    )
    pr.upload_voters()

@bot.callback_query_handler(func=lambda call: call.data.startswith("cbcheck:"))
def cb_check(call):
    answer = int(call.data.split(":")[1])

    pr.users[call.message.chat.id]["cbcheck"] = answer
    pr.cbcheck_stat[answer] += 1
    pr.cbcheck_stat[-1] += 1
    cryptokey = pr.crypto_gen(call.message.chat.id)
    pr.users[call.message.chat.id]["cryptokey"] = cryptokey
    pr.users[call.message.chat.id]["unique"] = pr.unique_check(answer)
    bot.edit_message_text(
        START_MESSAGE_AFTER+cryptokey,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
    )
    bot.send_message(call.message.chat.id, "Спасибо. Теперь сохраните код выше, а затем пропишите /reg")
    pr.activities_update(call.message.chat.id)
    pr.upload_voters()
    
@bot.message_handler(commands=["reg", "registration", "r"], chat_types=["private"])
def registration(message):
    if not pr.REG_PROCESS:
        bot.send_message(message.chat.id, "Регистрация ещё не открыта, после открытия регистрации введите команду /reg")
    if pr.users[message.from_user.id]["cbcheck"] == None:
        bot.send_message(message.chat.id, "Сначала нажмите одну из кнопок выше")
        return
    elif pr.users[message.from_user.id]["registration_datetime"] != None:
        bot.send_message(message.chat.id, "Вы уже зарегистрированы в качестве избирателя")
        return
    if not pr.REG_PROCESS:
        bot.send_message(message.chat.id, "Регистрация ещё не началась, после открытия регистрации вновь пропишите /start или /prereg")
        return
    pr.users[message.from_user.id]["voteability"] = True
    pr.users[message.from_user.id]["registration_datetime"] = pr.time_convert(message.date)
    pr.activities_update(message.from_user.id)
    bot.send_message(message.chat.id, "ВЫ ЗАРЕГИСТРИРОВАНЫ В КАЧЕСТВЕ ИЗБИРАТЕЛЯ")
    pr.upload_voters()
    if pr.VOTE_PROCESS:
        bot.send_message(message.chat.id, "Голосование уже открыто, пропишите /vote для получения бюллетеня")
    from spectators import spect_reg_note
    spect_reg_note(message.from_user.id)
    