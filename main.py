from PyQt5.QtWidgets import (QApplication, QTableWidgetItem)
from PyQt5.QtGui import QImage, QPalette, QBrush

from student_window import *


def return_parent(child, parent):
    parent.show()
    child.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class HelloWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window)
        uic.loadUi('ui_files/welcome_form.ui', self)
        self.authorization = False
        self.initUi()

    def initUi(self):
        self.setWindowTitle('Вход в систему')
        self.setWindowIcon(QIcon('images/icon.png'))

        self.pass_val.setEchoMode(QLineEdit.Password)

        self.show_pass.setIcon(QIcon('images/eye.png'))
        self.show_pass.pressed.connect(lambda: self.pass_val.setEchoMode(QLineEdit.Normal))
        self.show_pass.released.connect(lambda: self.pass_val.setEchoMode(QLineEdit.Password))

        self.con = sqlite3.connect('database.sqlite')

        sImage = QImage("images/base.jpg").scaled(QSize(self.width(), self.height()))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        self.setFixedSize(QSize(self.width(), self.height()))
        self.enter_btn.clicked.connect(self.find_user)

    def find_user(self):
        if self.login_val.text() == '' or self.pass_val.text() == '':
            self.status_label.setText('Введите данные для входа')
            self.status_label.setStyleSheet('border-style: solid; border-width: 1px; border-color: red;')
            return
        self.status_label.setText('')
        self.status_label.setStyleSheet('')

        cur = self.con.cursor()

        data = cur.execute(f"SELECT * FROM users"
                           f"   WHERE login = '{self.login_val.text().strip()}'"
                           ).fetchone()

        if not data:
            self.status_label.setText('Пользователь не найден')
            self.status_label.setStyleSheet('border-style: solid; border-width: 1px; border-color: red;')
            return
        elif str(data[2]) != self.pass_val.text():
            self.status_label.setText('Неверный пароль')
            return
        else:
            self.status_label.setText('Успешная авторизация!')
            self.authorization = True
            self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() + 1 == Qt.Key_Enter:
            self.find_user()

    def closeEvent(self, event):
        if self.authorization:
            if self.login_val.text().strip() == 'teacher':
                self.user_win = TeacherWindow()
            else:
                self.user_win = StudentWindow(self.login_val.text())
            self.user_win.show()
        self.con.close()


class TeacherWindow(QMainWindow):   
    def __init__(self):
        super().__init__()
        uic.loadUi('ui_files/teacher_ui/t_main_win.ui', self)
        self.initUi()

    def initUi(self):
        self.setFixedSize(QSize(self.width(), self.height()))

        self.setWindowTitle('Выберите действие')
        self.setWindowIcon(QIcon('images/icon.png'))

        self.create_change_test.clicked.connect(self.btn_clicked)
        self.del_test.clicked.connect(self.btn_clicked)
        self.edit_student_info.clicked.connect(self.btn_clicked)
        self.add_del_student.clicked.connect(self.btn_clicked)
        self.check_out_stat.clicked.connect(self.btn_clicked)
        self.edit_personal_info.clicked.connect(self.btn_clicked)

    def btn_clicked(self):
        if self.sender().text() == 'Создать/изменить тест':
            self.action_widget = ChooseAction(self, 'тест')
        elif self.sender().text() == 'Удалить тест':
            self.action_widget = DeleteTestWindow(self)
        elif self.sender().text() == 'Редактировать информацию об ученике':
            self.action_widget = DeleteEditStudentWindow(self, 'edit')
        elif self.sender().text() == 'Добавить/удалить ученика':
            self.action_widget = ChooseAction(self, 'ученика')
        elif self.sender().text() == 'Посмотреть статистику':
            self.action_widget = TeacherStatisticsWindow(self)
        else:
            self.action_widget = EditPersonalInfoWindow(self)
        self.action_widget.show()
        self.close()


class ChooseAction(QWidget):
    def __init__(self, parent, type):
        super().__init__()
        uic.loadUi('ui_files/teacher_ui/choose_action.ui', self)
        self.setWindowIcon(QIcon('images/icon.png'))
        self.parent = parent
        self.type = type
        self.initUi()

    def initUi(self):
        self.setWindowTitle('Выберите действие')

        self.object_type.setText(self.type)

        if self.type == 'ученика':
            self.open_protocol.addItems(['Добавить', 'Удалить'])
        else:
            self.open_protocol.addItems(['Изменить', 'Создать'])
        self.confirm_btn.clicked.connect(self.load_widget)
        self.return_btn.clicked.connect(lambda button, child=self, parent=self.parent: return_parent(child, parent))
        self.setFixedSize(QSize(self.width(), self.height()))

    def load_widget(self):
        if self.type == 'ученика':
            if self.open_protocol.currentText() == 'Добавить':
                self.user_widget = AddStudentInfoWindow(self)
            else:
                self.user_widget = DeleteEditStudentWindow(self, 'delete')
        else:
            if self.open_protocol.currentText() == 'Изменить':
                self.parent.action_win = TestCreationRedactionWindow(self, 'edit')
                self.user_widget = ChooseTestWindow(self.parent)
            else:
                self.user_widget = TestCreationRedactionWindow(self, 'create')
        self.user_widget.show()
        self.close()


