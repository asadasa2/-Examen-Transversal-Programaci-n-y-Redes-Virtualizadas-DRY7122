import requests
import urllib.parse

geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
key = "2715a6e0-ddbc-48a2-970b-2c0fd4bbf241"  

def geocoding(location, key):
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    
    try:
        replydata = requests.get(url)
        replydata.raise_for_status()  
        json_data = replydata.json()

        if 'hits' in json_data and len(json_data['hits']) > 0:
            lat = json_data["hits"][0]["point"]["lat"]
            lng = json_data["hits"][0]["point"]["lng"]
            return 200, lat, lng
        else:
            print(f"No se encontraron resultados para {location}.")
            return 404, None, None
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud HTTP: {e}")
        return 500, None, None

def calcular_distancia_duracion_indicaciones(origen, destino, key, medio_transporte):
    # Geocodificar origen y destino
    orig_status, orig_lat, orig_lng = geocoding(origen, key)
    dest_status, dest_lat, dest_lng = geocoding(destino, key)

    if orig_status != 200 or dest_status != 200:
        print("Error en la geocodificación. No se puede calcular la distancia y duración.")
        return None, None, None

    print(f"Coordenadas de origen: latitud {orig_lat}, longitud {orig_lng}")
    print(f"Coordenadas de destino: latitud {dest_lat}, longitud {dest_lng}")

    
    route_params = {
        "point": [f"{orig_lat},{orig_lng}", f"{dest_lat},{dest_lng}"],
        "vehicle": medio_transporte,  
        "key": key,
        "instructions": "true",  
        "locale": "es"  
    }
    
    try:
        route_response = requests.get(route_url, params=route_params)
        route_response.raise_for_status()  
        route_data = route_response.json()

        if 'paths' in route_data and len(route_data['paths']) > 0:
            distancia = route_data['paths'][0]['distance'] / 1000  
            duracion = route_data['paths'][0]['time'] / 1000 / 60  
            instrucciones = route_data['paths'][0]['instructions']

            print(f"Distancia: {distancia:.2f} km")
            print(f"Duración: {duracion:.2f} minutos")
            print("Instrucciones:")
            for instruccion in instrucciones:
                print(f"{instruccion['text']} - {instruccion['distance'] / 1000:.2f} km")
            
            return distancia, duracion, instrucciones
        else:
            print("No se encontraron rutas entre los puntos especificados.")
            return None, None, None
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud HTTP: {e}")
        return None, None, None

def main():
    while True:
        origen = input("Introduce la ciudad de origen (o 's' para salir): ")
        if origen.lower() == 's':
            break
        destino = input("Introduce la ciudad de destino (o 's' para salir): ")
        if destino.lower() == 's':
            break

        
        medio_transporte = input("Medio de transporte (car, bike, foot): ").strip().lower()
        if medio_transporte not in ['car', 'bike', 'foot']:
            print("Medio de transporte no válido. Por favor, elija entre 'car', 'bike', o 'foot'.")
            continue

        distancia, duracion, instrucciones = calcular_distancia_duracion_indicaciones(origen, destino, key, medio_transporte)

        if distancia is not None and duracion is not None:
            print(f"\nResumen del viaje de {origen} a {destino}:")
            print(f"Distancia: {distancia:.2f} km")
            print(f"Duración: {duracion:.2f} minutos")
            print("Instrucciones:")
            for instruccion in instrucciones:
                print(f"{instruccion['text']} - {instruccion['distance'] / 1000:.2f} km")
        else:
            print("No se pudo calcular la distancia y duración del viaje.\n")

if __name__ == "__main__":
    main()