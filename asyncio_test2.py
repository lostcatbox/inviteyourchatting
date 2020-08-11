import asyncio
import sqlite3
import time


async def sleep():
    await asyncio.sleep(1)


async def main():
    # asyncio.sleep은 아무리 많아져도 비동기적으로 잘 돌아간다.
    futures = [
        asyncio.ensure_future(sleep()) for i in range(1000)
    ]
    await asyncio.gather(*futures)


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(f'{end-start}')
