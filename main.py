import requests
import sys
import urllib.parse
from bs4 import BeautifulSoup
from nextcaptcha import NextCaptchaAPI
from file_process import get_data

# Configuración
NEXT_CLIENT_KEY = "next_f6b195bae16d02792a7be912778c7ad944"
URL_TARGET = "https://pedidodevistos.mne.gov.pt"
urlToGet = "http://ip-api.com/json"
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.3"
]

with open('proxy_list.txt', 'r') as file:
    proxy_list = [proxy for proxy in file.readlines()]

# Funciones


def get_captcha_solution():
    # Lógica para obtener la solución del captcha
    api = NextCaptchaAPI(client_key=NEXT_CLIENT_KEY)
    try:
        result = api.recaptchav2(website_url=f"{URL_TARGET}/VistosOnline/Authentication.jsp'",
                                 website_key="6Lf6CLIkAAAAAKzJGpTdrJO1ZglKivvyMUbfeAEA")
    except Exception as e:
        sys.exit(e)

    else:
        captcha_result = result.get('solution').get('gRecaptchaResponse')
        if captcha_result:
            print('Captcha solved succesfuly\n\n')
            return captcha_result
        else:
            sys.exit('Captcha not solved')


def login(username, password, proxy):
    pt_password = urllib.parse.unquote(password)
    captchaResult = get_captcha_solution()
    payload = {"username": username, "password": pt_password,
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
        r = requests.post(url=f"{URL_TARGET}/$J@5Yg0RAhCxKgAhgfwtTouVMlnWPHDd_ubZzU6uSScB8ZmN3SlXxLKGpc", headers=headers, proxies=proxy,
                          data=payload)
    except Exception as e:
        sys.exit(e)
    else:
        sesion_id = r.headers.get('Set-Cookie').split(';')[0][11:]
        print('Cookies:', r.headers.get('Set-Cookie'))
        if sesion_id:
            print('Log in succesfull: ', sesion_id, '\n\n')
            return sesion_id


def scrape_data(proxy, session_id):
    cookie = {"Vistos_sid": session_id}
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
            f'{URL_TARGET}/VistosOnline/Formulario', cookies=cookie, headers=headers, proxies=proxy, data=payload)
        # r = requests.post(
        #     f'{urlToGet}', cookies=cookie, headers=headers, proxies={'http': 'http://127.0.0.1:8080'}, data=payload)
    except Exception as e:
        sys.exit(e)
    else:
        soup = BeautifulSoup(r.text, 'html.parser')
        request_verification_token = soup.find(
            'input', {'type': 'hidden', 'name': '__RequestVerificationToken'})

        if request_verification_token:
            verification_token = request_verification_token['value']
            return verification_token
        else:
            sys.exit('No se encontró el input hidden con el nombre especificado.')


