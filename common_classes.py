import sqlite3
import json
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton)
from PyQt5.QtGui import QIcon
from PyQt5 import uic


class InfoWindow(QWidget):
    def __init__(self, info, parent, title="Инструкция"):
        super().__init__(parent, Qt.Window)
        self.setGeometry(500, 200, 400, 150)
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon('images/icon.png'))

        self.info = QLabel(self)
        self.info.setGeometry(20, 10, 360, 100)
        self.info.setText(info)
        self.info.setWordWrap(True)

        self.close_btn = QPushButton("Понятно", self)
        self.close_btn.setGeometry(300, 110, 80, 25)
        self.close_btn.clicked.connect(self.close)


class ChooseTestWindow(QWidget):
    def __init__(self, parent, sender_win='teacher'):
        super().__init__()
        uic.loadUi('ui_files/choose_test.ui', self)
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setWindowTitle('Выберите тест')
        self.sender_win = sender_win
        self.parent = parent
        self.initUi()

    def initUi(self):
        self.setFixedSize(QSize(self.width(), self.height()))
        self.return_btn.clicked.connect(self.return_parent)
        self.instruction_btn.setIcon(QIcon('images/question.jpg'))
        self.instruction_btn.clicked.connect(self.show_instruction)
        self.show_everyone()
        self.find_btn.clicked.connect(self.find_test)
        self.show_everyone_btn.clicked.connect(self.show_everyone)

    def find_test(self):
        self.status_label.setText('')
        self.status_label.setStyleSheet('')
        if self.testname_val.text().strip() == '':
            self.status_label.setText('Введите имя теста')
            self.status_label.setStyleSheet('border-style: solid; border-width: 1px; border-color: red;')
            return
        forbidden_tests = self.find_forbidden_tests()
        cur = sqlite3.connect('database.sqlite').cursor()
        try:
            data = cur.execute(f"SELECT title FROM tests"
                               f"   WHERE title LIKE '%{self.testname_val.text().strip()}%'"
                               ).fetchall()
            self.tests_list.clear()
            ind = 0
            while ind < len(data):
                if data[ind][0] in forbidden_tests:
                    data.pop(ind)
                    ind -= 1
                ind += 1
            if len(data) == 0:
                self.status_label.setText('По вашему запросу ничего не нашлось')
            else:
                for elem in data:
                    self.tests_list.addItem(elem[0])
        except sqlite3.OperationalError:
            self.status_label.setText('Некорректное имя теста')
            self.status_label.setStyleSheet('border-style: solid; border-width: 1px; border-color: red;')

    def show_everyone(self):
        self.tests_list.clear()
        forbidden_tests = self.find_forbidden_tests()
        cur = sqlite3.connect('database.sqlite').cursor()
        data = cur.execute(f"SELECT title FROM tests").fetchall()
        for elem in data:
            if self.sender_win == 'teacher' or (elem[0] not in forbidden_tests):
                self.tests_list.addItem(elem[0])

    def show_instruction(self):
        if self.sender_win == 'teacher':
            instr = 'Для изменения теста выберите его в списке и нажмите "Enter".'
        else:
            instr = 'Для прохождения теста выберите его в списке и нажмите "Enter".'
        instr_win = InfoWindow(instr, self)
        instr_win.show()

    def find_forbidden_tests(self):
        cur = sqlite3.connect('database.sqlite').cursor()
        if self.sender_win == 'student':
            forbidden_tests = cur.execute(f"SELECT tests_results FROM users"
                                          f"    WHERE login = '{self.parent.username}'"
                                          ).fetchone()[0]
            forbidden_tests = json.loads(forbidden_tests)
            for ind in range(len(forbidden_tests)):
                forbidden_tests[ind] = forbidden_tests[ind][0]
        else:
            forbidden_tests = list()

        return forbidden_tests

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() + 1 == Qt.Key_Enter:
            self.status_label.setText('')
            self.status_label.setStyleSheet('')
            if self.tests_list.currentRow() != -1:
                if self.sender_win == 'teacher':
                    self.parent.action_win.testname_val.setText(self.tests_list.currentItem().text())
                    cur = sqlite3.connect('database.sqlite').cursor()
                    tasks_id = cur.execute(f"SELECT tasks_id_json FROM tests"
                                           f"   WHERE title = '{self.parent.action_win.testname_val.text().strip()}'"
                                           ).fetchone()[0]
                    tasks_id = json.loads(tasks_id)
                    data = cur.execute(f"SELECT name FROM tasks"
                                       f"   WHERE id IN ({('?, ' * len(tasks_id))[:-2]})",
                                       (*tasks_id,)
                                       ).fetchall()
                    for ind in range(len(data)):
                        self.parent.action_win.test_questions.addItem(data[ind][0])
                    self.parent.action_win.fill_tasks_list(exclude=True)
                else:
                    self.parent.action_win.test_name = self.tests_list.currentItem().text()
                    self.parent.action_win.init_child_widget()
                self.parent.action_win.show()
                self.close()
            else:
                self.status_label.setText('Выберите тест')
                self.status_label.setStyleSheet('border-style: solid; border-width: 1px; border-color: red;')

    def return_parent(self):
        self.parent.show()
        self.close()
