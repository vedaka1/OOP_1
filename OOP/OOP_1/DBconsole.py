from classes import *


class BankTerm(object):
    def __init__(self):
        self.exam_database = ExamDatabase()

    def print_database(self):
        for exam in self.exam_database:
            print('--Exam number {0}--\n  Student: {1}\n  Mark: {2}'.format(exam.number, exam.person, exam.mark))

    def run(self):
        choice = 0
        choices = {
            1: lambda: self.print_database(),
            2: lambda: self.exam_database.add_exam(int(input('Enter mark: ')),
                                                   str(input('\nEnter student full name: '))),
            3: lambda: (self.print_database(), print('Which one do you want to remove?'),
                        self.exam_database.delete_exam(int(input('Enter number: ')))),
            4: lambda: self.exam_database.change_mark(int(input('Enter exam number: ')), int(input('Enter new mark: ')))
                  }
        while choice != 5:
            print()
            print('1. Print Database')
            print('2. Add Exam')
            print('3. Delete Exam')
            print('4. Change mark')
            print('5. EXIT\n')
            print('Choose: ')
            choice = int(input())
            if choice in choices:
                choices[choice]()


if __name__ == '__main__':
    BankTerm().run()
