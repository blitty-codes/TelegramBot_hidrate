from random import randint
from apscheduler.schedulers.background import BackgroundScheduler


greeting_list = [
    "Buenos das",
    "Adios",
    "Igual el metro te va mal hoy",
    "Haz lo que quieras",
    "¿Estas en clase? ¡No me hables!",
    "Necesito un día de descanso :c"
]

GIFs_list = [
    "https://giphy.com/clips/buzzfeed-buzzfeed-celeb-gray-reads-thirst-tweets-AYjntbKHpt5UeVHJYl",
    "https://media.giphy.com/media/da5BxvjlRRP9soY36k/giphy.gif",
    "https://media.giphy.com/media/xThuWpnG8UOeTmFVmg/giphy.gif",
    "https://media.giphy.com/media/EVFibcFzzYdecY0oux/giphy.gif",
    "https://media.giphy.com/media/ddrVX7zLLuHTcyCAOB/giphy.gif",
    "https://media.giphy.com/media/MWZpATDcg2wTVPGekK/giphy.gif",
    "https://media.giphy.com/media/kbp9RJimFwdatP6Imw/giphy.gif"
]


def get_random_greeting():
    return greeting_list[randint(0, len(greeting_list))]


def get_random_gif():
    return GIFs_list[randint(0, len(GIFs_list))]


def generate_timer(hour, minute, id, callback):
    # Se crea un objeto que se ejecutará en segundo plano, para que el timer no bloquee procesos
    scheduler = BackgroundScheduler()

    print(f"Se ha creado un temporizador de {hour}h y {minute}min.")

    # cron es una herramienta que se usa para temporizadores. Existe una web que te ayuda y facilita a
    # saber como usar cron.
    #   - cron helper - https://crontab.guru/#*/10_*/1_*_*_*
    hour = '*' if hour == 0 else f'*/{hour}'
    minute = '*' if minute == 0 else f'*/{minute}'

    # Se crea un job, éste es el encargado de que cada hora y minuto se llame a la función callback, que está en
    # la clase Bot
    job = scheduler.add_job(callback, trigger="cron", hour=hour,  minute=minute, args=(id,))
    scheduler.start()

    return job