class ConfirmWindow(QWidget):
    def __init__(self, type, parent, *args, **kwargs):
        super().__init__(parent, Qt.Window)
        self.action_protocol = type
        self.setWindowIcon(QIcon('images/icon.png'))

        if 'edit' in type or 'delete' in type or type == 'create_question':
            uic.loadUi('ui_files/simple_confirm_win.ui', self)
            if 'user_message' in kwargs.keys():
                self.message.setText(kwargs['user_message'])
            else:
                self.message.setText('Сохранить изменения?')
            self.closing_parent = kwargs['to_close']
            self.rows = list(args)
        else:
            self.values = kwargs
            uic.loadUi('ui_files/teacher_ui/confirm_win.ui', self)
        self.setWindowTitle('Подтвердите действие')
        self.parent = parent
        self.initUi()

    def initUi(self):
        self.message.setWordWrap(True)

        self.setFixedSize(QSize(self.width(), self.height()))
        if self.action_protocol == 'удалить' or self.action_protocol == 'добавить':
            self.message.setText(
                f'Вы уверены, что хотите {self.action_protocol} пользователя с указанными данными?')
            self.login.setText(self.values['login'])
            self.name.setText(self.values['name'])
            self.surname.setText(self.values['surname'])
        self.confirm_box.accepted.connect(self.act_with_user)
        self.confirm_box.rejected.connect(self.close)

    def act_with_user(self):
        if self.action_protocol == 'добавить':
            self.parent.status_label.setText('Пользователь успешно добавлен')
            self.parent.status_label.setStyleSheet('border-style: solid; border-width:'
                                                   ' 1px; border-color: green;')

            self.con = sqlite3.connect('database.sqlite')

            cur = self.con.cursor()

            try:
                cur.execute(
                    f"INSERT INTO users(login, pass, name, surname, tests_results) VALUES('{self.values['login']}', "
                    f"'{self.values['password']}', '{self.values['name']}', '{self.values['surname']}', '[]')"
                )
            except sqlite3.IntegrityError:
                self.parent.status_label.setText('Пользователь с указанными данными уже существует')
                self.parent.status_label.setStyleSheet('border-style: solid; border-width:'
                                                       ' 1px; border-color: red;')

            self.con.commit()

            self.con.close()
            self.close()
        elif self.action_protocol == 'удалить':
            self.parent.status_label.setText('Пользователь успешно удалён')
            self.parent.status_label.setStyleSheet('border-style: solid; border-width:'
                                                   ' 1px; border-color: green;')

            self.con = sqlite3.connect('database.sqlite')

            cur = self.con.cursor()

            cur.execute(f"DELETE FROM users"
                        f"  WHERE id={self.values['id']}"
                        )

            self.con.commit()

            self.con.close()
            self.close()

            self.parent.show_everyone()
        elif self.action_protocol == 'edit':
            con = sqlite3.connect('database.sqlite')

            cur = con.cursor()

            for elem in self.rows:
                cur.execute(f"UPDATE users"
                            f"  SET login = '{self.parent.students_table.item(elem, 1).text()}',"
                            f"  name = '{self.parent.students_table.item(elem, 2).text()}',"
                            f"  surname = '{self.parent.students_table.item(elem, 3).text()}'"
                            f"      WHERE id = {self.parent.students_table.item(elem, 0).text()}"
                            )

            con.commit()

            self.parent.status_label.setText('Данные успешно отредактированы')
            self.parent.status_label.setStyleSheet('border-style: solid; border-width: 1px; border-color: green;')

            self.close()
            if self.closing_parent:
                self.parent.close()
                self.parent.parent.show()
        elif 'edit' in self.action_protocol:
            con = sqlite3.connect('database.sqlite')

            cur = con.cursor()

            cur.execute(f"UPDATE users"
                        f"  SET name='{self.parent.name_val.text()}',"
                        f"  surname='{self.parent.surname_val.text()}',"
                        f"  pass='{self.parent.pass_val.text()}'"
                        f"      WHERE login='teacher'"

                        )

            con.commit()
            self.close()

            if self.closing_parent:
                self.parent.close()
                self.parent.parent.show()
        elif self.action_protocol == 'delete_test':
            con = sqlite3.connect('database.sqlite')

            cur = con.cursor()

            cur.execute(f"DELETE FROM tests"
                        f"  WHERE title = '{self.parent.tests_list.currentItem().text()}'"

                        )
            con.commit()

            self.parent.status_label.setText('Тест успешно удалён!')
            self.parent.status_label.setStyleSheet('border-style: solid; border-width: 1px; border-color: green;')

            self.parent.tests_list.takeItem(self.parent.tests_list.currentRow())
            self.close()
        elif self.action_protocol == 'delete_question':
            con = sqlite3.connect('database.sqlite')
            cur = con.cursor()
            cur.execute(f"DELETE FROM tasks"
                        f"  WHERE name = '{self.parent.question_base.currentItem().text()}'")
            self.parent.question_base.takeItem(self.parent.question_base.currentRow())
            self.parent.test_creation_sl.setText('Вопрос успешно удалён!')
            self.parent.test_creation_sl.setStyleSheet('border-style: solid; border-width: 1px; border-color: green;')
            con.commit()
            self.close()
        else:
            self.close()
            self.parent.close()

    def closeEvent(self, event):
        if 'edit' in self.action_protocol:
            if self.closing_parent:
                self.parent.close()
                self.parent.parent.show()


class AddingQuestionWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent, Qt.Window)
        uic.loadUi('ui_files/teacher_ui/create_question.ui', self)
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setFixedSize(QSize(self.width(), self.height()))
        self.parent = parent
        self.initUi()

    def initUi(self):
        self.instruction_btn.setIcon(QIcon('images/question.jpg'))
        self.instruction_btn.clicked.connect(self.show_info)
        self.return_btn.clicked.connect(self.confirm)
        self.close_btn.clicked.connect(self.confirm)
        self.create_btn.clicked.connect(self.create_question)
        self.add_var_btn.clicked.connect(self.add_variant)

    def show_info(self):
        instruction = 'Для создания вопроса введите всю требуемую информацию. ' \
                      'Если варианты ответа не будут введены система будет считать,' \
                      ' что это вопрос без вариантов ответа. При создании задания с ' \
                      'вариантами ответа нельзя указать < 2 вариантов. Для добавления варианта ' \
                      'ответа введите его в строку под "Заданые варианты ответа" и ' \
                      'нажмите кнопку "+". Тест не может содержать больше 8 вариантов ' \
                      'ответа. Для удаления варианта ответа выберите его в ' \
                      'списке и нажмите кнопку "Delete".'
        instr_win = InfoWindow(instruction, self)
        instr_win.show()

    def create_question(self):
        error_message = ''
        variants = list()
        for ind in range(self.variants_val.count()):
            variants.append(self.variants_val.item(ind).text())
        if self.name_val.text().strip() == '':
            error_message = 'Введите название вопроса'
        elif self.question_val.toPlainText().strip() == '':
            error_message = 'Введите содержание вопроса'
        elif self.right_ans_val.text().strip() == '':
            error_message = 'Введите правильный ответ'
        elif self.variants_val.count() == 1:
            error_message = 'Введите как минимум 2 варианта ответа'
        elif (self.right_ans_val.text().strip() not in variants) and len(variants) != 0:
            error_message = 'Правильный ответ должен содержаться в вариантах'
        elif len(variants) > 8:
            error_message = 'Тест не может содержать больше 8-ми вариантов ответа'
        self.status_label.setText(error_message)
        self.status_label.setStyleSheet('')
        if error_message:
            self.status_label.setStyleSheet('border-style: solid; border-width: 1px; border-color: red;')
            return
        new_question = {'question': self.question_val.toPlainText().strip(), 'variants': variants,
                        'right_ans': self.right_ans_val.text().strip()}
        con = sqlite3.connect('database.sqlite')
        cur = con.cursor()
        try:
            cur.execute(f"INSERT INTO tasks(name, json_data) VALUES(?, ?)",
                        (self.name_val.text().strip(), json.dumps(new_question)))
        except sqlite3.IntegrityError:
            self.status_label.setText('Вопрос с таким названием уже существует')
            self.status_label.setStyleSheet('border-style: solid; border-width: 1px; border-color: red;')
            return

        con.commit()

        self.status_label.setText('Вопрос успешно добавлен!')
        self.status_label.setStyleSheet('border-style: solid; border-width: 1px; border-color: green;')
        self.parent.test_questions.addItem(self.name_val.text().strip())

        self.name_val.setText('')
        self.question_val.clear()
        self.variants_val.clear()
        self.right_ans_val.setText('')

    def add_variant(self):
        current_vars = list()
        for ind in range(self.variants_val.count()):
            current_vars.append(self.variants_val.item(ind).text())
        self.status_label.setText('')
        self.status_label.setStyleSheet('')
        if self.new_var_val.text().strip() == '':
            self.status_label.setText('Для добавления варианта ответа запишите его')
            return
        if self.new_var_val.text().strip() in current_vars:
            self.status_label.setText('Данный вариант ответа уже добавлен')
            self.status_label.setStyleSheet('border-style: solid; border-width: 1px; border-color: red;')
            return
        self.variants_val.addItem(self.new_var_val.text().strip())
        self.new_var_val.setText('')

    def confirm(self):
        if self.name_val.text().strip() != '' or self.question_val.toPlainText().strip() != '' or \
                self.variants_val.count() != 0 or self.right_ans_val.text().strip() != '':
            confirm_win = ConfirmWindow('create_question', self,
                                        user_message='У вас остались несохранённые '
                                                     'данные. Выйти из окна создания?',
                                        to_close=False)
            confirm_win.show()
        else:
            self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            if self.variants_val.currentRow() != -1:
                self.variants_val.takeItem(self.variants_val.currentRow())


class ShowTaskInfoWindow(QWidget):
    def __init__(self, parent, data):
        super().__init__(parent, Qt.Window)
        self.setWindowIcon(QIcon('images/icon.png'))
        uic.loadUi('ui_files/teacher_ui/task_info.ui', self)
        self.setFixedSize(QSize(self.width(), self.height()))
        self.id_val.setText(str(data[0]))
        self.name_val.setText(data[1])
        self.question_val.insertPlainText(data[2]['question'])
        if len(data[2]['variants']) == 0:
            self.variants_val.addItems(['Варианты ответа не заданы'])
        else:
            self.variants_val.addItems(data[2]['variants'])
        self.right_ans_val.setText(data[2]['right_ans'])
        self.close_btn.clicked.connect(self.close)


