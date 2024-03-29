# object_oriented.py
"""Python Essentials: Object Oriented Programming.
<Name>
<Class>
<Date>
"""


import collections
import fileinput
from logging import exception

from numpy import outer


class Backpack:
    """A Backpack object class. Has a name and a list of contents.

    Attributes:
        name (str): the name of the backpack's owner.
        contents (list): the contents of the backpack.
    """

    # Problem: Modify __init__() and put(), and write dump().
    def __init__(self, name, color, max_size=5):
        """Set the name and initialize an empty list of contents.

        Parameters:
            name (str): the name of the backpack's owner.
        """
        self.name = name
        self.contents = []
        self.color = color
        self.max_size = (int) (max_size)

    def put(self, item):
        if len(self.contents) == self.max_size:
            print("No room!")
        else:
            self.max_size = (self.max_size + 1)
            """Add an item to the backpack's list of contents."""
            self.contents.append(item)

    def take(self, item):
        """Remove an item from the backpack's list of contents."""
        self.contents.remove(item)

    def dump(self):
        self.content = []
    # Magic Methods -----------------------------------------------------------

    # Problem: Write __eq__() and __str__().
    def __add__(self, other):
        """Add the number of contents of each Backpack."""
        return len(self.contents) + len(other.contents)

    def __lt__(self, other):
        """Compare two backpacks. If 'self' has fewer contents
        than 'other', return True. Otherwise, return False.
        """
        return len(self.contents) < len(other.contents)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Backpack):
            return False
        if __o.color != self.color or __o.name != self.name:
            return False
        if collections.Counter(__o.content) != collections.Counter(self.content):
            return False
        return True

    def __str__(self) -> str:
        output = ""
        output += "Owner:\\t" + self.name + "\\n"
        output += "Color:\\t" + self.color + "\\n"
        output += "Size:\\t" + len(self.content) + "\\n"
        output += "Max Size:\\t" + self.max_size + "\\n"
        output += "Content:\\t" + str(self.content) + "\\n"
        return output

# An example of inheritance. You are not required to modify this class.
class Knapsack(Backpack):
    """A Knapsack object class. Inherits from the Backpack class.
    A knapsack is smaller than a backpack and can be tied closed.

    Attributes:
        name (str): the name of the knapsack's owner.
        color (str): the color of the knapsack.
        max_size (int): the maximum number of items that can fit inside.
        contents (list): the contents of the backpack.
        closed (bool): whether or not the knapsack is tied shut.
    """
    def __init__(self, name, color):
        """Use the Backpack constructor to initialize the name, color,
        and max_size attributes. A knapsack only holds 3 item by default.

        Parameters:
            name (str): the name of the knapsack's owner.
            color (str): the color of the knapsack.
            max_size (int): the maximum number of items that can fit inside.
        """
        Backpack.__init__(self, name, color, max_size=3)
        self.closed = True

    def put(self, item):
        """If the knapsack is untied, use the Backpack.put() method."""
        if self.closed:
            print("I'm closed!")
        else:
            Backpack.put(self, item)

    def take(self, item):
        """If the knapsack is untied, use the Backpack.take() method."""
        if self.closed:
            print("I'm closed!")
        else:
            Backpack.take(self, item)

    def weight(self):
        """Calculate the weight of the knapsack by counting the length of the
        string representations of each item in the contents list.
        """
        return sum(len(str(item)) for item in self.contents)


# Problem: Write a 'Jetpack' class that inherits from the 'Backpack' class.

class Jetpack(Backpack):
    
    def __init__(self, name, color, max_size=2, fuel=10):
        """Set the name and initialize an empty list of contents.

        Parameters:
            name (str): the name of the backpack's owner.
        """
        Backpack.__init__(self, name, color, max_size=max_size)
        self.fuel = fuel
    
    def fly(self, fuel):
        if fuel > self.fuel:
            print("Not enoguh fuel!")
        else:
            self.fuel -= fuel
    
    def dump(self):
        super().dump()
        self.fuel = 0

class ContentFilter:
    
    def __init__(self,fname) -> None:
        self.name = ""
        tryOpen = fname
        while self.name == "":
            try:
                file = open(tryOpen,"r")
                self.content = file.readlines()
                self.name = tryOpen
            except FileNotFoundError or TypeError or OSError:
                print("Please enter a valid file name:")
                tryOpen = input()
