import os
from gtts import gTTS

Text = "I love Django central and Python programming Language"

# print("please wait...processing")
TTS = gTTS(text=Text, lang='en-uk')

next_Text = "Hello friend"

TTS = gTTS(text=next_Text, lang='en-us', voice='en-US-Standard-A')


# Save to mp3 in current dir.
TTS.save("voice.mp3")

# Plays the mp3 using the default app on your system
# that is linked to mp3s.
os.system("start voice.mp3")