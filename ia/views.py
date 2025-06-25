from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import ask_ollama_task
from celery.result import AsyncResult

class LocalIAInteractView(APIView):
    def post(self, request):
        prompt = request.data.get('prompt')
        user_id = request.data.get('user_id', 'anonimo')
        if not prompt:
            return Response({'error': 'Prompt requerido'}, status=status.HTTP_400_BAD_REQUEST)
        task = ask_ollama_task.delay(prompt, user_id)
        return Response({'task_id': task.id}, status=status.HTTP_202_ACCEPTED)

class IAResultView(APIView):
    def get(self, request, task_id):
        result = AsyncResult(task_id)
        if result.state == 'PENDING':
            return Response({'status': 'pending'}, status=status.HTTP_202_ACCEPTED)
        elif result.state == 'SUCCESS':
            return Response({'status': 'success', 'response': result.result}, status=status.HTTP_200_OK)
        else:
            return Response({'status': result.state, 'error': str(result.info)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
