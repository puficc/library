import requests

search_api_server = "https://search-maps.yandex.ru/v1/"
# api_key = "43424001-5e33-4359-8920-fddbce050b9d"

address_ll = "37.588392,55.734036"

search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)
with open('map2.jpg', 'wb') as file:
    file.write(response.content)
if not response:
    # ...
    pass
