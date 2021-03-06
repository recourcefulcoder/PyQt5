В данном файле содержится документацию к проекту. В частности, описаны основные принципы работы программы,
взаимодействия модулей, классы используемых модулей, описание устройства базы данных. Важно отметить, что данная
программа разрабатывалась для Windows, так что на ОС MacOs или Linux могут наблюдаться некоторые отклонения в 
работе - в частности, некорректная установка иконки окон (установка дефолтной вместо указанной в программе)
						СУТЬ ПРОГРАММЫ:
Программа представляет собой тестирующую систему, в которой зарегестрирован один учитель и этим учителем 
может быть зарегистрированно неограниченное число учеников. Первое окно, встречающее пользователя - окно 
авторизации, после которого, согласно введённым пользователем данным открывается одно из двух окон: учительское
или ученическое. На каждом окне реализованы некоторые уникцальные функции
Учительское окно:
	Создание/изменение существующего теста
	Удаление созданного теста
	Редактирование информации о зарегистрированном ученике
	Добавление/удаление ученика в БД
	Просмотр статистики - ответы каждого ученика по каждому тесту
	Редакция личной информации
Ученическое окно:
	Прохождение доступного теста
	Просмотр статистики по пройденным тестам
	Изменение пароля
Практически все окна имеют status_label, информирующий пользователя об ошибке с его стороны и кнопку "назад".
Исключения будут отмечены тегом #easy
Рассмотрим детальнее каждую функцию данных окон
					
						УЧИТЕЛЬСКОЕ ОКНО
					Создание/изменение существующего теста
При нажатии на эту кнопку открывается окно выбора - создать или всё-таки изменить тест. При выборе опции "создать"
открывается окно создания, иначе - окно выбора теста.
Окно создания
С двумя списками - базы вопросов и вопросов, добавленных в новый тест, а также линия ввода 
названия теста, кнопки "добавить вопрос в тест", "создать свой вопрос", "удалить вопрос из базы", "создать тесет", 
"удалить задание из теста". Doubleclick по вопросу в одной из таблиц показывает информацию о задании. Нажатие на 
кнопку "добавить вопрос в тест" добавляет выбранный вопрос в тест. Аналогично действие кнопок "удалить вопрос из 
базы" (+ открывается окно подтверждения действия), "Создать тест" , "удалить задание из теста", в соответствии с 
текстом кнопки.. Кнопка "создать свой вопрос" активирует окно создания вопроса, в котором нужно ввести имя вопроса, 
его текст, верный ответ и варианты ответа (опционально). 
Окно выбора теста
Список тестов, созданных учителем, виджеты для поиска теста в списке. Существует также кнопка инструкции в правом
верхнем углу. Выбор теста осуществляется выбором элемента в списке и нажатием на кнопку "Enter" и открывает окно 
редакции теста.
Окно редакции теста
Полностью аналогично окну создания, с той лишь разницей, что окно заданий тестов по умлочанию заполнено значениями,
линия ввода имени теста неактивна и содержит имя заданного теста, а также отсуствует кнопка удаления вопроса из БД.
						Удаление теста
Окно удаления теста содержит две таблицы - в левой отображаются тесты учителя, в правой - список вопросов выбранного
теста. Doubleclick по названию вопроса вызывает окно#easy с информацией о вопросе. Под левым списком расположена
кнопка удаления, нажатие на которую вызывает окно#easy подтверждения действия.
					Редактирование информации об ученике
Окно редакции информации об ученике содержит таблицу с информацией об учениках, виджеты для поиска ученика и 
кнопку "показать всех учеников", демонстрирующей информацию о всех учениках в таблице. Клетки таблицы редактируемы.
При нажатии на кнопку "подтвердить" открывается окно#easy подтверждения действия. То же окно вызывается при нажатии
на кнопку "назад", если данные в таблице были отредактированны.
						Добавить/удалить ученика
Открывается окно выбора действия; нажатие "добавить" открывает окно добавления ученика, кнопка "удалить" - окно 
удаления ученика.
Окно добавления ученика
Содержит виджеты ввода имени, фамилии, логина и пароля ученика, а также кнопку "Добавить".
Окно удаления ученика
Аналогично окну редактирования информации, с тем отличием, что ячейки таблицы неизменяемы, нажатие на кнопку 
"назад" не вызывает окно подтверждения действия, нажатие на кнопку вызывает окно#easy подтверждения действия
с краткой информации о предлагаемом к удалению ученике.
						Посмотреть статистику			
