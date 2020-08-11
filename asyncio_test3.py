import asyncio
async def  sleep():
    loop = asyncio.get_event_loop()
    print("전")
    
    await asyncio.sleep(5) 
    print("후")
    
async def main():
    futures = [asyncio.create_task(sleep()) for x in range(4)]
    await asyncio.sleep(10)
    
loop = asyncio.get_event_loop()
loop.run_until_complete(main())



