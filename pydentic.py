from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int
    city: str

person = Person(name="John", age=30, city="New York")
print(person.model_dump_json())


