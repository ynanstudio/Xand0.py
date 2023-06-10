#╔╗──╔╗╔═╗─╔╗╔═══╗╔═╗─╔╗     ╔═══╗╔════╗╔╗─╔╗╔═══╗╔══╗╔═══╗
#║╚╗╔╝║║║╚╗║║║╔═╗║║║╚╗║║     ║╔═╗║║╔╗╔╗║║║─║║╚╗╔╗║╚╣─╝║╔═╗║
#╚╗╚╝╔╝║╔╗╚╝║║║─║║║╔╗╚╝║     ║╚══╗╚╝║║╚╝║║─║║─║║║║─║║─║║─║║
#─╚╗╔╝─║║╚╗║║║╚═╝║║║╚╗║║     ╚══╗║──║║──║║─║║─║║║║─║║─║║─║║
#──║║──║║─║║║║╔═╗║║║─║║║     ║╚═╝║──║║──║╚═╝║╔╝╚╝║╔╣─╗║╚═╝║
#──╚╝──╚╝─╚═╝╚╝─╚╝╚╝─╚═╝     ╚═══╝──╚╝──╚═══╝╚═══╝╚══╝╚═══╝
# Copyright 2023 YNAN STUDIO

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import tkinter as tk#{
import tkinter.ttk as ttk
import tkinter.font as font
from tkinter import *#}UI библиотека(ГОВ%О)
from random import choice, randint#Рандом
from os import path#Чтобы найти расположение исполняемого файла
import pyglet#Для импорта шрифта
import json#Библиотека для сохранения статистики и настроек
from PIL import Image, ImageTk#Библиотека для картинок
from cryptography.fernet import Fernet#Библиотека для шифровки сохранения
import threading#Мульти поточность(ну типа)
from playsound import playsound #Для звука
#========================================================Класс для окна меню==================================================================
# Класс для главного меню
class Menu:
    # Значения по умолчанию для настроек
    setting_intboard = 3  # Меняет размер поля (только против друга) | default:3
    setting_stretgbot = 6  # Меняет силу бота | default:6
    setting_color = randint(1, 7)  # Меняет цвет интерфейса | default:randint(1, 7)
    script_dir = path.dirname(__file__)#Директория расположения файла запуска
    #шрифты
    pyglet.font.add_file(path.join(script_dir, 'fonts', 'main.otf'))#Добавляю шрифт Jolly Lodger Cyrillic(Нужно именно название шрифта)
    h1=30 #Большой заголовок | default:30
    h2=25 #Средний заголовок | default:25
    h3=20 #Меньше  заголовок | default:20
    h4=10 #Ещё меньше | default:10
    # Настройки для окна
    icon_path = path.join(script_dir, 'icon', 'app.ico')#Иконка приложения
    root = tk.Tk()#Создаем Главное окно приложения
    root.iconbitmap(icon_path)
    root.title("Крестики-нолики | Меню")#Название ГЛ.окна
    root.overrideredirect(1)#Убираем дефолт меню винды с приложения
    root.wm_attributes("-topmost", 1)#Тут ставим чтобы у нас приложение всегда было поверх всех других
    #(не менять,т.к тхинкер тупой и приложение будет закрываться)
    width = root.winfo_screenwidth() // 2 + 150#Делаем чтобы приложение масштабировалось под экран
    height = root.winfo_screenheight() // 2 + 50#Делаем чтобы приложение масштабировалось под экран
    root.minsize(width, height)#Делаем чтобы нельзя было сделать меньше окно чем задали выше
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    # Функция, обновляющая цветовую схему гл.меню
    def build_menuupdate(self):
        self.root.configure(bg=self.Main_color)
        self.lbl.configure(bg=self.Main_color, fg=self.Text_color)
        self.play_button.configure(bg=self.Main_color,activebackground=self.Main_color)
        self.bot_button.configure(bg=self.Main_color,activebackground=self.Main_color)
        self.settings_button.configure(bg=self.Main_color,activebackground=self.Main_color)
        self.exit_button.configure(bg=self.Main_color,activebackground=self.Main_color)
        self.button_frame.configure(bg=self.Main_color)
        self.close_button.configure(bg='#CE2029',activebackground=self.Text_color,borderwidth=0)
        self.drag_canvas.configure(borderwidth=0,height=30,highlightthickness=0,bg=self.Text_color)

    def music(self,file):playsound(path.join(self.script_dir, 'sound', file))#функция которая будет играть мюзика


    # Функция, создающая главное меню
    def build_menu(self):
        self.ui_colorchange(self.setting_color)
        # Загружаем изображения
        self.drag_canvas = tk.Canvas(self.root)
        self.drag_canvas.pack(fill = tk.BOTH)
        self.drag_canvas.bind('<B1-Motion>', lambda e:self.b1motion(self.root,e))
        self.drag_canvas.bind('<Motion>',    lambda e:self.motion(self.root,e))
        self.close_button = tk.Button(self.drag_canvas, text="X",command = lambda: self.quit())
        self.close_button.place(relx=1.0, rely=0.0, anchor='ne',relheight=1, relwidth=0.060)
        play_image = ImageTk.PhotoImage(Image.open(path.join(Menu.script_dir, 'icon', 'play.png')))
        bot_image = ImageTk.PhotoImage(Image.open(path.join(Menu.script_dir, 'icon', 'bot.png')))
        settings_image = ImageTk.PhotoImage(Image.open(path.join(Menu.script_dir, 'icon', 'settings.png')))
        exit_image = ImageTk.PhotoImage(Image.open(path.join(Menu.script_dir, 'icon', 'exit.png')))
        # Создаем заголовок
        Menu.lbl = tk.Label(self.root, text='Крестики-нолики', font=('Jolly Lodger Cyrillic', self.h1), borderwidth=0, relief="ridge")
        self.lbl.pack(pady=20)
        # Создаем кнопки
        self.button_frame = tk.Frame(self.root)
        self.play_button = tk.Button(self.button_frame, image=play_image, width=160, height=250, bd=0, command=self.start, borderwidth=0, relief="ridge")
        self.play_button.pack(side='left', padx=20)
        self.bot_button = tk.Button(self.button_frame, image=bot_image, width=160, height=250, bd=0, command=self.bot_start, borderwidth=0, relief="ridge")
        self.bot_button.pack(side='left', padx=20)
        self.settings_button = tk.Button(self.button_frame, image=settings_image, width=160, height=250, bd=0, command=self.settings, borderwidth=0, relief="ridge")
        self.settings_button.pack(side='left', padx=20)
        self.exit_button = tk.Button(self.button_frame, image=exit_image, width=160, height=250, bd=0, command=self.quit, borderwidth=0, relief="ridge")
        self.exit_button.pack(side='left', padx=20)
        self.button_frame.pack(pady=self.root.winfo_height() // 2.8)
        self.build_menuupdate()
        self.root.mainloop()
    def b1motion(self,root,e):#Функция чтобы перетаскивать окно
        root.geometry("+%d+%d" % (root.winfo_x()+e.x-root.start.x, root.winfo_y()+e.y-root.start.y))
    def motion(self,root,e):
        root.start=e

    # Функция для кнопки "Выход"
    def quit(self):
        threading.Thread(target = self.music('click.mp3'), daemon=True).start()
        Statistics.save()
        self.root.destroy()

    # Функция для кнопки "Начать игру с другом"
    def start(self):
        threading.Thread(target = self.music('click.mp3'), daemon=True).start()
        Game.int_board = self.setting_intboard
        Game.bot_mode = False
        threading.Thread(target=Game.Start()).start()
    # Функция для кнопки "Начать игру с ботом"
    def bot_start(self):
        threading.Thread(target = self.music('click.mp3'), daemon=True).start()
        Game.int_board = 3
        Game.botstregth = self.setting_stretgbot
        Game.bot_mode = True
        threading.Thread(target=Game.Start()).start()
    # Функция для кнопки "Настройки"-Ползунок размер поля
    def settings_boardchange(self,value):
        self.setting_intboard=int(value)
    # Функция для кнопки "Настройки"-Ползунок сила
    def settings_stretgchange(self,value):
        self.setting_stretgbot=int(value)

    def settings_colorchange(self,value):
        # получить текущее выбранное значение
        current_value = self.selected_option.get()
        # получить индекс выбранного элемента в списке
        self.setting_color = self.options.index(current_value)
        self.ui_colorchange(self.setting_color)
        self.build_menuupdate()
        self.build_settingsupdate()

    def ui_colorchange(self,color):#ТУТ ВСЕ ЦВЕТОВЫЕ СХЕМЫ ПРИЛОЖЕНИЯ(можна менять)
        if color == 0:#|Помидорка
            Menu.Main_color="#F67280"#default:#F67280
            Menu.Text_color="#6C5B7B"#default:#6C5B7B
        elif color == 1:#|Сливка
            Menu.Main_color="#48466D"#default:#48466D
            Menu.Text_color="#46CDCF"#default:#46CDCF
        elif color == 2:#|Авокадо
            Menu.Main_color="#1FAB89"#default:#1FAB89
            Menu.Text_color="#9DF3C4"#default:#9DF3C4
        elif color == 3:#|Апельсинка
            Menu.Main_color="#FF8264"#default:#FF8264
            Menu.Text_color="#FFF5A5"#default:#FFF5A5
        elif color == 4:#|Клубничка
            Menu.Main_color="#E23E57"#default:#E23E57
            Menu.Text_color="#522546"#default:#522546
        elif color == 5:#|Бананчик
            Menu.Main_color="#FDFFAB"#default:#FDFFAB
            Menu.Text_color="#3E4149"#default:#3E4149
        elif color == 6:#Маракуя
            Menu.Main_color="#212121"#default:#212121
            Menu.Text_color="#FFFFFF"#default:#FFFFFF
    # Функция, обновляющая цветовую схему окна настроек
    def build_settingsupdate(self):
        self.style.configure('Vertical.TScrollbar', gripcount=0, background=self.Text_color, darkcolor=self.Text_color, lightcolor=self.Main_color, troughcolor=self.Main_color, bordercolor=self.Main_color)
        self.style.map('Vertical.TScrollbar', background=[('active', self.Text_color)])
        self.scrollbar.config(style='Vertical.TScrollbar')
        self.canvas.configure(bg=self.Main_color)
        self.frame.configure(bg=self.Main_color)
        self.settings_title_label.configure(font=('Jolly Lodger Cyrillic', self.h1, 'bold'),fg=self.Text_color,bg=self.Main_color)
        self.board_size_label.configure(font=('Jolly Lodger Cyrillic', self.h2),bg=self.Main_color,fg=self.Text_color)
        self.board_size_slider.configure(troughcolor=self.Text_color,bg=self.Main_color, fg=self.Text_color, bd=0,activebackground=self.Text_color)
        self.bot_strength_label.configure(font=('Jolly Lodger Cyrillic', self.h2),bg=self.Main_color,fg=self.Text_color)
        self.bot_strength_slider.configure(troughcolor=self.Text_color,bg=self.Main_color, fg=self.Text_color, bd=0,activebackground=self.Text_color)
        self.ui_color_label.configure(font=('Jolly Lodger Cyrillic', self.h2),bg=self.Main_color,fg=self.Text_color)
        self.statistics_label.configure(font=('Jolly Lodger Cyrillic', self.h2),bg=self.Main_color,fg=self.Text_color)
        self.copyright_label.configure(font=('Jolly Lodger Cyrillic', self.h2),fg=self.Text_color,bg=self.Main_color)
        self.copyright_text.configure(font=('Jolly Lodger Cyrillic', self.h3),bg=self.Main_color,fg=self.Text_color)
        self.statistics_text.configure(font=('Jolly Lodger Cyrillic', self.h3),bg=self.Main_color,fg=self.Text_color)
        self.option_menu.configure(width = 10,font=('Jolly Lodger Cyrillic', self.h3),bg=self.Text_color, fg=self.Main_color,bd=0,activebackground=self.Text_color,highlightbackground=self.Main_color,activeforeground=self.Main_color, borderwidth=0,indicatoron=0)
        self.option_menu['menu'].config(font=('Jolly Lodger Cyrillic', 15),bg=self.Text_color,relief='ridge',fg=self.Main_color, bd=0,activebackground=self.Main_color,activeforeground=self.Text_color)
        self.close_button_sett.configure(bg='#CE2029',activebackground=self.Text_color,borderwidth=0)
        self.drag_canvas_sett.configure(borderwidth=0,height=30,highlightthickness=0,bg=self.Text_color)
        # Функция для кнопки "Настройки"
    def settings(self):
        threading.Thread(target = self.music('click.mp3'), daemon=True).start()
        # Создаем окно настроек
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.configure(bg=self.Main_color)
        self.settings_window.wm_attributes("-topmost", 1)
        self.settings_window.title('Крестики-нолики | Настройки')
        self.settings_window.geometry('400x555')
        self.settings_window.overrideredirect(1)
        self.settings_window.iconbitmap(self.icon_path)

        self.drag_canvas_sett = tk.Canvas(self.settings_window)
        self.drag_canvas_sett.pack(fill = tk.BOTH)
        self.drag_canvas_sett.bind('<B1-Motion>', lambda e:self.b1motion(self.settings_window,e))
        self.drag_canvas_sett.bind('<Motion>',    lambda e:self.motion(self.settings_window,e))
        self.close_button_sett = tk.Button(self.drag_canvas_sett, text="X",command = lambda: self.settings_window.destroy())
        self.close_button_sett.place(relx=1.0, rely=0.0, anchor='ne',relheight=1, relwidth=0.125)

        # создаем виджет Scrollbar
        self.scrollbar = ttk.Scrollbar(self.settings_window, orient=VERTICAL)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        # создаем виджет Canvas
        self.canvas = Canvas(self.settings_window, yscrollcommand=self.scrollbar.set, bd=0, highlightthickness=0, relief='ridge')
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # устанавливаем связь между Canvas и Scrollbar
        self.scrollbar.config(command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # создаем фрейм для размещения элементов
        self.frame = Frame(self.canvas)
        # Создаем заголовок настроек
        self.settings_title_label = tk.Label(self.frame, text='Настройки',borderwidth=0,relief="ridge")
        self.settings_title_label.pack(pady=20)

        # Создаем подзаголовок "Размер поля"
        self.board_size_label = tk.Label(self.frame, text='Размер поля\n(Только против друга)',borderwidth=0,relief="ridge")
        self.board_size_label.pack()

        # Создаем слайдер для выбора размера поля
        self.board_size_slider = tk.Scale(self.frame,command=self.settings_boardchange, from_=2, to=13, orient='horizontal',highlightthickness=0)
        self.board_size_slider.pack(pady=10)
        self.board_size_slider.set(self.setting_intboard)

        # Создаем подзаголовок "Сила бота"
        self.bot_strength_label = tk.Label(self.frame, text='Сила бота',borderwidth=0,relief="ridge")
        self.bot_strength_label.pack()

        # Создаем слайдер для выбора силы бота
        self.bot_strength_slider = tk.Scale(self.frame,command=self.settings_stretgchange, from_=1, to=10, orient='horizontal',highlightthickness=0)
        self.bot_strength_slider.pack(pady=10)
        self.bot_strength_slider.set(self.setting_stretgbot)

        # Создаем подзаголовок "Цвет интерфейса"
        self.ui_color_label = tk.Label(self.frame, text='Цвет интерфейса',borderwidth=0,relief="ridge")
        self.ui_color_label.pack()

        # Создаем выпадающий список цветов интерфейса
        self.options = ["Помидорка", "Сливка", "Авокадо", "Апельсинка", "Клубничка", "Бананчик", "Маракуя"]
        self.selected_option = tk.StringVar()
        self.option_menu = tk.OptionMenu(self.frame, self.selected_option, *self.options,command=self.settings_colorchange)
        self.selected_option.set(self.options[self.setting_color])
        self.option_menu.pack(pady=10)

        # Создаем подзаголовок "Статистика"
        self.statistics_label = tk.Label(self.frame, text='Статистика',borderwidth=0,relief="ridge")
        self.statistics_label.pack()
        #---ВЫВОД СТАТЫ--------------------------------------------------------------
        self.statistics_text = tk.Label(self.frame, text=f"""
Всего игр:{Statistics.all_Games}
Игр против бота:{Statistics.all_Games_vsbot}
Игр против друга:{Statistics.all_Games_vsfriend}
Всего игр за X:{Statistics.all_GamesX}
Всего игр за O:{Statistics.all_GamesO}
Побед против бота:{Statistics.all_winvsbot}
Поражений против бота:{Statistics.all_winbot}
Всего побед за X:{Statistics.all_winX}
Всего побед за O:{Statistics.all_winO}
Всего ничьих:{Statistics.all_draws}
Ничьих против бота:{Statistics.all_drawsvsbot}
Ничьих против друга:{Statistics.all_drawsvsfriend}
Ничьих за O:{Statistics.all_drawsO}
Ничьих за X:{Statistics.all_drawsX}
        """
        ,borderwidth=0,relief="ridge")
        self.statistics_text.pack(pady=10)
        #Copyright
        self.copyright_label = tk.Label(self.frame, text='Разработка',borderwidth=0,relief="ridge")
        self.copyright_label.pack(pady=5)
        self.copyright_text = tk.Label(self.frame, text='© Ynan Studio 2023',borderwidth=0,relief="ridge")
        self.copyright_text.pack(pady=5)
        # размещаем фрейм на Canvas
        self.canvas.create_window((0, 0), window=self.frame, anchor=NW)
        # выравниваем элементы по центру фрейма
        self.frame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda event: self.canvas.itemconfigure(self.frame_id, width=event.width))
        self.frame_id = self.canvas.create_window((0, 0), window=self.frame, anchor=NW)
        #Выводим окно settings
        self.build_settingsupdate()
        self.settings_window.mainloop()
#========================================================Game CLASS==================================================================
class Game:
    bot_mode = False#Если бот мод true то запускаем режим игры с ботом если false то с другом| Default:false
    int_board = 3#размер поля, меняется через переменные класса Menu
    botstregth = 5#сила бота, меняется через переменные класса Menu
    h_choice = ''  # X or O определяем переменную
    c_choice = ''  # X or O определяем переменную
    HUMAN = -1
    COMP = +1
    #Вывод кнопок в окно Game.window
    def boards(self):
        self.drag_canvas_game = tk.Canvas(self.window)
        self.drag_canvas_game.configure(borderwidth=0,height=30,width=450,highlightthickness=0,bg=Menu.Text_color)
        self.drag_canvas_game.grid()
        self.drag_canvas_game.bind('<B1-Motion>', lambda e:Menu.b1motion(self.window,e))
        self.drag_canvas_game.bind('<Motion>',    lambda e:Menu.motion(self.window,e))
        self.close_button_game = tk.Button(self.drag_canvas_game, text="X",command = lambda: self.window.destroy())
        self.close_button_game.configure(bg='#CE2029',activebackground=Menu.Text_color,borderwidth=0)
        self.close_button_game.place(relx=1.0, rely=0.0, anchor='ne',relheight=1, relwidth=0.110)
        f = Frame(self.window)
        f.grid()
        width = 129//(self.int_board*3)
        height = 9//self.int_board
        self.buttons =[[0 for j in range(self.int_board)] for i in range(self.int_board)]
        for i in range(self.int_board):
            for j in range(self.int_board):
                button = tk.Button(f, text="", width=width, height=height ,font=('Jolly Lodger Cyrillic', Menu.h3, 'bold'),fg = Menu.Text_color,bg=Menu.Main_color,highlightbackground='#000000',activebackground=Menu.Text_color,activeforeground=Menu.Main_color,
                                   command=lambda x=i, y=j: self.HUMAN_turn(x,y))
                button.grid(row=i, column=j,sticky=N+S)
                self.buttons[i][j] = button
    #Опредеяем текущее положение поля (часть Minimax)
    def evaluate(self):
        if self.wins(self.COMP):
            score = +1
        elif self.wins(self.HUMAN):
            score = -1
        else:
            score = 0

        return [-1,-1,score]
    #Определяем выигрывает ли кто то
    def wins(self, player,winset = False):
        state = self.board
        size = len(state)
        lines = []
        winning_cells = []

        # добавляем строки, столбцы и диагонали
        for i in range(size):
            # добавляем строку
            line = [state[i][j] for j in range(size)]
            lines.append(line)
            # добавляем столбец
            line = [state[j][i] for j in range(size)]
            lines.append(line)
            # добавляем диагональ 1
            if i == 0:
                line = [state[j][j] for j in range(size)]
                lines.append(line)
            # добавляем диагональ 2
            if i == size-1:
                line = [state[j][size-j-1] for j in range(size)]
                lines.append(line)

        # проверяем наличие выигрышной комбинации
        for line in lines:
            if line == [player]*size:
                winning_cells = [(i, j) for i in range(size) for j in range(size) if state[i][j] == player]
                for winbut in winning_cells:
                  row, col = winbut
                  if winset == True:
                      if self.bot_mode and player == self.COMP:#Если бот одержал победу
                          self.buttons[row][col].config(bg='#CC6666')#Устанавливаем красный цвет поля чтобы было красиво и понятно
                      else:#в ином случае
                          self.buttons[row][col].config(bg='#99FF66')#Устанавливаем синий цвет поля чтобы было красиво и понятно
                return True
        return False
    #
    def Game_over(self,state):
        return self.wins(self.HUMAN) or self.wins(self.COMP)

    def Game_exit(self):
        self.window.after(2000, self.window.destroy)


    def empty_cells(self,state):
        return [[x, y] for x, row in enumerate(state) for y, cell in enumerate(row) if cell == 0]


    def valid_move(self,x, y):#Проверяем занята ли клетка ли переданных координатах в поле 
        if [x, y] in self.empty_cells(self.board):
            return True#Если свободна
        else:
            return False#Если занята


    def set_move(self,x, y, player,choice):#Устанавливаем на переданных координатах переданные X или 0
        chars = {
            -1: self.h_choice,
            +1: self.c_choice,
            0: ' '
        }
        if self.valid_move(x, y):#проверяем
            self.board[x][y] = player
            self.buttons[x][y].config(text=choice)
            self.checkwin()
            return True
        else:
            return False

#========================================================AI BOT==================================================================

    def minimax(self, state, depth, player, alpha = -float('inf'), beta =float('inf')):#Алгоритм минимакса
        if player == self.COMP:
            best = [-1, -1, -float('inf')]
        else:
            best = [-1, -1, float('inf')]

        if depth == 0 or self.Game_over(state):
            return self.evaluate()#Проверяем лучший ход

        empty_cells = self.empty_cells(state)
        for cell in empty_cells:#Вытаскиваем все свободные ячейки с поля
            x, y = cell[0], cell[1]
            state[x][y] = player
            score = self.minimax(state, depth - 1, -player, alpha, beta)#min
            state[x][y] = 0
            score[0], score[1] = x, y

            if player == self.COMP:
                if score[2] > best[2]:
                    best = score
                alpha = max(alpha, score[2])#Альфа бета отсечение
                if alpha >= beta:
                    break
            else:
                if score[2] < best[2]:
                    best = score
                beta = min(beta, score[2])#Альфа бета отсечение
                if beta <= alpha:
                    break

        return best#Возвращаем картеж с лучшими координатами x,y
        
    def ai_turn(self,onehod = False):#Функция хода бота
        x=None
        y=None
        k=0
        if self.botstregth < 10:#Если сила бота меньше 10 то будем делать ошибки с помощью рандома
          k=randint(1, self.botstregth)
        depth = len(self.empty_cells(self.board))#Смотрим все свободные координаты 
        if depth == 0 or self.Game_over(self.board):#Если нету свободных клеток или игра кончилась то ничего не делаем
            return
        if depth == 9 or k == 1 :#Если глубина 9 то начало и 1 ход рандомный или если выпало на рандоме 1
          while self.valid_move(x,y) == False:
            x = choice([0, 1, 2])
            y = choice([0, 1, 2])
        else:#если ничего подобного то ищем лучший ход с помощью алгоритма минимакса
            move = self.minimax(self.board, depth, self.COMP)
            x, y = move[0], move[1]
        self.set_move(x, y, self.COMP,self.c_choice)
#========================================================AI BOT==================================================================
    def HUMAN_turn(self,x,y):#Ход игрока
        depth = len(self.empty_cells(self.board))#Смотрим все свободные координаты 
        if depth == 0 or self.Game_over(self.board) or self.board[x][y] != 0:
            return
        if self.bot_mode == True:#Тут определяем включен ли бот мод ,если да то следующий ход бота 
          self.set_move(x,y, self.HUMAN,self.h_choice)
          threading.Thread(target=self.ai_turn()).start()#Чтоб не залагивало
          return
        if self.bot_mode == False and self.player_cur ==1:#Если нет то игра против друга определяем какой игрок ходит и ходим
          self.set_move(x,y, self.HUMAN,self.h_choice)
          self.player_cur =2
        elif self.player_cur ==2:
          self.set_move(x,y, self.COMP,self.c_choice)
          self.player_cur =1


    def checkwin(self):#Проверяем победу или ничью в игре
        if self.wins(self.HUMAN,True):#Выиграл игрок(№1)
            self.Game_exit()#Завершаем игру
            Statistics.statics_add(self.h_choice)#Добавляем в статистику
            Menu.lbl.config(text=f'Выиграл:{self.h_choice}')#Выводим кто выиграл(его знак x или 0 )
        elif self.wins(self.COMP,True):#Выиграл компьютер или игрок №2
            self.Game_exit()#Завершаем игру
            Statistics.statics_add(self.c_choice)#Добавляем в статистику
            Menu.lbl.config(text=f'Выиграл:{self.c_choice}')#Выводим кто выиграл(его знак x или 0 )
        else:#Ничья
            for i in range(self.int_board):
                for j in range(self.int_board):
                    if self.board[i][j] == 0:
                        return
            for i in range(self.int_board):
                for j in range(self.int_board):
                  self.buttons[i][j].config(bg='#666666')#Устанавливаем серый цвет поля чтобы было красиво и понятно
            self.Game_exit()#Завершаем игру
            Statistics.statics_add(self.h_choice,True)#Добавляем в статистику
            Menu.lbl.config(text="Ничья")#Пишем что ничья

    #Старт игры
    def Start(self):
        Menu.lbl.config(text='Крестики-нолики')
        self.player_cur=1
        self.board =  [[0 for j in range(self.int_board)] for i in range(self.int_board)]#Создаем поле x на y размеров (изменяется в классе Menu)
        self.window = tk.Toplevel(Menu.root)
        self.window.configure(bg=Menu.Text_color)
        self.window.overrideredirect(1)
        self.window.wm_attributes("-topmost", 1)
        self.window.title("Крестики-нолики | YNAN")
        self.window.iconbitmap(Menu.icon_path)#Ставим иконку
        self.boards()
        #Определяем рандомно кто будет первым ходить
        if randint(1, 2) == 1:
            self.h_choice = 'X'
            self.c_choice = 'O'
        else:
            self.h_choice = 'O'
            self.c_choice = 'X'
        if self.bot_mode == True and randint(1, 2) == 1:
            self.ai_turn(True)
        #Создаем окно window
        self.window.mainloop()
#========================================================Класс статистики и сохранения настроек================================================================
class Statistics:
    all_Games = 0#Все игры
    all_Games_vsbot = 0#Все игры против бота
    all_Games_vsfriend = 0#Все игры против друга
    all_GamesX = 0#Все игры за Х
    all_GamesO = 0#Все игры за 0
    #Победы
    all_winbot = 0#Все победы против бота
    all_winvsbot = 0#Все победы против друга
    all_winX = 0#Все победы за Х
    all_winO = 0#Все победы за 0
    #Ничьи
    all_draws = 0#Все ничьи
    all_drawsvsbot=0#Все ничьи против бота
    all_drawsvsfriend = 0#Все ничьи против друга
    all_drawsX = 0#Все ничьи за Х
    all_drawsO = 0#Все ничьи за 0

    keykey=b'qT0ZDjwCvnKkfPEYBm23q5p8srNkM-nWC6Ss4aGcMEw='#Контрольный ключ дешифровки
    def encrypt_data(self,data):#шифруем данные
        key = Fernet.generate_key()
        fernet = Fernet(key)
        encrypted_data = {}
        for keys,value in data.items():
            encrypted_value = fernet.encrypt(str.encode(str(value))).decode("utf-8")
            encrypted_data[keys] = encrypted_value
        encrypted_data['key'] = str(Fernet(self.keykey).encrypt(key).decode())
        return encrypted_data

    def decrypt_data(self,data):#дешифруем данные
        dkey = Fernet(self.keykey).decrypt(data.pop('key').encode())
        dfernet = Fernet(dkey)
        decrypted_data = {}
        for keys,value in data.items():
            decrypted_value = dfernet.decrypt(str.encode(value)).decode("utf-8")
            decrypted_data[keys] = int(decrypted_value)
        return decrypted_data

    def save(self):
        data = {#Тут записываем все переменные в соответствующие им ключи
            'all_Games': self.all_Games,
            'all_Games_vsbot': self.all_Games_vsbot,
            'all_Games_vsfriend': self.all_Games_vsfriend,
            'all_XGames': self.all_GamesX,
            'all_OGames': self.all_GamesO,
            #Win
            'all_winX': self.all_winX,
            'all_winO': self.all_winO,
            'all_winvsbot': self.all_winvsbot,
            'all_winbot': self.all_winbot,
              #Draws
            'all_draws' : self.all_draws,
            'all_drawsX' : self.all_drawsX,
            'all_drawsO' : self.all_drawsO,
            'all_drawsvsfriend' : self.all_drawsvsfriend,
            'all_drawsvsbot':self.all_drawsvsbot,
            #Settings
            'setting_intboard': Menu.setting_intboard,
            'setting_stretgbot': Menu.setting_stretgbot,
            'setting_color': Menu.setting_color,
        }
        encrypted_data = self.encrypt_data(data)
        with open('data.yuna', 'w') as fp:#Сохраняем все загруженное в файл с именем data.yuna в директорию где находится файл исполнения
            json.dump(encrypted_data, fp)
            
    def load(self):#Загрузка сохранения(происходит при запуске)
        try:
            with open('data.yuna', 'r') as fp:#Открываем файл с именем data.yuna который находится в директории где находится файл исполнения
                encrypted_data = json.load(fp)
            decrypted_data = self.decrypt_data(encrypted_data)
            self.all_Games = decrypted_data.get('all_Games', 0)
            self.all_Games_vsbot = decrypted_data.get('all_Games_vsbot', 0)
            self.all_Games_vsfriend = decrypted_data.get('all_Games_vsfriend', 0)
            self.all_GamesX = decrypted_data.get('all_XGames',0)
            self.all_GamesO = decrypted_data.get('all_OGames', 0)
            #Win
            self.all_winX = decrypted_data.get('all_winX', 0)
            self.all_winO = decrypted_data.get('all_winO', 0)
            self.all_winvsbot = decrypted_data.get('all_winvsbot', 0)
            self.all_winbot = decrypted_data.get('all_winbot', 0)
            #Draws
            self.all_draws = decrypted_data.get('all_draws', 0)
            self.all_drawsX = decrypted_data.get('all_drawsX', 0)
            self.all_drawsO = decrypted_data.get('all_drawsO', 0)
            self.all_drawsvsfriend = decrypted_data.get('all_drawsvsfriend', 0)
            self.all_drawsvsbot = decrypted_data.get('all_drawsvsbot', 0)
            #Settings
            Menu.setting_intboard = decrypted_data.get('setting_intboard', 0)
            Menu.setting_stretgbot = decrypted_data.get('setting_stretgbot', 0)
            Menu.setting_color = decrypted_data.get('setting_color', 0)
        except FileNotFoundError:#Если не нашли то ничего не делаем
            print("Файл сохранения не найден.")
        except(Exception,KeyError,ValueError,TypeError) as e:#Если произошла ошибка(допустим неверный ключ)
            print(f"При загрузке файла сохранения произошла ошибка:{e}")
            os.remove('data.yuna') # удалить поврежденный файл сохранения

    def statics_add(self,whowin, draw=False):#Добавляем статистику
        if not draw:#Если ничья
            if Game.bot_mode:#Если режим бота включен
                if whowin == Game.c_choice:#Если победивший игрок бот
                    self.all_winbot += 1
                    if Game.h_choice == 'X':#Если победивший игрок играет за Х
                        self.all_GamesX += 1
                    else:
                        self.all_GamesO += 1
                else:#Если победивший игрок не бот
                    self.all_winvsbot += 1
                    if Game.h_choice == 'X':#Если победивший игрок играет за Х
                        self.all_winX += 1
                        self.all_GamesX += 1
                    else:
                        self.all_winO += 1
                        self.all_GamesO += 1
                self.all_Games_vsbot += 1
            else:#Если режим бота выключен
                if Game.c_choice == 'X':#Если победивший игрок играет за Х
                    self.all_winX += 1
                    self.all_GamesX += 1
                else:
                    self.all_winO += 1
                    self.all_GamesO += 1
                self.all_Games_vsfriend += 1
        else:#Если не ничья
            if Game.bot_mode:#Если режим бота включен
                self.all_drawsvsbot += 1
                self.all_Games_vsbot += 1
            else:
                self.all_drawsvsfriend += 1
            if Game.h_choice == 'X':#Если победивший игрок играет за Х
                self.all_drawsX += 1
                self.all_GamesX += 1
            else:
                self.all_drawsO += 1
                self.all_GamesO += 1
            self.all_draws += 1

        self.all_Games += 1
        self.save()#Сохраняем
#========================================================Самый старт==================================================================
if __name__ == "__main__":
    Statistics = Statistics()#Обьявляем класс Статисткс как переменную статистикс
    Menu = Menu()#Обьявляем класс Меню как переменную меню
    Game = Game()#Обьявляем класс Гейм как переменную гейм
    Statistics.load()#Загружаем сохранение
    Menu.build_menu()#билдим главное меню