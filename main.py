#Импорты
import customtkinter as ctk
from functions import button_start, change_theme, change_scaling

if __name__ == '__main__':
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
