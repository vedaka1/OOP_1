import sys
from PyQt5 import uic, QtCore
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from DBconsole import ExamDatabase


active_exam = ''
mark = 0
exam_number = 0


class Main(QDialog):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi("main.ui", self)
        self.exams_list.itemClicked.connect(self.clicked)
        self.label_name.setAlignment(QtCore.Qt.AlignCenter)
        self.add_btn.clicked.connect(self.go_to_add_exam)
        exams_list = []
        try:
            for exam in ExamDatabase():
                exams_list.append(str('{0} {1}'.format(exam.number, exam.person)))
        except:
            pass
        else:
            self.exams_list.addItems(exams_list)

    def clicked(self):
        global active_exam, exam_number
        active_exam = self.exams_list.currentItem().text()
        self.go_to_exam()

    def go_to_exam(self):
        exam = Exam()
        widget.addWidget(exam)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_add_exam(self):
        new_exam = NewExam()
        widget.addWidget(new_exam)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Exam(QDialog):
    def __init__(self):
        global mark, exam_number
        super(Exam, self).__init__()
        uic.loadUi("exam.ui", self)
        self.exam_label.setText(f'{active_exam}')
        self.go_to_main_btn.clicked.connect(self.go_to_main)
        self.delete_exam_btn.clicked.connect(self.delete_exam)
        self.change_mark_btn.clicked.connect(self.change_mark)
        exam_number = int(str(active_exam[:1]))
        ty = ExamDatabase().database[exam_number]
        mark = ty.mark
        self.mark_field.setText(f'{mark}')

    def go_to_main(self):
        main = Main()
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def delete_exam(self):
        exam = ExamDatabase()
        exam.delete_exam(int(str(active_exam[:1])))
        self.go_to_main()

    def change_mark(self):
        main = ChangeMark()
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ChangeMark(QDialog):
    def __init__(self):
        super(ChangeMark, self).__init__()
        uic.loadUi("changemark.ui", self)
        self.new_mark_field.setPlaceholderText('Введите оценку')
        self.change_mark_btn.clicked.connect(self.new_mark)

    def new_mark(self):
        global exam_number
        _mark = int(self.new_mark_field.text())
        ExamDatabase().change_mark(exam_number, _mark)
        self.go_to_main()

    def go_to_main(self):
        main = Main()
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class NewExam(QDialog):
    def __init__(self):
        super(NewExam, self).__init__()
        uic.loadUi("newexam.ui", self)
        self.invalid.setVisible(False)
        self.go_to_main_btn.clicked.connect(self.go_to_main)
        self.new_exam_name_field.setPlaceholderText('ФИО студента')
        self.new_exam_mark_field.setPlaceholderText('Оценка')
        self.add_new_exam_btn.clicked.connect(self.push_new_exam)

    def push_new_exam(self):
        global mark
        student_name = str(self.new_exam_name_field.text())
        mark = self.new_exam_mark_field.text()
        try:
            mark = int(mark)
        except:
            self.invalid.setVisible(True)
        else:
            self.invalid.setVisible(False)
            exam = ExamDatabase()
            exam.add_exam(mark, student_name)
            self.go_to_main()

    def go_to_main(self):
        main = Main()
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex() + 1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Main()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(main_window)
    widget.setFixedWidth(360)
    widget.setFixedHeight(650)
    widget.setWindowTitle('Exams')
    widget.show()
    app.exec()
