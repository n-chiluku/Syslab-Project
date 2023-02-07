import sys, os, time, subprocess, webbrowser

from tkinter import *
import playsound
from playsound import playsound
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import scrolledtext
import pyttsx3
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

apikey = 'Yfqw8JtvqTEiLO2Rc8l3ZIwtf4XV5PyIt7rbLmVlX8r3'
url = 'https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/1501b488-86e4-47d8-9778-23e47db0d67b'

#setup service
authenticator = IAMAuthenticator(apikey)
#Create our service
tts = TextToSpeechV1(authenticator=authenticator)
#set the IBM service url
tts.set_service_url(url)

padding = 5
tile_size = 50
brown = "#654321"
white = "#ffffff"
black = "#000000"
grey = "#505050"
green = "#00ff00"
yellow = "#ffff00"
brown = "#654321"
blue = "#0000ff"
cyan = "#00ffff"
speaker_file = "speakerCues.txt"
file_menu = tk.Tk()
details_menu = None
file_menu.title("Menu")
file_menu.resizable(False, False)
file_menu.geometry('700x400')
file_menu.configure(bg='light green')

def menu():
  
   tk.Label(text="|", bg='light green', font=("Georgia bold", 20), fg='light green').grid(row=0, column=1, sticky=tk.W+tk.E+tk.N+tk.S)
   
   tk.Label(text="Audiobook Creator", bg='light green', font=("Georgia bold", 20), fg=black).grid(row=1, column=1, sticky=tk.W+tk.E+tk.N+tk.S)

   tk.Label(text="Directions: Open a text file or enter text and click submit", bg='light green', font=("Georgia bold", 12), fg=black).grid(row=2, column=1, sticky=tk.W+tk.E+tk.N+tk.S)

   open_button = ttk.Button(file_menu, text='Open a File',command=select_file).grid(row=4, column=5)
   
   tk.Label(text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=3, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
   tk.Label(text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=4, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
   tk.Label(text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=4, column=4, sticky=tk.W+tk.E+tk.N+tk.S)

   textfield = scrolledtext.ScrolledText(file_menu, wrap=tk.WORD, width=40, height=10)
   textfield.grid(row=4, column=1)
   getText = ttk.Button(file_menu, text="Submit text", command=lambda: retrieve_input(textfield)).grid(row=4, column=3)
    
   file_menu.mainloop()
   
def retrieve_input(textfield):
   data = textfield.get("1.0", END)
   
   global text_array
   text_array = data.splitlines()
   print("text_array", text_array)
   
   show_extraction_details(file_menu)

def show_extraction_details(file_menu):
   file_menu.destroy()
   details_menu = tk.Tk()
   details_menu.title("Breakdown of extraction")
   details_menu.geometry('1000x500')
   details_menu.configure(bg='light green')
   #for each line, give it a different voice in the mp3 after being able to play it
   
   book_array, dialogue_array = identify_dialogue(text_array)
   
   print("book_array", book_array)
   print("characters", characters)

   tk.Label(text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S) # leftmost padding
   tk.Label(text="Reason", bg='light green', font=("Georgia bold", 15), fg=black).grid(row=1, column=1, sticky=tk.W+tk.E+tk.N+tk.S)
   tk.Label(text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=1, column=2, sticky=tk.W+tk.E+tk.N+tk.S)
   
   tk.Label(text="Dialogue", bg='light green', font=("Georgia bold", 15), fg=black).grid(row=1, column=3, sticky=tk.W+tk.E+tk.N+tk.S)
   tk.Label(text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=1, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
   
   tk.Label(text="Speaker", bg='light green', font=("Georgia bold", 15), fg=black).grid(row=1, column=5, sticky=tk.W+tk.E+tk.N+tk.S)
   tk.Label(text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=0, column=6, sticky=tk.W+tk.E+tk.N+tk.S)

   tk.Label(text="Excerpt of text", bg='light green', font=("Georgia bold", 15), fg=black).grid(row=1, column=7, sticky=tk.W+tk.E+tk.N+tk.S)

   tk.Label(text="", bg='light green', font=("Georgia bold", 15), fg=black).grid(row=2, column=1, sticky=tk.W+tk.E+tk.N+tk.S)
   
   #table details: col 0 = reason, col 1 = dialogue, col 2 = speaker
   text_Arr_len = len(text_array)   
   rowCount = 3
   for x in range(0, len(dialogue_array)):
      tk.Label(text=dialogue_array[x][1], bg='light green', font=("Georgia", 12), fg=black).grid(row=rowCount, column=1, sticky=tk.W+tk.E+tk.N+tk.S)
      tk.Label(text=" | ", bg='light green', font=("Georgia bold", 12), fg='light green').grid(row=rowCount, column=2, sticky=tk.W+tk.E+tk.N+tk.S)
   
      tk.Label(text='"' + dialogue_array[x][0] + '"', bg='light green', font=("Georgia", 12), fg=black).grid(row=rowCount, column=3, sticky=tk.W+tk.E+tk.N+tk.S)      
      tk.Label(text=" | ", bg='light green', font=("Georgia bold", 12), fg='light green').grid(row=rowCount, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
   
      tk.Label(text=dialogue_array[x][2], bg='light green', font=("Georgia", 12), fg=black).grid(row=rowCount, column=5, sticky=tk.W+tk.E+tk.N+tk.S)
      tk.Label(text=" | ", bg='light green', font=("Georgia bold", 12), fg='light green').grid(row=rowCount, column=6, sticky=tk.W+tk.E+tk.N+tk.S)
   
      tk.Label(text=text_array[x], bg='light green', font=("Georgia", 12), fg=black).grid(row=rowCount, column=7, sticky=tk.W+tk.E+tk.N+tk.S)
         
      rowCount+=4
         
   tk.Label(text=" ", bg='light green', font=("Georgia", 10), fg=black).grid(row=1, column=9, sticky=tk.W+tk.E+tk.N+tk.S)   
   
   textfield = scrolledtext.ScrolledText(details_menu, wrap=tk.WORD, width=30, height=0.25)
   textfield.grid(row=1, column=10)
   textfield.insert('1.0', 'audiobook.mp3')
   
   ttk.Button(text="Create an audiobook", command=lambda: open_Audio_real(details_menu, textfield)).grid(row=3, column=10, columnspan=1, sticky=tk.W+tk.E+tk.N+tk.S)

   tk.Label(text=" | ", bg='light green', font=("Georgia", 10), fg='light green').grid(row=1, column=11, sticky=tk.W+tk.E+tk.N+tk.S)   

   
   ttk.Button(text="Exit the program", command=lambda: exit_program(details_menu)).grid(row=1, column=12, columnspan=1, sticky=tk.W+tk.E+tk.N+tk.S)
   

def exit_program(details_menu):
   
   sys.exit()
   
def open_Audio_real(file_menu, textfield):
   
   audio_file_name = textfield.get("1.0", END).strip()
   
   if len(audio_file_name) < 1:  # not a file name
      audio_file_name = 'audiobook.mp3'
   
   if 'mp3' not in audio_file_name:
      audio_file_name += 'mp3'
   
   path_name = 'C:/Users/1504522/Desktop/Syslab Project/Audiobooks/'
   
   with open('./' + audio_file_name, 'wb') as audio_file:  # works for two characters rn
      for line in book_array:
         if line[0:1] == 'd':    #it's dialogue
            if line[2:line.find('-')-1] == characters[0]:     #speaker 1
               res = tts.synthesize(line[line.find('-'):], accept='audio/mp3', voice='en-US_MichaelV3Voice').get_result() #selecting the audio format and voice
               audio_file.write(res.content) #writing the contents from text file to a audio file
            else:    # speaker 2
               res = tts.synthesize(line[line.find('-'):], accept='audio/mp3', voice='en-US_KevinV3Voice').get_result() #selecting the audio format and voice
               audio_file.write(res.content) #writing the contents from text file to a audio file
         else:       # it's narration
            res = tts.synthesize(line[2:], accept='audio/mp3', voice='en-US_OliviaV3Voice').get_result() #selecting the audio format and voice
            audio_file.write(res.content) #writing the content from text file to a audio file

   print(audio_file_name)

   os.startfile(audio_file_name)  #works

def collect_text(filename):
   f = open(filename)
   global text_array
   text_array = f.read().splitlines() #array of each line in the text
   print("text_array", text_array)
   f.close()
      
def select_file():
   filetypes = (('text files', '*.txt'),('All files', '*.*'))

   global filename
   filename = fd.askopenfilename(title='Open a file', filetypes=filetypes)
   collect_text(filename)
 
   show_extraction_details(file_menu)
 
def identify_dialogue(text_array):                    #returns an array with smaller arrays of each dialogue within quotations, reason, and speaker
   
   global characters
   characters = []
   
   dialogue_array = [] #[dialogue, reason, speaker] 
   global book_array
   
   book_array = [] 

   for element in text_array:
      if element.find('"') != -1:         # it has quotations and is dialogue, so find the closing, then add to array followed by narration
         starting_index = int(element.find('"')) + 1
         closing_index = int(element.find('"', starting_index+1))
         
         speaker = find_speaker(element, closing_index)
         
         dialogue_piece = "d " + speaker + "-" + element[starting_index:closing_index]
         
         dialogue_array.append([element[starting_index:closing_index],"Q", speaker])
         book_array.append(dialogue_piece)
      
         narration_piece = "n" + element[closing_index+1:]
      
         book_array.append(narration_piece)
         
      else:                               #it doesn't have quotations and is not dialogue, so assign it the narrator voice
      
         book_array.append("n " + element)
          
   return book_array, dialogue_array

def find_speaker(line, dialogue_closing_index): # make an array of all the speakers of the text
 #   for index in range(0,len(book_array)):
 #      if book_array[index] == 'n' && book_array[index-1]: #it's narration and there's dialogue before
         
   f = open(speaker_file)
   
   verb_array = f.read().splitlines() #array of each line in the text
   speaker = ""
   
   # CURRENT STATE: CAN FIND SPEAKER IF THE VERB IS AFTER THE SPEAKER NAME
   
   for verb in verb_array:
      if verb in line:
         speaker = line[dialogue_closing_index+1: line.index(verb)]
         if speaker not in characters: characters.append(speaker)
         # if len(characters) > 0:
        #  if (characters.contains(line[dialogue_closing_index+1: line.index(verb)])): #finds the speaker using the verb, BEFORE verb
#             speaker = character
#             break
#          elif (characters.contains(line[line.index(verb)+ len(verb):])): # speaker is AFTER verb (may need precaution in case it goes over line length
#             speaker = line[line.index(verb)+ len(verb):]
#                break
#          else:                         # speaker not in characters 
#             if len(line[dialogue_closing_index: line.index(verb)]) == 1: #verb comes right after dialogue 
#                speaker = line[line.index(verb)+ len(verb):]
#                characters.append(speaker)
#                break
#             else:    #speaker is after dialogue
#                speaker = line[dialogue_closing_index+1: line.index(verb)]
#                characters.append(speaker)
#                break
              
         
   f.close()   
   
   return speaker
 
menu()