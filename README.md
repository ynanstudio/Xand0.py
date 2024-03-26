# MinimaxUIpy
## Ознакомление
Это приложение было сделано в целях проектной деятельности и может работать не совсем корректно и правильно в каких то частях кода,
UI реализован полностью на Tkinter.<br>
За основу алгоритма минимакса были взяты части кода из <a href="https://github.com/hrbang/Minimax-algorithm-PY/tree/master">этого</a> проекта.<br>
Там можно ознакомитсяя с алгоритмом минимакса и его работой,ничего почти не было изменено в алгоритме,кроме добавления альфа-бета отсечения для увеличения производительности.
## О приложении и коде
Я постарался в комментариях в коде расписать каждый его кусок,поэтому нужды расписывать тут его нету.
Приложение.Основные его функции:<br><br>
  • AI бот<br>
  • Изменение размера поля<br>
  • Изменение силы бота<br>
  • Изменение оформления<br>
  • Подробная статистика<br>
  • Сохранение<br>
### Главное меню
<p align="center">
	<img src="https://raw.githubusercontent.com/ynanstudio/MinimaxTicTacToeUIpy/main/main_menu_readme.png"></img>
</p>

### Меню настроек
<p align="center">
	<img src="https://raw.githubusercontent.com/ynanstudio/MinimaxTicTacToeUIpy/main/settings_menu_readme.png"></img>
  <img src="https://raw.githubusercontent.com/ynanstudio/MinimaxTicTacToeUIpy/main/settings_menu_readme_2.png"></img>
</p>

### Окно игры
<p align="center">
	<img src="https://raw.githubusercontent.com/ynanstudio/MinimaxTicTacToeUIpy/main/game_readme.png"></img>
</p>

### Изменение поля на 5х5
<p align="center">
	<img src="https://raw.githubusercontent.com/ynanstudio/MinimaxTicTacToeUIpy/main/game_5x5_readme.png"></img>
</p>

## Запуск
Для начала скачайте все файлы проекта далее откройте консоль и перейдите в папку с проектом:
```cmd
  cd [путь к скачанным файлам]
```
Далее установим все необходимые библиотеки:
```cmd
  pip install -r requirements.txt
```
Можем запускать:
```cmd
  py main.py
```
## Билд
Для билда я использовал библиотеку <a href="https://pypi.org/project/auto-py-to-exe/">auto-py-to-exe</a>
Установим её:
```cmd
  pip install auto-py-to-exe
```
Теперь можно запустить:
```cmd
  auto-py-to-exe
```
Более подробно с auto-py-to-exe ознакомится можно <a href="https://pypi.org/project/auto-py-to-exe/">здесь</a>
