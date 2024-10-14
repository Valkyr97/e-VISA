import requests

username = "u52b13312567405cc-zone-custom-region-eu-session-9QupBUbJB-sessTime-8"
password = "u52b13312567405cc"
PROXY_DNS = "118.193.59.102:2334"
urlToGet = "http://ip-api.com/json"
proxy = {"http":"http://{}:{}@{}".format(username, password, PROXY_DNS)}
r = requests.get(urlToGet , proxies=proxy)

print("Response:{}".format(r.text))