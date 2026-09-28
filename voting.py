from core import *
from parties import *
from bulletenpars import *
import propreg as pr
import telebot.types as tbtypes

import os

VOTES_DIR = 'votes/'

@bot.message_handler(commands=['vote'],chat_types=['private'])
def vote_out(message):
    if not pr.VOTE_PROCESS:
        bot.send_message(message.chat.id, 'Голосование ещё не началось, дождитесь начала голосования')
        return
    bulleten = open('bulleten.png', 'rb')
    bot.send_photo(message.chat.id, bulleten,'Скачайте изображение\n В ЛЮБОМ фоторедакторе поставьте ЛЮБОЙ значок в квадрате партии, за которую хотите проголосовать\nПостарайтесь немножко аккуратнее\nОтправьте заполненную бюллетень обратно боту')
    pr.users[message.from_user.id]['wait_bul'] = True
    upload_voters()
    
@bot.message_handler(content_types=['photo'],chat_types=['private'])
def vote_in(message):
    if not pr.users[message.from_user.id]['wait_bul']:
        bot.send_message(message.chat.id, "Вы не можете проголосовать, пропишите /vote для получения заверенного бюллетеня")
        return
    if not pr.users[message.from_user.id]['vote_datetime'] == None:
        bot.send_message(message.chat.id, "Вы уже проголосовали. Дожидайтесь результатов")
        return
    pr.users[message.from_user.id]['vote_datetime'] = pr.time_convert(message.date)
    photo_info = message.photo[-1]
    file_id = photo_info.file_id
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path
    downloaded_file = bot.download_file(file_path)
    with open(VOTES_DIR+f'{message.from_user.id}.png', 'wb') as new_file:
        new_file.write(downloaded_file)
    parsvote(message.from_user.id, VOTES_DIR+f'{message.from_user.id}.png')
    bot.send_message(message.chat.id, 'Ваш голос засчитан. Спасибо за участие в выборах в КэсДуму')
    pr.upload_voters()
    from spectators import spect_vote_note
    spect_vote_note(message.from_user.id)
    
@bot.message_handler(commands=['parties'], chat_types=['private'])
def parties_infos(message):
    markup = tbtypes.InlineKeyboardMarkup(row_width=1)
    markup.add(*[
        tbtypes.InlineKeyboardButton(f"{PARTIES[list(PARTIES.keys())[i]]}", callback_data=f"cbpart:{i}") for i in range(len(PARTIES)-1)
    ])
    bot.send_message(
        message.chat.id,
        'ИНФОРМАЦИЯ О ПАРТИЯХ\nДля получения краткой информации о партии, нажмите на соответствующую кнопку ниже',
        reply_markup=markup,
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("cbpart:"))
def get_party_info(call):
    party_cb = int(call.data.split(":")[1])
    bot.send_message(call.chat.id, f'{generate_party_info(list(PARTIES.keys())[party_cb])}')