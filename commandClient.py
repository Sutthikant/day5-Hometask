import asyncio
import aioconsole

class CommandClient:
    def __init__(self):
        pass

    # read messages from the server and print them to the console
    async def receive_messages(self, reader):
        while True:
            data = await reader.readline()
            if not data:
                break
            print(data.decode().rstrip())


    # read messages from the user and send them to the server
    async def send_messages(self, writer):
        while True:
            command = await aioconsole.ainput()

            # print(f'Sending: {command}')
            writer.write((command + "\n").encode())
            await writer.drain()


    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection('localhost', 8888)

        # get event loop
        loop = asyncio.get_event_loop()

        # start a task to send messages to the server
        # loop.run_until_complete(self.receive_messages(self.reader))
        # loop.run_until_complete(self.send_messages(self.writer))

        t2 = asyncio.create_task(self.receive_messages(self.reader))
        t1 = asyncio.create_task(self.send_messages(self.writer))

        # await asyncio.create_task(self.receive_messages(self.reader))
        # await asyncio.create_task(self.send_messages(self.writer))
        # #
        await asyncio.gather(t1, t2)

if __name__ == '__main__':
    client = CommandClient()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(client.connect())
    except KeyboardInterrupt:
        pass

    loop.close()
