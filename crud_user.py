import asyncio

from sqlalchemy import select
from sqlalchemy.engine import Result, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from core.models import db_manager, User, Post, Profile


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print("user", user)
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    result: Result = await session.execute(stmt)
    user: User | None = result.scalar_one()
    # user: User | None = await session.scalar(stmt)
    print(f"find username = {username} by {user}")
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
) -> Profile:
    profile = Profile(user_id=user_id, first_name=first_name, last_name=last_name)
    session.add(profile)
    await session.commit()
    print("profile", profile)
    return profile


async def snow_profiles(session: AsyncSession):
    stmt = select(User).options(joinedload(User.profile))
    result: Result = await session.execute(stmt)
    users = result.scalars()
    for user in users:
        print(user.profile.first_name)


async def create_posts(
    session: AsyncSession, user_id: int, *post_titles: str
) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in post_titles]
    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts


async def get_users_with_posts(session: AsyncSession):
    # stmt = select(User).options(joinedload(User.posts)).order_by(User.id)  //// var 1
    # users = await session.scalars(stmt)                                   ////  var 1
    # for user in users.unique():                                           ////  var 1

    # stmt = select(User).options(joinedload(User.posts)).order_by(User.id)   //// var2
    # result: Result = await session.execute(stmt)                            //// var2
    # users = result.unique().scalars()                                       //// var2

    stmt = select(User).options(selectinload(User.posts)).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars()
    for user in users:

        print("**" * 10)
        print(user)
        for post in user.posts:
            print("--", post)


async def get_users_with_posts_and_profiles(session: AsyncSession):

    stmt = (
        select(User)
        .options(selectinload(User.posts), joinedload(User.profile))
        .order_by(User.id)
    )
    result: Result = await session.execute(stmt)
    users = result.scalars()
    for user in users:

        print("**" * 10)
        print(user)
        print("profile:=", user.profile)
        for post in user.posts:
            print("--", post)


async def get_post_with_authors(session: AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)
    for post in posts:
        print("**" * 10)
        print("post = ", post)
        print("user = ", post.user)


async def get_profiles_with_users_and_users_with_posts(session: AsyncSession):
    # stmt = (
    #     select(Profile)
    #     .options(joinedload(Profile.user).selectinload(User.posts))
    #     .order_by(Profile.id)
    # )
    ###### добавляем фильтрацию для этог добавляем джойн ############

    stmt = (
        select(Profile)
        .join(Profile.user)  ### + JOIN
        .options(joinedload(Profile.user).selectinload(User.posts))
        .where(User.username == "sam")
        .order_by(Profile.id)
    )

    result: Result = await session.execute(stmt)
    profiles: ScalarResult[Profile] = result.scalars()
    for prof in profiles:
        print("**" * 10)
        print("prof = ", prof.first_name)
        print("user = ", prof.user)
        print(prof.user.posts)


async def main():
    async with db_manager.session_factory() as session:
        # await create_user(session=session, username="John")
        # await create_user(session=session, username="sam")
        # await create_user(session=session, username="alice")
        # user1_jo = await get_user_by_username(session=session, username="John")
        # user2 = await get_user_by_username(session=session, username="sam")

        # id1 = int(user1.id)
        # iiid = user1.username
        # print(type(id1))
        # await create_user_profile(
        #     session=session, user_id=user1_jo.id, first_name="John", last_name="smith"
        # )
        # await create_user_profile(session=session, user_id=user2.id, first_name="sam")
        # await snow_profiles(session=session)
        # await create_posts(session, user1_jo.id, "SQL 2.0", "SQL Joins")
        #
        # await create_posts(
        #     session, user2.id, "SQL Alchemy", "SQL Create", "DELETE Table"
        # )
        # await get_users_with_posts(session)
        # await get_post_with_authors(session)
        # await get_users_with_posts_and_profiles(session)
        await get_profiles_with_users_and_users_with_posts(session)


if __name__ == "__main__":
    asyncio.run(main())
