import requests
import json 

url = "http://127.0.0.1:5000/v1/completions"
headers = {"Content-Type": "application/json"}

def lista_modelos():
    try:
        response = requests.get("http://127.0.0.1:5000/v1/internal/model/list")
        response.raise_for_status()
        data = response.json()
        return data['model_names']
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener la lista de modelos: {e}")
        return []

def seleccionar_modelo():
    modelos = lista_modelos()
    if not modelos:
        print("No hay modelos disponibles.")
        return None
    print("\n---Selecciona un modelo:---")
    for i, modelo in enumerate(modelos, 1):
        print(f"{i}. {modelo}")
    
    while True:
        try:
            option = input("Introduce el número del modelo: ")
            option = int(option) - 1
            if 0 <= option < len(modelos):
                selected_model = modelos[option]
                cargar_modelo(selected_model)
                return selected_model
            else:
                print("Por favor, selecciona un modelo válido.")
        except ValueError:
            print("Entrada no válida. Introduce un número.")

def cargar_modelo(model):
    url = "http://127.0.0.1:5000/v1/internal/model/load"
    
    body = {
        'model_name': model,
        "args": {
            "load_in_4bit": True,
            "n_gpu_layers": 12,
        },
        "settings": {
            "instruction_template": "Alpaca"
        }
    }
    
    try:
        res = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(body))
        res.raise_for_status()
        print(f"Modelo {model} cargado exitosamente.")
    except requests.exceptions.RequestException as e:
        print(f"Error al cargar el modelo: {e}")

def obtener_parametros():
    personaje_principal = input("Nombre del personaje principal: ")
    personaje_secundario = input("Nombre del personaje secundario: ")
    lugar = input("Lugar donde transcurre el relato: ")
    accion = input("Acción importante que debe acontecer en la historia: ")
    
    print("\n---Selecciona la creatividad:---")
    print("a) Creatividad alta")
    print("b) Creatividad media")
    print("c) Creatividad baja")
    opcion = input("Opción (a/b/c): ").lower()

    temperatura = {"a": 1.0, "b": 0.7, "c": 0.3}.get(opcion, 0.7)
    return personaje_principal, personaje_secundario, lugar, accion, temperatura

def creacion_prompt(personaje_principal, personaje_secundario, lugar, accion, temperatura):
    prompt = f"Créame una historia con menos de 200 tokens con estos dos personajes: {personaje_principal} y {personaje_secundario}, en este lugar: {lugar}, y tiene que pasar esta acción: {accion}."
    body = {"prompt": prompt, "max_tokens": 250, "temperature": temperatura}
    return body


while True:
    print("¡Bienvenido al generador de historias!")
    res = input("¿Quieres generar una historia? (Presiona Enter para empezar o escribe 'No' para salir): ")
    if res == "No":
        exit()
    modelo = seleccionar_modelo()
    body = creacion_prompt(*obtener_parametros())
    print("\n--- Generando Historia ---")
    response = requests.post(url=url, headers=headers, json=body, verify=False)
    message_response = json.loads(response.content.decode("utf-8"))
    assistant_message = message_response['choices'][0]['text']
    print("\n--- Historia Generada ---")
    print(assistant_message)

