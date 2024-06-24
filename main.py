import telebot
from telebot.types import Message as mes
from telebot.types import InlineKeyboardMarkup as ikm
from telebot.types import InlineKeyboardButton as ikb
import time
import s_taper as s
from s_taper.consts import *
import token

bot = telebot.TeleBot(token.TOKEN)

db_table1 = {'user_id':INT+KEY,'clicks':INT}
connect1 = s.Taper('db1','db.db').create_table(db_table1)

@bot.message_handler(['tim'])
def tim(message:mes):
    bot.send_message(message.chat.id, message.text)
    try:
        time.sleep(int(message.text.split()[1]))
        bot.send_message(message.chat.id, f"время прошло")
    except:
        bot.send_message(message.chat.id, f"ошибка")

@bot.message_handler(['start'])
def start(message:mes):
    kb = ikm()
    kb.row(ikb('🐹', callback_data=f'click'))
    bot.send_message(message.chat.id, f"тапай", reply_markup=kb)

@bot.callback_query_handler(func = lambda call:True)
def callback(call: telebot.types.CallbackQuery):
    if call.data.startswith('click'):
        try:
            connect1.write((call.message.chat.id,connect1.read('user_id',call.message.chat.id)[1]+1))
        except:
            connect1.write((call.message.chat.id,1))

@bot.message_handler(['check'])
def check(message:mes):
    try:
        clck = connect1.read('user_id', message.chat.id)
        bot.send_message(message.chat.id,clck[1])
    except:
        connect1.write((message.chat.id, 0))

bot.infinity_polling()