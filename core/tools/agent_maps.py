import json
import googlemaps
from prompt import Prompt
from langchain_google_genai import ChatGoogleGenerativeAI


class MapsAgent:

    def __init__(self, model_name: str, temperature: float, api_key: str, gmaps_api_key: str) -> None:
        llm = ChatGoogleGenerativeAI(
            model=model_name, temperature=temperature,
            api_key=api_key
        )
        self.llm = llm
        self.gmaps = googlemaps.Client(key=gmaps_api_key)

    def _destination_parser(self, query: str):
        result = self.llm.invoke(Prompt.dest_prompt.format(question=query))
        print("[Result Destination Parser]", result)
        result_destination = result.content
        return result_destination

    def _source_parser(self, lon: float, lat: float):
        result_reverse_geo = self.gmaps.reverse_geocode([lat, lon])
        print("[Result Geo Reverse]", result_reverse_geo)
        result_reverse_geo = result_reverse_geo[0]["formatted_address"]
        return result_reverse_geo
    
    def _gmaps_suggest(self, origin: str, destination: str):
        result_transit = self.gmaps.directions(origin=origin, destination=destination, mode="transit", transit_routing_preference="fewer_transfers")
        result_driving = self.gmaps.directions(origin=origin, destination=destination, mode="driving")
        scope_context_transit = [
            f"""
            {index['distance']['text']}
            {index['duration']['text']}
            Travel Mode: {index['travel_mode']}
            """ for index in result_transit[0]["legs"][0]["steps"]
        ]
        scope_context_transit = "\n".join(scope_context_transit)
        scope_context_drive = {
            "distance": result_driving[0]["legs"][0]["distance"]["text"],
            "duration": result_driving[0]["legs"][0]["duration"]["text"]
        }
        return scope_context_transit, scope_context_drive

    def _parsing_json(self, content: str):
        return json.loads(content.replace("```json", "").replace("```", ""))

    def invoke(self, query: str, lon: float, lat: float):
        response = {}
        destination = self._destination_parser(query=query)
        origin = self._source_parser(lon=lon, lat=lat)
        data_transit, data_drive = self._gmaps_suggest(origin=origin, destination=destination)
        _result_maps = self.llm.invoke(
            input=Prompt.transit_prompt.format(rute_perjalanan=data_transit, transit_prompt_json=Prompt.transit_prompt_json)
        )
        print(_result_maps.content)
        result_maps = self._parsing_json(_result_maps.content)
        _result_drive = self.llm.invoke(
            input=Prompt.drive_prompt.format(info_perjalanan=str(data_drive), drive_prompt_json=Prompt.drive_prompt_json)
        )
        print(_result_drive.content)
        result_drive = self._parsing_json(_result_drive.content)
        response["transit"] = result_maps
        response["grab-ride"] = result_drive
        return response