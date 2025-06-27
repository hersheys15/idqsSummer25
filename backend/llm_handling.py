# def generate_response(prompt):
#     # Example: store to local file (simple logging)
#     with open("prompt_log.txt", "a") as f:
#         f.write(f"{prompt}\n")

#     # TODO: Replace this with real LLM API call
#     response = f"Echo: {prompt}"  # or use OpenAI/Claude/Gemini/etc.
#     requests.post("http://localhost:11434/api/generate", json={"model": "llama3", "prompt": prompt})
#     return response

#G Map APIKEY
#AIzaSyAj1C-cYIoQVTgJuStqpTtGoLIjhTBbvdA

import googlemaps
from datetime import datetime
import requests
import json

def generate_response(prompt):
    # TODO: Prompt engineering: ensure the prompt is well-formed
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": prompt},
        stream=True
    )

    output = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            if "response" in data:
                output += data["response"]
            if data.get("done"):
                break

    return output.strip()


# This module handles the interaction with the LLM (Large Language Model) API.
# def generate_response(prompt):
#     gmaps = googlemaps.Client(key='AIzaSyAj1C-cYIoQVTgJuStqpTtGoLIjhTBbvdA')

#     # Geocoding an address
#     geocode_result = gmaps.geocode('4000 Central Florida Blvd, Orlando, FL')

#     # Look up an address with reverse geocoding
#     reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

#     # Request directions via public transit
#     now = datetime.now()
#     directions_result = gmaps.directions("Sydney Town Hall",
#                                         "Parramatta, NSW",
#                                         mode="transit",
#                                         departure_time=now)

#     # Validate an address with address validation
#     addressvalidation_result =  gmaps.addressvalidation(['1600 Amphitheatre Pk'], 
#                                                         regionCode='US',
#                                                         locality='Mountain View', 
#                                                         enableUspsCass=True)

#     # # Get an Address Descriptor of a location in the reverse geocoding response
#     # address_descriptor_result = gmaps.reverse_geocode((40.714224, -73.961452), enable_address_descriptor=True)
#     return f"Echoing your question: '{geocode_result}' is a great question!"