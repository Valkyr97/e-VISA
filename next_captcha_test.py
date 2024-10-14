from nextcaptcha import NextCaptchaAPI
import sys
 
client_key = "next_f6b195bae16d02792a7be912778c7ad944"
 
api = NextCaptchaAPI(client_key=client_key)
try:
  result = api.recaptchav2(website_url="https://pedidodevistos.mne.gov.pt/VistosOnline/Authentication.jsp'", website_key="6Lf6CLIkAAAAAKzJGpTdrJO1ZglKivvyMUbfeAEA")
 
except Exception as e:
  sys.exit(e)
 
else:
  sys.exit('solved: ' + str(result.get('solution').get('gRecaptchaResponse')))