import sys
from PyQt5.QtWidgets import (QMainWindow, QScrollArea,
                             QLineEdit, QRadioButton, QButtonGroup)

from common_classes import *


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class StudentWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.test_name = None
        uic.loadUi('ui_files/student_win.ui', self)
        self.setWindowIcon(QIcon('images/icon.png'))
        self.initUi()

    def initUi(self):
        self.complete_test_btn.clicked.connect(self.complete_test)
        self.statistics_btn.clicked.connect(self.statistics)
        self.change_pass_btn.clicked.connect(self.change_password)
        self.setFixedSize(self.width(), self.height())

    def complete_test(self):
        action_win = ChooseTestWindow(self, sender_win='student')
        self.action_win = TestPassing(action_win, None)
        action_win.label.setText('Тесты:')
        action_win.show()
        self.close()

    def change_password(self):
        self.change_pass_win = ChangingPasswordWindow(self)
        self.change_pass_win.show()
        self.close()

    def statistics(self):
        self.statistics_win = StudentStatisticsWindow(self)
        self.statistics_win.show()
        self.close()


class TestPassing(QWidget):
    def __init__(self, parent, test_name):
        super().__init__()
        self.parent = parent
        self.test_name = test_name
        uic.loadUi('ui_files/passing_test_win.ui', self)
        self.setWindowIcon(QIcon('images/icon.png'))
        self.initUi()

    def initUi(self):
        self.setFixedSize(self.width(), self.height())
        self.instruction_btn.setIcon(QIcon('images/question.jpg'))
        self.instruction_btn.clicked.connect(self.show_instruction)
        self.return_btn.clicked.connect(self.return_parent)
        self.finish_test_btn.clicked.connect(self.confirm_finishing)

    def init_child_widget(self):
        self.child_widget = QWidget(self)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setGeometry(50, 50, self.width() - 100, self.height() - 100)
        self.setStyleSheet('QScrollArea {border-style: none;}')
        self.scroll_area.setWidget(self.child_widget)

        self.child_widget.resize(400, 0)
        cur = sqlite3.connect('database.sqlite').cursor()
        tasks_id = cur.execute(f"SELECT tasks_id_json FROM tests"
                               f"   WHERE title = '{self.test_name}'"
                               ).fetchall()[0][0]
        tasks_id = json.loads(tasks_id)
        data = cur.execute(f"SELECT json_data FROM tasks"
                           f"   WHERE id IN ({('?, ' * len(tasks_id))[:-2]})",
                           tasks_id
                           ).fetchall()
        self.right_answers = list()
        for ind in range(len(data)):
            data[ind] = json.loads(data[ind][0])
            self.right_answers.append(data[ind]['right_ans'])
        current_elem_ordinate = 20
        self.answers_list = list()
        for elem in data:
            question = QLabel(elem['question'], self.child_widget)  # setting question
            question.setWordWrap(True)
            question.setFixedWidth(380)
            question.adjustSize()
            question.move(0, current_elem_ordinate)
            current_elem_ordinate += question.height() + 10  # setting question
            if len(elem['variants']) == 0:
                line_edit = QLineEdit(self.child_widget)
                self.answers_list.append(line_edit)
                line_edit.setGeometry(0, current_elem_ordinate, 100, 16)
                current_elem_ordinate += 36
            else:
                btn_group = QButtonGroup(self.child_widget)
                for elem1 in elem['variants']:
                    new_btn = QRadioButton(elem1, self.child_widget)
                    new_btn.setFixedWidth(200)
                    new_btn.adjustSize()
                    new_btn.move(0, current_elem_ordinate)
                    current_elem_ordinate += 5 + new_btn.height()
                    btn_group.addButton(new_btn)
                current_elem_ordinate += 20
                self.answers_list.append(btn_group)
            self.child_widget.resize(self.child_widget.width(), current_elem_ordinate)

    def show_instruction(self):
        instr = 'Тест не имеет ограничения по времени. Выполняйте ' \
                'задания, а по завершении теста нажмите кнопку "сдать на проверку". ' \
                'Учтите, что у вас будет только одна попытка, пересдать тест ' \
                'уже не представится возможным - поэтому нажимайте на кнопку ' \
                '"сдать на проверку" только тогда, когда вы удостоверитесь, что ' \
                'ответили на все возможные вопросы\n' \
                'Нажатие на кнопку "вернуться" сбросит все введённые ответы.'
        instr_win = InfoWindow(instr, self)
        instr_win.show()

    def finish_test(self):
        result = 0
        for ind in range(len(self.answers_list)):
            if type(self.answers_list[ind]) == QButtonGroup and self.answers_list[ind].checkedButton() is not None:
                result += (self.answers_list[ind].checkedButton().text() == self.right_answers[ind])
            elif type(self.answers_list[ind]) == QLineEdit:
                result += (self.answers_list[ind].text().strip() == self.right_answers[ind])
        con = sqlite3.connect('database.sqlite')
        cur = con.cursor()
        current_results_data = cur.execute(f"SELECT tests_results FROM users"
                                           f"   WHERE login = '{self.parent.parent.username}'"
                                           ).fetchone()[0]
        current_results_data = json.loads(current_results_data)
        current_results_data.append(tuple([self.test_name, round(result / len(self.right_answers) * 100, 2)]))
        current_results_data = json.dumps(current_results_data)
        cur.execute(f"UPDATE users"
                    f"    SET tests_results = '{current_results_data}'"
                    f"    WHERE login = '{self.parent.parent.username}'"

                    )
        con.commit()
        self.return_parent()

    def return_parent(self):
        self.parent.show_everyone()
        self.parent.show()
        self.close()

    def confirm_finishing(self):
        confirm_win = SimpleConfirmWindow(self)
        confirm_win.show()

    def closeEvent(self, event):
        delattr(self, 'scroll_area')
        delattr(self, 'child_widget')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() + 1 == Qt.Key_Enter:
            self.confirm_finishing()


class ChangingPasswordWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi('ui_files/change_student_pass.ui', self)
        self.parent = parent
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setFixedSize(QSize(self.width(), self.height()))
        self.initUi()

    def initUi(self):
        cur = sqlite3.connect('database.sqlite').cursor()
        password = cur.execute(f"SELECT pass FROM users"
                               f"   WHERE login = '{self.parent.username}'"

                               ).fetchone()[0]
        self.old_pass.setText(str(password))

        self.show_old_pass.setIcon(QIcon('images/eye.png'))
        self.show_new_pass.setIcon(QIcon('images/eye.png'))
        self.show_repeated_pass.setIcon(QIcon('images/eye.png'))

        self.show_old_pass.pressed.connect(lambda: self.old_pass.setEchoMode(QLineEdit.Normal))
        self.show_old_pass.released.connect(lambda: self.old_pass.setEchoMode(QLineEdit.Password))
        self.show_new_pass.pressed.connect(lambda: self.new_pass.setEchoMode(QLineEdit.Normal))
        self.show_new_pass.released.connect(lambda: self.new_pass.setEchoMode(QLineEdit.Password))
        self.show_repeated_pass.pressed.connect(lambda: self.repeated_pass.setEchoMode(QLineEdit.Normal))
        self.show_repeated_pass.released.connect(lambda: self.repeated_pass.setEchoMode(QLineEdit.Password))
        self.return_btn.clicked.connect(self.return_parent)
        self.save_btn.clicked.connect(self.save)

    def save(self):
        self.status_label.setText('')
        self.status_label.setStyleSheet('')
        if self.new_pass.text().strip() == '':
            self.status_label.setText('Введите новый пароль')
            return
        elif self.new_pass.text().strip() != self.repeated_pass.text().strip():
            self.status_label.setText('Введённые пароли не совпадают')
            self.status_label.setStyleSheet('border-style: solid; border-width: 1px; border-color: red;')
            return
        elif self.new_pass.text().strip() == self.old_pass.text():
            self.status_label.setText('Введённый пароль не отличается от старого.')
            return
        con = sqlite3.connect('database.sqlite')
        cur = con.cursor()
        cur.execute(f"UPDATE users"
                    f"   SET pass = '{self.new_pass.text().strip()}'"
                    f"   WHERE login = '{self.parent.username}'"
                    )
        con.commit()
        self.status_label.setText('Пароль успешно изменён. Проверьте, что он указан верно!')
        self.status_label.setStyleSheet('border-style: solid; border-width: 1px; border-color: green;')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() + 1 == Qt.Key_Enter:
            self.save()

    def return_parent(self):
        self.parent.show()
        self.close()


class SimpleConfirmWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent, Qt.Window)
        uic.loadUi('ui_files/simple_confirm_win.ui', self)
        self.setWindowTitle('Завершить тест?')
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setFixedSize(QSize(self.width(), self.height()))
        self.parent = parent
        self.initUi()

    def initUi(self):
        self.message.setText('Вы уверены, что хотите завершить тест? Возможности пройти его повторно у вас не будет!')
        self.message.setStyleSheet('font-size: 10pt')
        self.confirm_box.accepted.connect(self.finish)
        self.confirm_box.rejected.connect(self.close)

    def finish(self):
        self.close()
        self.parent.finish_test()


class StudentStatisticsWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi('ui_files/student_statistics.ui', self)
        self.setFixedSize(QSize(self.width(), self.height()))
        self.setWindowIcon(QIcon('images/icon.png'))
        self.parent = parent
        self.initUi()

    def initUi(self):
        self.return_btn.clicked.connect(self.return_parent)
        self.show_all_btn.clicked.connect(self.show_all)
        self.find_test_btn.clicked.connect(self.find_test)
        self.instruction_btn.clicked.connect(self.show_instruction)
        self.instruction_btn.setIcon(QIcon('images/question.jpg'))

        cur = sqlite3.connect('database.sqlite').cursor()
        self.results = cur.execute(f"SELECT tests_results FROM users"
                                   f"    WHERE login = '{self.parent.username}'"
                                   ).fetchone()[0]
        self.results = json.loads(self.results)
        average = 0
        for elem in self.results:
            average += elem[1]
        if len(self.results) != 0:
            if int(average / len(self.results)) == average / len(self.results):
                self.average_val.setText(str(int(average / len(self.results))) + '%')
            else:
                self.average_val.setText(str(round(average / len(self.results), 2)) + '%')
        self.completed_tests.currentRowChanged.connect(
            lambda ind: self.set_chosen_test_val(ind))

        self.show_all()

    def show_instruction(self):
        instr = 'Отсутствие тестов в списке означает, что вы ещё не прошли ни одного теста. ' \
                'Вы не можете посмотреть несуществующую статистику!'
        instr_win = InfoWindow(instr, self)
        instr_win.show()

    def set_chosen_test_val(self, ind):
        if self.results[ind][1] != int(self.results[ind][1]):
            self.chosen_test_res.setText(str(self.results[ind][1]) + '%')
        else:
            self.chosen_test_res.setText(str(int(self.results[ind][1])) + '%')

    def show_all(self):
        self.completed_tests.clear()
        self.status_label.setText('')
        self.status_label.setStyleSheet('')
        for ind in range(len(self.results)):
            self.completed_tests.addItem(self.results[ind][0])

    def find_test(self):
        self.status_label.setText('')
        self.status_label.setStyleSheet('')
        if self.find_test_val.text().strip() == '':
            self.status_label.setText('Введите информацию для поиска')
            self.status_label.setStyleSheet('border-style: solid; border-width: 1px; border-color: red;')
        self.completed_tests.clear()
        for i in range(len(self.results)):
            if self.find_test_val.text().strip() in self.results[i][0]:
                self.completed_tests.addItem(self.results[i][0])
        if self.completed_tests.count() == 0:
            self.status_label.setText('По вашему запросу ничего не нашлось')

    def return_parent(self):
        self.parent.show()
        self.close()
