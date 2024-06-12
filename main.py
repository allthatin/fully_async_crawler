import sys
import asyncio
import time
from management import execute_from_command_line
from database.connection import get_async_session

async def main():
    async with get_async_session() as session:
        await execute_from_command_line(sys.argv, session)


if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")