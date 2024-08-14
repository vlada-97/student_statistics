from pydantic import BaseModel, conlist, constr, ValidationError
from typing import Dict


class KlassModel(BaseModel):
    klass: Dict[str, conlist(constr(min_length=1), min_length=1)]


klass = {
    "A": [
        "Иванов",
        "Смирнов",
        "Кузнецов",
        "Попов",
        "Васильев",
        "Петров",
        "Соколов",
        "Михайлов",
        "Новиков",
        "Федоров",
    ],
    "B": [
        "Морозов",
        "Волков",
        "Алексеев",
        "Лебедев",
        "Семенов",
        "Егоров",
        "Павлов",
        "Козлов",
        "Степанов",
        "Николаев",
    ],
}

try:
    klass_model = KlassModel(klass=klass)
    print("Data is valid.")
    print(klass_model)
except ValidationError as e:
    print("Validation error occurred:")
    print(e.json())
