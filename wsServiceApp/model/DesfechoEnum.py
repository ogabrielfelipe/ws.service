import enum
import pydantic
import typing as t


class Desfecho(int, enum.Enum):
    EM_ATENDIMENTO = 0
    EM_DESENVOLVIMENTO = 1
    SEM_SOLUCAO = 2
    RESOLVIDO = 3


class Model(pydantic.BaseModel):
    m: t.Dict[Desfecho, int]

    class Config:
        use_enum_values = True


Model(m={Desfecho.EM_ATENDIMENTO: 0,
         Desfecho.EM_DESENVOLVIMENTO: 1,
         Desfecho.SEM_SOLUCAO: 2,
         Desfecho.RESOLVIDO: 3}).json()
