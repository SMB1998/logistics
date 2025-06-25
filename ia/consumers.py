import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from .tasks import ask_ollama_task

class IAConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.history = []  # Historial por conexión
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        prompt = data.get('prompt', '')
        self.history.append({"role": "user", "content": prompt})
        task = ask_ollama_task.delay(prompt, self.history)
        response = await self.wait_for_task(task)
        self.history.append({"role": "assistant", "content": response})
        await self.send(text_data=json.dumps({'response': response}))

    async def wait_for_task(self, task, timeout=1440):
        import asyncio
        for _ in range(timeout * 2):
            if task.ready():
                return task.result
            await asyncio.sleep(0.5)
        return 'La tarea tardó demasiado en responder.'
