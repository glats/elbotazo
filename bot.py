from webbrowser import get
from attr import s
import telebot
import requests
from bs4 import BeautifulSoup
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import secrets

#id de T E S T I N G grupo 
c_id = secrets.c_id
m_id = secrets.m_id

#Scheduler instantiate
sched = BlockingScheduler()

#la parte del bot

bot = telebot.TeleBot(secrets.TELEGRAM_TOKEN)

#get hora
def gettime():
    now = datetime.datetime.now()
    return now.strftime("%H:%M")

#get fecha
def getdate():
    now = datetime.datetime.now()
    return now.strftime("%d/%m/%Y")

#USDCLP
def getusd():
    url = 'https://www.xe.com/es/currencyconverter/convert/?Amount=1&From=USD&To=CLP'
    page = requests.get(url)
    soup = BeautifulSoup (page.content , 'html.parser')
    algo = soup.find_all('p' , class_='result__BigRate-sc-1bsijpp-1 iGrAod')
    valor = list()
    for i in algo:
        valor.append(i.text)

    separado = valor.pop(0)
    separado=separado.split()
    separado=separado.pop(0)
    separado=list(separado)
    separado[3]="."
    separado=''.join(separado)
    separado=int(float(separado))
    separado=round(separado)
    return separado
    
#BTCUSD
def getbtcusd():
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    data = response.json()
    return data['bpi']['USD']['rate']


#add start command
@bot.message_handler(commands=['ids'])
def send_welcome(message):
    print(message.chat.id)
    print(message.id)
    #bot.send_message(message.chat.id, "MODIFICAR")


@sched.scheduled_job('interval',id='send_welcome', minutes = 1)
def send_welcome():
    bot.edit_message_text(
        chat_id=c_id, 
        text="Precio del dolar: $" + 
        str(getusd()) + 
        "\nPrecio del Bitcoin: $" + 
        str(getbtcusd()) + 
        "\n\n" + 
        "Ultima actualizacion: " + 
        str(gettime()) + 
        " | " + 
        str(getdate()), 
        message_id=m_id)        



#start schedule / bot
sched.start()


#initialize the bot
#bot.polling()







