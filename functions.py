import speech_recognition as sr
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from pydub import AudioSegment
from pydub.playback import play
import os, pyautogui
from time import sleep
from fuzzywuzzy import fuzz
import webbrowser as web
import customtkinter as ctk
import multiprocessing, json, threading

# Чтение команд из JSON файла
with open('commands.json', 'r', encoding='utf-8') as file:
    commands_data = json.load(file)

commands_dict = {command['trigger']: command['phrases'] for command in commands_data['commands']}

#Звук
def adjust_volume():
    # Ваш код для управления громкостью здесь
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevel(-28.0, None)

#Цикл
def process_commands():
    while True:
        command = recognize_speech()
        
        # Сопоставляем введённую команду с ключевыми словами
        matched_commands = {key: match_command(command, value) for key, value in commands_dict.items()}
        #Прощание
        if matched_commands['sleepj']:
            play_sound('Jarvis Sound Pack от Jarvis Desktop\Отключаю питание.wav')
            wait_for_wake_word()  # Ждем ключевое слово для активации
        #Громкость
        if matched_commands['volume']:
            play_sound('Jarvis Sound Pack от Jarvis Desktop\Загружаю сэр.wav')
            adjust_volume()
        #Диспетчер задач
        elif matched_commands['taskmgr']:
            play_sound('Jarvis Sound Pack от Jarvis Desktop\Есть.wav')
            os.system('taskmgr')
        #Смена языка
        elif matched_commands['switch_language']:
            play_sound('Jarvis Sound Pack от Jarvis Desktop\Загружаю сэр.wav')
            pyautogui.hotkey('alt', 'shift')
        #Ютуб
        elif matched_commands['youtube']:
            play_sound('Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav')
            web.open('https://www.youtube.com/')
        #Проводник
        elif matched_commands['explorer']:
            play_sound('Jarvis Sound Pack от Jarvis Desktop\Есть.wav')
            os.system('explorer.exe')
        #Свернуть окна
        elif matched_commands['hide_windows']:
            pyautogui.hotkey('win', 'd')
            play_sound('Jarvis Sound Pack от Jarvis Desktop\sound_jarvis-og_ok3.wav')
        #Гугл
        elif matched_commands['google']:
            play_sound('Jarvis Sound Pack от Jarvis Desktop\sound_jarvis-og_ok4.wav')
            web.open_new_tab('https://www.google.ru/?hl=ru')
        #Спасибо
        elif matched_commands['thank_you']:
            play_sound('Jarvis Sound Pack от Jarvis Desktop\К вашим услугам сэр.wav')
        #Переводчик
        elif matched_commands['translator']:
            play_sound('Jarvis Sound Pack от Jarvis Desktop\sound_jarvis-og_ok1.wav')
            web.open_new_tab('https://www.deepl.com/translator')        
        #Выключить ПК
        elif matched_commands['off_PC']:
            play_sound('Jarvis Sound Pack от Jarvis Desktop\sound_jarvis-og_ok1.wav')
            os.system('shutdown -s')        
        #На весь экран
        elif matched_commands['full_screen']:
            play_sound('Jarvis Sound Pack от Jarvis Desktop\Есть.wav')
            pyautogui.hotkey('winleft', 'up')        
        #Закрыть программу
        elif matched_commands['kill_process']:
            play_sound('Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav')
            pyautogui.hotkey('alt', 'f4')       
        #Vscode
        elif matched_commands['vscode']:
            play_sound('Jarvis Sound Pack от Jarvis Desktop\Мы работаем над проектом сэр 2.wav')
            os.startfile(r'C:\Users\user\AppData\Local\Programs\Microsoft VS Code\Code.exe')
            sleep(1)
            play_sound('Jarvis Sound Pack от Jarvis Desktop\Мы подключены и готовы.wav')

# Функция для ожидания ключевого слова 'джарвис' перед началом прослушивания
def wait_for_wake_word():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            audio = recognizer.listen(source)
            try:
                command = recognizer.recognize_google(audio, language='ru-RU').lower()
                matched_commands = {key: match_command(command, value) for key, value in commands_dict.items()}
                if matched_commands['hi']:
                    play_sound('Jarvis Sound Pack от Jarvis Desktop\Да сэр(второй).wav')
                    print('Джарвис активирован. Говорите команды...')
                    return  # Выход из цикла при обнаружении ключевого слова
            except sr.UnknownValueError:
                pass

# Функция для распознавания команд
def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print('Говорите что-нибудь...')
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio, language='ru-RU').lower()
        print('Вы сказали: ' + command)
        return command
    except sr.UnknownValueError:
        print('Извините, не могу понять команду')
        return ''
    except sr.RequestError:
        print('Проблема с подключением к сервису распознавания речи')
        return ''

# Функция для сравнения ввода пользователя с ключевыми словами
def match_command(user_input, commands):
    max_ratio = 0
    matched_command = ''

    for command in commands:
        similarity = fuzz.partial_ratio(user_input, command)
        if similarity > max_ratio:
            max_ratio = similarity
            matched_command = command

    # Определяем пороговое значение сходства (можно настроить)
    threshold = 80
    if max_ratio >= threshold:
        return matched_command
    else:
        return None

# Функция для воспроизведения звука
def play_sound(file_path):
    sound = AudioSegment.from_file(file_path)
    play(sound)

#Старт
def button_start():
    #Приветствие
    play_sound('Jarvis Sound Pack от Jarvis Desktop\Джарвис - приветствие.wav')
    process_threading()

def process_threading():
    thread = threading.Thread(target=process_commands)
    thread.start()

#Приближение
def change_scaling(values):
    if values == '100%':
        ctk.set_widget_scaling(1)
    elif values == '150%':
        ctk.set_widget_scaling(1.5)

#Тема
def change_theme(values):
    if values == 'Dark':
        ctk.set_appearance_mode('dark')
    elif values == 'Light':
        ctk.set_appearance_mode('light')

if __name__ == '__main__':
    recognition_process = multiprocessing.Process(target=recognize_speech)
    recognition_process.start()