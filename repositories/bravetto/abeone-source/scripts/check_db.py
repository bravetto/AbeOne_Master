import asyncio
from sqlalchemy import text
from app.core.database import get_db

async def check_tables():
    try:
        async for session in get_db():
            result = await session.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public';"))
            tables = result.fetchall()
            print("Existing tables:")
            for row in tables:
                print(f"  {row[0]}")
            await session.close()
            break
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_tables())
