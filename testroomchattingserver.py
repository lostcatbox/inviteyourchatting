import asyncio
import websockets
from random import randint

HOST = ''
PORT = 7777
lock = asyncio.Lock()

class UserManager:  # 사용자관리 및 채팅 메세지 전송을 담당하는 클래스
    # ① 채팅 서버로 입장한 사용자의 등록
    # ② 채팅을 종료하는 사용자의 퇴장 관리
    # ③ 사용자가 입장하고 퇴장하는 관리
    # ④ 사용자가 입력한 메세지를 채팅 서버에 접속한 모두에게 전송

    def __init__(self):
        self.users = {}  # 사용자의 등록 정보를 담을 사전 {사용자 이름:(소켓,주소),...}

    async def addUser(self, username, conn, addr):  # 사용자 ID를 self.users에 추가하는 함수
        if not username:
            await conn.send('사용자 이름을 등록해주세요\n')
            return None
        if username in self.users:  # 이미 등록된 사용자라면
            await conn.send('이미 등록된 사용자입니다.\n')
            return None
        await lock.acquire()
        try:
            self.users[username] = (conn, addr)
        finally:
            lock.release()

        await self.sendMessageToAll('[%s]님이 입장했습니다.' % username)
        print('+++ 대화 참여자 수 [%d]' % len(self.users))

        return username

    async def removeUser(self, username):  # 사용자를 제거하는 함수
        if username not in self.users:
            return

        await lock.acquire()
        try:
            del self.users[username]
        finally:
            lock.release()


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
            for username, conn in self.users.items():
                try:
                    await conn[0].send(msg)
                except:
                    self.removeUser(username)
                    pass

    async def registerUsername(self, websocket):
        while True:
            await websocket.send('로그인ID:')
            username = await websocket.recv()
            username = username.strip()
            if await self.addUser(username, websocket, websocket.remote_address[0]):
                return username


present_room = {}
using_room_number = []

async def issued_using_room_number():
    while True:
        room_number = randint(1000,9999)
        if not room_number in using_room_number:
            break
    await lock.acquire()
    try:
        using_room_number.append(room_number)
    finally:
        lock.release()
    return room_number

class ChattingRoom():
    @classmethod
    async def create(cls):
        self = ChattingRoom()
        self.user = UserManager()
        self.room_number = await issued_using_room_number()
        present_room[self.room_number] = self
        return self










async def accept(websocket, path):

    print('[%s] 연결됨' % websocket.remote_address[0])
    try:
        await websocket.send("룸서버를입력해주세요")
        room_number = await websocket.recv()
        room_number = int(room_number) #str에서 int로 변환
        print("1")

        if not room_number in list(present_room.keys()):
            print("2")
            await websocket.send('룸이 존재하지않습니다.')
            chattingroom = await ChattingRoom.create()
            await websocket.send('[%i]룸이 생성합니다' % chattingroom.room_number)
        else:
            await lock.acquire()
            try:
                chattingroom = present_room[room_number]
            finally:
                lock.release()

            await websocket.send('[%i]룸에 입장하였습니다' % chattingroom.room_number)

        username = await chattingroom.user.registerUsername(websocket)
        msg = await websocket.recv()
        while msg:
            print(msg)
            print(chattingroom.user.users.values())
            if await chattingroom.user.messageHandler(username, msg) == -1:
                break
            msg = await websocket.recv()
        print('[%s] 접속종료' % websocket.remote_address[0])
        await chattingroom.user.removeUser(username)

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




