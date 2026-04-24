# from typing import Annotated, TypeVar
# from uuid import UUID
#
# from fastapi import Depends, HTTPException
# from sqlalchemy import select
# from sqlalchemy.orm import DeclarativeBase
# from starlette.status import HTTP_403_FORBIDDEN
#
# from api.dependencies.database_session import DBSession
# from api.dependencies.services.auth import TokenPayloadDepends
#
# BaseSQLTableT = TypeVar("BaseSQLTableT", bound=DeclarativeBase)
#
#
# async def _model_user(model_user) -> type[BaseSQLTableT]:
#     return model_user
#
#
# UserTableDep = Annotated[type[BaseSQLTableT], Depends(dependency=_model_user)]
#
#
# async def _current_user_id(token_payload: TokenPayloadDepends) -> UUID:
#     if token_payload.get("sub"):
#         return token_payload.sub
#
#     raise HTTPException(
#         status_code=HTTP_403_FORBIDDEN,
#         detail="user_not_found",
#     )
#
#
# def user_id_with_check_action(
#         user_model: UserTableDep,
# ):
#     async def check_action_status(
#             session: DBSession,
#             user_id: CurrentUserIDDeps,
#     ) -> UUID:
#         if await session.scalar(select(user_model.).where(user_model.id == user_id)):
#             raise HTTPException(
#                 status_code=HTTP_403_FORBIDDEN,
#                 detail="Access denied for this action",
#             )
#         return user_id
#
#     return check_action_status
#
# CurrentUserIDDeps = Annotated[UUID, Depends(dependency=_current_user_id)]