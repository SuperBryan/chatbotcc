import tkinter as tk
import openai
from pymongo import MongoClient
# Conectar a una instancia de MongoDB
client = MongoClient("mongodb+srv://devn8:4891@newcluster.xmnp2fj.mongodb.net/?retryWrites=true&w=majority")
db = client["dataOpenAI"]
coleccion = db["chatBotGPT"]


# Establecer la clave de acceso de la API de OpenAI
openai.api_key = "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"

# Crear una ventana principal
ventana = tk.Tk()

# Obtener el ancho y alto de la pantalla
screen_width = ventana.winfo_screenwidth()
screen_height = ventana.winfo_screenheight()

# Establecer la geometría de la ventana en base al ancho y alto de la pantalla
ventana.geometry(f"{screen_width}x{screen_height}")
ventana.title("Chatbot")

# Centro la ventana


# Crear un cuadro de entrada para el usuario
entrada_usuario = tk.Entry(ventana, width=50)
entrada_usuario.place(x=50, y=500)

# Crear un cuadro de salida para mostrar la respuesta del chatbot
salida_chatbot = tk.Text(ventana, width=50, height=20)
salida_chatbot.place(x=50, y=50)

# Configurar las etiquetas para diferenciar el dondo y colores de texto
salida_chatbot.tag_config("Usuario", background="blue", foreground= "white")
salida_chatbot.tag_config("Chatbot", background="black", foreground= "white")

# Crear una función para enviar la entrada del usuario a la API de OpenAI
def enviar_mensaje():
    # Obtener la entrada del usuario
    mensaje = entrada_usuario.get()

    # Enviar la entrada del usuario a la API de OpenAI
    respuesta = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Chatbot: {mensaje}",
        max_tokens=100
    )

    # Obtener la respuesta del chatbot
    respuesta_chatbot = respuesta.choices[0].text

    # Insertar la respuesta del chatbot en el cuadro de salida con las etiquetas
    salida_chatbot.insert("end", "Usuario: ", "Usuario")
    salida_chatbot.insert("end", mensaje + "\n", "Usuario")
    salida_chatbot.insert("end", "Chatbot: ", "Chatbot")
    salida_chatbot.insert("end", respuesta_chatbot + "\n", "Chatbot")

    # Escribir los datos en la base de datos
    coleccion.insert_one({"pregunta": mensaje, "respuesta": respuesta_chatbot})

    # Eliminar el texto del cuadro de entrada
    entrada_usuario.delete(0, "end")


# Crear un botón para enviar el mensaje
boton_enviar = tk.Button(ventana, text="Enviar", command=enviar_mensaje)
boton_enviar.place(x=350, y=500)

# Crear una funcion para enviar mensaje al presionar enter
ventana.bind("<Return>", (lambda event: enviar_mensaje()))

# Iniciar la ventana
ventana.mainloop()