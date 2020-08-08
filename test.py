import asyncio

async def cat(i):
    print("hello")
    await asyncio.sleep(5)
    print('world')
    return i

async def main():
    futures = [asyncio.ensure_future(cat(i)) for i in range(6)]

    result = await asyncio.gather(*futures)
    print(result)

# Python 3.7+
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()