# Кофигурационное управление

## Домашнее задание 1

### Общее описание

Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу
эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС.
Эмулятор должен запускаться из реальной командной строки, а файл с
виртуальной файловой системой не нужно распаковывать у пользователя.
Эмулятор принимает образ виртуальной файловой системы в виде файла формата tar. Эмулятор должен работать в режиме GUI.

Конфигурационный файл имеет формат json и содержит:
• Имя пользователя для показа в приглашении к вводу.
• Путь к архиву виртуальной файловой системы.
• Путь к лог-файлу.

Лог-файл имеет формат csv и содержит все действия во время последнего
сеанса работы с эмулятором. Для каждого действия указан пользователь.
Необходимо поддержать в эмуляторе команды ls, cd и exit, а также
следующие команды:
1. uniq.
2. whoami.
3. echo.

Все функции эмулятора должны быть покрыты тестами, а для каждой из
поддерживаемых команд необходимо написать 2 теста.

### Классы и функции

#### ShellEmulator

Основной класс эмулятора оболочки, который реализует функциональность командной строки и работы с виртуальной файловой системой.

##### __init__(self, config_file) 

Функция инициализирует эмулятор, загружая конфигурацию из файла и инициализируя виртуальную файловую систему.

##### load_config(self, config_file) 

Функция загружает конфигурационный файл JSON, который содержит информацию о пользователе, архиве файловой системы и файле лога.

##### load_filesystem(self) 

Функция загружает виртуальную файловую систему из tar-архива, создавая структуру словаря с путями файлов и их содержимым.

##### log_action(self, action) 

Функция записывает действие пользователя в лог-файл CSV.

##### execute_command(self, command) 

Функция выполняет команду, переданную в виде строки, и вызывает соответствующую функцию из списка команд.

### Команды

##### ls(self, args) 

Отображает список файлов в текущем каталоге. Если файлов нет, выводит сообщение "No files found". Используется для просмотра содержимого текущей директории.

username@shell:/$ ls
Ввод команды ls и нажатие Enter выводит список файлов.Если в текущем каталоге нет файлов, команда выведет:"No files found."

##### cd(self, args) 

Изменяет текущую директорию. Поддерживает переход на родительскую директорию с использованием команды ... Если указанный каталог не существует, выводит сообщение об ошибке.

username@shell:/$ cd <путь_к_каталогу>
Ввод команды cd с указанием пути к каталогу и нажатие Enter.Если указать .., возврат в родительскую директорию.Если указанный каталог не существует, вывод сообщения об ошибке.

##### exit_shell(self, args) 

Завершает работу эмулятора и записывает действие в лог.

username@shell:/$ exit
Ввод команды exit и нажатие Enter, эмулятор завершает работу и выводит сообщение "Exiting shell."

##### uniq(self, args)

Удаляет повторяющиеся строки из переданного текста.Принимает текстовый ввод и возвращает результат, где каждая строка будет уникальной.

uniq "строка1\nстрока2\nстрока1\nстрока3"
Ввод команды uniq и передача аргументов, которая удаляет повторяющиеся строки из переданного текста.Если не переданы аргументы, будет выведено сообщение:"No input provided."

##### whoami(self, args) 

Возвращает имя пользователя, указанное в конфигурационном файле.

username@shell:/$ whoami
Ввод команды exit и нажатие Enter, которая выводит имя пользователя. Имя пользователя считывается из конфигурации, указанной при инициализации эмулятора.


##### echo(self, args)

Выводит переданный текст на экран. Аргументы команды будут объединены в одну строку и выведены.

echo <текст_для_вывода>
Ввод команды echo с текстом,который нужно вывести и нажатие Enter, которая выводит переданный текст на экран.Если не передать аргументы, будет выведена пустая строка.


#### ShellGUI

Класс ShellGUI представляет собой графический интерфейс (GUI) для эмулятора командной оболочки. Он построен с использованием библиотеки tkinter, которая позволяет создавать графические интерфейсы в Python. Класс ShellGUI предоставляет окно, в котором пользователи могут вводить команды и получать вывод в текстовом формате.


##### __init__(self, emulator)

Конструктор инициализирует графический интерфейс. Он принимает объект эмулятора оболочки (класс ShellEmulator) в качестве аргумента и использует его для выполнения команд и получения информации (например, текущего пользователя и текущего каталога). Конструктор также настраивает элементы интерфейса и отображает начальную строку приглашения.

##### display_prompt(self)

Этот метод отображает строку запроса командной строки в поле ввода. Строка запроса отображает имя пользователя (из конфигурации эмулятора) и текущий каталог.

##### on_enter(self, event)

Этот метод вызывается при нажатии клавиши "Enter" в поле ввода. Он обрабатывает введенную команду, выполняет её с помощью метода execute_command из эмулятора, а затем выводит результат в поле вывода.

### Примеры использования

![image](https://github.com/user-attachments/assets/e91a3a7d-5955-491f-b532-2f929babf423)
![image](https://github.com/user-attachments/assets/e7c78fbc-87bf-4ec8-8774-913ac8dfc03d)

### Результаты прогона тестов

![image](https://github.com/user-attachments/assets/31f45aa1-8056-4722-be20-3c5f173ed402)
