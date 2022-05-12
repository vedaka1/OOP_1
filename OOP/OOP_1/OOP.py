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


class Students:

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

    def __init__(self, name: str, pulpit: str, hours: int, test_kind='none'):
        self.name = name
        self.pulpit = pulpit
        self.hours = hours
        self.test_kind = test_kind

    def __str__(self):
        return 'name: {0}, pulpit: {1}, hours: {2}, test_kind: {3}'.format(self.name, self.pulpit, self.hours,
                                                                           self.test_kind)

    def add_hours(self, time):
        self.hours += time
        with open('add_hours.txt', 'a') as file:
            file.write('when {0} : total_hours {1} : added {2} \n'.format(datetime.today(), self.hours, time))


class LastExam(object):

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

    def __init__(self, teacher: str, discipline: str, student: str, mark: int):
        self._teacher = teacher
        self._discipline = discipline
        self._student = student
        self._mark = mark

        self.id = _next_statement_id()

    last_exam = LastExam()

    def __str__(self):
        return 'teacher: {0}, discipline: {1}, student: {2}, mark: {3}, last exam: {4}'.format(self._teacher,
                                                                                               self._discipline,
                                                                                               self._student,
                                                                                               self._mark,
                                                                                               self._last_exam)

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


class StudentMark(Students):

    mark = "5"

    def __str__(self):
        return '{0},{1}, mark: {2}'.format(self.name, self.surname, self.mark)


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
