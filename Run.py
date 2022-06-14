import telebot
from telebot import types
import requests

bot = telebot.TeleBot("", parse_mode=None)
bot.remove_webhook()

@bot.message_handler(commands=['chekfind'])
def sendindication(message):
    msg = bot.send_message(message.chat.id, 'Пришлите регистрационный номер ФН') 
    bot.register_next_step_handler(msg, dfn)
def dfn(message):
    fn = message.text
    msg = bot.send_message(message.chat.id, 'Пришлите номер фискального документа')
    bot.register_next_step_handler(msg, ddocNum, fn)
def ddocNum(message,fn):
    docNum = message.text
    msg = bot.send_message(message.chat.id, 'Пришлите фискальный признак документа')
    bot.register_next_step_handler(msg, dfiscalSign, fn, docNum)
def dfiscalSign(message, fn, docNum):
    fiscalSign = message.text
    msg = bot.send_message(message.chat.id, 'Пришлите дата документа в формате YYYY-MM-DDThh:mm:ss')
    bot.register_next_step_handler(msg, ddocDate, fn, docNum, fiscalSign)
def ddocDate(message, fn, docNum, fiscalSign):
    docDate = message.text
    payload = {'sid': ''} 
    bot.send_message(message.chat.id, 'https://api.sbis.ru/ofd/v1/storage/'+fn+'/doc?docNum='+docNum+'&fiscalSign='+fiscalSign+'&docDate='+docDate)
    #r = requests.get('https://api.sbis.ru/ofd/v1/storage/'+fn+'/doc?docNum='+docNum+'&fiscalSign='+fiscalSign+'&docDate='+docDate, params=payload)
    #bot.send_message(message.chat.id, r.text)
    

if __name__ == '__main__':
    bot.infinity_polling()