class TestCreationRedactionWindow(QWidget):
    def __init__(self, parent, action_protocol):
        super().__init__()
        uic.loadUi('ui_files/teacher_ui/test_creation.ui', self)
        if action_protocol == 'create':
            self.setWindowTitle('Создание теста')
        else:
            self.del_question_btn.hide()
            self.setWindowTitle('Редактирование теста')
        self.parent = parent
        self.action_protocol = action_protocol
        self.setFixedSize(self.width(), self.height())
        self.initUi()

    def initUi(self):
        self.return_btn.clicked.connect(lambda button, child=self, parent=self.parent: return_parent(child, parent))
        self.setWindowIcon(QIcon('images/icon.png'))
        self.instruction_btn.setIcon(QIcon('images/question.jpg'))
        if self.action_protocol == 'create':
            self.fill_tasks_list()
            self.create_test_btn.clicked.connect(
                lambda button, action_protocol='create': self.create_edit_test(action_protocol=action_protocol))
        else:
            self.testname_val.setReadOnly(True)
            self.create_test_btn.setText('Изменить')
            self.create_test_btn.clicked.connect(
                lambda button, act_protocol='edit': self.create_edit_test(action_protocol=act_protocol))
        self.question_base.itemDoubleClicked.connect(lambda item: self.give_task_info(item))
        self.test_questions.itemDoubleClicked.connect(lambda item: self.give_task_info(item))
        self.add_question_btn.clicked.connect(self.add_question)
        self.instruction_btn.clicked.connect(self.show_instruction)
        self.delete_task_btn.clicked.connect(self.delete_test_task)
        self.create_question_btn.clicked.connect(self.create_question)
        self.del_question_btn.clicked.connect(self.delete_base_task)

    def add_question(self):
        self.test_creation_sl.setText('')
        self.test_creation_sl.setStyleSheet('')
        self.total_sl.setText('')
        self.total_sl.setStyleSheet('')
        self.test_task_sl.setText('')
        self.test_task_sl.setStyleSheet('')
        if self.question_base.currentRow() == -1:
            self.test_task_sl.setText('Задание не выбрано')
            self.test_task_sl.setStyleSheet('border-style: solid; border-width: 1px; border-color: red;')
            return

        self.test_questions.addItem(self.question_base.currentItem().text())

        self.question_base.takeItem(self.question_base.currentRow())

    def give_task_info(self, item):
        cur = sqlite3.connect('database.sqlite').cursor()

        data = list(cur.execute(f"SELECT * FROM tasks"
                                f"   WHERE name = '{item.text()}'"
                                ).fetchone())

        data[2] = json.loads(data[2])

        info = ShowTaskInfoWindow(self, data)
        info.show()

    def delete_test_task(self):
        self.test_creation_sl.setText('')
        self.test_creation_sl.setStyleSheet('')
        self.total_sl.setText('')
        self.total_sl.setStyleSheet('')
        self.test_task_sl.setText('')
        self.test_task_sl.setStyleSheet('')
        if self.test_questions.currentRow() == -1:
            self.test_task_sl.setText('Задание не выбрано')
            self.test_task_sl.setStyleSheet('border-style: solid; border-width: 1px; border-color: red;')
            return

        self.question_base.addItem(self.test_questions.currentItem().text())

        self.test_questions.takeItem(self.test_questions.currentRow())

    def delete_base_task(self):
        if self.question_base.currentRow() == -1:
            info = 'Для удаления вопроса из БД выберите его в таблице' \
                   ' справа и нажмите кнопку "удалить вопрос из базы".'
            info_win = InfoWindow(info, self)
            info_win.show()
            return
        confirm_win = ConfirmWindow('delete_question', self, user_message="Подтвердите удаление", to_close=False)
        confirm_win.show()

    def create_edit_test(self, **kwargs):
        action_protocol = kwargs['action_protocol']
        self.test_task_sl.setText('')
        self.test_task_sl.setStyleSheet('')
        self.test_creation_sl.setText('')
        self.test_creation_sl.setStyleSheet('')

        if self.testname_val.text().strip() == '' and action_protocol == 'create':
            self.test_task_sl.setText('Название теста не задано!')
            self.test_task_sl.setStyleSheet('border-style: solid; border-width: 1px; border-color: red;')
            return
        if self.test_questions.count() == 0:
            self.test_creation_sl.setText('В тест не добавлены вопросы')
            self.test_creation_sl.setStyleSheet('border-style: solid; border-width: 1px; border-color: red;')
            return
        con = sqlite3.connect('database.sqlite')
        cur = con.cursor()
        tasks_names = list()
        for ind in range(self.test_questions.count()):
            tasks_names.append(self.test_questions.item(ind).text())
        data = cur.execute(f"SELECT id FROM tasks"
                           f"   WHERE name IN ({('?, ' * len(tasks_names))[:-2]})", (*tasks_names,)
                           ).fetchall()
        data = list(data)
        for i in range(len(data)):
            data[i] = data[i][0]
        data = json.dumps(data)
        if action_protocol == 'edit':
            test_questions = cur.execute(f"SELECT tasks_id_json FROM tests"
                                         f"    WHERE title = '{self.testname_val.text()}'"

                                         ).fetchone()[0]
            if test_questions == data:
                self.total_sl.setText('Внесите изменения  в тест')
                return
        if action_protocol == 'create':
            try:
                cur.execute(f"INSERT INTO tests(title, tasks_id_json) VALUES('{self.testname_val.text().strip()}',"
                            f"'{data}')")

                self.total_sl.setText('Тест успешно создан!')
                self.total_sl.setStyleSheet('border-style: solid; border-width: 1px; border-color: green;')
                self.testname_val.setText('')

                self.question_base.clear()
                self.test_questions.clear()

                self.fill_tasks_list()
            except sqlite3.Error:
                self.total_sl.setText('Тест с таким именем уже существует!')
                self.total_sl.setStyleSheet('border-style: solid; border-width: 1px; border-color: red;')
        else:
            cur.execute(f"UPDATE tests"
                        f"  SET tasks_id_json = '{data}'"
                        f"  WHERE title = '{self.testname_val.text().strip()}'"
                        )

            self.total_sl.setText('Тест успешно отредактирован!')
            self.total_sl.setStyleSheet('border-style: solid; border-width: 1px; border-color: green;')

        con.commit()

    def show_instruction(self):
        instruction = 'Для добавления вопроса в свой тест, выберите его в ' \
                      'правой таблице одиночным нажатием мыши и нажмите на ' \
                      'кнопку "Добавить вопрос в тест". Удаление выглядит ' \
                      'аналогично - выберите в таблице слева вопрос и нажмите ' \
                      'кнопку "Удалить задание из теста". Если вы хотите посмотреть' \
                      ' более подробную информацию по вопросу (текст вопроса, ' \
                      'варианты ответа и верный ответ), активируйте соответствующую ' \
                      'ячейку в таблице двойным кликом.'
        instr_win = InfoWindow(instruction, self)
        instr_win.show()

    def fill_tasks_list(self, exclude=False):
        cur = sqlite3.connect('database.sqlite').cursor()

        if not exclude:
            data = cur.execute(f"SELECT name FROM tasks"
                               ).fetchall()
        else:
            included_questions = list()
            for ind in range(self.test_questions.count()):
                included_questions.append(self.test_questions.item(ind).text())
            data = cur.execute(f"SELECT name FROM tasks"
                               f"   WHERE name NOT IN ({('?, ' * len(included_questions))[:-2]})",
                               (*included_questions,)
                               ).fetchall()

        for elem in data:
            self.question_base.addItem(elem[0])

    def create_question(self):
        creation_win = AddingQuestionWindow(self)
        creation_win.show()


class DeleteTestWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi('ui_files/teacher_ui/delete_test.ui', self)
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setFixedSize(QSize(self.width(), self.height()))
        self.parent = parent
        self.initUi()

    def initUi(self):
        cur = sqlite3.connect('database.sqlite').cursor()

        data = cur.execute("SELECT title FROM tests"
                           ).fetchall()

        self.instruction_btn.setIcon(QIcon('images/question.jpg'))
        self.return_btn.clicked.connect(lambda button, child=self, parent=self.parent: return_parent(child, parent))

        for elem in data:
            self.tests_list.addItem(elem[0])

        self.instruction_btn.clicked.connect(self.show_instruction)
        self.del_btn.clicked.connect(self.delete)
        self.tests_list.currentItemChanged.connect(lambda item: self.load_questions(item))
        self.questions_list.itemDoubleClicked.connect(lambda item: self.give_task_info(item))  # !!!!!

    def delete(self):
        if self.tests_list.currentRow() == -1:
            self.status_label.setText('Тест для удаления не выбран')
            self.status_label.setStyleSheet('border-style: solid; border-width: 1px; border-color: red;')
            return
        self.status_label.setText('')
        self.status_label.setStyleSheet('')
        confirm_win = ConfirmWindow('delete_test', self,
                                    user_message=f'Удалить тест {self.tests_list.currentItem().text()}?',
                                    to_close=False)
        confirm_win.show()

    def load_questions(self, item):
        self.questions_list.clear()

        cur = sqlite3.connect('database.sqlite').cursor()
        data = cur.execute(f"SELECT tasks_id_json FROM tests"
                           f"   WHERE title = '{item.text()}'"
                           ).fetchone()
        data = tuple(json.loads(data[0]))
        tasks_data = cur.execute(f"SELECT name FROM tasks"
                                 f"    WHERE id IN ({('?, ' * len(data))[:-2]})",
                                 data
                                 ).fetchall()
        for elem in tasks_data:
            self.questions_list.addItem(elem[0])

    def give_task_info(self, item):
        cur = sqlite3.connect('database.sqlite').cursor()

        data = list(cur.execute(f"SELECT * FROM tasks"
                                f"   WHERE name = '{item.text()}'"
                                ).fetchone())

        data[2] = json.loads(data[2])

        info = ShowTaskInfoWindow(self, data)
        info.show()

    def show_instruction(self):
        instruction = 'Для удаления теста выберите его в списке перед вами и нажмите кнопку "удалить". ' \
                      'Если вы не видите перед собой тестов, это значит, что вы не создали ещё ни одного ' \
                      'теста. \n' \
                      'Информацию о вопросе выбранного теста можно получить, кликнув по нему дважды в таблице' \
                      ' справа'
        instr_win = InfoWindow(instruction, self)
        instr_win.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() + 1 == Qt.Key_Enter:
            self.delete()


