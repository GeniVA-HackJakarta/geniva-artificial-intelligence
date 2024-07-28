import base64
import requests

def hit_text_recommendation(url: str, query: str):
    payload = {"query": query}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(response.json())
    else:
        response.raise_for_status()

def hit_image_recommendation(url: str, file_path: str):
    with open(file_path, 'rb') as file:
        encoded_string = base64.b64encode(file.read()).decode('utf-8')
        payload = {"file": encoded_string}
        response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(response.json())
    else:
        response.raise_for_status()

def hit_multimodal_recommendation(url: str, query: str, file_path: str):
    payload = {"query": query, "file": ""}
    with open(file_path, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode("utf-8")
        payload["file"] = encoded_string
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(response.json())
    else:
        response.raise_for_status()

def hit_transportation_recommendation(url: str, query: str, lon: float = 106.7829313, lat: float = -6.2847815):
    payload = {"query": query, "lon": lon, "lat": lat}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(response.json())
    else:
        response.raise_for_status()

# Example usage:
if __name__ == "__main__":
    # url = "http://localhost:8000/generate-recommendation"
    url = "http://170.64.228.233:8000/generate-recommendation"
    text_result = hit_text_recommendation(url, "Nama: Alif Ramadhan, siapa kamu")
    text_result = hit_text_recommendation(url, "Nama: Alif Ramadhan, siapa kamu bangsat")
    text_result = hit_text_recommendation(url, "Nama: Alif Ramadhan, aku laper banget pengen makan yang manis-manis dengan budget 50$")
    text_result = hit_text_recommendation(url, "Nama: Alif Ramadhan, aku laper banget pengen makan")
    text_result = hit_text_recommendation(url, "Nama: Alif Ramadhan, ada promo apa aja hari ini")
    image_result = hit_image_recommendation(url, "static/keju.jpg")
    multimodal_result = hit_multimodal_recommendation(url, query="Berikan rekomendasi makanan terkait gambar yang diberikan", file_path="static/keju.jpg")
    geo_result = hit_transportation_recommendation(url, query="Pengen jalan-jalan ke monas, enaknya naik apa yaa")