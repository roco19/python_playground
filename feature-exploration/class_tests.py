from dataclasses import field, dataclass
from typing import Optional


class Dog:
    def __init__(self, name, breed):
        self._name = name
        self._breed = breed

    @property
    def name(self):
        print("Getter")
        return self._name

    @name.setter
    def name(self, name):
        print("Setter")
        self._name = name

    @staticmethod
    def this_is_a_static_method():
        print("Hello from static method.")

# dog1 = Dog("Rex", "Golden Retriever")
# dog1.name = "Rex Updated"
# print(dog1.name)
# Dog.this_is_a_static_method()
# dog1.this_is_a_static_method()

@dataclass()
class Person:
    """
    Here is where I should put the comment explaining the class usage.
    """

    first_name: str
    last_name: Optional[str] = None
    email: Optional[str] = None
    alt_email: Optional[str] = field(default=None)
    address: str = field(default=None)
    phone: str = field(default="555555")
    hobbies: list = field(default_factory=list)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

person = Person(first_name="Juan", last_name="Valdez", email="juan.valdez@example.com")
print(person)
print(person.full_name())
print(person == Person("Juan", "Valdez", "juan.valdez@example.com")) # Prints True
