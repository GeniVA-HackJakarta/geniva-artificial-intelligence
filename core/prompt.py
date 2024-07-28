class Prompt:
    inst_prompt: str = "kamu adalah GenieVA virtual assisten membantu perjalanan di aplikasi Grab, jawab secara singkat dan padat namun tetap intuitif respon nya"
    desc_prompt: str = "Berdasarkan gambar yang di upload, apa nama makanan tersebut menggunakan bahasa inggris?"
    base_prompt_routing = \
    """
    Based on provided question, please choose which action / tools should be used to fulfill the question objective

    tools provided:
    {list_tools}

    Example
    -----------------------
    question: Saya mau pesan makanan hangat dan berkuah
    tools_choosen: menu_makanan

    question: saya ingin rute perjalanan hemat dari kantor ke rumah dengan menggunakan grab car / transportasi umum
    tools_choosen: rute_bus
    -----------------------
    question: {query}
    tools_choosen: 
    """
    desc_food_prompt: str = \
    """
    Berdasarkan informasi data dibawah, berikan 1 kalimat narasi yang padat dan interaktif (disertai membaca emosi pertanyaan dari user, usahakan harus selalu solutif dan ramah)
    untuk menjawab pertanyaan dari user tanpa menyebutkan informasi terkait ID (menu id / restoran id / zomato id).
    Cukup jawab pertanyaan tanpa menyebutkan ulang pertanyaan dari user.

    data:
    {context_data}

    question: {question}
    answer:
    """
    dest_prompt: str = "Berdasarkan informasi dari user, estimasi kan kira-kira user mau ke lokasi apa dalam 1 frasa untuk dicari ke google maps\ninformasi: {question}"
    transit_prompt_json = \
    """
    {
    "total_distance": "0 km",
    "total_duration": "0 minutes",
    "steps": [
            {
                "type": "grab-bike", // opsi grab-bike / transit / walking
                "distance": "5 km",
                "duration": "15 mins",
                "price": "10.000" // mata uang IDR, untuk grab-bike disesuaikan dengan jarak tempuh, kalo transit 3.500, kalo walking 0.
            }
            ...
    ]
    }
    """
    transit_prompt: str = \
    """
    anda adalah expert dari aplikasi grab

    berdasarkan data yang diberikan, berikan estimasi jarak total, durasi total, dan opsi untuk naik grab-ride atau mengikuti angkutan umum 

    data rute perjalanan:
    {rute_perjalanan}
    
    contoh skema json:
    {transit_prompt_json}

    dengan syarat:
    - apabila jarak kurang dari 1 km dan arahan instruksi sebelumnya adalah walking, maka suggest untuk naik grab-bike untuk menuju ke lokasi transit angkutan umum
    - apabila jarak kurang dari 1 km dan arahan instruksi sebelumnya adalah walking dan sesudahnya walking, maka suggest untuk naik grab-bike untuk menuju ke lokasi transit angkutan umum
    - apabila jarak kurang dari 1 km dan arahan instruksi sebelumnya adalah transit dan sesudahnya transit, maka suggest untuk walking untuk menuju ke lokasi transit angkutan umum
    - pastikan untuk grab-bike harga nya minimal 10.000
    
    target output:
    - data berbentuk json yang telah di simplifikasi berdasarkan syarat yang disebutkan, disertai dengan estimasi harga grab-bike mengacu pada jarak tempuh, untuk transit harga tetap di harga 3500
    - output dihasilkan dalam format json tanpa diberikan penjelasan atau deskripsi
    """
    drive_prompt_json: str = \
    """
    [
        {
            "total_distance": "0 km",
            "total_duration": "0 minutes",
            "price": "5.000" // mata uang IDR, untuk grab-bike / grab-car disesuaikan dengan jarak tempuh
            "type": "grab-bike" // opsi grab-bike / grab-car
        }
        ...
    ]
    """
    drive_prompt: str = \
    """
    anda adalah expert dari aplikasi grab

    berdasarkan data yang diberikan, berikan estimasi jarak total, durasi total, serta estimasi total harga untuk naik grab ride dan grab car di Indonesia

    data durasi dan jarak:
    {info_perjalanan}

    contoh skema json:
    {drive_prompt_json}

    dengan syarat:
    - Secara logika antara melaju menggunakan mobil dan motor memiliki perbedaan waktu sampai meskipun dengan durasi yang sama, tolong pertimbangkan itu dalam penentuan durasi waktu.

    target output:
    - data berbentuk json yang telah di simplifikasi berdasarkan syarat yang disebutkan, disertai dengan estimasi harga grab-bike mengacu pada jarak tempuh, untuk transit harga tetap di harga 3500
    - output dihasilkan dalam format json tanpa diberikan penjelasan atau deskripsi
    """
    disc_prompt: str = \
    """
    anda adalah expert dari aplikasi grab

    berdasarkan data yang diberikan, berikan informasi terkait promosi yang tersedia saat ini.

    data promosi:
    Grab Food Makan Siang - 20%
    Grab Food Hemat       - 30%
    Grab Bike Jakarta      - 15%
    Grab Bike Hemat        - 30%
    Grab Car Jakarta      - 10%
    Grab Car Hemat        - 30%

    Question: {query}
    """