В окне располагаются два списка: правый - список тестов, левый - результаты учеников, элементы которого имеют вид
"Имя_ученика: результат_в_процентах%", а также виджеты поиска теста по названию и кнопку инструкции.
					Редактирование личной информации
В открытом окне присутствуют строки, содержащие имя/фамилию учителя и его пароль (а также виджет "повторить пароль")
Строки редактируемы, нажатие на кнопку "Редактировать" не вызывает окно подстверждения, однако выдаёт пользователю
просьбу проверить введённые данные, уже отредактированные и сохранённые, в status_label.

						УЧЕНИЧЕСКОЕ ОКНО
							Пройти тест
Открывается окно выбор теста, полностью аналогичное таковому в учительском окне (см. Окно редакции теста). В списке
не отображаются тесты, пройденные учеником, поскольку на каждый даётся 1 попытка. Выбор теста открывает окно 
прохождения теста.
Окно прохождения теста
Содержит область, возможную для "скроллинга", в которой отображены вопросы теста. Нажатие на кнопку "Сдать на 
проверку" открывает окно#easy подтверждения действия. Если пользователь подтверждает действие, он возвращается
к окну выбора теста.
						Посмотреть статистику
В открытом окне расположен список выполненных тестов, заголовок вверху посередине, отображающий средний результат
за все выполненные когда-либо тесты. Также в левом нижнем углу отображается результат (в процентах) выполнения 
выбранного в списке теста. Также присутствуют виджеты поиска теста в списке и кнопка "Показать все", демонстрирующая
все тесты в списке.
						Изменить пароль
Окно имеет три строки - старого пароля (неизменяемая, значение - пароль пользователя), новый пароль и повтор нового 
пароля, а также кнопку "Сохранить", нажатие на которую, при соответствии пароля правилам (отличается от старого, в 
последних двух строках пароль равен), выводит сообщение о сообщении пароля в status_label и просьбу проверить 
введённые данные, сохраняет новый пароль. Дабы ещё раз изменить пароль, пользователю нужно вернуться в начальное
окно и заново нажать "изменить пароль"


**************************************************ОПИСАНИЕ ПРОГРАММНОЙ ЧАСТИ********************************************
Некоторые общие положения:
Приложение написано с помощью PyQt5.
Все изображения, используемые программой, лежат, как нетрудно догадаться, в папке "images", ui файлы лежат в папке
ui_files.
					УСТРОЙСТВО БАЗЫ ДАННЫХ
Таблица users содержит колонки:
	id
	login: уникальный элемент
	pass: пароль пользователя, ненулевой элемент
	name
	surname
	tests_results: JSON-объект, список выполненных учеником тестов и их результатов; элементами
списка являются кортежи вида (название_теста, результат_в_процентах).
Данные каждой колонки ненулевые, кроме completed_tests

Таблица tests содержит колонки:
	id
	title: уникальный элемент
	tasks_id_json: JSON-объект, список id заданий

Таблица tasks содержит колонки:
	id
	name: уникальный элемент
	json_data: JSON-объект, словарь, имеющий ключи question (содержание вопроса), variants (
	           список вариантов ответа, если они отсустствуют - пустой список), right_ans (
		   верный ответ)

				ОПИСАНИЕ ПРОГРАММНОГО КОДА

Приложение написано с помощью PyQt5.

Код разделён на три модуля - main, student_window и commin_classes. Модуль "main.py" содержит описание класса 
приветственного окна, а также всех классов, необходимых для функционирования учительского окна; модуль 
"student_window.py" содержит описание всех классов, требуемых ученическому окну; модуль "common_classes.py"
содержит классы, используемых в обоих окнах - и учительском, и ученическом. Все классы common_classes.py 
импортируются в модуль student_window.py, который, в свою очередь, импортируется в модуль main.py целиком.
Все классы, описанные в программе, наследуются от QWidget.
В каждом классе, кроме InfoWindow (см. модуль common_classes.py) присутствует функция initUi, в которую выносится
основная инициализация класса - связь слотов с сигналами виджетов, установка заднего изображения и прочее.

Рассмотрим классы данных модулей детальнее:
	МОДУЛЬ "common_classes.py"
class InfoWindow
	functions:
		def __init__(self, info, parent, title='Инструкция')
