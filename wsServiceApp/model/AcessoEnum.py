import enum
import pydantic
import typing as t

class Acesso(int, enum.Enum):
    ADMINISTRADOR = 0
    USUARIO = 1

class Model(pydantic.BaseModel):
    m: t.Dict[Acesso, int]

    class Config:
        use_enum_values = True

Model(m={Acesso.ADMINISTRADOR: 0,
         Acesso.USUARIO: 1}).json()
