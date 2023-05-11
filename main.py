import tkinter as tk#{
import tkinter.ttk as ttk
import tkinter.font as font
from tkinter import *#}UI библиотека
from random import choice, randint#Рандом
from os import path#Чтобы найти расположение исполняемого файла
import json#Библиотека для сохранения статистики и настроек
from PIL import Image, ImageTk#Библиотека для картинок
from cryptography.fernet import Fernet#Библиотека для шифровки сохранения
import threading#Мульти поточность
#========================================================Класс для окна меню==================================================================
class Menu:
    setting_intboard=3#Меняет размер поля(только против друга)| Default:3
    setting_stretgbot=5#Меняет силу бота| Default:5
    script_dir = path.dirname(__file__)
    root = tk.Tk()
    Main_color = '#9933CC'#Главный цвет приложения(фон)
    Text_color = '#CCCCFF'#Цвет текста
    icon_path = path.join(script_dir, 'icon', 'app.ico')#Путь к иконки приложения

    # Задаем цвет фона
    root.configure(bg=Main_color)
    root.iconbitmap(icon_path)#Устанавливаем иконку

    # Размер окна
    width = root.winfo_screenwidth() // 2+150
    height = root.winfo_screenheight() // 2+ 50
    root.minsize(width, height)
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)

    # Задаем размер окна и его позицию
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    # Задаем название окна
    root.title("Крестики-нолики | Меню")

    # Создаем заголовок
    lbl = tk.Label(root, text='Крестики-нолики', font=('Arial', 20, 'bold'),bg=Main_color,fg=Text_color,borderwidth=0,relief="ridge")
    lbl.pack(pady=20)

    # Создаем кнопки
    button_frame = tk.Frame(root, bg=Main_color)

    # Загружаем изображения
    play_image = ImageTk.PhotoImage(Image.open(path.join(script_dir, 'icon', 'play.png')))#кнопка игры против друга
    bot_image=ImageTk.PhotoImage(Image.open(path.join(script_dir, 'icon', 'bot.png')))#Кнопка игры против бота
    settings_image = ImageTk.PhotoImage(Image.open(path.join(script_dir, 'icon', 'settings.png')))#Кнопка настроек
    exit_image=ImageTk.PhotoImage(Image.open(path.join(script_dir, 'icon', 'exit.png')))#Кнопка выхода

    # Функция для кнопки "Выход"
    def quit():
        Statistics.save()
        Menu.root.destroy()

    # Функция для кнопки "Начать игру с другом"
    def start():
        game.int_board = Menu.setting_intboard
        game.bot_mode = False
        threading.Thread(target=game.Start()).start()
    # Функция для кнопки "Начать игру с ботом"
    def bot_start():
        game.int_board = 3
        game.botstregth = Menu.setting_stretgbot
        game.bot_mode = True
        threading.Thread(target=game.Start()).start()
    # Функция для кнопки "Настройки"-Ползунок размер поля
    def settings_boardchange(value):
        Menu.setting_intboard=int(value)
    # Функция для кнопки "Настройки"-Ползунок сила
    def settings_stretgchange(value):
        Menu.setting_stretgbot=int(value)
    # Функция для кнопки "Настройки"
    def settings():
          # Создаем окно настроек
        settings_window = tk.Toplevel(Menu.root)
        settings_window.configure(bg=Menu.Main_color)
        settings_window.title('Крестики-нолики | Настройки')
        settings_window.geometry('400x555')
        settings_window.iconbitmap(Menu.icon_path)

        # создаем виджет Scrollbar
        scrollbar = ttk.Scrollbar(settings_window, orient=VERTICAL)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Vertical.TScrollbar', gripcount=0, background='#7a29a3', darkcolor='#7a29a3', lightcolor=Menu.Main_color, troughcolor=Menu.Main_color, bordercolor=Menu.Main_color)
        style.map('Vertical.TScrollbar', background=[('active', '#7a29a3')], troughcolor=[('active', Menu.Main_color)])
        scrollbar.config(style='Vertical.TScrollbar')
        # создаем виджет Canvas
        canvas = Canvas(settings_window, bg=Menu.Main_color, yscrollcommand=scrollbar.set, bd=0, highlightthickness=0, relief='ridge')
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # устанавливаем связь между Canvas и Scrollbar
        scrollbar.config(command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        # создаем фрейм для размещения элементов
        frame = Frame(canvas, bg=Menu.Main_color)
        # Создаем заголовок настроек
        settings_title_label = tk.Label(frame, text='Настройки', font=('Arial', 20, 'bold'),fg=Menu.Text_color,bg=Menu.Main_color,borderwidth=0,relief="ridge")
        settings_title_label.pack(pady=20)

        # Создаем подзаголовок "Размер поля"
        board_size_label = tk.Label(frame, text='Размер поля\n(Только против друга)', font=('Arial', 15),bg=Menu.Main_color,fg=Menu.Text_color,borderwidth=0,relief="ridge")
        board_size_label.pack()

        # Создаем слайдер для выбора размера поля
        board_size_slider = tk.Scale(frame,command=Menu.settings_boardchange, from_=2, to=13, orient='horizontal',bg=Menu.Main_color,fg=Menu.Text_color,highlightthickness=0)
        board_size_slider.pack(pady=10)
        board_size_slider.set(Menu.setting_intboard)

        # Создаем подзаголовок "Сила бота"
        bot_strength_label = tk.Label(frame, text='Сила бота', font=('Arial', 15),bg=Menu.Main_color,fg=Menu.Text_color,borderwidth=0,relief="ridge")
        bot_strength_label.pack()

        # Создаем слайдер для выбора силы бота
        bot_strength_slider = tk.Scale(frame,command=Menu.settings_stretgchange, from_=1, to=9, orient='horizontal',bg=Menu.Main_color,highlightthickness=0,fg=Menu.Text_color)
        bot_strength_slider.pack(pady=10)
        bot_strength_slider.set(Menu.setting_stretgbot)

        # Создаем подзаголовок "Статистика"
        statistics_label = tk.Label(frame, text='Статистика', font=('Arial', 15),bg=Menu.Main_color,fg=Menu.Text_color,borderwidth=0,relief="ridge")
        statistics_label.pack(pady=10)
        #---ВЫВОД СТАТЫ--------------------------------------------------------------
        statistics_text = tk.Label(frame, text=f"""
Всего игр:{Statistics.all_games}
Игр против бота:{Statistics.all_games_vsbot}
Игр против друга:{Statistics.all_games_vsfriend}
Всего игр за X:{Statistics.all_gamesX}
Всего игр за O:{Statistics.all_gamesO}
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
        , font=('Arial', 10),bg=Menu.Main_color,fg=Menu.Text_color,borderwidth=0,relief="ridge")
        statistics_text.pack(pady=10)
        #Copyright
        copyright_label = tk.Label(frame, text='Разработка', font=('Arial', 15),fg=Menu.Text_color,bg=Menu.Main_color,borderwidth=0,relief="ridge")
        copyright_label.pack(pady=5)
        copyright_text = tk.Label(frame, text='© Ynan Studio 2023', font=('Arial', 10),bg=Menu.Main_color,fg=Menu.Text_color,borderwidth=0,relief="ridge")
        copyright_text.pack(pady=5)
        # размещаем фрейм на Canvas
        canvas.create_window((0, 0), window=frame, anchor=NW)
        # выравниваем элементы по центру фрейма
        frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda event: canvas.itemconfigure(frame_id, width=event.width))
        frame_id = canvas.create_window((0, 0), window=frame, anchor=NW)
        #Выводим окно settings
        settings_window.mainloop()

    #кнопка игры против друга
    play_button = tk.Button(button_frame ,width=160 ,height=160,image=play_image, bg=Main_color, bd=0, command=start,borderwidth=0,relief="ridge")
    play_button.pack(side='left', padx=20)
    #Кнопка игры с ботом
    bot_button = tk.Button(button_frame,width=160 ,height=160, image=bot_image, bg=Main_color, bd=0, command=bot_start,borderwidth=0,relief="ridge")
    bot_button.pack(side='left', padx=20)
    #Кнопка настроек
    settings_button = tk.Button(button_frame,width=160 ,height=160, bg=Main_color, image=settings_image, bd=0, command=settings,borderwidth=0,relief="ridge")
    settings_button.pack(side='left', padx=20)

    # Функция для кнопки "Выход"
    exit_button = tk.Button(button_frame,width=160 ,height=160, image=exit_image, bg=Main_color, bd=0, command=quit,borderwidth=0,relief="ridge")
    exit_button.pack(side='left', padx=20)

    button_frame.pack(pady=root.winfo_height() // 2)
#========================================================GAME CLASS==================================================================
class Game:
    bot_mode = False#Если бот мод true то запускаем режим игры с ботом если false то с другом| Default:false
    int_board = 3#размер поля, меняется через переменные класса Menu
    botstregth = 5#сила бота, меняется через переменные класса Menu
    HUMAN = -1
    COMP = +1
    #Вывод кнопок в окно game.window
    def boards(self):
        width = self.window.winfo_screenwidth()//50//self.int_board
        height = self.window.winfo_screenheight()//50//self.int_board
        self.buttons =[[0 for j in range(self.int_board)] for i in range(self.int_board)]
        for i in range(self.int_board):
            for j in range(self.int_board):
                button = tk.Button(self.window, text="", width=width, height=height ,font=('Arial', 20, 'bold'),fg = Menu.Text_color,bg=Menu.Main_color,highlightbackground='#000000',
                                   command=lambda x=i, y=j: self.HUMAN_turn(x,y))
                button.grid(row=i, column=j)
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
    def game_over(self,state):
        return self.wins(self.HUMAN) or self.wins(self.COMP)

    def game_exit(self):
        for i in range(self.int_board):
          for j in range(self.int_board):
            self.buttons[i][j].config(state="disabled")
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

        if depth == 0 or self.game_over(state):
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
        if self.botstregth <= 8:#Если сила бота меньше 8 то будем делать ошибки с помощью рандома
          k=randint(1, self.botstregth) 
        depth = len(self.empty_cells(self.board))#Смотрим все свободные координаты 
        if depth == 0 or self.game_over(self.board):#Если нету свободных клеток или игра кончилась то ничего не делаем
            return
        if depth == 9 or k == 1:#Если глубина 9 то начало и 1 ход рандомный или если выпало на рандоме 1
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
        if depth == 0 or self.game_over(self.board) or self.board[x][y] != 0:
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
            self.game_exit()#Завершаем игру
            Statistics.statics_add(self.h_choice)#Добавляем в статистику
            Menu.lbl.config(text=f'Выиграл:{self.h_choice}')#Выводим кто выиграл(его знак x или 0 )
        elif self.wins(self.COMP,True):#Выиграл компьютер или игрок №2
            self.game_exit()#Завершаем игру
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
            self.game_exit()#Завершаем игру
            Statistics.statics_add(self.h_choice,True)#Добавляем в статистику
            Menu.lbl.config(text="Ничья")#Пишем что ничья

    #Старт игры
    def Start(self):
        Menu.lbl.config(text='Крестики-нолики')
        self.player_cur=1
        self.board =  [[0 for j in range(self.int_board)] for i in range(self.int_board)]#Создаем поле x на y размеров (изменяется в классе Menu)
        self.h_choice = ''  # X or O определяем переменную
        self.c_choice = ''  # X or O определяем переменную
        self.window = tk.Tk()
        self.window.configure(bg=Menu.Main_color)
        self.window.resizable(False, False)
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
    all_games = 0#Все игры
    all_games_vsbot = 0#Все игры против бота
    all_games_vsfriend = 0#Все игры против друга
    all_gamesX = 0#Все игры за Х
    all_gamesO = 0#Все игры за 0
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
    def encrypt_data(data):#шифруем данные
        key = Fernet.generate_key()
        fernet = Fernet(key)
        encrypted_data = {}
        for keys,value in data.items():
            encrypted_value = fernet.encrypt(str.encode(str(value))).decode("utf-8")
            encrypted_data[keys] = encrypted_value
        encrypted_data['key'] = str(Fernet(Statistics.keykey).encrypt(key).decode())
        return encrypted_data

    def decrypt_data(data):#дешифруем данные
        dkey = Fernet(Statistics.keykey).decrypt(data.pop('key').encode())
        dfernet = Fernet(dkey)
        decrypted_data = {}
        for keys,value in data.items():
            decrypted_value = dfernet.decrypt(str.encode(value)).decode("utf-8")
            decrypted_data[keys] = int(decrypted_value)
        return decrypted_data

    def save():
        data = {#Тут записываем все переменные в соответствующие им ключи
            'all_games': Statistics.all_games,
            'all_games_vsbot': Statistics.all_games_vsbot,
            'all_games_vsfriend': Statistics.all_games_vsfriend,
            'all_Xgames': Statistics.all_gamesX,
            'all_Ogames': Statistics.all_gamesO,
            #Win
            'all_winX': Statistics.all_winX,
            'all_winO': Statistics.all_winO,
            'all_winvsbot': Statistics.all_winvsbot,
            'all_winbot': Statistics.all_winbot,
              #Draws
            'all_draws' : Statistics.all_draws,
            'all_drawsX' : Statistics.all_drawsX,
            'all_drawsO' : Statistics.all_drawsO,
            'all_drawsvsfriend' : Statistics.all_drawsvsfriend,
            'all_drawsvsbot':Statistics.all_drawsvsbot,
            #Settings
            'setting_intboard': Menu.setting_intboard,
            'setting_stretgbot': Menu.setting_stretgbot,
        }
        encrypted_data = Statistics.encrypt_data(data)
        with open('data.yuna', 'w') as fp:#Сохраняем все загруженное в файл с именем data.yuna в директорию где находится файл исполнения
            json.dump(encrypted_data, fp)
            
    def load():#Загрузка сохранения(происходит при запуске)
        try:
            with open('data.yuna', 'r') as fp:#Открываем файл с именем data.yuna который находится в директории где находится файл исполнения
                encrypted_data = json.load(fp)
            decrypted_data = Statistics.decrypt_data(encrypted_data)
            Statistics.all_games = decrypted_data.get('all_games', 0)
            Statistics.all_games_vsbot = decrypted_data.get('all_games_vsbot', 0)
            Statistics.all_games_vsfriend = decrypted_data.get('all_games_vsfriend', 0)
            Statistics.all_gamesX = decrypted_data.get('all_Xgames', 0)
            Statistics.all_gamesO = decrypted_data.get('all_Ogames', 0)
            #Win
            Statistics.all_winX = decrypted_data.get('all_winX', 0)
            Statistics.all_winO = decrypted_data.get('all_winO', 0)
            Statistics.all_winvsbot = decrypted_data.get('all_winvsbot', 0)
            Statistics.all_winbot = decrypted_data.get('all_winbot', 0)
            #Draws
            Statistics.all_draws = decrypted_data.get('all_draws', 0)
            Statistics.all_drawsX = decrypted_data.get('all_drawsX', 0)
            Statistics.all_drawsO = decrypted_data.get('all_drawsO', 0)
            Statistics.all_drawsvsfriend = decrypted_data.get('all_drawsvsfriend', 0)
            Statistics.all_drawsvsbot = decrypted_data.get('all_drawsvsbot', 0)
            #Settings
            Menu.setting_intboard = decrypted_data.get('setting_intboard', 0)
            Menu.setting_stretgbot = decrypted_data.get('setting_stretgbot', 0)
        except FileNotFoundError:#Если не нашли то ничего не делаем
            print("Файл сохранения не найден.")
        except(Exception,KeyError,ValueError,TypeError) as e:#Если произошла ошибка(допустим неверный ключ)
            print(f"При загрузке файла сохранения произошла ошибка:{e}")
            os.remove('data.yuna') # удалить поврежденный файл сохранения

    def statics_add(whowin, draw=False):#Добавляем статистику
        if not draw:#Если ничья
            if game.bot_mode:#Если режим бота включен
                if whowin == game.c_choice:#Если победивший игрок бот
                    Statistics.all_winbot += 1
                    if game.h_choice == 'X':#Если победивший игрок играет за Х
                        Statistics.all_gamesX += 1
                    else:
                        Statistics.all_gamesO += 1
                else:#Если победивший игрок не бот
                    Statistics.all_winvsbot += 1
                    if game.h_choice == 'X':#Если победивший игрок играет за Х
                        Statistics.all_winX += 1
                        Statistics.all_gamesX += 1
                    else:
                        Statistics.all_winO += 1
                        Statistics.all_gamesO += 1
                Statistics.all_games_vsbot += 1
            else:#Если режим бота выключен
                if game.c_choice == 'X':#Если победивший игрок играет за Х
                    Statistics.all_winX += 1
                    Statistics.all_gamesX += 1
                else:
                    Statistics.all_winO += 1
                    Statistics.all_gamesO += 1
                Statistics.all_games_vsfriend += 1
        else:#Если не ничья
            if game.bot_mode:#Если режим бота включен
                Statistics.all_drawsvsbot += 1
                Statistics.all_games_vsbot += 1
            else:
                Statistics.all_drawsvsfriend += 1
            if game.h_choice == 'X':#Если победивший игрок играет за Х
                Statistics.all_drawsX += 1
                Statistics.all_gamesX += 1
            else:
                Statistics.all_drawsO += 1
                Statistics.all_gamesO += 1
            Statistics.all_draws += 1

        Statistics.all_games += 1
        Statistics.save()#Сохраняем
#========================================================Самый старт==================================================================
if __name__ == "__main__":
    game = Game()#определяем переменную game как класс Game()
    Statistics.load()#Загружаем статистику и настройки
    Menu.root.mainloop()#Создаем окно главного меню