import asyncio
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


async def sleep(executor=None):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, time.sleep, 1)


async def main():

    # max_workers에 따라서 실행시간이 달라지는 것을 확인할 수 있다.
    # (하지만 workers가 많아질수록 컨텍스트 스위칭 비용도 커진다.)
    # None으로 하는 경우는 디폴트로 설정한 workers수가 작아서 인지 훨씬 더 오래걸린다.

    executor = ThreadPoolExecutor(max_workers=1000)

    # asyncio.ensure_future함수는 태스크를 현재 실행하지 않고,
    # 이벤트 루프가 실행될 때 실행할 것을 보증해주는 함수
    futures = [
        asyncio.ensure_future(sleep(executor)) for i in range(1000)
    ]
    await asyncio.gather(*futures)


if __name__ == "__main__":
    start = time.time()
    # python 3.7부터는 이벤트 루프를 따로 명시적으로 지정하지 않고,
    # asyncio.run으로 돌릴 수 있다.
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    
    end = time.time()
    print(f'time taken: {end-start}')