Детальное описание:
Создаёт простое окошко, единственное содержимое которое - сообщение для пользователя и кнопка "понятно". Этот
класс помогает передавать инструкции и прочую информацию для пользователя. При инициализации принимает 
аргументы info (информация, которую следует показать пользователю, в форме текста), parent (для инициализации
класса и задания флага Qt.Window, в противном случае окно не открывается), title (заголовок окна. По умолчанию = 
'Инструкция')

***

class ChooseTestWindow
	functions:
		def initUi(self)
		def find_test(self)
		def show_everyone(self)
		def show_instruction(self)
		def find_forbidden_tests(self)
		def keyPressEvent(self, event)
		def return_parent(self)
Детальное описание:
Класс создаёт окно выбора теста - для учителя на изменение теста или для ученика для прохождения теста. Поскольку 
окна идентичны в плане внешнего вида, требуется лишь изменить обработку этих окон, чем и занимаются функции 
класса. При инициализации принимает 2 параметра: parent(родительский виджет для  возможности открытия его) и 
sender_win (опционально, если не указывать этот именованный аргумент, класс будет считать, что окно-отправитель это
учительское окно. Возможны значения 'teacher' - дефолтное и 'student', если вызывает окно студент).

find_forbidden_tests(self) - вычисляет список запрещённых для пользователя тестов и возвращает его. У учителя этот
список пуст, у ученика соответствует всем пройдённым когда-либо тестам.

find_test(self) - проверяет корректность введённых пользователем данных, находит в базе данных и выводит в 
список все тесты, которые разрешены для взаимодействия пользователю, имя которых соответствует введённым
пользоателем данным. Вызывается при нажатии на кнопку поиска теста.

show_everyone(self) - находит в БД и выводит в список все разрешённые пользователю для взаимодействия тесты.

show_instruction(self) - инициализирует окно инструкции и демонстрирует его пользователю. Вызывается при нажатии
на кнопку инструкции.

keyPressEvent(self) - можно сказать, "ключевая" функция класса. Проверяет, кто был отправителем запроса на 
инициализацию класса, и выполняет в зависимости от этого различные действия - либо открывает учителю окно редакции
теста, либо открывает ученику окно прохождения теста. Для демонстрации окна используется атрибут action_widget 
"родителя" - при инициализации данного класса для корректной работы программы в родительском виджете должен 
быть проинициализирован аттрибут action_widget, то есть объект класса, описаывающий требуемое окно.



	МОДУЛЬ "main.py"

class HelloWindow
	functions:
		def initUi(self)	
		def find_user(self)
		def keyPressEvent(self, event)
		def closeEvent(self, event)
Детальное описание:
Класс, создающий стартовое окно. При инициализации объекта класса не принимает никаких аргументов.

