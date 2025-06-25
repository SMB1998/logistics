from celery import shared_task
from django.core.management import call_command
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain_community.llms import Ollama

llm = Ollama(model="llama2", base_url="http://llama:11434")
user_memories = {}

def get_user_memory(user_id):
    # Convierte user_id a string para asegurar que sea hashable
    user_id = str(user_id) if user_id is not None else "anonimo"
    if user_id not in user_memories:
        user_memories[user_id] = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
    return user_memories[user_id]

def build_context_text():
    from components.models import Components
    from discussion_board.models import DiscussionBoard
    components = Components.objects.all().values(
        'nombre', 'referencia', 'stock_number', 'price_breaks', 'precio', 'proveedor__nombre', 'url', 'datasheet_url', 'image_url'
    )
    boards = DiscussionBoard.objects.all().values(
        'nombre', 'description', 'referencia', 'created_at', 'status', 'admin__username'
    )
    comp_text = "\n".join([
        f"- {c['nombre']} (ref: {c['referencia']}, stock: {c['stock_number']}, precio: {c['precio']}, proveedor: {c['proveedor__nombre']})"
        for c in components
    ])
    board_text = "\n".join([
        f"- {b['nombre']} (desc: {b['description']}, admin: {b['admin__username']}, estado: {b['status']})"
        for b in boards
    ])
    return f"Componentes disponibles:\n{comp_text}\n\nTableros de discusión:\n{board_text}"

template = (
    "Eres un asesor experto en electrónica de una tienda.\n"
    "{contexto_usuario}\n"
    "Historial de la conversación:\n{chat_history}\n"
    "Respuesta:"
)
prompt = PromptTemplate(
    input_variables=["contexto_usuario", "chat_history"],
    template=template
)

@shared_task
def ask_ollama_task(prompt_text, user_id=None, history=None):
    try:
        catalogo = build_context_text()
        memory = get_user_memory(user_id or "anonimo")
        contexto_usuario = (
            f"{catalogo}\n\n"
            f"Pregunta del usuario: {prompt_text}"
        )
        chain = LLMChain(
            llm=llm,
            prompt=prompt,
            memory=memory
        )
        response = chain.predict(
            contexto_usuario=contexto_usuario
        )
        # Siempre retorna string
        return str(response)
    except Exception as e:
        # Devuelve un mensaje de error serializable
        return f"Error interno: {str(e)}"

@shared_task
def sync_discussion_board_elasticsearch():
    call_command('sync_elasticsearch_disc_boards')