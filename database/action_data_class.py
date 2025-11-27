import datetime

from sqlalchemy import select, insert, update, column, text, delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from database.model import (UsersTable, DeeplinksTable, OneTimeLinksIdsTable, AdminsTable, DiagnosticFormTable, ConsultFormTable)


class DataInteraction():
    def __init__(self, session: async_sessionmaker):
        self._sessions = session

    async def check_user(self, user_id: int) -> bool:
        async with self._sessions() as session:
            result = await session.scalar(select(UsersTable).where(UsersTable.user_id == user_id))
        return True if result else False

    async def add_user(self, user_id: int, username: str, name: str, link: str | None = None):
        if await self.check_user(user_id):
            return
        async with self._sessions() as session:
            await session.execute(insert(UsersTable).values(
                user_id=user_id,
                username=username,
                name=name,
                join=link
            ))
            await session.commit()

    async def add_diagnostic_form(self, user_id: int, niche: str, pain: str, problem: str,
                                  digitalization: str, finance: str, purpose: str):
        if await self.get_diagnostic_form(user_id):
            await self.update_diagnostic_form(
                user_id=user_id,
                niche=niche,
                pain=pain,
                problem=problem,
                digitalization=digitalization,
                finance=finance,
                purpose=purpose
            )
            return
        async with self._sessions() as session:
            await session.execute(insert(DiagnosticFormTable).values(
                user_id=user_id,
                niche=niche,
                pain=pain,
                problem=problem,
                digitalization=digitalization,
                finance=finance,
                purpose=purpose
            ))
            await session.commit()

    async def add_consult_form(self, user_id: int, focus: str, process: str, deadline: str,
                               features: str, criteria: str):
        if await self.get_consult_form(user_id):
            await self.update_consult_form(
                user_id=user_id,
                focus=focus,
                process=process,
                deadline=deadline,
                features=features,
                criteria=criteria
            )
            return
        async with self._sessions() as session:
            await session.execute(insert(ConsultFormTable).values(
                user_id=user_id,
                focus=focus,
                process=process,
                deadline=deadline,
                features=features,
                criteria=criteria
            ))
            await session.commit()

    async def add_entry(self, link: str):
        async with self._sessions() as session:
            await session.execute(update(DeeplinksTable).where(DeeplinksTable.link == link).values(
                entry=DeeplinksTable.entry+1
            ))
            await session.commit()

    async def add_deeplink(self, link: str):
        async with self._sessions() as session:
            await session.execute(insert(DeeplinksTable).values(
                link=link
            ))
            await session.commit()

    async def add_link(self, link: str):
        async with self._sessions() as session:
            await session.execute(insert(OneTimeLinksIdsTable).values(
                link=link
            ))
            await session.commit()

    async def add_admin(self, user_id: int, name: str):
        async with self._sessions() as session:
            await session.execute(insert(AdminsTable).values(
                user_id=user_id,
                name=name
            ))
            await session.commit()

    async def get_diagnostic_form(self, user_id: int):
        async with self._sessions() as session:
            result = await session.scalar(select(DiagnosticFormTable).where(DiagnosticFormTable.user_id == user_id))
        return result

    async def get_diagnostic_form_by_id(self, id: int):
        async with self._sessions() as session:
            result = await session.scalar(select(DiagnosticFormTable).where(DiagnosticFormTable.id == id))
        return result

    async def get_consult_form(self, user_id: int):
        async with self._sessions() as session:
            result = await session.scalar(select(ConsultFormTable).where(ConsultFormTable.user_id == user_id))
        return result

    async def get_consult_form_by_id(self, id: int):
        async with self._sessions() as session:
            result = await session.scalar(select(ConsultFormTable).where(ConsultFormTable.id == id))
        return result

    async def get_users(self):
        async with self._sessions() as session:
            result = await session.scalars(select(UsersTable))
        return result.fetchall()

    async def get_user(self, user_id: int):
        async with self._sessions() as session:
            result = await session.scalar(select(UsersTable).where(UsersTable.user_id == user_id))
        return result

    async def get_user_by_username(self, username: str):
        async with self._sessions() as session:
            result = await session.scalar(select(UsersTable).where(UsersTable.username == username))
        return result

    async def get_links(self):
        async with self._sessions() as session:
            result = await session.scalars(select(OneTimeLinksIdsTable))
        return result.fetchall()

    async def get_admins(self):
        async with self._sessions() as session:
            result = await session.scalars(select(AdminsTable))
        return result.fetchall()

    async def get_deeplinks(self):
        async with self._sessions() as session:
            result = await session.scalars(select(DeeplinksTable))
        return result.fetchall()

    async def set_activity(self, user_id: int):
        async with self._sessions() as session:
            await session.execute(update(UsersTable).where(UsersTable.user_id == user_id).values(
                activity=datetime.datetime.today()
            ))
            await session.commit()

    async def set_active(self, user_id: int, active: int):
        async with self._sessions() as session:
            await session.execute(update(UsersTable).where(UsersTable.user_id == user_id).values(
                active=active
            ))
            await session.commit()

    async def update_diagnostic_form(self, user_id: int, niche: str, pain: str, problem: str,
                                  digitalization: str, finance: str, purpose: str):
        async with self._sessions() as session:
            await session.execute(update(DiagnosticFormTable).where(DiagnosticFormTable.user_id == user_id).values(
                niche=niche,
                pain=pain,
                problem=problem,
                digitalization=digitalization,
                finance=finance,
                purpose=purpose
            ))
            await session.commit()

    async def update_consult_form(self, user_id: int, focus: str, process: str, deadline: str,
                               features: str, criteria: str):
        async with self._sessions() as session:
            await session.execute(update(ConsultFormTable).where(ConsultFormTable.user_id == user_id).values(
                focus=focus,
                process=process,
                deadline=deadline,
                features=features,
                criteria=criteria
            ))
            await session.commit()

    async def del_deeplink(self, link: str):
        async with self._sessions() as session:
            await session.execute(delete(DeeplinksTable).where(DeeplinksTable.link == link))
            await session.commit()

    async def del_link(self, link_id: str):
        async with self._sessions() as session:
            await session.execute(delete(OneTimeLinksIdsTable).where(OneTimeLinksIdsTable.link == link_id))
            await session.commit()

    async def del_admin(self, user_id: int):
        async with self._sessions() as session:
            await session.execute(delete(AdminsTable).where(AdminsTable.user_id == user_id))
            await session.commit()