find_user(self) - функция, вызываемая при нажатии на "Enter" или на соответствующую кнопку окна. Функция проверяет
корректность введённых данных и ищет пользователя в БД. При ненахождении пользователя, вводе неверного пароля
выводит соответствующее сообщение в атрибут self.status_label - статусная строка, объект QLabel. В случае ввода 
корректного имени и пароля закрывает приветственное окно и открывает требуемое пользователю окно взаимдействия.
При открытии ученического окна (см. class StudentWindow в модулe student_window.py

keyPressEvent(self, event) - обработчик нажатия на клавишу клавиатуры - если клавишей является Enter (любой из двух),
вызывает функцию find_user(self)

closeEvent(self, event) - обработчик события закрытия окна. Класс имеют такую структуры, что открытие
пользовательского окна происходит после закрытия объекта класса HelloWindow - в функции find_user, в случае успешной
авторизации, атрибуту sefl.authorization присваивается значение True (дефолтное - False), и закрывается приветственное
окно. В closeEvent, в случае успешной авторизации (что проверяется значением self.authorization), инициализируется и 
вызывается пользовательское окно.

***

class TeacherWindow
	functions:	
		def initUi(self)
		def btn_clicked(self)	
Детальное описание:
Класс, создающий стартовое окно учителя. При инициализации объекта класса не принимает никаких аргументов.

btn_clicked(self) - функция, вызываемая при нажатии на одну из кнопок главного учительского окна и открывающая одно
из дочерних окон - ChooseAction(parent, type), DeleteTestWindow(parent), DeleteEditStudentWindow(parent, action_protocol),
TeacherStatisticsWindow(parent), EditPersonalInfoWindow(parent).

***

class ChooseAction
	functions: 
		def initUi(self)
		def load_widget(self)

Детальное описание:
Класс, создающий окно выбора действия. Поскольку в учительском окне присутствуют кнопку "создать/изменить тест",
"добавить/удалить ученика", необходимо уточнить у пользователя, если он нажал на эту кнопку, что же он хочет сделать.
При инициализации принимает два аргумента: parent - родительский виджет (для возможности функционирования 
кнопки "назад" и type - тип выбора (возможные значения - 'ученика', 'тест'). Тип выбора используется в функции 
load_widget и в условной конструкции, и при описании текста QLabel посреди окна - поэтому значения должны, при 
редакции кода, оставаться 'ученика' и 'тест'.

load_function(self) - основная функция класса, вызываемая при нажатии на кнопку "подтвердить" окна выбора. Загружает
для пользователя, в зависимости от его выбора, один из 4-ёх видов окон - добавления/удаления ученика, создания/
изменения теста, описанных в классах AddStudentInfoWindow(parent), DeleteEditStudentInfo(parent, 'delete'), 
TestCreationRedactionWindow(parent, 'edit'), TestCreationRedactionWindow(parent, 'create') соответственно.

***

class ConfirmWindow
	functions:
		def initUi(self)
		def act_with_user(self)
		def closeEvent(self, event)

Детальное описание:
Данный класс создаёт окно подтверждения действий пользователя. Поскольку данная функция требуется во многих 
окнах приложения (и, соответственно, может вызываться из нескольких классов), и всякий вызов лишь незначительно
отличается от остальных, все окна подтверждения были как бы объединены в единый класс, функция act_with_user
которго смотрит, какое окно были вызвано и обрабатывает нажатие пользователя на кнопку. Также, в зависимости от 
типа заданного окна, класс может быть по разному инициализирован - то есть может быть погружен один из двух
ui файлов: либо simple_confirn_win.ui, либо confirm_win.ui. При инициализации принимает аргументы type (тип 
запрашиваемого окна), parent(окно-родитель, для возможности нажатия на кнопку "назад"), *args и **kwargs. 
type может принимать одно из данных значений: 'create_question', 'delete_question', 'delete_test', 'удалить', 'добавить',
'edit', 'edit_personal_info'.
Возможные ключи словаря **kwargs: 'user_message', 'to_close', блок (id, login, name, surname), блок(login, name, surname,
password)
Возможные зачения args будут описаны в ходе пояснения видов окон подтверждения 

***

class AddingQuestionWindow
	functions:
		def initUi(self)

***

class ShowTaskInfoWindow
	functions:
		def initUi(self)
***

class TestCreationRedactionWindow
	functions:
		def initUi(self)
***

class DeleteTestWindow
	functions:
		def initUi(self)
***

class DeleteEditStudentWindow
	functions:
		def initUi(self)
***

class AddStudentInfoWindow
	functions:
		def initUi(self)

***

class TeacherStatisticsWindow
	functions:
		def initUi(self)
***

class EditPersonalInfoWindow
	functions:
		def initUi(self)
	

	МОДУЛЬ "student_window.py"
class StudentWindow
	functions: 
		def initUi(self)
		def complete_test(self)
		def change_password(self)
		def statistics(self)
Детальное описание: 
Главное окно ученика. 

complete_test(self) - функция, запускающаяся при нажатии на кнопку "пройти тест". Внутри функции вызыватся 
инициализация класса ChooseTestWindow с именованным аргументом sender_win='student', объект которого есть
окно выбора теста (см. МОДУЛЬ "common_classes.pt", ChooseTestWindow), а атрибуту self.action_window присваивается
значение "объект класса TetsPassing (зачем нужен атрубит self.action_window смотрите в документации к классу 
ChooseTestWindow).

change_password(self) - инициализирует и открывает окно смены пароля (ChangingPasswordWindow)

statistics(self) - инициализирует и открывает окно ученической статистики (StudentsStatisticsWindow)

***

class TestPassing
	functions: 
		def initUi(self)\

***

class ChangingPasswordWindow
	functions: 
		def initUi(self)

***

class SimpleConfirmWindow
	functions: 
		def initUi(self)

***

class StudentStatisticsWindow
	functions: 
		def initUi(self)

