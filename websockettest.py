#websockettest.py

import asyncio
# 웹 소켓 모듈을 선언한다.
import websockets


# 클라이언트 접속이 되면 호출된다.
async def accept(websocket, path):
    count_number = 0
    while True:
        # 클라이언트로부터 메시지를 대기한다.
        data = await websocket.recv();
        print("receive : " + data);
        user_address=websocket.remote_address[0]
        # 클라인언트로 echo를 붙여서 재 전송한다.
        count_number +=1
        await websocket.send("echo : " + data + str(count_number) + user_address);

# 웹 소켓 서버 생성.호스트는 localhost에 port는 9998로 생성한다.
start_server = websockets.serve(accept, "", 7777);

# 비동기로 서버를 대기한다.
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()