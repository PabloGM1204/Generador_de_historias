import requests
import json 

url = "http://127.0.0.1:5000/v1/completions"
headers = {"Content-Type": "application/json"}

def obtener_parametros():
    personaje_principal = input("Nombre del personaje principal: ")
    personaje_secundario = input("Nombre del personaje secundario: ")
    lugar = input("Lugar donde transcurre el relato: ")
    accion = input("Acción importante que debe acontecer en la historia: ")
    
    print("\nSelecciona la creatividad:")
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
    body = creacion_prompt(*obtener_parametros())
    print("\n--- Generando Historia ---")
    response = requests.post(url=url, headers=headers, json=body, verify=False)
    message_response = json.loads(response.content.decode("utf-8"))
    assistant_message = message_response['choices'][0]['text']
    print("\n--- Historia Generada ---")
    print(assistant_message)

