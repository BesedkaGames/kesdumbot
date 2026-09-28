import telebot
from core import *
import propreg as pr

def spect_reg_note(usid):
    SPECTATOR_REG_MESSAGE = f"""☑ РЕГИСТРАЦИЯ НОВОГО ИЗБИРАТЕЛЯ №{len(pr.users)}
        ПОДТВЕРЖДЁННОСТЬ ЧЕЛОВЕКА: {"✔" if pr.users[usid]["bot_analysis"] else "✖"}
        УНИКАЛЬНОСТЬ ПОЛЬЗОВАТЕЛЯ: {pr.users[usid]["unique"]}%
        УНИКАЛЬНЫЙ КРИПТОКЛЮЧ: {pr.users[usid]["cryptokey"]}
        ДАТА ПЕРВИЧНОЙ РЕГИСТРАЦИИ: {pr.users[usid]["prereg_datetime"]}
        ДАТА РЕГИСТРАЦИИ: {pr.users[usid]["registration_datetime"]}
        #наблюдение
        #регистрация"""
    for spect in pr.spectators:
        bot.send_message(spect, SPECTATOR_REG_MESSAGE)
        
def spect_vote_note(usid):
    SPECTATOR_VOTE_MESSAGE = f"""☑ ОПУЩЕН ГОЛОС ЗА ПАРТИЮ «{pr.users[usid]["vote_option_name"]}»
        Криптоключ избирателя: {pr.users[usid]["cryptokey"]}
        #наблюдение
        #голос_{pr.users[usid]["vote_id"]+1}"""
    for spect in pr.spectators:
        bot.send_message(spect, SPECTATOR_VOTE_MESSAGE)

@bot.message_handler(commands=['spectate'],chat_types=['private'])
def spectate_application_submission(message):
    if message.from_user.id in pr.spectators:
        bot.send_message(message.from_user.id, 'Вы уже включены в списки наблюдателей, пропишите /spectator_info для получения дополнительной информации')
    bot.send_message(message.from_user.id, 'Отправлена заявка на наблюдение')
    bot.send_message(pr.BOTADMIN_ID, f'Заявка на наблюдение от {message.from_user.id} (Введите /add_spectator {message.from_user.id})')

@bot.message_handler(func=lambda m: '/add_spectator' in m.text)
def accept_spectate(message):
    com, user_id = str(message.text).split(' ')
    pr.spectators.append(int(user_id))
    bot.send_message(user_id, "Заявка на наблюдение принята, напишите команду /spectator_info для получения информации о порядке наблюдения")
    bot.send_message(message.chat.id, "Пользователь добавлен в наблюдатели")
    pr.upload_spectators()

SPECTATE_INFO = """НАБЛЮДЕНИЕ ЗА ВЫБОРАМИ
Наблюдатели - это пользователи, подавшие заявку на наблюдение, которые, помимо общедоступной информации о выборах, в реально времени будут получать также некоторые отчёты и уведомление о регистрации новых избирателей (включая обезличенные отчёты различных проверок данного наблюдателя для предупреждения вбросов, в том числе и вбросов со стороны проведения), во время самих выборов наблюдатели также будут получать в реальном времени обезличенные голоса с указанием только партии, в чью пользу был опущен голос."""
SPECTATOR_INFO = """ИНСТРУКЦИИ ДЛЯ НАБЛЮДАТЕЛЕЙ
Во время регистрации любого пользователя на выборы вам будет отправляться уведомление о регистрации, в котором не будет указано идентификационных данных, но будет указан уникальный криптоключ-идентификатор внутри системы, также в данном уведомлении будут представлены результаты всех многофакторных проверок пользователя, проведённых внутри бота. В случае подозрений вы можете обратиться к создателю данного бота, мне - @Rus_lan_ST, я прям вот обязан вам объяснить. Туда же обратитесь, если вам нужны дополнительные пояснения, я всё объясню как и что работает, если вам нужна будет помощь или пояснения.
Каждое сообщение с регистрацией будет отмечено двумя хэштэгами для удобного поиска: #нaблюдeниe и #рeгиcтрaция. С помощью поиска сообщений в чате вы, таким образом, сможете легко найти эти сообщения, помимо этого сможете узнать их число (тг сам считает каждое упоминание, в поиске нужно просто ввести #рeгиcтрaция)
Во время самих выборов вы также будете получать уведомления о голосах с фото бюллетеней, также в этом сообщении будет криптоключ, с помощью которого через поиск вы в случае чего сможете узнать, регистрировался ли пользователь в качестве избирателя. Также в сообщении будет два хэштэга: #нaблюдeниe и #гoлoc_|номер партии/варианта в бюллетени|}. Таким образом у вас в итоге будет полная база каждого голоса и вы сможете также пересчитать голоса за каждую партию через поиск сообщений в чате бота при вводе соответствующих хэштегов (не волнуйтесь насчёт хэштегов в данной инструкции, они не будут считаться в поиске)"""
@bot.message_handler(command=['spectator_info'])
def spectator_info(message):
    bot.send_message(message.chat.id, SPECTATE_INFO)
    if message.from_user.id not in pr.spectators:
        bot.send_message(message.chat.id, 'Чтобы подать заявку на наблюдение, введите команду /spectate')
        return
    bot.send_message(message.chat.id, SPECTATOR_INFO)
