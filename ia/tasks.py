from celery import shared_task
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain_community.llms import Ollama

def get_user_memory(user_id):
    user_id = str(user_id) if user_id is not None else "anonimo"
    if user_id not in get_user_memory.memories:
        get_user_memory.memories[user_id] = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
    return get_user_memory.memories[user_id]
get_user_memory.memories = {}

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
    "Eres un asesor virtual experto en electrónica y debes responder SIEMPRE en español. "
    "Utiliza únicamente la información del catálogo de productos y tableros de discusión que se te proporciona a continuación para asesorar al usuario. "
    "No inventes productos ni tableros, y no menciones información que no esté en el catálogo. "
    "Responde de forma clara, útil y profesional, como lo haría un asesor humano en una tienda. "
    "Si la pregunta del usuario no puede ser respondida con la información del catálogo, sugiere alternativas de los productos/tableros disponibles o indica que no tienes información suficiente. "
    "No menciones que tienes un contexto ni detalles técnicos internos.\n"
    "\nCATÁLOGO DE PRODUCTOS Y TABLEROS DISPONIBLES:\n{contexto_usuario}\n"
    "Historial de la conversación:\n{chat_history}\n"
    "Pregunta del usuario: (incluida arriba en el contexto)\n"
    "Respuesta:"
)
prompt = PromptTemplate(
    input_variables=["contexto_usuario", "chat_history"],
    template=template
)

llm = Ollama(model="llama2", base_url="http://llama:11434")

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
        return str(response)
    except Exception as e:
        return f"Error interno: {str(e)}"