class DeleteEditStudentWindow(QWidget):
    def __init__(self, parent, action_protocol):
        super().__init__()
        self.setWindowIcon(QIcon('images/icon.png'))
        uic.loadUi('ui_files/teacher_ui/delete_edit_student.ui', self)
        if action_protocol == 'edit':
            self.setWindowTitle('Редактирование информации об учениках')
        else:
            self.setWindowTitle('Удаление ученика')
        self.action_protocol = action_protocol
        self.initUi()
        self.parent = parent

    def initUi(self):
        self.return_btn.clicked.connect(self.return_parent)
        self.setFixedSize(QSize(self.width(), self.height()))

        self.action_btn.setText('Удалить')
        self.students_table.setHorizontalHeaderLabels(['id', 'логин', 'имя', 'фамилия'])
        if self.action_protocol == 'edit':
            self.setWindowTitle('Редактирование информации об ученике')
            self.instruction_label.setText('Отредактируйте информацию в таблице и нажмите кнопку "подтвердить"')
            self.action_btn.setText('Подтвердить')
            self.action_btn.clicked.connect(self.edit_delete_student)
            self.search_protocol.addItems(['id', 'логину', 'имени', 'фамилии'])

            self.cnt = 0

            self.students_table.cellChanged.connect(self.record_editions)
            self.edited = set()  # list of rows with user's edits

            self.find_btn.clicked.connect(self.find_with_parameter)
            self.show_everyone_btn.clicked.connect(self.show_everyone)

            self.show_everyone()
        else:
            self.instruction_label.setText(
                'Для удаления выберите логин ученика в таблице и нажмите кнопку "удалить"')
            self.show_everyone_btn.clicked.connect(self.show_everyone)
            self.find_btn.clicked.connect(self.find_with_parameter)
            self.show_everyone()

            self.action_btn.clicked.connect(self.edit_delete_student)

            self.search_protocol.addItems(['id', 'логину', 'имени', 'фамилии'])
            self.students_table.setHorizontalHeaderLabels(['id', 'логин', 'имя', 'фамилия'])
        self.students_table.verticalHeader().hide()

    def fill_table(self, data):
        self.students_table.setRowCount(len(data))
        self.students_table.setColumnCount(4)

        for i in range(len(data)):
            for j in range(4):
                item = QTableWidgetItem(str(data[i][j]))
                if self.action_protocol == 'delete' or j == 0:
                    item.setFlags(Qt.ItemIsEnabled)
                self.students_table.setItem(i, j, item)

        # self.students_table.resizeColumnsToContents()

    def show_everyone(self):
        self.search_val.setText('')
        self.find_status_label.setText('')
        self.find_status_label.setStyleSheet('')
        con = sqlite3.connect('database.sqlite')

        cur = con.cursor()

        data = cur.execute(f"SELECT id, login, name, surname FROM users"
                           f"   WHERE login NOT LIKE 'teacher'"
                           ).fetchall()

        self.fill_table(data)

    def find_with_parameter(self):
        if self.search_val.text() == '':
            self.find_status_label.setText('Пустой параметр поиска')
            self.find_status_label.setStyleSheet('border-style: solid; border-width: 1px; border-color: red;')
            return
        elif not self.search_val.text().strip().isdigit() and self.search_protocol.currentText() == 'id':
            self.find_status_label.setText('id может быть только числом')
            self.find_status_label.setStyleSheet('border-style: solid; border-width: 1px; border-color: red;')
            return
        self.find_status_label.setText('')
        self.find_status_label.setStyleSheet('')
        con = sqlite3.connect('database.sqlite')

        cur = con.cursor()

        if self.search_protocol.currentText() == 'id':
            find_protocol = 'id'
        elif self.search_protocol.currentText() == 'логину':
            find_protocol = 'login'
        elif self.search_protocol.currentText() == 'имени':
            find_protocol = 'name'
        else:
            find_protocol = 'surname'

        data = cur.execute(f"SELECT id, login, name, surname from users"
                           f"   WHERE login NOT LIKE 'teacher' AND "
                           f"   {find_protocol} LIKE '%{self.search_val.text().strip()}%'"
                           ).fetchall()

        if not len(data):
            self.find_status_label.setText('По вашему запросу ничего не нашлось')
            self.students_table.setRowCount(0)
            self.students_table.setColumnCount(0)
        else:
            self.fill_table(data)

    def edit_delete_student(self):
        if self.action_protocol == 'delete':
            if self.students_table.currentRow() != -1:
                self.status_label.setText('')
                self.status_label.setStyleSheet('')

                confirm_win = ConfirmWindow('удалить', self,
                                            id=self.students_table.item(self.students_table.currentRow(), 0).text(),
                                            login=self.students_table.item(self.students_table.currentRow(),
                                                                           1).text(),
                                            name=self.students_table.item(self.students_table.currentRow(),
                                                                          2).text(),
                                            surname=self.students_table.item(self.students_table.currentRow(),
                                                                             3).text(), to_close=False)
                confirm_win.show()
            else:
                self.status_label.setText('Пользователь не выбран')
                self.status_label.setStyleSheet('border-style: solid; border-width: 1px; border-color: red;')
        else:
            con = sqlite3.connect('database.sqlite')

            cur = con.cursor()

            flag = False
            self.cnt = self.students_table.rowCount() * 4
            for elem in self.edited:
                data = cur.execute(f"SELECT login, name, surname FROM users"
                                   f"   WHERE id = {self.students_table.item(elem, 0).text()}"

                                   ).fetchall()
                for j in range(1, 4):
                    if self.students_table.item(elem, j).text() != data[0][j - 1]:
                        flag = True
                        break
                if flag:
                    break
            if len(self.edited) == 0 or not flag:
                self.status_label.setText('Данные в таблице не отредактированны')
                self.status_label.setStyleSheet('border-style: solid; border-width: 1px; border-color: red;')
                return
            self.status_label.setText('')
            self.status_label.setStyleSheet('')
            confirm_win = ConfirmWindow('edit', self, *self.edited, to_close=False)
            confirm_win.show()

    def record_editions(self):
        self.cnt += 1
        if self.cnt > self.students_table.rowCount() * 4:
            self.edited.add(self.students_table.currentRow())

    def return_parent(self):
        if self.action_protocol == 'edit':
            con = sqlite3.connect('database.sqlite')

            cur = con.cursor()

            flag = False
            for elem in self.edited:
                data = cur.execute(f"SELECT login, name, surname FROM users"
                                   f"   WHERE id = {self.students_table.item(elem, 0).text()}"

                                   ).fetchall()
                for j in range(1, 4):
                    if self.students_table.item(elem, j).text() != data[0][j - 1]:
                        flag = True
                        break
                if flag:
                    break
            if flag:
                confirm_win = ConfirmWindow('edit', self, *self.edited, to_close=True)
                confirm_win.show()
            else:
                self.close()
                self.parent.show()
        else:
            self.close()
            self.parent.show()


class AddStudentInfoWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi('ui_files/teacher_ui/add_student.ui', self)
        self.setWindowTitle('Добавление ученика')
        self.setWindowIcon(QIcon('images/icon.png'))
        self.initUi()
        self.parent = parent

    def initUi(self):
        self.return_btn.clicked.connect(self.return_parent)
        self.setFixedSize(QSize(self.width(), self.height()))

        self.action_btn.clicked.connect(self.add_student)

        self.pass_val.setEchoMode(QLineEdit.Password)
        self.repeat_pass.setEchoMode(QLineEdit.Password)

        self.show_pass.setIcon(QIcon('images/eye.png'))
        self.show_repeated_pass.setIcon(QIcon('images/eye.png'))

        self.show_pass.pressed.connect(lambda: self.pass_val.setEchoMode(QLineEdit.Normal))
        self.show_pass.released.connect(lambda: self.pass_val.setEchoMode(QLineEdit.Password))
        self.show_repeated_pass.pressed.connect(lambda: self.repeat_pass.setEchoMode(QLineEdit.Normal))
        self.show_repeated_pass.released.connect(lambda: self.repeat_pass.setEchoMode(QLineEdit.Password))

    def add_student(self):
        if self.login_val.text() == '' or self.pass_val.text() == '' or \
                self.name_val.text() == '' or self.surname_val.text() == '' \
                or self.repeat_pass.text() == '':
            self.status_label.setText('Введены не все данные')
            self.status_label.setStyleSheet('border-style: solid; border-width: 1px; border-color: red;')
            return
        elif self.repeat_pass.text() != self.pass_val.text():
            self.status_label.setText('Введённые пароли не совпадают')
            self.status_label.setStyleSheet('border-style: solid; border-width: 1px; border-color: red;')
            return
        self.status_label.setText('')
        self.status_label.setStyleSheet('')

        new_widget = ConfirmWindow('добавить', self, login=self.login_val.text(),
                                   name=self.name_val.text(),
                                   surname=self.surname_val.text(),
                                   password=self.pass_val.text(),
                                   to_close=False)

        new_widget.show()

    def return_parent(self):
        self.parent.show()
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() + 1 == Qt.Key_Enter:
            self.add_student()


class TeacherStatisticsWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi('ui_files/teacher_ui/teacher_statistics.ui', self)
        self.setFixedSize(QSize(self.width(), self.height()))
        self.setWindowIcon(QIcon('images/icon.png'))
        self.initUi()
        self.parent = parent

    def initUi(self):
        self.instruction_btn.setIcon(QIcon('images/question.jpg'))
        self.instruction_btn.clicked.connect(self.show_instruction)
        self.return_btn.clicked.connect(self.return_parent)
        self.find_test_btn.clicked.connect(self.find_test)
        self.tests_list.currentRowChanged.connect(lambda row: self.show_statistics(row))
        self.show_all_btn.clicked.connect(self.show_all)
        cur = sqlite3.connect('database.sqlite').cursor()  # вычисляем словарь, где ключи - имена тестов, значения -
        # списки кортежей вида (ученик; результат)

        self.tests = cur.execute(f"SELECT title FROM tests"  # создание описанного словаря
                                 ).fetchall()
        for ind in range(len(self.tests)):
            self.tests[ind] = self.tests[ind][0]
        self.students_result = cur.execute(f"SELECT name, surname, tests_results FROM users"
                                           f"   WHERE login != 'teacher'").fetchall()
        # self.students_result - "сырые" данные об именах и результатах учеников
        self.stud_res_dict = dict()

        for ind in range(len(self.students_result)):
            res_dict = dict()
            data = json.loads(self.students_result[ind][2])
            for i in range(len(data)):
                res_dict[data[i][0]] = data[i][1]
            self.stud_res_dict[self.students_result[ind][0] + ' ' + self.students_result[ind][1]] \
                = res_dict
            del res_dict
        # self.stud_res_dict - собранные в словарь словарей данные о результатах учеников
        students_names = list()
        for elem in self.students_result:
            students_names.append(elem[0] + ' ' + elem[1])
        self.data = dict()
        for elem in self.tests:
            self.data[elem] = list()
        # self.data = dict.fromkeys(self.tests, list())
        for test_name in self.data.keys():
            for student_name in students_names:
                if test_name not in self.stud_res_dict[student_name].keys():
                    self.data[test_name].append((student_name, 0))
                else:
                    self.data[test_name].append((student_name, self.stud_res_dict[student_name][test_name]))
        # создание описанного словаря завершено - self.data
        self.show_all()

    def show_statistics(self, row):
        self.status_label.setText('')
        self.status_label.setStyleSheet('')
        self.results_list.clear()
        if row == -1:
            return
        test_name = self.tests_list.item(row).text()
        if not test_name:
            return
        for elem in self.data[test_name]:
            if int(elem[1]) == elem[1]:
                percent_result = elem[0] + ': ' + str(int(elem[1])) + '%'
            else:
                percent_result = elem[0] + ': ' + str(elem[1]) + '%'
            self.results_list.addItem(percent_result)

    def show_all(self):
        self.tests_list.clear()
        self.status_label.setText('')
        self.status_label.setStyleSheet('')
        self.testname_val.setText('')
        for elem in self.tests:
            self.tests_list.addItem(elem)

    def show_instruction(self):
        instruction = 'Для нахождения теста в списке введите его название ' \
                      'в соответствующую строку и нажмите "найти".'
        instr_win = InfoWindow(instruction, self)
        instr_win.info.setStyleSheet('font-size: 14pt;')
        instr_win.show()

    def find_test(self):
        self.status_label.setText('')
        self.status_label.setStyleSheet('')
        if self.testname_val.text().strip() == '':
            self.status_label.setText('Введите имя теста')
            self.status_label.setStyleSheet('border-style: solid; border-width: 1px; border-color: red;')
            return
        self.tests_list.clear()
        for elem in self.tests:
            if self.testname_val.text().strip() in elem:
                self.tests_list.addItem(elem)
        if self.tests_list.count() == 0:
            self.status_label.setText('По вашему запросу ничего не нашлось')

    def return_parent(self):
        self.parent.show()
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() + 1 == Qt.Key_Enter:
            self.find_test()


class EditPersonalInfoWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setWindowIcon(QIcon('images/icon.png'))
        uic.loadUi('ui_files/teacher_ui/edit_personal_info.ui', self)
        self.setFixedSize(QSize(self.width(), self.height()))
        self.initUi()
        self.parent = parent

    def initUi(self):
        self.return_btn.clicked.connect(self.return_parent)
        self.show_pass.setIcon(QIcon('images/eye.png'))
        self.show_pass_2.setIcon(QIcon('images/eye.png'))

        self.pass_val_2.setEchoMode(QLineEdit.Password)
        self.pass_val.setEchoMode(QLineEdit.Password)

        self.show_pass.pressed.connect(lambda: self.pass_val.setEchoMode(QLineEdit.Normal))
        self.show_pass.released.connect(lambda: self.pass_val.setEchoMode(QLineEdit.Password))
        self.show_pass_2.pressed.connect(lambda: self.pass_val_2.setEchoMode(QLineEdit.Normal))
        self.show_pass_2.released.connect(lambda: self.pass_val_2.setEchoMode(QLineEdit.Password))

        con = sqlite3.connect('database.sqlite')

        cur = con.cursor()

        self.data = cur.execute(f"SELECT name, surname, pass FROM users"
                                f"   WHERE login = 'teacher'"
                                ).fetchone()

        self.name_val.setText(self.data[0])
        self.surname_val.setText(self.data[1])
        self.pass_val.setText(str(self.data[2]))

        self.action_btn.clicked.connect(self.edit)

    def edit(self):
        if self.name_val.text() == self.data[0] and \
                self.surname_val.text() == self.data[1] and self.pass_val.text() == str(self.data[2]):
            self.status_label.setText('Введённые данные не отличаются от изначальных')
            self.status_label.setStyleSheet('border-style: solid; border-width: 1px; border-color: red;')
            return
        if self.pass_val.text() != str(self.data[2]) and self.pass_val.text() != self.pass_val_2.text():
            self.status_label.setText('Новый пароль не повторён')
            self.status_label.setStyleSheet('border-style: solid; border-width: 1px; border-color: red;')
            return
        elif self.name_val.text() == '' or self.surname_val.text() == '' or self.pass_val.text() == '':
            self.status_label.setText('Не все строки заполнены')
            self.status_label.setStyleSheet('border-style: solid; border-width: 1px; border-color: red;')
            return
        confirm_win = ConfirmWindow('edit_personal_info', self, to_close=False)
        confirm_win.show()
        self.status_label.setText('')
        self.status_label.setStyleSheet('')

    def return_parent(self):
        con = sqlite3.connect('database.sqlite')

        cur = con.cursor()

        self.data = cur.execute(f"SELECT name, surname, pass FROM users"
                                f"   WHERE login = 'teacher'"
                                ).fetchone()

        if self.name_val.text() != self.data[0] or \
                self.surname_val.text() != self.data[1] or self.pass_val.text() != str(self.data[2]):
            confirm_win = ConfirmWindow('edit_personal_info', self, to_close=True)
            confirm_win.show()
        else:
            self.close()
            self.parent.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = HelloWindow()
    win.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
