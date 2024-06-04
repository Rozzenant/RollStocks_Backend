from datetime import datetime
from typing import List
from sqlalchemy import JSON, Select, insert, select, text
from exceptions import RollNotAddedInDB
from scr.database import async_session_maker
from scr.rolls.models import Roll
from sqlalchemy import func
from fastapi import Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from scr.rolls.schemas import RollCreate, RollFilter


class RollDAO:

    @classmethod
    async def find_all(
        cls,
        filter: RollFilter
    ) -> List[Roll] | None:
        async with async_session_maker() as session:
            query = select(Roll)
            if filter.min_id is not None:
                query = query.filter(Roll.id >= filter.min_id)
            if filter.max_id is not None:
                query = query.filter(Roll.id <= filter.max_id)
            if filter.min_weight is not None:
                query = query.filter(Roll.weight >= filter.min_weight)
            if filter.max_weight is not None:
                query = query.filter(Roll.weight <= filter.max_weight)
            if filter.min_length is not None:
                query = query.filter(Roll.length >= filter.min_length)
            if filter.max_length is not None:
                query = query.filter(Roll.length <= filter.max_length)
            if filter.min_date_added is not None:
                query = query.filter(Roll.date_added >= filter.min_date_added)
            if filter.max_date_added is not None:
                query = query.filter(Roll.date_added <= filter.max_date_added)
            if filter.min_date_removed is not None:
                query = query.filter(Roll.date_removed >=
                                     filter.min_date_removed)
            if filter.max_date_removed is not None:
                query = query.filter(Roll.date_removed <=
                                     filter.max_date_removed)
            rolls = await session.execute(query)
            rolls = rolls.scalars().all()
            if not rolls:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Рулонов, подходящих под критерии, "
                                    "не найдено")
            return rolls

    # @classmethod
    # async def find_id(cls, id: int):
    #     async with async_session_maker() as session:
    #         query = Select(Roll).filter_by(id=id)
    #         rolls = await session.execute(query)
    #         return rolls.scalars().first()

    @classmethod
    async def add(
        cls,
        roll=Depends(RollCreate)
    ) -> Roll:
        query = insert(Roll).values(length=roll.length,
                                    weight=roll.weight).returning(Roll)
        async with async_session_maker() as session:
            roll = await session.execute(query)
            await session.commit()
            roll = roll.scalars().first()
            if not roll:
                raise RollNotAddedInDB
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                                content=jsonable_encoder(roll))

    @classmethod
    async def delete(
        cls,
        roll_id: int
    ) -> Roll | None:
        async with async_session_maker() as session:
            query = Select(Roll).filter_by(id=roll_id)
            result = await session.execute(query)
            roll = result.scalars().first()

            if roll:
                if roll.date_removed:
                    raise HTTPException(status_code=status.HTTP_410_GONE,
                                        detail='Запрашиваемый рулон '
                                        'был удален ранее')
                roll.date_removed = datetime.now()
                # delete_query = delete(Roll).where(Roll.id==roll_id)
                # await session.execute(delete_query)
                await session.commit()
                return roll
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail='Такого рулона не существует')

    @classmethod
    async def get_rolls_statistics(cls,
                                   start_date: datetime,
                                   end_date: datetime) -> JSON:
        async with async_session_maker() as session:
            # Количество добавленных рулонов за указанный период
            added_rolls_count = await session.scalar(
                select(func.count())
                .where(Roll.date_added.between(start_date, end_date))
            )

            # Количество удаленных рулонов за указанный период
            removed_rolls_count = await session.scalar(
                select(func.count())
                .where(Roll.date_removed.between(start_date, end_date))
            )

            # Средняя длина и вес рулонов,
            # находившихся на складе за указанный период
            avg_length_weight = await session.execute(
                select(func.avg(Roll.length), func.avg(Roll.weight))
                .where(Roll.date_added >= start_date)
                .where(Roll.date_removed <= end_date)
            )
            avg_length, avg_weight = avg_length_weight.first()

            # Максимальная и минимальная длина и вес рулонов,
            # находившихся на складе за указанный период
            max_min_length_weight = await session.execute(
                select(func.max(Roll.length), func.min(Roll.length),
                       func.max(Roll.weight), func.min(Roll.weight))
                .where(Roll.date_added >= start_date)
                .where(Roll.date_removed <= end_date)
            )
            max_length, min_length, max_weight, min_weight = \
                max_min_length_weight.first()

            # Суммарный вес рулонов на складе за указанный период
            total_weight = await session.scalar(
                select(func.sum(Roll.weight))
                .where(Roll.date_added >= start_date)
                .where(Roll.date_removed <= end_date)
            )

            # Максимальный и минимальный промежуток между добавлением
            # и удалением рулона за указанный период
            max_min_duration = await session.execute(
                select(func.max(Roll.date_removed - Roll.date_added),
                       func.min(Roll.date_removed - Roll.date_added))
                .where(Roll.date_added >= start_date)
                .where(Roll.date_removed <= end_date)
            )
            max_duration, min_duration = max_min_duration.first()

            # Преобразование datetime в date
            # start_date = start_date.date()
            # end_date = end_date.date()

            # Дата с минимальным количеством рулонов
            min_rolls_date = await session.execute(
                select(func.date(Roll.date_added), func.count())
                .where(Roll.date_added.between(start_date, end_date))
                .group_by(Roll.date_added)
                .order_by(func.count())
                .limit(1)
            )

            # Дата с максимальным количеством рулонов
            max_rolls_date = await session.execute(
                select(func.date(Roll.date_added), func.count())
                .where(Roll.date_added.between(start_date, end_date))
                .group_by(func.date(Roll.date_added))
                .order_by(func.count().desc())
                .limit(1)
            )

            # Дата с минимальным суммарным весом рулонов
            min_weight_date = await session.execute(
                select(func.date(Roll.date_added), func.sum(Roll.weight)
                       .label('total_weight'))
                .where(Roll.date_added.between(start_date, end_date))
                .group_by(Roll.date_added)
                .order_by(text('total_weight'))
                .limit(1)
            )

            # Дата с максимальным суммарным весом рулонов
            max_weight_date = await session.execute(
                select(func.date(Roll.date_added), func.sum(Roll.weight)
                       .label('total_weight'))
                .where(Roll.date_added.between(start_date, end_date))
                .group_by(Roll.date_added)
                .order_by(text('total_weight desc'))
                .limit(1)
            )

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "added_rolls_count": added_rolls_count,
                    "removed_rolls_count": removed_rolls_count,
                    "avg_length": avg_length,
                    "avg_weight": avg_weight,
                    "max_length": max_length,
                    "min_length": min_length,
                    "max_weight": max_weight,
                    "min_weight": min_weight,
                    "total_weight": total_weight,
                    "max_duration": max_duration.days if max_duration
                    else None,
                    "min_duration": min_duration.days if min_duration
                    else None,
                    "min_rolls_date":
                        jsonable_encoder(min_rolls_date)['iterator'],
                    "max_rolls_date":
                        jsonable_encoder(max_rolls_date)['iterator'],
                    "min_weight_date":
                        jsonable_encoder(min_weight_date)['iterator'],
                    "max_weight_date":
                        jsonable_encoder(max_weight_date)['iterator']
                }
            )
