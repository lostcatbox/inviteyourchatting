import asyncio
import websockets

HOST = ''
PORT = 7777

class UserManager:  # 사용자관리 및 채팅 메세지 전송을 담당하는 클래스
    # ① 채팅 서버로 입장한 사용자의 등록
    # ② 채팅을 종료하는 사용자의 퇴장 관리
    # ③ 사용자가 입장하고 퇴장하는 관리
    # ④ 사용자가 입력한 메세지를 채팅 서버에 접속한 모두에게 전송

    def __init__(self):
        self.users = {}  # 사용자의 등록 정보를 담을 사전 {사용자 이름:(소켓,주소),...}

    async def addUser(self, username, conn, addr):  # 사용자 ID를 self.users에 추가하는 함수
        if username in self.users:  # 이미 등록된 사용자라면
            await conn.send('이미 등록된 사용자입니다.\n')
            return None

        self.users[username] = (conn, addr)

        await self.sendMessageToAll('[%s]님이 입장했습니다.' % username)
        print('+++ 대화 참여자 수 [%d]' % len(self.users))

        return username

    async def removeUser(self, username):  # 사용자를 제거하는 함수
        if username not in self.users:
            return

        del self.users[username]

        await self.sendMessageToAll('[%s]님이 퇴장했습니다.' % username)
        print('--- 대화 참여자 수 [%d]' % len(self.users))

    async def messageHandler(self, username, msg):  # 전송한 msg를 처리하는 부분
        if msg[0] != '/':  # 보낸 메세지의 첫문자가 '/'가 아니면
            await self.sendMessageToAll('[%s] %s' % (username, msg))
            return

        if msg.strip() == '/quit':  # 보낸 메세지가 'quit'이면
            await self.removeUser(username)
            return -1

    async def sendMessageToAll(self, msg):
        for conn, addr in self.users.values():
            await conn.send(msg)

    async def registerUsername(self, websocket):
        while True:
            await websocket.send('로그인ID:')
            username = await websocket.recv()
            username = username.strip()
            if await self.addUser(username, websocket, websocket.remote_address[0]):
                return username

userman = UserManager()
async def accept(websocket, path):

    print('[%s] 연결됨' % websocket.remote_address[0])
    try:
        username = await userman.registerUsername(websocket)
        msg = await websocket.recv()
        while msg:
            print(msg)
            if await userman.messageHandler(username, msg) == -1:
                await websocket.close()
                break
            msg = await websocket.recv()
        print('[%s] 접속종료' % websocket.remote_address[0])
        await userman.removeUser(username)

    except Exception as e:
        print(e)

#--------------------------------------------------------
    # --------------------------------------------------------
    # --------------------------------------------------------
try:
    start_server = websockets.serve(accept, "", 7777);

    # 웹 소켓 서버 생성.호스트는 localhost에 port는 9998로 생성한다.

    # 비동기로 서버를 대기한다.
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    print('--- 채팅 서버를 종료합니다.')

