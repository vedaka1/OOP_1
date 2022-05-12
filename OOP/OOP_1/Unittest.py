import OOP
import unittest


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


if __name__ == '__main__':
    unittest.main()


class Test(unittest.TestCase):
    def setUp(self):
        self.pulpit = OOP_1.Pulpit(**Data_pulpit)
        self.discipline = OOP_1.Discipline(**Data_discipline)

    # Лабораторная № 3
    def test_add_teachers(self):
        self.pulpit.add_teachers(2)

    def test_add_hours(self):
        self.discipline.add_hours(5)

    def test_serialize(self):
        ba = self.pulpit
        self.test = OOP_1.PersistencePulpit.serialize(ba)
        print(OOP_1.PersistencePulpit.deserialize())