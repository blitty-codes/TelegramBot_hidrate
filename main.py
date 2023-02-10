import os
from dotenv import load_dotenv
from src.Bot import Bot

if __name__ == '__main__':
    # se carga el fichero .env
    load_dotenv()

    # se recoge el valor de la clave BOT_TOKEN que hemos definido en .env
    # y lo guardamos en una variable BOT_TOKEN
    BOT_TOKEN = os.getenv('BOT_TOKEN')

    # se crea un objeto de la clase Bot, pasando el TOKEN
    bot = Bot(BOT_TOKEN)

    # Ejecutar el bot
    bot.run()
