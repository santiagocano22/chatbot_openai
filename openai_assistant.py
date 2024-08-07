import markdown2
from openai import OpenAI, AssistantEventHandler
from typing_extensions import override
import os

# Inicializa el cliente OpenAI con tu clave API
client = OpenAI(api_key="copy-your-key")

# Crea el asistente de viajes
def create_assistant():
    assistant = client.beta.assistants.create(
        name="Travel Assistant",
        instructions=(
            "Eres un asistente personal de viajes. Responde a las preguntas del usuario "
            "con información clara y concisa, utilizando un lenguaje cercano y amigable. "
            "Las respuestas deben ser fluidas y no exceder las 200 palabras. Los usuarios "
            "son de Latinoamérica."
        ),
        tools=[{"type": "code_interpreter"}],
        model="gpt-4o",
    )
    return assistant.id

# Crea un nuevo hilo de conversación
def create_thread():
    thread = client.beta.threads.create()
    return thread.id

# Agrega un mensaje al hilo de conversación
def add_message(thread_id, content):
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )
    return message.id

# Define la clase EventHandler para manejar eventos
class CapturingEventHandler(AssistantEventHandler):    
    def __init__(self):
        self.response_text = ""
        super().__init__()
    
    @override
    def on_text_created(self, text) -> None:
        self.response_text += text.value  # Extraer solo el valor del texto
  
    @override
    def on_text_delta(self, delta, snapshot):
        self.response_text += delta.value  # Extraer solo el valor del texto
  
    def on_tool_call_created(self, tool_call):
        pass

    def on_tool_call_delta(self, delta, snapshot):
        pass

# Ejecuta el hilo de conversación y transmite la respuesta
def run_thread(thread_id, assistant_id):
    event_handler = CapturingEventHandler()
    with client.beta.threads.runs.stream(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions="El usuario es de Latinoamérica y desea una conversación fluida y amigable.",
        event_handler=event_handler,
    ) as stream:
        stream.until_done()
    
    # Convertir Markdown a HTML
    html_response = markdown2.markdown(event_handler.response_text)
    return html_response
