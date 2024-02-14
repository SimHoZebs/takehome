import unittest

from Bicycle import Bicycle


class BicycleTest(unittest.TestCase):

    def setUp(self):
        self.target_ratio = 1.6
        self.front_cogs = [38, 30]
        self.rear_cogs = [28, 23, 19, 16]
        self.expected_shift_sequence = [
            {"Front": 38, "Rear": 28, "Ratio": 1.357},
            {"Front": 30, "Rear": 28, "Ratio": 1.071},
            {"Front": 30, "Rear": 23, "Ratio": 1.304},
            {"Front": 30, "Rear": 19, "Ratio": 1.579}
        ]

        self.bike = Bicycle(self.front_cogs, self.rear_cogs)

    def test_init(self):
        self.assertEqual(self.bike.get_front_cogs(), self.front_cogs)
        self.assertEqual(self.bike.get_rear_cogs(), self.rear_cogs)

        with self.assertRaises(Exception):
            self.bike = Bicycle([], [])

    def test_calc_gear_ratio(self):
        self.assertEqual(Bicycle.calc_gear_ratio(38, 28), 1.357)
        self.assertEqual(Bicycle.calc_gear_ratio(30, 28), 1.071)
        self.assertEqual(Bicycle.calc_gear_ratio(30, 23), 1.304)
        self.assertEqual(Bicycle.calc_gear_ratio(30, 19), 1.579)

    def test_get_gear_combination(self):
        gear_combination = self.bike.get_gear_combination(self.target_ratio)
        gear_ratio = self.bike.calc_gear_ratio(
            gear_combination["Front"], gear_combination["Rear"])

        self.assertEqual(gear_combination["Front"], 30)
        self.assertEqual(gear_combination["Rear"], 19)
        self.assertEqual(gear_combination["Ratio"], gear_ratio)

    def test_get_shift_sequence(self):
        shift_sequence = self.bike.get_shift_sequence(
            self.target_ratio, [self.front_cogs[0], self.rear_cogs[0]])

        for i, shift in enumerate(shift_sequence):
            self.assertDictEqual(shift, self.expected_shift_sequence[i])

    def test_print_shift_sequence(self):
        self.bike.print_shift_sequence(
            self.target_ratio, [self.front_cogs[0], self.rear_cogs[0]])


if __name__ == "__main__":
    unittest.main()
