from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from firebase import firebase  
import os

firebases = firebase.FirebaseApplication('https://whattodo-7e167.firebaseio.com/', None)  

def start(bot, update):
    update.message.reply_text("Hi! Ini adalah bot buat nyimpen semua URL penting kamu biar gak ilang\nLangsung aja simpan!^^")

def listed(bot, update):
    idchat = update['message']['chat']['id']
    result = firebases.get('/'+str(idchat)+'/','')
    error = 'Kamu belum simpan link apapun :('
    print(result)
    if (result == None):
        update.message.reply_text(error)
    else:
        url = []
        cap = []
        send = 'Ini semua link kamu: \n'
        for i in result:
            cap.append(result[i]['caption'])
            url.append(result[i]['link'])
        for i in range(0,len(cap)):
            send += str(i+1) + " " + str(url[i]) + " " + str(cap[i]) + "\n" + "\n"
        if (len(cap) != 0):
            update.message.reply_text(send)
        else:
            update.message.reply_text(error)

# def convert_uppercase(bot, update):
#     print(update.message.text)
#     update.message.reply_text(update.message.text.upper())

def saveurl(bot, update):
    idchat = update['message']['chat']['id']
    text = update['message']['text']
    texts = text.split()
    cap = ''
    for i in range(1,len(texts)):
        cap += texts[i]+" "

    data = {
        'link':texts[0],
        'caption': cap.rstrip()
    }

    s = firebases.post('/'+str(idchat)+'/', data)
    if (s != ''):
        rep = 'URL "'+str(cap)+'"'+' sudah disimpan! Jangan lupa dibaca ya^^'
    else:
        rep = 'Maaf formatmu salah. Coba diulang kembali \n Format: URL <caption>'
    update.message.reply_text(rep)


def main():
    # Create Updater object and attach dispatcher to it
    # updater = Updater(token="745005265:AAEoWaJnC9RukFHtESunTO2jYIw-Vzca1kI")
    TOKEN = "745005265:AAEoWaJnC9RukFHtESunTO2jYIw-Vzca1kI"
    PORT = int(os.environ.get('PORT','5000'))
    updater = Updater(TOKEN)
    updater.start_webhook(listen="0.0.0.0",
                    port = PORT,
                    url_path=TOKEN)

    dispatcher = updater.dispatcher
    print("Bot started")

    # Add command handler to dispatcher
    start_handler = CommandHandler('start',start)
    list_handler = CommandHandler('list',listed)
    save_url = MessageHandler(Filters.text, saveurl)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(list_handler)
    dispatcher.add_handler(save_url)

    # Start the bot
    updater.bot.set_webhook("https://whispering-forest-84298.herokuapp.com/"+TOKEN)
    updater.idle()
    # updater.start_polling()

    # Run the bot until you press Ctrl-C
    # updater.idle()

if __name__ == '__main__':
    main()