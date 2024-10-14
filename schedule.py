#!/usr/bin/env python3

from nextcaptcha import NextCaptchaAPI
from twocaptcha import TwoCaptcha
import requests
import sys
import urllib.parse
from bs4 import BeautifulSoup
from iterator import CircularIterator

user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.3", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.3", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.1",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.1", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.3"]

username = "u52b13312567405cc-zone-custom-region-eu-session-N1UANRcNh-sessTime-5"
password = "u52b13312567405cc"
PROXY_DNS = "118.193.59.102:2334"
urlToGet = "http://ip-api.com/json"
urlTarget = "https://pedidodevistos.mne.gov.pt"

proxy_list = [
    "u52b13312567405cc-zone-custom-region-pt-session-QWboH8j18-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-1ngzovK7r-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-rBTdbYqzO-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-qxEWvYNsC-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-bfDkm1VWp-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-3qcBbNHOU-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-GFzU4OEnt-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-yVVXYwDHP-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-BZKTKF7Xs-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-oq3Uc2ro9-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-siHyrLO1C-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-M80Jk1fQh-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-06swUkoj9-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-PvKuRvygO-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-70j3qOOKh-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-Jec9M3Jzp-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-Rf0YLZibN-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-H1CKk8EZZ-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-AhpUasoMM-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-4R72btuHZ-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-7QBsVRF5J-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-rzXg7xVWN-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-n68BXW5UL-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-aOEqwZIff-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-6vQhQLUTR-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-6yj19RfmF-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-3gBSleVd3-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-sJzYPlJTx-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-23m20sFBv-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-0XSffbEYi-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-GzYOEH9gf-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-LbOR6mzYd-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-QV5jc4klH-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-o1fF6nrgu-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-JREoa9WhA-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-im4Rr3uNu-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-CEJhEE9tF-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-6S4WZof77-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-4IajnazpL-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-OJvJwziSS-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-NDRDEvZeJ-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-katDnarpY-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-ER10UxEkC-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-Cd7TgaQkr-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-xun3sRAXN-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-5dUoPC9wC-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-R4LEECdvz-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-oZ1kfnuLl-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-Jd9ZWWwRH-sessTime-8:u52b13312567405cc@118.193.59.102:2333",
    "u52b13312567405cc-zone-custom-region-pt-session-Ap7O4g9Yb-sessTime-8:u52b13312567405cc@118.193.59.102:2333",

]

proxy = {"http": f'http://{proxy_list[3]}'}

# r = requests.get(urlToGet, proxies=proxy)

key = "6Lf6CLIkAAAAAKzJGpTdrJO1ZglKivvyMUbfeAEA"

api_key = "17bb72e141b597ae7d3916d47d2d374e"

# solver = TwoCaptcha(api_key)


client_key = "next_f6b195bae16d02792a7be912778c7ad944"

api = NextCaptchaAPI(client_key=client_key)
try:
    result = api.recaptchav2(website_url=f"{urlTarget}/VistosOnline/Authentication.jsp'",
                             website_key="6Lf6CLIkAAAAAKzJGpTdrJO1ZglKivvyMUbfeAEA")

except Exception as e:
    sys.exit(e)

else:
    pt_username = "Karen88"
    password = "_hx2F5RGd_H%3AgCQ"
    pt_password = urllib.parse.unquote(password)
    captchaResult = result.get('solution').get('gRecaptchaResponse')
    payload = {"username": pt_username, "password": pt_password,
               "language": "ENG",
               "rgpd": 'Y',
               "captchaResponse": captchaResult}
    headers = {"Host": "pedidodevistos.mne.gov.pt",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
               "Accept": "*/*",
               "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
               "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               "X-Requested-With": "XMLHttpRequest",
               "Origin": "https://pedidodevistos.mne.gov.pt",
               "Referer": "https://pedidodevistos.mne.gov.pt/VistosOnline/Authentication.jsp",
               "Sec-Fetch-Dest": "empty",
               "Sec-Fetch-Mode": "cors",
               "Sec-Fetch-Site": "same-origin",
               "Priority": "u=0",
               "Te": 'trailers',
               "Connection": "keep-alive"
               }
    try:
        r = requests.post(url=f"{urlTarget}/$J@5Yg0RAhCxKgAhgfwtTouVMlnWPHDd_ubZzU6uSScB8ZmN3SlXxLKGpc", headers=headers, proxies=proxy,
                          data=payload)
        # print(f'headers: {r.request.headers}, body: {r.request.body}')
        print(r.headers)

    except Exception as e:
        sys.exit(e)

    else:
        cookies = r.headers.get('Set-Cookie').split(';')
        sesion_id = cookies[0][11:]
        print(cookies, sesion_id)

        cookie = {"Vistos_sid": sesion_id}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
            "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "null",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Priority": "u=0, i",
            "Te": "trailers",
            "Connection": "keep-alive"
        }
        payload = {
            "lang": "ENG",
            "nacionalidade": "CUB",
            "pais_residencia": "CUB",
            "tipo_passaporte": "01",
            "copia_pedido": "null",
            "cb_pais_residencia": "CUB",
            "cb_tipo_passaporte": "01",
            "cb_qt_dias": "NAC",
            "cb_estabelecer_residencia": "N",
            "cb_pretende_ficar": "N",
            "cb_motivo_estada_mais1ano": "PRO",
            "tipo_visto": "DP",
            "tipo_visto_desc": "RESIDENCY+VISA+-+JOB+SEEKER+VISA",
            "class_visto": "NAC",
            "cod_estada": "81",
            "id_visto_doc": 49
        }

        try:
            r = requests.post(
                f'{urlTarget}/VistosOnline/Formulario', cookies=cookie, headers=headers, proxies=proxy)
        except Exception as e:
            sys.exit(e)
        else:
            soup = BeautifulSoup(r.text, 'html.parser')
            print(soup)
            request_verification_token = soup.find(
                'input', {'type': 'hidden', 'name': '__RequestVerificationToken'})

            if request_verification_token:
                valor = request_verification_token['value']
                print(f'El valor del input hidden es: {valor}')
            else:
                print('No se encontró el input hidden con el nombre especificado.')

        # try:
        #     requests.get(f'{urlTarget}/VistosOnline/logout',
        #                  cookies={'Vistos_sid': sesion_id})

        # except Exception as e:
        #     sys.exit(e)
        # else:
        #     sys.exit(r.text)
