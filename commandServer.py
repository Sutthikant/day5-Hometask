import asyncio
import os

class CommandServer:
    def __init__(self):
        pass

    async def handle_client(self, reader, writer):
        while True:
            data = await reader.readline()
            if not data:
                break

            command = data.decode().strip()
            if command.startswith("cd"):
                path = command.split(" ")[1]
                os.chdir(path)
                writer.write(b"OK\n")
            elif command == "list":
                files = os.listdir()
                for file in files:
                    writer.write(file.encode() + b"\n")
            elif command.startswith("get"):
                filename = command.split(" ")[1]
                if not os.path.isfile(filename):
                    writer.write(b"File not found\n")
                else:
                    with open(filename, "rb") as f:
                        content = f.readlines()
                        for line in content:
                            writer.write(line)

    async def start(self):
        server = await asyncio.start_server(self.handle_client, 'localhost', 8888)

        async with server:
            await server.serve_forever()

if __name__ == '__main__':
    command_server = CommandServer()
    asyncio.run(command_server.start())
