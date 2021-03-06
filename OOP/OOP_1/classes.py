import pickle
from datetime import datetime, date

_pulpit_id = 0


def _next_pulpit_id():
    global _pulpit_id
    _pulpit_id += 1
    return _pulpit_id


_statement_id = 0


def _next_statement_id():
    global _statement_id
    _statement_id += 1
    return _statement_id


# Ошибка неудаляемого атрибута
class UndeletableArgument(Exception):

    def __str__(self):
        return 'Error: Undeleteable Argument.'


class Pulpit:

    ''' Pulpit class. Full name is a name of manager.'''

    def __init__(self, name: str, faculty: str, full_name: str, room_number: int, building_number: int, phone: int,
                 number_teachers: int):
        self.name = name
        self.faculty = faculty
        self.full_name = full_name
        self.room_number = room_number
        self.building_number = building_number
        self.phone = phone
        self.number_teachers = number_teachers

        self.id = _next_pulpit_id()

    def add_teachers(self, amount):
        self.number_teachers += amount
        with open('add_teachers.txt', 'a') as file:
            file.write('when {0} : total_teachers {1} : added {2} \n'.format(datetime.today(), self.number_teachers,
                                                                             amount))


class Teachers:

    '''Teachers class.'''

    def __init__(self, surname: str, name: str, patronymic: str, pulpit: Pulpit, year_of_birth: int,
                 year_of_joining: int, experience: int, position: str, gender: str, address: str, year: int, town: str,
                 telephone_number: int):
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.pulpit = pulpit
        self._year_of_birth = year_of_birth
        self._year_of_joining = year_of_joining
        self._experience = experience
        self._position = position
        self._gender = gender
        self._address = address
        self._year = year
        self._town = town
        self._telephone_number = telephone_number

    @classmethod
    def recruit(cls, value):
        return cls(value)


class Students:

    '''Students class.'''

    def __init__(self, surname: str, name: str, patronymic: str, pulpit: Pulpit, year_of_birth: int, gender: str,
                 address: str, town: str, telephone_number=0):
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.pulpit = pulpit
        self._year_of_birth = year_of_birth
        self._gender = gender
        self._address = address
        self._town = town
        self._telephone_number = telephone_number


class Discipline:

    '''Discipline class.'''

    def __init__(self, name: str, pulpit: Pulpit, hours: int, test_kind='none'):
        self.name = name
        self.pulpit = pulpit
        self.hours = hours
        self.test_kind = test_kind

    def __str__(self):
        return 'name: {0}, pulpit: {1}, hours: {2}, test_kind: {3}'.format(self.name,
                                                                           self.pulpit,
                                                                           self.hours,
                                                                           self.test_kind)

    def __call__(self, value):
        self.hours = value
        with open('add_hours.txt', 'a') as file:
            file.write('when {0} : total_hours {1} : added {2} \n'.format(datetime.today(),
                                                                          self.hours,
                                                                          value))


class LastExam:

    '''Checking if the exam date is correct.'''

    def __init__(self):
        self.maxdate = date.today()

    def __get__(self, instance, cls):
        return instance._last_exam

    def __set__(self, instance, value):
        if self.maxdate < value:
            instance._last_exam = self.maxdate
        else:
            instance._last_exam = value


class Statement:

    '''Statement class.'''

    def __init__(self, teacher=None, discipline=None, student=None, mark=0):
        self.teacher = teacher
        self.discipline = discipline
        self.student = student
        self.mark = mark

        self.id = _next_statement_id()

    last_exam = LastExam()

    def __str__(self):
        return 'teacher: {0}, discipline: {1}, student: {2}, mark: {3}'.format(self.teacher,
                                                                               self.discipline,
                                                                               self.student,
                                                                               self.mark)

    @staticmethod
    def log(func):
        def wrapper(*args, **kwargs):
            print('* Called `{}`.\n* Args: {}\n* Kwargs: {}'.format(func.__name__, args, kwargs))
            return func(*args, **kwargs)
        return wrapper

# Лабораторная № 5
    @property
    def mark(self):
        return self._mark

    @mark.setter
    def mark(self, value):
        if not isinstance(value, int):
            raise TypeError('Mark is number!')
        else:
            self._mark = value

    @mark.deleter
    def mark(self):
        raise UndeletableArgument()


# Лабораторная № 7
class TakeExam:

    def __init__(self, mark: int, student=None, discipline=None, number=0):
        self.person = student
        self.exam = Statement(discipline)
        self.mark = mark
        self.number = number

    def get_mark(self, x: int):
        self.mark = x

    def __str__(self):
        return 'student: {0}, discipline: {1}, mark: {2}'.format(self.person,
                                                                 self.exam.discipline,
                                                                 self.mark)

    @Statement.log
    def exam_with_logging(self, x: int):
        return self.get_mark(x)


class PersistencePulpit:

    @staticmethod
    def serialize(pulpit):
        with open('pulpit.pkl', 'wb') as file:
            pickle.dump(pulpit, file)

    @staticmethod
    def deserialize():
        with open('pulpit.pkl', 'rb') as file:
            pulpit = pickle.load(file)
        return pulpit


class ExamDatabase(object):
    def __init__(self):
        self.filename = 'exam.pkl'
        self.database = {}
        self.index = 0
        try:
            self.open_database()
        except:
            self.save_database()
    number = property(lambda self: self.database[self.index].number)
    mark = property(lambda self: self.database[self.index].balance)

    def __iter__(self):
        for item in self.database:
            yield self.database[item]

    def next(self):
        if self.index == len(self.database):
            raise StopIteration
        self.index = self.index + 1
        return self.database[self.index]

    def prev(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.database[self.index]

    def open_database(self):
        with open(self.filename, 'rb') as f:
            self.database = pickle.load(f)
        f.closed

    def save_database(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.database, f)
        f.closed

    def add_exam(self, mark, student):
        ex = TakeExam(mark, student)
        if ex.number in self.database:
            ex.number = len(self.database) + 1
        self.database[ex.number] = ex
        self.save_database()

    def get_exam_by_number(self, number):
        if number not in self.database:
            return None
        return self.database[number]

    def delete_exam(self, number):
        del self.database[number]
        self.save_database()

    def change_mark(self, number, mark):
        exam = self.get_exam_by_number(number)
        if not exam:
            raise ValueError('value does not exist')
        exam.mark = mark
        self.save_database()

