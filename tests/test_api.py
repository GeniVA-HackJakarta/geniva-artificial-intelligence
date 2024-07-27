
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

# Example usage:
if __name__ == "__main__":
    url = "http://localhost:8000/generate-recommendation"
    # text_result = hit_text_recommendation(url, "Nama: Alif Ramadhan, aku laper banget pengen makan yang manis-manis dengan budget 50$")
    image_result = hit_image_recommendation(url, "static/keju.jpg")