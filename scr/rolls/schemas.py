from fastapi import Query
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class BaseRoll(BaseModel):
    length: float
    weight: float


class RollCreate(BaseRoll):
    length: float = Field(gt=0,
                          description="Длина должена быть больше или равна 0")
    weight: float = Field(gt=0,
                          description="Вес должен быть больше или равен 0")


class RollDelete(BaseModel):
    id: int = Field(ge=0,
                    description="ID должен быть больше или равен 0")


class Roll(BaseRoll):
    id: int
    date_added: datetime
    date_removed: Optional[datetime] = None

    class Config:
        orm_mode = True


class RollFilter(BaseModel):
    min_id: Optional[int] = Query(default=None,
                                  ge=0,
                                  description="Минимальный ID должен быть "
                                  "больше или равен 0")
    max_id: Optional[int] = Query(default=None,
                                  ge=0,
                                  description="Максимальный ID должен быть "
                                  "больше или равен 0")
    min_weight: Optional[float] = Query(default=None,
                                        gt=0,
                                        description="Минимальный вес должен "
                                        "быть больше 0")
    max_weight: Optional[float] = Query(default=None,
                                        gt=0,
                                        description="Максимальный вес должен "
                                        "быть больше 0")
    min_length: Optional[float] = Query(default=None,
                                        gt=0,
                                        description="Минимальная длина должна "
                                        "быть больше 0")
    max_length: Optional[float] = Query(default=None,
                                        gt=0,
                                        description="Максимальная длина "
                                        "должна быть больше 0")
    min_date_added: Optional[datetime] = Query(default=None,
                                               description="Минимальная дата "
                                               "добавления")
    max_date_added: Optional[datetime] = Query(default=None,
                                               description="Максимальная дата "
                                               "добавления")
    min_date_removed: Optional[datetime] = Query(default=None,
                                                 description="Минимальная "
                                                 "дата удаления")
    max_date_removed: Optional[datetime] = Query(default=None,
                                                 description="Максимальная "
                                                 "дата удаления")
