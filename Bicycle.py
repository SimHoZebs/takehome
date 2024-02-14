from typing import List


class Bicycle:
    def __init__(self, front_cogs: List[int], rear_cogs: List[int]):
        """
        Notes:
        - Following assumptions are made about the input:
            - `front_cogs` and `rear_cogs` are always sorted in descending order, as per typical bike cog structure.
            - `front_cogs` will have less or equal number of cogs compared to `rear_cogs`, as per typical bike design.
        - The current error handling is basic; more error handling could be implemented (e.g. checking if the cogs are sorted, if the cogs are unique, are list of numbers, etc.).
        """

        # error handling for empty lists
        if len(front_cogs) < 1 or len(rear_cogs) < 1:
            raise Exception("cogs can't be an empty list")

        for cog in front_cogs+rear_cogs:
            if cog < 1:
                raise Exception("cogs can't have a less than 1 teeth")

        self.front_cogs = front_cogs
        self.rear_cogs = rear_cogs

    def get_front_cogs(self):
        """getter for front_cogs"""
        return self.front_cogs

    def get_rear_cogs(self):
        """getter for rear_cogs"""
        return self.rear_cogs

    @staticmethod
    def calc_gear_ratio(front_cog: int, rear_cog: int):
        """
        returns the gear ratio of the front and rear cogs, rounded to 3 decimal places

        Note:
            - The argument could've been an array, but based on screening documentation, I assume there is an unknown benefit to distinguishing each cog.
        """
        return round(front_cog / rear_cog, 3)

    def get_gear_combination(self, target_ratio: float):
        """
        returns gear combination with ratio closest to the target_ratio but less than or equal to it

        Notes:
        - The function assumes target_ratio is always different from the current ratio. Otherwise, the current gear combination should be tracked and considered in this function to skip computation when possible.
        - A combination of linear and binary search was chosen as a middle ground for performance and memory usage.
            - Alternatively, the gear ratios could be pre-computed for every gear combination at instantiation. `get_gear_combiantion` would then do a binary search from the pre-computed list. Considering reasonable number of cogs, this should have little effect on memory and would be the fastest, but I decided to make no assumption about the total memory of the system.
            - A quadratic search would simplify the code and may be more readable. Considering reasonable number of cogs, there should be no significant performance impact as well. 
        - I'm assuming that the expected return value is a dictionary (`{Front: value, Rear: value, Ratio: value}`) based on the information given on the screening document. 
            - Concern: this is inconsistent with `initial_gear_combination` in `get_shift_sequence`, which represents gear as `[front_value, rear_value]`
        """
        rear_cogs = self.get_rear_cogs()

        front = rear = ratio = 0

        # O(nlogn) search for the closest gear combination
        for front_cog in self.front_cogs:
            target_rear = front_cog / target_ratio
            closest_rear = rear

            # inverse binary search to find the closest rear cog for this front cog
            high = 0
            low = len(rear_cogs) - 1
            while high <= low:
                mid = (high + low) // 2
                rear_cog = rear_cogs[mid]

                # update closest_rear if the current rear_cog is closer to the target, but not smaller
                # rear >= target_rear ensures tmp_ratio is not larger than target_ratio
                if abs(target_rear - rear_cog) < abs(target_rear - closest_rear) and rear_cog >= target_rear:
                    closest_rear = rear_cog

                if rear_cog > target_rear:
                    high = mid + 1
                else:
                    low = mid - 1

            tmp_ratio = self.calc_gear_ratio(front_cog, closest_rear)
            if abs(target_ratio - tmp_ratio) < abs(target_ratio - ratio):
                front = front_cog
                rear = closest_rear
                ratio = tmp_ratio

        return {
            "Front": front,
            "Rear": rear,
            "Ratio": ratio
        }

    def get_shift_sequence(self, target_ratio: float, initial_gear_combination: List[int]):
        """
        returns a list of gear combinations to shift through to reach the target_ratio
        """

        # gear combination for the target ratio
        gear_combination = self.get_gear_combination(target_ratio)

        # restructure gear_combination to list for indexed access
        target_gear = [gear_combination["Front"], gear_combination["Rear"]]
        cogs = [self.get_front_cogs(), self.get_rear_cogs()]

        # get the list of the target and initial cog indexes
        target_gear_index = [cog.index(target_gear[i])
                             for i, cog in enumerate(cogs)]
        initial_gear_index = [
            cog.index(initial_gear_combination[i]) for i, cog in enumerate(cogs)]

        # the number of shifts needed for each cog
        gear_shift_count = [target_gear_index[0] - initial_gear_index[0],
                            target_gear_index[1] - initial_gear_index[1]]

        # initial gear combination
        shift_sequence = [{
            "Front": initial_gear_combination[0],
            "Rear": initial_gear_combination[1],
            "Ratio": self.calc_gear_ratio(initial_gear_combination[0], initial_gear_combination[1])
        }]

        current_gear = initial_gear_combination

        # for each cog, shift to the target cog one step at a time
        for i, shift in enumerate(gear_shift_count):
            for j in range(1, shift + 1, -1 if shift < 0 else 1):
                current_gear[i] = cogs[i][initial_gear_index[i] + j]
                shift_sequence.append({
                    "Front": current_gear[0],
                    "Rear": current_gear[1],
                    "Ratio": self.calc_gear_ratio(current_gear[0], current_gear[1])
                })
        return shift_sequence

    def print_shift_sequence(self, target_ratio: float, initial_gear_combination: List[int]):
        """prints formatted shift sequence to reach the target_ratio from the initial_gear_combination"""
        shift_sequence = self.get_shift_sequence(
            target_ratio, initial_gear_combination)

        for shift in shift_sequence:
            print(
                f"Front: {shift['Front']}, Rear: {shift['Rear']}, Ratio: {shift['Ratio']}")
