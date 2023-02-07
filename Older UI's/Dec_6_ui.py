import sys, os, time, subprocess, webbrowser

from tkinter import *
import playsound
from playsound import playsound
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
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
file_menu.geometry('1300x700')
# file_menu.attributes('-fullscreen', True)
file_menu.configure(bg='light green')
file_menu.bind("<Escape>", lambda e: file_menu.destroy())
style = Style()
style.configure('TButton', font =('calibri', 20, 'bold'), borderwidth = '4')

# file_menu.mainloop()

def menu():
  
   tk.Label(text="|", bg='light green', font=("Georgia bold", 20), fg='light green').grid(row=0, column=1, sticky=tk.W+tk.E+tk.N+tk.S)
   
   tk.Label(text="Audiobook Creator", bg='light green', font=("Georgia bold", 20), fg=black).grid(row=1, column=1, sticky=tk.W+tk.E+tk.N+tk.S)

   tk.Label(text="Directions: Open a text file or enter text and click submit", bg='light green', font=("Georgia bold", 12), fg=black).grid(row=2, column=1, sticky=tk.W+tk.E+tk.N+tk.S)

   tk.Label(text="Click escape to exit", bg='light green', font=("Georgia bold", 12), fg=black).grid(row=3, column=1, sticky=tk.W+tk.E+tk.N+tk.S)

 #   file_menu.bind("<Return>", lambda e: select_file)
   open_button = ttk.Button(file_menu, text='Open a File', command=select_file).grid(row=4, column=5)
   tk.Label(text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=3, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
   tk.Label(text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=4, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
   tk.Label(text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=4, column=4, sticky=tk.W+tk.E+tk.N+tk.S)

   textfield = scrolledtext.ScrolledText(file_menu, wrap=tk.WORD, width=100, height=30)
   textfield.grid(row=4, column=1)
   tk.Label(text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=4, column=2, sticky=tk.W+tk.E+tk.N+tk.S)

   getText = ttk.Button(file_menu, text="Submit text", command=lambda: retrieve_input(textfield)).grid(row=4, column=3)
    
   file_menu.mainloop()
   
def retrieve_input(textfield):
   data = textfield.get("1.0", END)
   
   global text_array
   text_array = data.splitlines()
   print("text_array", text_array)
   
 #   print("winner")
  #  make_audiobook()
 #   print("loser")
   show_extraction_details(file_menu)
   

def show_extraction_details(file_menu):
   file_menu.destroy()
   details_menu = tk.Tk()
   # self.window
   details_menu.title("Breakdown of extraction")
   details_menu.geometry('1900x900') #widthxheight 
   details_menu.configure(bg='light green')
  #  details_menu.attributes('-fullscreen', True)
 #   details_menu.bind("<Enter>", lambda e: exit_program(details_menu))

   style = Style()
   style.configure('TButton', font =('calibri', 12, 'bold'), borderwidth = '4')
   
   #for each line, give it a different voice in the mp3 after being able to play it
   
   book_array, dialogue_array, characters = identify_dialogue(text_array)
   
   print("book_array", book_array)
   print("characters", characters)
   print("dialogue_array", dialogue_array)


   tk.Label(text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S) # leftmost padding
   tk.Label(text="Reason", bg='light green', font=("Georgia bold", 15), fg=black, relief = 'sunken').grid(row=1, column=1, sticky=tk.W+tk.E+tk.N+tk.S)
   tk.Label(text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=1, column=2, sticky=tk.W+tk.E+tk.N+tk.S)
   
   tk.Label(text="Dialogue", bg='light green', font=("Georgia bold", 15), fg=black, relief = 'sunken').grid(row=1, column=3, sticky=tk.W+tk.E+tk.N+tk.S)
   tk.Label(text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=1, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
   
   tk.Label(text="Speaker", bg='light green', font=("Georgia bold", 15), fg=black, relief = 'sunken').grid(row=1, column=5, sticky=tk.W+tk.E+tk.N+tk.S)
   tk.Label(text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=0, column=6, sticky=tk.W+tk.E+tk.N+tk.S)

   tk.Label(text="Context", bg='light green', font=("Georgia bold", 15), fg=black, relief = 'sunken').grid(row=1, column=7, sticky=tk.W+tk.E+tk.N+tk.S)
   tk.Label(text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=1, column=8, sticky=tk.W+tk.E+tk.N+tk.S)
   
   
 #   tk.Label(text="Excerpt of text", bg='light green', font=("Georgia bold", 15), fg=black).grid(row=1, column=7, sticky=tk.W+tk.E+tk.N+tk.S)

 #   tk.Label(text="", bg='light green', font=("Georgia bold", 15), fg=black).grid(row=2, column=1, sticky=tk.W+tk.E+tk.N+tk.S)
   
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
   
      tk.Label(text=dialogue_array[x][3], bg='light green', font=("Georgia", 12), fg=black).grid(row=rowCount, column=7, sticky=tk.W+tk.E+tk.N+tk.S)
  #     tk.Label(text=text_array[x:], bg='light green', font=("Georgia", 12), fg=black).grid(row=rowCount, column=7, sticky=tk.W+tk.E+tk.N+tk.S)
     #  tk.Label(text=dialogue_array[x][2], bg='light green', font=("Georgia", 12), fg=black).grid(row=rowCount, column=5, sticky=tk.W+tk.E+tk.N+tk.S) 
      
      rowCount+=4
         
   tk.Label(text=" ", bg='light green', font=("Georgia", 10), fg=black).grid(row=1, column=9, sticky=tk.W+tk.E+tk.N+tk.S)   
   
   textfield = scrolledtext.ScrolledText(details_menu, wrap=tk.WORD, width=30, height=0.25)
   textfield.grid(row=1, column=10)
   textfield.insert('1.0', 'audiobook.mp3')
   
   tk.Label(text=" | ", bg='light green', font=("Georgia", 10), fg='light green').grid(row=1, column=11, sticky=tk.W+tk.E+tk.N+tk.S)   

   ttk.Button(text="Create an audiobook", command=lambda: open_Audio_real(details_menu, textfield)).grid(row=1, column=13, columnspan=1, sticky=tk.W+tk.E+tk.N+tk.S)

   tk.Label(text=" | ", bg='light green', font=("Georgia", 10), fg='light green').grid(row=1, column=14, sticky=tk.W+tk.E+tk.N+tk.S)   

   ttk.Button(text="View the full text", command=lambda: view_full_text(details_menu, text_array)).grid(row=1, column=15, columnspan=1, sticky=tk.W+tk.E+tk.N+tk.S)
   
   tk.Label(text=" | ", bg='light green', font=("Georgia", 10), fg='light green').grid(row=1, column=16, sticky=tk.W+tk.E+tk.N+tk.S)   

   
   ttk.Button(text="Exit the program", command=lambda: exit_program(details_menu)).grid(row=1, column=17, columnspan=1, sticky=tk.W+tk.E+tk.N+tk.S)
   
  #  details_menu.mainloop()
#    make_audiobook(characters)

def view_full_text(details_menu, text_array):
   # print("hi")
   
   full_text_menu = tk.Tk()
   # self.window
   full_text_menu.title("Full text")
   full_text_menu.geometry('800x900') #widthxheight 
   full_text_menu.configure(bg='light green')

   tk.Label(full_text_menu, text=" | ", bg='light green', font=("Georgia", 10), fg='light green').grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S) 
   
   tk.Label(full_text_menu, text=" | ", bg='light green', font=("Georgia", 10), fg='light green').grid(row=1, column=0, sticky=tk.W+tk.E+tk.N+tk.S)

   tk.Label(full_text_menu, text="Full Text", bg='light green', font=("Georgia bold", 15), fg=black).grid(row=1, column=1, sticky=tk.W+tk.E+tk.N+tk.S) 

   for index in range(0, len(text_array)):
      
      tk.Label(full_text_menu, text=text_array[index], bg='light green', font=("Georgia", 12), fg=black).grid(row=index+2, column=1, sticky=tk.W) 


def exit_program(details_menu):
   
   sys.exit()
   
def exit_program1(file_menu):
   
   sys.exit()
   
def make_audiobook(characters):
   print("entered")   
   path_name = 'C:/Users/1504522/Desktop/Syslab Project/Audiobooks/'
   audio_file_name = 'audiobook.mp3'
   
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

   print("hi,", audio_file_name)
      
def open_Audio_real(file_menu, textfield):

   audio_file_name = textfield.get("1.0", END).strip()
   print("audio_file_name", audio_file_name)
   if len(audio_file_name) < 1:  # not a file name
      audio_file_name = './audiobook.mp3'
   
    #   os.rename('./C:/Users/1504522/Desktop/Syslab Project/Audiobooks/audiobook.mp3', './C:/Users/1504522/Desktop/Syslab Project/Audiobooks/'+audio_file_name)
      
   if 'mp3' not in audio_file_name:
      audio_file_name += 'mp3'
    #   os.rename('./', './')
   if audio_file_name != 'audiobook.mp3': 
      print("checkpoint")
      os.rename('./audiobook.mp3', './'+audio_file_name)
   
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
   
   dialogue_array = [] #[dialogue, reason, speaker, context] 
   global book_array
   #    global characters
   characters = []
   book_array = [] 

   for element in text_array:
      if element.find('"') != -1:         # it has quotations and is dialogue, so find the closing, then add to array followed by narration
         starting_index = int(element.find('"')) + 1
         closing_index = int(element.find('"', starting_index+1))
         
         speaker, characters = find_speaker(element, closing_index, characters)
#          print("speaker found", speaker)
         
         dialogue_piece = "d " + speaker + "- " + element[starting_index:closing_index]
         
         dialogue_array.append([element[starting_index:closing_index],"Q", speaker, element])
         book_array.append(dialogue_piece)
      
         narration_piece = "n" + element[closing_index+1:]
      
         book_array.append(narration_piece)
         
      else:                               #it doesn't have quotations and is not dialogue, so assign it the narrator voice
      
         book_array.append("n " + element)
          
   return book_array, dialogue_array, characters

def find_speaker(line, dialogue_closing_index, characters): # make an array of all the speakers of the text
 #   for index in range(0,len(book_array)):
 #      if book_array[index] == 'n' && book_array[index-1]: #it's narration and there's dialogue before
         
   f = open(speaker_file)
   
   verb_array = f.read().splitlines() #array of each line in the text
   speaker = ""
   
   # CURRENT STATE: CAN FIND SPEAKER IF THE VERB IS AFTER OR BEFORE THE SPEAKER NAME
   

   for verb in verb_array:
      if verb in line:
        #  speaker = line[dialogue_closing_index+1: line.index(verb)]
        #  if speaker not in characters: characters.append(speaker)
         
         # print("name test speaker after verb:", line[line.index(verb)+len(verb)+1:len(line)-1])
         # print("name test speaker before verb:", line[dialogue_closing_index+2: line.index(verb)-1])
        #  if len(characters) > 0:    #there are already characters to choose from 
         if str(line[dialogue_closing_index+2: line.index(verb)-1]) in characters: #finds the speaker using the verb, BEFORE verb
            speaker = line[dialogue_closing_index+1:line.index(verb)]    #goes from end of dialogue to start of verb for the speaker 
         #    print("before verb: ", speaker)
            break
              
         elif str(line[line.index(verb)+len(verb)+1:len(line)-1]) in characters: # speaker is AFTER verb (may need precaution in case it goes over line length
             
            speaker = line[line.index(verb)+ len(verb):len(line)-1] #goes from end of verb to end of line for the speaker 
         #    print("after verb: ", speaker)
            break
         else:                         # speaker not in characters 
           #  print("", len(line[dialogue_closing_index: line.index(verb)]))
            if len(line[dialogue_closing_index: line.index(verb)]) == 2: #verb comes right after dialogue 
               speaker = line[line.index(verb)+len(verb):len(line)-1]   #goes from end of verb to end of line for the speaker 
             #   print("new speaker after verb:", speaker)
               characters.append(speaker)      #add speaker to character array since it's not there aleady 
               
               break
            else:    #speaker is after dialogue
               speaker = line[dialogue_closing_index+2: line.index(verb)-1]    #goes from end of dialogue to start of verb for the speaker 
             #   print("new speaker before verb:", speaker)
               characters.append(speaker)      #add speaker to character array since it's not there aleady 
               break
              
         
   f.close()   
   
   # print("the characters:", characters)
   # print("the speaker found:", speaker)

   return speaker, characters

 
menu()