from datetime import datetime, date
import requests
import speech_recognition as sr
import webbrowser
import pyttsx3
import pyautogui
import time
from newsapi import NewsApiClient
import random

recognizer = sr.Recognizer()
engine = pyttsx3.init()
is_playing_music = False

my_api_key = "6b89ef1251ab4c3193785df7957e9840"  
newsapi = NewsApiClient(api_key=my_api_key)

def inicio_asistente():
    mensaje = 'Hola, mi nombre es Aura tu asistente personal, por favor dime ¿Cómo te puedo ayudar?'
    talk(mensaje)

def talk(text):
    print(f"Asistente dice: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        comando = recognizer.recognize_google(audio, language='es-ES')
        print(f"Comando reconocido: {comando}")
        return comando.lower()
    except sr.UnknownValueError:
        print("No se ha reconocido el comando")
        talk("No entendí lo que dijiste, por favor intenta de nuevo.")
        return None
    except sr.RequestError as e:
        print(f"Error de conexión: {e}")
        talk(f"Error de conexión: {e}")
        return None

def consultar_clima(ciudad):
    api_key = "b85fe6c25d57023a2e6fb34763631fb6"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric&lang=es"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp = round(data["main"]["temp"], 1)
        feels_like = round(data["main"]["feels_like"], 1)
        wind_speed = data["wind"]["speed"]
        latitude = data["coord"]["lat"]
        longitude = data["coord"]["lon"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]

        talk(f"El clima en {ciudad} es el siguiente:")
        talk(f"La temperatura es de {temp} grados Celsius, con una sensación térmica de {feels_like} grados Celsius.")
        talk(f"La velocidad del viento es de {wind_speed} metros por segundo.")
        talk(f"La latitud es {latitude} y la longitud es {longitude}.")
        talk(f"La humedad es del {humidity}%.")
        talk(f"Descripción del clima: {description}.")
    else:
        talk("No pude obtener la información del clima para esa ciudad. Por favor, intenta nuevamente.")

def consultar_noticia():
    try:
        talk("Te escucho, ¿sobre qué tema quieres noticias?")
        rec = listen() 

        if not rec:
            talk("No entendí lo que dijiste, por favor intenta de nuevo.")
            return

        talk(f"Buscando noticias sobre {rec}.")
        data = newsapi.get_everything(q=rec, language="es", page_size=5)
        articles = data.get("articles", [])

        if articles:
            for i, article in enumerate(articles):
                talk(f"Noticia {i+1}: {article['title']}")

            while True:
                talk("¿Quieres escuchar la primera, segunda, tercera, cuarta o quinta noticia?")
                rec = listen()

                if not rec:
                    continue

                if "primera" in rec and len(articles) > 0:
                    talk(articles[0].get("content", "No hay más detalles disponibles."))
                    break
                elif "segunda" in rec and len(articles) > 1:
                    talk(articles[1].get("content", "No hay más detalles disponibles."))
                    break
                elif "tercera" in rec and len(articles) > 2:
                    talk(articles[2].get("content", "No hay más detalles disponibles."))
                    break
                elif "cuarta" in rec and len(articles) > 3:
                    talk(articles[3].get("content", "No hay más detalles disponibles."))
                    break
                elif "quinta" in rec and len(articles) > 4:
                    talk(articles[4].get("content", "No hay más detalles disponibles."))
                    break
                else:
                    talk("No entendí tu respuesta o la noticia solicitada no está disponible.")
        else:
            talk(f"No encontré noticias sobre {rec} en este momento.")

    except Exception as e:
        print(f"Error al consultar la API: {e}")
        talk("Hubo un problema al obtener las noticias.")

def jugar_piedra_papel_tijera():
    opciones = ["piedra", "papel", "tijera"]
    
    talk("Vamos a jugar piedra, papel o tijera. ¿Cuál es tu elección?")
    jugador = listen()
    
    if jugador not in opciones:
        talk("No entendí tu elección. Por favor elige entre piedra, papel o tijera.")
        return

    asistente = random.choice(opciones)
    talk(f"Yo elijo {asistente}.")

    # Determinación del ganador
    if jugador == asistente:
        talk(f"Ambos elegimos {jugador}. Es un empate.")
    elif (jugador == "piedra" and asistente == "tijera") or \
         (jugador == "papel" and asistente == "piedra") or \
         (jugador == "tijera" and asistente == "papel"):
        talk("¡Ganaste! Felicidades.")
    else:
        talk("Yo gano. Mejor suerte la próxima vez.")

def ejecutar_comando(comando):
    global is_playing_music
    if 'amazon' in comando:
        talk('¿Qué quieres comprar en Amazon?')
        nuevo_comando = listen()
        if nuevo_comando:
            webbrowser.open(f'https://www.amazon.es/s?k={nuevo_comando}')

    elif 'youtube' in comando:
        talk('¿Qué quieres buscar en YouTube?')
        nuevo_comando = listen()
        if nuevo_comando:
            webbrowser.open(f"https://www.youtube.com/results?search_query={nuevo_comando}")
            time.sleep(5)
            pyautogui.press('down')
            pyautogui.press('up')
            pyautogui.press('enter')
            is_playing_music = True
            talk("Reproduciendo tu video.")

    elif 'google' in comando:
        talk('¿Qué quieres buscar en Google?')
        nuevo_comando = listen()
        if nuevo_comando:
            webbrowser.open(f'https://www.google.com/search?q={nuevo_comando}')
            time.sleep(5)
            pyautogui.press('down')
            pyautogui.press('enter')

    elif 'clima' in comando:
        talk('¿En qué ciudad quieres consultar el clima?')
        ciudad = listen()
        if ciudad:
            consultar_clima(ciudad)
    
    elif 'noticia' in comando:
        consultar_noticia()
    
    elif 'fecha' in comando:
        fecha = date.today()
        talk(f"La fecha de hoy es: {fecha}")
    
    elif 'hora' in comando:
        hora = datetime.now().strftime("%H:%M %p")
        talk(f"La hora actual es: {hora}")

    elif 'jugar' in comando or 'piedra papel o tijera' in comando:
        jugar_piedra_papel_tijera()
    
    elif 'cerrar' in comando:
        talk("Gracias, hasta pronto")
        exit()

def main():
    inicio_asistente()
    while True:
        comando = listen()
        if comando:
            ejecutar_comando(comando)

if __name__ == "__main__":
    main()
