import speech_recognition as sr
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from pydub import AudioSegment
from pydub.playback import play
import os, pyautogui, send2trash
from time import sleep
from fuzzywuzzy import fuzz
from commands import *
import webbrowser as web
import customtkinter as ctk

#Звук
def adjust_volume():
    # Ваш код для управления громкостью здесь
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevel(-28.0, None)

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
    threshold = 75
    if max_ratio >= threshold:
        return matched_command
    else:
        return None

# Функция для воспроизведения звука
def play_sound(file_path):
    sound = AudioSegment.from_file(file_path)
    play(sound)

#Команды
commands_dict = {
'hi': hi,
'volume': volume,
'bye': bye,
'taskmgr': taskmgr,
'switch_language': switch_language,
'youtube': youtube,
'explorer': explorer,
'hide_windows': hide_windows,
'google': google,
'thank_you': thank_you,
'translator': translator,
'off_PC': off_PC,
'full_screen': full_screen,
'kill_process': kill_process,
'vscode': vscode
}
#Старт
def button_start():

    #Приветствие
    play_sound('Jarvis Sound Pack от Jarvis Desktop\Джарвис - приветствие.wav')
    # Основной цикл программы
    while True:

        command = recognize_speech()

        # Сопоставляем введённую команду с ключевыми словами
        matched_commands = {key: match_command(command, value) for key, value in commands_dict.items()}
        #Прощание
        if matched_commands['bye']:
            play_sound('Jarvis Sound Pack от Jarvis Desktop\Отключаю питание.wav')
            wait_for_wake_word()  # Ждем ключевое слово для активации
        #Громкость
        elif matched_commands['volume']:
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
        #
        elif matched_commands['vscode']:
            play_sound('Jarvis Sound Pack от Jarvis Desktop\Мы работаем над проектом сэр 2.wav')
            os.startfile(r'C:\Users\user\AppData\Local\Programs\Microsoft VS Code\Code.exe')
            sleep(1)
            play_sound('Jarvis Sound Pack от Jarvis Desktop\Мы подключены и готовы.wav')
#Тема
def change_theme(values):
    if values == 'Dark':
        ctk.set_appearance_mode('dark')
    elif values == 'Light':
        ctk.set_appearance_mode('light')
#Приближение
def change_scaling(values):
    if values == '100%':
        ctk.set_widget_scaling(1)
    elif values == '150%':
        ctk.set_widget_scaling(1.5)
#Интерфес
root = ctk.CTk()
root.title('Jarvis')
root.geometry('500x500')
root.resizable(0, 0)
ctk.set_widget_scaling(1.5)
#Tabview
tabview = ctk.CTkTabview(root)
tabview.pack()
tabview.add('Jarvis')
tabview.add('Settings')
tabview.add('Commands')
#Label
label = ctk.CTkLabel(tabview.tab('Settings'), text='Тема')
label.pack(pady=12, padx=10)
text = 'Громкость на 15, диспетчер задач, смена языка, ютуб, проводник'\
',сверни окна, гугл, спасибо, переводчик, выключать ПК, на весь экран, закрывать прогу, Vscode'
#Label_Commands
label = ctk.CTkLabel(tabview.tab('Commands'), font=('Arial', 18), wraplength=200, text=text)
label.pack(pady=12, padx=10)
#Button
button = ctk.CTkButton(tabview.tab('Jarvis'), text='Запуск', command=button_start, corner_radius=32)
button.place(relx=0.5, rely=0.5, anchor='center')
#Combobox
combobox = ctk.CTkComboBox(tabview.tab('Settings'), values=['Dark', 'Light'], command=change_theme)
combobox.pack(pady=12, padx=10)
#Combobox2
combobox2 = ctk.CTkComboBox(tabview.tab('Settings'), values=['150%', '100%'], command=change_scaling)
combobox2.pack(pady=12, padx=10)
root.mainloop()