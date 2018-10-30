import os
from telegram.ext import Updater

TOKEN = "745005265:AAEoWaJnC9RukFHtESunTO2jYIw-Vzca1kI"
PORT = int(os.environ.get('PORT','5000'))
updater = Updater(TOKEN)
updater.start_webhook(listen="0.0.0.0",
                    port = PORT,
                    url_path=TOKEN)
updater.bot.set_webhook("https://whispering-forest-84298.herokuapp.com/"+TOKEN)
updater.idle()