from celery import shared_task
from django.core.management import call_command
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama

def build_context():
    from components.models import Components
    from discussion_board.models import DiscussionBoard, DiscussionBoardComponent
    components = list(Components.objects.all().values())
    boards = list(DiscussionBoard.objects.all().values())
    board_components = list(DiscussionBoardComponent.objects.all().values())
    return {
        'components': components,
        'boards': boards,
        'board_components': board_components
    }

@shared_task
def ask_ollama_task(prompt, history=None):
    context = build_context()
    # Construye el historial en el prompt si existe
    history_text = ""
    if history:
        for turn in history:
            if turn["role"] == "user":
                history_text += f"Usuario: {turn['content']}\n"
            elif turn["role"] == "assistant":
                history_text += f"Asistente: {turn['content']}\n"
    template = (
        "Eres un asistente experto en electrónica. "
        "Siempre debes fundamentar tus respuestas usando la información de los tableros de discusión o los componentes que aparecen en el contexto. "
        "Si la pregunta no se puede responder usando esa información, indícalo explícitamente. "
        "En cada respuesta, cita o referencia los tableros de discusión o componentes relevantes del contexto. "
        "No menciones ni uses información de usuarios. "
        "Historial de la conversación hasta ahora:\n{history}\n"
        "Contexto:\n{context}\n"
        "Pregunta del usuario: {user_question}"
    )
    prompt_template = ChatPromptTemplate.from_template(template)
    formatted_prompt = prompt_template.format(context=context, user_question=prompt, history=history_text)
    llm = Ollama(model="llama2", base_url="http://llama:11434")
    response = llm.invoke(formatted_prompt, max_tokens=128)
    return response

@shared_task
def sync_discussion_board_elasticsearch():
    call_command('sync_elasticsearch_disc_boards')