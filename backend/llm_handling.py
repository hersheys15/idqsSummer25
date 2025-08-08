#G Map APIKEY
#AIzaSyAj1C-cYIoQVTgJuStqpTtGoLIjhTBbvdA

import requests, json, googlemaps
from datetime import datetime
from prompt_utils import retrieve_chunks, build_prompt

def generate_response(prompt, stream=True):
    retrieved_chunks = retrieve_chunks(prompt)
    # Build the prompt using the retrieved chunks
    prompt = build_prompt(prompt, retrieved_chunks)
    # Make a POST request to the LLM API with the prompt
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": prompt},
        stream=True
    )

    if stream:
        # This is a generator — used for streaming line-by-line
        def generator():
            for line in response.iter_lines():
                if line:
                    data = json.loads(line.decode("utf-8"))
                    if "response" in data:
                        yield data["response"]
                    if data.get("done"):
                        break
        return generator()
    # else:
    #     # For non-streaming mode
    #     output = ""
    #     for line in response.iter_lines():
    #         if line:
    #             data = json.loads(line.decode("utf-8"))
    #             if "response" in data:
    #                 output += data["response"]
    #             if data.get("done"):
    #                 break
    #     return output.strip()


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