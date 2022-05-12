from OOP import *


Data_pulpit = {
    "name": "Programming Python",
    "faculty": "OOP Programming",
    "full_name": "Belov Leonid Victorovich",
    "room_number": 3,
    "building_number": 4,
    "phone": 89501234567,
    "number_teachers": 8
}

Data_discipline = {
    "name": "Programming",
    "pulpit": Data_pulpit["name"],
    "hours": 20,
    "test_kind": "Exam"
}

Pulpit(**Data_pulpit)
dis = Discipline(**Data_discipline)

# Лабораторная № 5
state1 = Statement("Кулешов В.А.", "Программирование", "Голубев М.В.", 5)
state1.last_exam = date(2031, 6, 7)
print(state1.last_exam)

try:
    del state1.mark
except Exception as error:
    print(error)

# Лабораторная № 6
dis(11)
print(dis.hours)
print(Pulpit.__doc__)

