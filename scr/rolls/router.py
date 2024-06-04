from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends

from scr.rolls.dao import RollDAO
from scr.rolls.schemas import Roll as SRoll, RollDelete, RollFilter
from scr.rolls.schemas import RollCreate as SRollCreate

router = APIRouter(
    prefix="/rolls",
    tags=["Рулоны"]
)


@router.get(
        "",
        response_model=List[SRoll] | None,
        responses={
            404: {"model": None,
                  "description": "Рулонов, подходящих под критерии, "
                  "не найдено"},
            503: {"model": None,
                  "description": "Произошла ошибка при выполнении запроса "
                  "к базе данных"}
        }
    )
async def get_rolls(filter=Depends(RollFilter)) -> List[SRoll]:
    return await RollDAO.find_all(filter)

# @router.get("/{roll_id}")
# async def get_roll(roll_id: int) -> SRoll | None:
#     return await RollDAO.find_id(id=roll_id)


@router.post(
        "/",
        response_model=SRoll | None,
        responses={
            201: {"model": SRoll,
                  "description": "Рулон добавлен на склад"},
            503: {"model": None,
                  "description": "Произошла ошибка при выполнении запроса "
                  "к базе данных"}
        }
    )
async def add_roll(roll: SRollCreate) -> SRoll:
    return await RollDAO.add(roll)


@router.delete(
        "/{roll_id}",
        response_model=SRoll,
        responses={
            404: {"model": SRoll,
                  "description": "Такого рулона не существует"},
            410: {"model": SRoll,
                  "description": "Запрашиваемый рулон был удален ранее"},
            503: {"model": None,
                  "description": "Произошла ошибка при выполнении запроса "
                  "к базе данных"}
        }
    )
async def delete_roll(roll=Depends(RollDelete)) -> SRoll | None:
    return await RollDAO.delete(roll.id)


@router.get(
        "/stats"
    )
async def get_stats_rolls(start_date: datetime,
                          end_date: datetime) -> dict | None:
    start_date = start_date.replace(tzinfo=None)
    end_date = end_date.replace(tzinfo=None)
    return await RollDAO.get_rolls_statistics(start_date, end_date)
