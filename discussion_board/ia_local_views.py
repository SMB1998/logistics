from rest_framework.views import APIView
from rest_framework.response import Response
from celery.result import AsyncResult
from .tasks import ask_ollama_task

class LocalIAInteractView(APIView):
    def post(self, request):
        prompt = request.data.get('prompt')
        task = ask_ollama_task.delay(prompt)
        return Response({"task_id": task.id})

class IAResultView(APIView):
    def get(self, request, task_id):
        result = AsyncResult(task_id)
        if result.ready():
            return Response({"status": "done", "response": result.result})
        else:
            return Response({"status": "pending"})
