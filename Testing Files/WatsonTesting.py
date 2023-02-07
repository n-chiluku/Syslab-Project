from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
# 
# authenticator = IAMAuthenticator('my_apikey')
# authenticator.set_client_id_and_secret('my-client-id', 'my-client-secret');
# service = ExampleService(authenticator=authenticator)
# 
# service.get_authenticator.set_disable_ssl_verification(true);



apikey = 'Yfqw8JtvqTEiLO2Rc8l3ZIwtf4XV5PyIt7rbLmVlX8r3'
url = 'https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/1501b488-86e4-47d8-9778-23e47db0d67b'
# url = 'https://api.eu-de.text-to-speech.watson.cloud.ibm.com/text-to-speech/api'

#setup service
authenticator = IAMAuthenticator(apikey)
#Create our service
tts = TextToSpeechV1(authenticator=authenticator)
#set the IBM service url
tts.set_service_url(url)

with open('./speech.mp3', 'wb') as audio_file:
    res = tts.synthesize('Hello World!', accept='audio/mp3', voice='en-US_MichaelV3Voice').get_result()
    audio_file.write(res.content) #write the content to the audio file


with open('C:/Users/1504522/Desktop/Syslab Project/AndrewNeil.mp3', 'r') as f:
    text = f.readlines()

text = [line.replace('\n','') for line in text]
text = ''.join(str(line) for line in text)

with open('./winston.mp3', 'wb') as audio_file:
    res = tts.synthesize(text, accept='audio/mp3', voice='en-GB_JamesV3Voice').get_result() #selecting the audio format and voice
    audio_file.write(res.content) #writing the contents from text file to a audio file
