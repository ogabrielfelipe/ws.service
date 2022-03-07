import enum
import pydantic
import typing as t


class Status(int, enum.Enum):
    ABERTO = 0
    ENCERRADO = 1


class Model(pydantic.BaseModel):
    m: t.Dict[Status, int]

    class Config:
        use_enum_values = True


Model(m={Status.ABERTO: 0,
         Status.ENCERRADO: 1}).json()
