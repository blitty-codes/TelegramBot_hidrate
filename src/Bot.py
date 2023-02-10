# Se importa la librería para conectarse y programar al bot.
import telebot
from apscheduler.schedulers.blocking import BlockingScheduler

# Se importa la función de utils
from .utils import get_random_greeting, generate_timer, get_random_gif


class Bot:
    def __init__(self, TOKEN):
        # Se pasa el token a la librería para poder realizar una conexión con el bot.
        self.bot = telebot.TeleBot(TOKEN)
        self.job = None

        # Se usan los handler de la librería, para que cuando llegue un comando, de los especificados
        # en los parámetros como texto, podamos hacer calgo. En este caso se usa una función
        # llamada self.welcome definida abajo
        self.welcome = self.bot.message_handler(commands=["start", "hola"])(self.welcome)

        self.water = self.bot.message_handler(commands=["agua"])(self.water)
        self.stop = self.bot.message_handler(commands=["stop"])(self.stop)
        self.help = self.bot.message_handler(commands=["help"])(self.help)

    # La función llama a otra función para obtener un elementos aleatorio de una lista y
    # así, llamar al método "send_message" que enviará un mensaje al chat que ha enviado ese comando.
    def welcome(self, message):
        self.bot.send_message(message.chat.id, get_random_greeting())

    # /agua <timepo> command
    def water(self, message):
        # print(type(message)) # te imprime el tipo de la variable
        # El tipo de message es "Message", cogemos el texto que ha mandado el usuario y sabemos que debería de separarse
        # el comando y el numero por un espacio: /agua 1. El número es en minutos, es decir, que 120 se traducirá en 2h
        text = message.text.split(' ')

        # Si el usuario ha puesto bien el comando, tendremos una lista con dos elementos
        # y para poder crear un nuevo temporizador, debemos de no tener ninguno activo
        if len(text) == 2 and self.job is None:
            # Se pasa al tipo entero (esta acción se la suele llamar castear)
            time = int(text[1])

            # Se sacan horas y minutos
            hours = time // 60
            minutes = time % 60

            self.bot.send_message(message.chat.id, f"Se ha creado un temporizador de {hours}h y {minutes}min.")

            # Se llama a la función generate_timer de utils para generar nuestro scheduler y job
            # que usará el callback (función que llama una función y se pasa por parámetro), que en este caso es
            # self._send_message. Esta función se llamará cada vez X horas e Y minutos
            self.job = generate_timer(hours, minutes, message.chat.id, self._send_message)
        else:
            self.bot.send_message(message.chat.id,
                                  "Lo siento, has hecho algo mal. Escriba \"/help\" para más información,")

    # /stop command
    def stop_timer(self, msg):
        # Si existe un temporizador, entonces podemos cancelarlo.
        if self.job is not None:
            self.job.remove()
            self.job = None
            self.bot.send_message(msg.chat.id, "Se ha cancelado el temporizador 💦")
            print(f"Se ha cancelado el temporizador,")
        else:
            self.bot.send_message(msg.chat.id, "No existe temporizador.")

    def _send_message(self, id):
        self.bot.send_message(id, "💦💦💦 Hora de beber agua 💦💦💦")

        # Y vamos a enviar también un GIF, porque si uwu
        self.bot.send_animation(id, get_random_gif())

    def help(self, msg):
        help_msg = '''
        Comandos:
        
        - /help : Proporciona información sobre los comandos del bot
        - /start u /hola : Te da un saludo caluroso
        - /agua <tiempo en minutos> : Genera un recordatorio para beber agua. Ej._ /agua 125 te recordará cada 1 hora y 5 minutos de que tienes que beber agua
        - /stop : Cancela el recordatorio
        
        
        Made by @blitty with love & fun.
        '''

        self.bot.send_animation(msg.chat.id, help_msg)

    # Se comunica y ejecuta el bot
    def run(self):
        print("[+] Bot is online.")
        self.bot.polling(none_stop=True)