def schedule_controller_form(proxy, session_id, verification_token, data):
    f = data
    cookie = {"Vistos_sid": session_id}
    headers = {
        "Host": "pedidodevistos.mne.gov.pt",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
        "Content-Type": "multipart/form-data",
        "Origin": "null",
        'Upgrade-Insecure-Requests': '1',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        'Sec-Fetch-User': '?1',
        "Priority": "u=0, i",
        "Te": 'trailers',
        "Connection": "keep-alive"
    }
    payload = {
        'lang': 'ENG',
        'txtHuman': '',
        '__RequestVerificationToken': verification_token,
        'RGPDAccepted': '',
        'posto_representacao': 'null',
        'f0sf1': '2044',
        'f1': f['1'],
        'f2': f['2'],
        'f3': f['3'],
        'f4': f['4'],
        'f6': f['5'],
        'f6sf1': 'CUB',
        'f7sf1': 'CUB',
        'f8': 'CUB',
        'f9': f['8'],
        'f10': '1',
        'txtApelidoPaternal': '',
        'txtNomePaternal': '',
        'txtEnderecoPaternal': '',
        'txtTelefonePaternal': '',
        'txtEmailPaternal': '',
        'cmbNacionalidadePaternal': '',
        'f5': '',
        'f13': '01',
        'f14': f['13'],
        'f16': f['14'],
        'f17': f['15'],
        'f15': 'CUB',
        'f43': '',
        'f43sf2': '',
        'f43sf3': '',
        'f43sf4': '',
        'f43sf5': '',
        'f43sf6': '',
        'f0': f['19'],
        'f45': f['19.1'],
        'f46': f['19.2'],
        'f18sf1': '',
        'f18sf2': '',
        'f18sf3': '',
        'f19': f['21'],
        'f20sf1': f['22.1'],
        'f20sf2': f['22.2'],
        'f29': '81',
        'f29sf2': '',
        'txtInfoMotEstada': '',
        'em_destino_1': 'PRT',
        'f32': 'PRT',
        'f24': '1',
        'f25': '120',
        'f30': f['27.3'],
        'f31': f['27.4'],
        'cmbImpressoesDigitais': 'N',
        'dataImpressoesDigitais': '',
        'numVinImpressoesDigitais': '',
        'f27': 'N',
        'f27sf2': '',
        'cmbReferencia': 'individual',
        'f34': f['30.1'],
        'f34sf3': '',
        'f34sf2': f['30.2'],
        'f34sf4': '',
        'f34sf5': '80',
        'cmbDespesasRequerente_1': '1',
        'cmbDespesasRequerente_2': '',
        'cmbDespesasPatrocinador_1': '',
        'tipo_visto': 'DP',
        'tipo_visto_desc': 'RESIDENCY VISA - JOB SEEKER VISA',
        'class_visto': 'NAC',
        'cod_estada': '81',
        'id_visto_doc': '49',
        'tipo_passaporte': '01',
        'nacionalidade': 'CUB',
        'pais_residencia': 'CUB',
        'foto': {'Content-Type': 'application/octet-stream', 'filename': ''},
        'file1': {'Content-Type': 'application/octet-stream', 'filename': ''},
        'file2': {'Content-Type': 'application/octet-stream', 'filename': ''},
        'file3': {'Content-Type': 'application/octet-stream', 'filename': ''},
        'file3': {'Content-Type': 'application/octet-stream', 'filename': ''},
        'file4': {'Content-Type': 'application/octet-stream', 'filename': ''},
        'f_date_c': '',
        'cmbPeriodo': '',
    }

    try:
        r = requests.post(
            f'{URL_TARGET}/VistosOnline/ScheduleController', cookies=cookie, headers=headers, proxies=proxy, data=payload)

    except Exception as e:
        sys.exit(e)
    else:
        return


def SubmeterVistoCriaPDF(proxy, session_id):
    cookie = {"Vistos_sid": session_id}

    headers = {
        "Host": "pedidodevistos.mne.gov.pt",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
        "Content-Type": "multipart/form-data",
        "Origin": "null",
        'Upgrade-Insecure-Requests': '1',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        'Sec-Fetch-User': '?1',
        "Priority": "u=0, i",
        "Te": 'trailers',
        "Connection": "keep-alive"
    }

    payload = {
        'lang': 'ENG',
        'txtHuman': '',
        'back': '',
        'f_date_c': '2024/11/7',
        'cmbPeriodo': '3'
    }

    try:
        r = requests.post(
            f'{URL_TARGET}/VistosOnline/ScheduleController', cookies=cookie, headers=headers, proxies=proxy, data=payload)

    except Exception as e:
        sys.exit(e)
    else:
        print(r.text)
        return


def main():
    proxy = {"http": f"http://{proxy_list[4]}"}
    data = get_data('INFO_SUSANA.TXT')
    session_id = login(username=data['username'],
                       password=data['password'], proxy=proxy)
    verification_token = scrape_data(proxy=proxy, session_id=session_id)

    schedule_controller_form(
        proxy=proxy, session_id=session_id, verification_token=verification_token, data=data)
    SubmeterVistoCriaPDF(proxy=proxy, session_id=session_id)


if __name__ == "__main__":
    main()
