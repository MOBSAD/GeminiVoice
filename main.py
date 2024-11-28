import gtts
import speech_recognition as sr
import google.generativeai as genai
import dotenv
import os
from sys import platform

# Ignorar warnings
os.environ['PYTHONWARNINGS'] = 'ignore'
os.environ['ALSA_CARD'] = 'default'

# Configuração da chave de API
genai.configure(api_key=dotenv.get_key(".env", "API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Inicializar o reconhecedor
reconhecedor = sr.Recognizer()

# Usar o microfone como fonte
with sr.Microphone(device_index=0) as fonte:
    print("Ajustando para o ambiente...")
    
    # Ajuste maior para o ambiente
    reconhecedor.adjust_for_ambient_noise(fonte, duration=5)  # Ajustando para 5 segundos
    print("Preparando para ouvir...")

    try:
        # Aumentando o timeout e phrase_time_limit
        audio = reconhecedor.listen(fonte, timeout=15, phrase_time_limit=15)  # Aumento para 15 segundos
        print("Gravando...")

        texto = reconhecedor.recognize_google(audio, language="pt-BR")
        print("Texto capturado:", texto)

        # Construir prompt para o modelo
        newtext = "Responda a isso em português do Brasil da melhor maneira possível: " + texto

        # Resposta do modelo
        response = model.generate_content(newtext)
        print(response.text)

        # Gerar a voz com gTTS
        tts = gtts.gTTS(response.text, lang='pt', slow=False)
        tts.save("resposta.mp3")  # Salva o áudio gerado como um arquivo .mp3

        # Reproduzir a resposta por meio do os
        if platform == 'linux':
            os.system("mpg123 resposta.mp3")
        elif platform == 'win32':
            os.system("start /wait mpg123 resposta.mp3")  # Reproduzir o áudio com o mpg123 (necessário instalar mpg123)
        elif platform == 'darwin':
            os.system("open -a mpg123 resposta.mp3")  # Reproduzir o áudio com o mpg123 (necessário instalar mpg123)

    except sr.UnknownValueError:
        print("Desculpe, não entendi o que você disse.")
    except sr.RequestError as e:
        print(f"Erro ao acessar o serviço: {e}")
    except sr.WaitTimeoutError:
        print("Tempo de espera excedido! Não ouvi nada.")