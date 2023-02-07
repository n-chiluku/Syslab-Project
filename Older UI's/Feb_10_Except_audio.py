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
from tkinter.tix import *

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

#    menubar = Menu(file_menu)
# 
#    helpmenu = Menu(file_menu, tearoff=0)
#    helpmenu.add_command(label="Help Index",accelerator="Ctrl+O", command=lambda: select_file(file_menu))
#    menubar.add_cascade(label="Help",underline=1, menu=helpmenu)
#    file_menu.config(menu=menubar)

   file_menu.bind("<Control-o>", lambda f: select_file(file_menu))
   
   
  #  file_menu.bind("<Control-o>", lambda f: select_file(file_menu))
   # file_menu.add_cascade(label="H",underline=0 ,menu=helpmenu)
  #  new_menu.bind("<Control-h>", donothing)
   open_button = ttk.Button(file_menu, text='Open a File', command=lambda: select_file(file_menu)).grid(row=4, column=5) 
 #   open_button = ttk.Button(file_menu, text='Open a File').grid(row=4, column=5) 

   
 #   open_button.bind("<Enter>", on_enter)
#    open_button.bind("<Leave>", select_file(file_menu))
   
   # open_button.configure(text="Control O")
  #  CreateToolTip(open_button, text = 'Hello World')
   
   
   tk.Label(text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=3, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
   tk.Label(text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=4, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
   tk.Label(text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=4, column=4, sticky=tk.W+tk.E+tk.N+tk.S)

   textfield = scrolledtext.ScrolledText(file_menu, wrap=tk.WORD, width=100, height=30)
   textfield.grid(row=4, column=1)
   tk.Label(text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=4, column=2, sticky=tk.W+tk.E+tk.N+tk.S)

   # file_menu.bind("<Return>", lambda f: retrieve_input(textfield, file_menu))
   getText = ttk.Button(file_menu, text="Submit text", command=lambda: retrieve_input(textfield, file_menu)).grid(row=4, column=3)
    
   file_menu.mainloop()
   
def retrieve_input(textfield, the_menu):
   data = textfield.get("1.0", END)
   
   global text_array
   text_array = data.splitlines()
   print("text_array", text_array)

   show_extraction_details(the_menu)
  
def on_enter(e):
   print("HI")


 
def return_to_menu(details_menu):

   details_menu.destroy()
   
   new_menu = tk.Tk()
   # self.window
   new_menu.title("Breakdown of extraction")
   new_menu.geometry('1300x700') #widthxheight 
   new_menu.configure(bg='light green')
   style = Style()
   style.configure('TButton', font =('calibri', 12, 'bold'), borderwidth = '4')
   new_menu.bind("<Escape>", lambda e: new_menu.destroy())
 

   tk.Label(text="|", bg='light green', font=("Georgia bold", 20), fg='light green').grid(row=0, column=1, sticky=tk.W+tk.E+tk.N+tk.S)
   
   tk.Label(text="Audiobook Creator", bg='light green', font=("Georgia bold", 20), fg=black).grid(row=1, column=1, sticky=tk.W+tk.E+tk.N+tk.S)

   tk.Label(text="Directions: Open a text file or enter text and click submit", bg='light green', font=("Georgia bold", 12), fg=black).grid(row=2, column=1, sticky=tk.W+tk.E+tk.N+tk.S)

   tk.Label(text="Click escape to exit", bg='light green', font=("Georgia bold", 12), fg=black).grid(row=3, column=1, sticky=tk.W+tk.E+tk.N+tk.S)

 #   file_menu.bind("<Return>", lambda e: select_file)
   new_menu.bind("<Control-o>", lambda f: select_file(new_menu))
   open_button = ttk.Button(new_menu, text='Open a File', command=lambda: select_file(new_menu)).grid(row=4, column=5)
   tk.Label(text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=3, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
   tk.Label(text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=4, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
   tk.Label(text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=4, column=4, sticky=tk.W+tk.E+tk.N+tk.S)

   textfield = scrolledtext.ScrolledText(new_menu, wrap=tk.WORD, width=100, height=30)
   textfield.grid(row=4, column=1)
   tk.Label(text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=4, column=2, sticky=tk.W+tk.E+tk.N+tk.S)

   getText = ttk.Button(new_menu, text="Submit text", command=lambda: retrieve_input(textfield,new_menu)).grid(row=4, column=3)
    
   new_menu.mainloop()



def onFrameConfigure(canvas):
    # Reset the scroll region to encompass the inner frame
   canvas.configure(scrollregion=canvas.bbox("all"))



def show_extraction_details(file_menu):
   file_menu.destroy()
   details_menu = tk.Tk()
   # self.window
   details_menu.title("Breakdown of extraction")
   details_menu.geometry('1300x700') #widthxheight 
   details_menu.configure(bg='light green')


   canvas = tk.Canvas(details_menu, borderwidth=0, background="light green")
   frame = tk.Frame(canvas, background="light green")
   vsb = tk.Scrollbar(details_menu, orient="vertical", command=canvas.yview)
   canvas.configure(yscrollcommand=vsb.set)

   vsb.pack(side="right", fill="y")
   canvas.pack(side="left", fill="both", expand=True)
   canvas.create_window((4,4), window=frame, anchor="nw")

   frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

  #  populate(frame)
  
  
  
   style = Style()
   style.configure('TButton', font =('calibri', 12, 'bold'), borderwidth = '4')
   #for each line, give it a different voice in the mp3 after being able to play it
   
   book_array, dialogue_array, characters = identify_dialogue(text_array)
   
   print("book_array", book_array)
   print("characters", characters)
   print("dialogue_array", dialogue_array)
   
   tk.Label(frame, text="Extraction Breakdown", bg='light green', font=("Georgia bold", 18), fg=black).grid(row=1, column=3, sticky=tk.W+tk.E+tk.N+tk.S)

   tk.Label(frame, text=" | ", bg='light green', font=("calibri bold", 15), fg='light green').grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S) # leftmost padding
   tk.Label(frame, text="Reason", bg='light green', font=("calibri bold", 15), fg=black, relief = 'sunken').grid(row=4, column=1, sticky=tk.W+tk.E+tk.N+tk.S)
   tk.Label(frame, text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=4, column=2, sticky=tk.W+tk.E+tk.N+tk.S)
   
   tk.Label(frame, text="Dialogue", bg='light green', font=("Georgia bold", 15), fg=black, relief = 'sunken').grid(row=4, column=3, sticky=tk.W+tk.E+tk.N+tk.S)
   tk.Label(frame, text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=4, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
   
   tk.Label(frame, text="Speaker", bg='light green', font=("Georgia bold", 15), fg=black, relief = 'sunken').grid(row=4, column=5, sticky=tk.W+tk.E+tk.N+tk.S)
   tk.Label(frame, text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=0, column=6, sticky=tk.W+tk.E+tk.N+tk.S)

   tk.Label(frame, text="Context", bg='light green', font=("Georgia bold", 15), fg=black, relief = 'sunken').grid(row=4, column=7, sticky=tk.W+tk.E+tk.N+tk.S)
   tk.Label(frame, text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=4, column=8, sticky=tk.W+tk.E+tk.N+tk.S)
   
   
   tk.Label(frame, text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=3, column=1, sticky=tk.W+tk.E+tk.N+tk.S)
   
   tk.Label(frame, text=" | ", bg='light green', font=("Georgia bold", 15), fg='light green').grid(row=5, column=0, sticky=tk.W+tk.E+tk.N+tk.S)


   #table details: col 0 = reason, col 1 = dialogue, col 2 = speaker
   text_Arr_len = len(text_array)   
   rowCount = 6
   for x in range(0, len(dialogue_array)):
      tk.Label(frame, text=dialogue_array[x][1], bg='light green', font=("Georgia", 12), fg=black).grid(row=rowCount, column=1, sticky=tk.W+tk.E+tk.N+tk.S)
      tk.Label(frame, text=" | ", bg='light green', font=("Georgia bold", 12), fg='light green').grid(row=rowCount, column=2, sticky=tk.W+tk.E+tk.N+tk.S)
   
      tk.Label(frame, text='"' + dialogue_array[x][0] + '"', bg='light green', font=("Georgia", 12), fg=black, wraplength=300).grid(row=rowCount, column=3, sticky=tk.W+tk.E+tk.N+tk.S)      
      tk.Label(frame, text=" | ", bg='light green', font=("Georgia bold", 12), fg='light green').grid(row=rowCount, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
   
      tk.Label(frame, text=dialogue_array[x][2], bg='light green', font=("Georgia", 12), fg=black, wraplength=300).grid(row=rowCount, column=5, sticky=tk.W+tk.E+tk.N+tk.S)
      tk.Label(frame, text=" | ", bg='light green', font=("Georgia bold", 12), fg='light green').grid(row=rowCount, column=6, sticky=tk.W+tk.E+tk.N+tk.S)
      
      context = dialogue_array[x][3]
      if len(context) > 70: context = dialogue_array[x][3][0:context.find(' ', 70)] #cut down context that's displaye dif it's too long 
      
      tk.Label(frame, text=context, bg='light green', font=("Georgia", 12), fg=black, wraplength=300, justify='left').grid(row=rowCount, column=7, sticky=tk.W+tk.E+tk.N+tk.S)
   #     tk.Label(text=text_array[x:], bg='light green', font=("Georgia", 12), fg=black).grid(row=rowCount, column=7, sticky=tk.W+tk.E+tk.N+tk.S)
     #  tk.Label(text=dialogue_array[x][2], bg='light green', font=("Georgia", 12), fg=black).grid(row=rowCount, column=5, sticky=tk.W+tk.E+tk.N+tk.S) 
      
      rowCount+=4
   tk.Label(frame, text=" | ", bg='light green', font=("Georgia", 10), fg='light green').grid(row=rowCount+1, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
   tk.Label(frame, text=" | ", bg='light green', font=("Georgia", 10), fg='light green').grid(row=rowCount+2, column=0, sticky=tk.W+tk.E+tk.N+tk.S)

   
   tk.Label(frame, text=" ", bg='light green', font=("Georgia", 10), fg=black).grid(row=2, column=9, sticky=tk.W+tk.E+tk.N+tk.S)   
   
 #   textfield = scrolledtext.ScrolledText(frame, details_menu, wrap=tk.WORD, width=30, height=0.25)
 #   textfield.grid(row=2, column=3)
 #   textfield.insert('1.0', 'audiobook.mp3')
   
   tk.Label(frame, text=" | ", bg='light green', font=("Georgia", 10), fg='light green').grid(row=2, column=2, sticky=tk.W+tk.E+tk.N+tk.S)   

   # ttk.Button(frame, text="Create an audiobook", command=lambda: open_Audio_real(details_menu, textfield, characters)).grid(row=2, column=5, columnspan=1, sticky=tk.W+tk.E+tk.N+tk.S)
   ttk.Button(frame, text="Create an audiobook", command=lambda: open_Audio_real(details_menu, characters)).grid(row=2, column=5, columnspan=1, sticky=tk.W+tk.E+tk.N+tk.S)

   tk.Label(frame, text=" | ", bg='light green', font=("Georgia", 10), fg='light green').grid(row=2, column=4, sticky=tk.W+tk.E+tk.N+tk.S)   

   ttk.Button(frame, text="View the full text", command=lambda: view_full_text(details_menu, text_array)).grid(row=2, column=7, columnspan=1, sticky=tk.W+tk.E+tk.N+tk.S)
   
   tk.Label(frame, text=" | ", bg='light green', font=("Georgia", 10), fg='light green').grid(row=2, column=6, sticky=tk.W+tk.E+tk.N+tk.S)   
   
   ttk.Button(frame, text="Exit the program", command=lambda: exit_program(details_menu)).grid(row=2, column=1, columnspan=1, sticky=tk.W+tk.E+tk.N+tk.S)

   tk.Label(frame, text=" | ", bg='light green', font=("Georgia", 10), fg='light green').grid(row=2, column=8, sticky=tk.W+tk.E+tk.N+tk.S)   

   ttk.Button(frame, text="Return to previous page", command=lambda: return_to_menu(details_menu)).grid(row=2, column=9, columnspan=1, sticky=tk.W+tk.E+tk.N+tk.S)

  #  details_menu.mainloop()
#    make_audiobook(characters)

def view_full_text(details_menu, text_array):
   
   full_text_menu = tk.Tk()
   full_text_menu.title("Full text")
   full_text_menu.geometry('1350x900') #widthxheight 
   full_text_menu.configure(bg='light green')
   
  #  canvas = tk.Canvas(full_text_menu, borderwidth=0, background="light green")
#    framer = tk.Frame(canvas, background="light green")
#    vsb = tk.Scrollbar(full_text_menu, orient="vertical", command=canvas.yview)
#    canvas.configure(yscrollcommand=vsb.set)
# 
#    vsb.pack(side="right", fill="y")
#    canvas.pack(side="left", fill="both", expand=True)
#    canvas.create_window((4,4), window=framer, anchor="nw")
# 
#    framer.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))


   tk.Label(full_text_menu, text=" | ", bg='light green', font=("Georgia", 10), fg='light green').grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S) 
  
   tk.Label(full_text_menu, text=" | ", bg='light green', font=("Georgia", 10), fg='light green').grid(row=1, column=0, sticky=tk.W+tk.E+tk.N+tk.S)

   tk.Label(full_text_menu, text="Full Text", bg='light green', font=("Georgia bold", 15), fg=black).grid(row=1, column=1, sticky=tk.W+tk.E+tk.N+tk.S) 

   rowCount = 2
   for index in range(0, len(text_array)):
      tk.Label(full_text_menu, text='            '+text_array[index], bg='light green', font=("Georgia", 12), fg=black, wraplength=1300, justify="left").grid(row=rowCount, column=1, sticky=tk.W+tk.N) 
         
      rowCount+=2
         
def exit_program(details_menu):
   
   sys.exit()
   
# def exit_program1(file_menu):
#    
#    sys.exit()
   
def make_audiobook(characters):
   print("entered")   
   path_name = 'C:/Users/1504522/Desktop/Syslab Project/Audiobooks/'
   audio_file_name = 'audiobook.mp3'
   
   for x in book_array: print(x)
   
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
            print("text", line[2:])
            ok = "Neil didn't have the breath to answer. It didn't matter; Kevin's angry voice and the loud smack of Neil's body against the dormitory's concrete walls was enough to fill the hall with Foxes. Andrew was the first to show up in the cousins' doorway, but Matt was the one who went for Kevin. He wrapped an arm around Kevin's throat and wrenched Kevin's head back at a dangerous angle."
         
            res = tts.synthesize(ok, accept='audio/mp3', voice='en-US_OliviaV3Voice').get_result() #selecting the audio format and voice
         
            # res = tts.synthesize(line[2:], accept='audio/mp3', voice='en-US_OliviaV3Voice').get_result() #selecting the audio format and voice
            
            audio_file.write(res.content) #writing the content from text file to a audio file

   print("audio_file_name ", audio_file_name)
      
# def open_Audio_real(file_menu, textfield, characters):
def open_Audio_real(file_menu, characters):
   
   make_audiobook(characters)
   
  #  audio_file_name = textfield.get("1.0", END).strip()
#    print("audio_file_name", audio_file_name)
#    if len(audio_file_name) < 1:  # not a file name
#       audio_file_name = './audiobook.mp3'
   
    #   os.rename('./C:/Users/1504522/Desktop/Syslab Project/Audiobooks/audiobook.mp3', './C:/Users/1504522/Desktop/Syslab Project/Audiobooks/'+audio_file_name)
 #      
#    if 'mp3' not in audio_file_name:
#       audio_file_name += 'mp3'
#     #   os.rename('./', './')
#    if audio_file_name != 'audiobook.mp3': 
#       print("checkpoint")
#       os.rename('./audiobook.mp3', './'+audio_file_name)
#  
   audio_file_name = 'audiobook.mp3'
 
   os.startfile(audio_file_name)  #works

def collect_text(filename):
   f = open(filename)
   global text_array
   text_array = f.read().splitlines() #array of each line in the text
   print("text_array", text_array)
   f.close()
      
def select_file(the_menu):
   filetypes = (('text files', '*.txt'),('All files', '*.*'))

   global filename
   filename = fd.askopenfilename(title='Open a file', filetypes=filetypes)
   collect_text(filename)
 
   show_extraction_details(the_menu)
 
def identify_dialogue(text_array):                    #returns an array with smaller arrays of each dialogue within quotations, reason, and speaker
   
   dialogue_array = [] #[dialogue, reason, speaker, context] 
   global book_array
   characters = []
   book_array = []

   for element in text_array:
      counter = element.count('"')
      # print("num of quotations", counter)
      if counter > 0:         # it has quotations and is dialogue, so find the closing, then add to array followed by narration
         
         starting_index = int(element.find('"')) + 1  
         closing_index = int(element.find('"', starting_index+1))
         # print("start", starting_index, element[starting_index:])
         speaker, characters = find_speaker(element, closing_index, characters)
         if speaker == '': speaker = 'NS'
       #   print("speaker", speaker, "OOOOO", element)
        #  print("start", starting_index, element[starting_index:], speaker)
         dialogue_piece = "d " + speaker + "- " + element[starting_index:closing_index]
         
         dialogue_array.append([element[starting_index:closing_index],"Q", speaker, element])
         book_array.append(dialogue_piece)
         
         if starting_index > 1: #if there's narration before the dialogue 
            narration_piece = "n " + element[0:starting_index-1]
          #   print("oooh", element.find('"',starting_index+1))
          #   print("start", starting_index, element[starting_index:], speaker)
           #  print("NARR", narration_piece)
         
         else: 
            narration_piece = "n " + element[closing_index+1:element.find('"',closing_index+1)]
         # if narration_piece == 'n':
      #             # print("oh")
      #             print(closing_index, element[closing_index+1:])
      #          
            # print("NARR", narration_piece) #PROBLEM W AUDIO- ITS PUTTING AN EMPTY STR IN BOOK_ARRAY?
      #          print("ELEMENT", element)
         
         book_array.append(narration_piece)
         
         counter-=2
         
         
         while counter > 0:         #keep checking for dialogue + speaker combos 
            starting_index = element.find('"', closing_index+1) + 1
            closing_index = int(element.find('"', starting_index+1))
               
            dialogue_piece = "d " + speaker + "- " + element[starting_index:closing_index]
         
            dialogue_array.append([element[starting_index:closing_index],"Q", speaker, element])
            book_array.append(dialogue_piece)
            
            
         
            counter-=2    
         
      else:                               #it doesn't have quotations and is not dialogue, so assign it the narrator voice
      
         book_array.append("n " + element)
        #  print("NARR", narration_piece)

   
   dialogue_array = check_speakers(dialogue_array, characters)
          
   return book_array, dialogue_array, characters

def find_speaker(line, dialogue_closing_index, characters): # make an array of all the speakers of the text
   f = open(speaker_file)
   
   verb_array = f.read().splitlines() #array of each line in the text
   speaker = ""
   
   # CURRENT STATE: CAN FIND SPEAKER IF THE VERB IS AFTER OR BEFORE THE SPEAKER NAME
   checked_verbs = verb_array
   for verb in verb_array:
      if verb in line:
        
         speaker = verb_directly_after_speaker(line, verb, dialogue_closing_index, characters)
         if verb == "shrugged": print("HI", speaker, "VERB,", verb)
         if speaker == 0: 
            speaker = verb_directly_before_speaker(line, verb, dialogue_closing_index, characters)
            if verb == "shrugged": print("HI", speaker, "VERB,", verb)
         if speaker == 0:
          #   if line == '"How is Mother?" Nezha asks.': print("nez speak ffr", speaker)
            speaker, characters = speaker_not_in_characters(checked_verbs, line, verb, dialogue_closing_index, characters, verb_array,speaker)
         if verb == "shrugged": print("HI", speaker, "VERB,", verb)
            # if speaker=='Neil': print(line)
                        
         
   f.close()   
 #   if speaker=='Neil': print(line)
   return speaker, characters

def speaker_not_in_characters(checked_verbs, line, verb, dialogue_closing_index, characters, verb_array, speaker):
   pronouns = ["he", "she", "they"]
  #  print("d", line.index(verb), dialogue_closing_index, line)
  #  print("Tst", line[dialogue_closing_index: line.index(verb)])
  #  print("next", len(line[dialogue_closing_index: line.index(verb)]))
   if len(line[dialogue_closing_index: line.index(verb)]) == 2: #verb comes right after dialogue, speaker after verb
   #     print("oh")
      speaker = line[line.index(verb)+len(verb):len(line)-1]   #goes from end of verb to end of line for the speaker
   #     if verb == "shrugged": print("HELLO", speaker, "VERB,", verb)
      if speaker == '': speaker = 'NS' #if the speaker wasn't found then DON'T ADD TO THE CHAR ARRAY! 
      else: characters.append(speaker)      #add speaker to character array since it's not there aleady 
   #    print("speaK WOO,", speaker)
      return speaker, characters
   
   else:    #speaker is after dialogue, speaker before verb?
     #  print("ohhh", line)
      for v in verb_array:
         if v != verb and v in line:     #there's another verb in array 
          #   print("v", v, verb)
          #   print("ck", checked_verbs)
            checked_verbs.remove(verb)
            speaker_not_in_characters(checked_verbs, line, v, dialogue_closing_index, characters, verb_array, speaker)
            break
            
      if speaker == 0:
         speaker = line[dialogue_closing_index+2: line.index(verb)-1]    #goes from end of dialogue to start of verb for the speaker 
      
   
      # if verb == "shrugged": print("Hola", speaker, "VERB,", verb)
      
      if speaker == '': speaker = 'NS' #if the speaker wasn't found then DON'T ADD TO THE CHAR ARRAY! 
      else: characters.append(speaker)      #add speaker to character array since it's not there aleady 
      return speaker, characters

   return 0   
   
   
def verb_directly_before_speaker(line, verb, dialogue_closing_index, characters):

   if str(line[line.index(verb)+len(verb)+1:len(line)-1]) in characters: # speaker is AFTER verb (may need precaution in case it goes over line length 
      speaker = line[line.index(verb)+ len(verb):len(line)-1] #goes from end of verb to end of line for the speaker 
      return speaker

   return 0
   
def verb_directly_after_speaker(line, verb, dialogue_closing_index, characters):
   
   if str(line[dialogue_closing_index+2: line.index(verb)-1]) in characters: #finds the speaker using the verb, BEFORE verb            
      speaker = line[dialogue_closing_index+1:line.index(verb)]    #goes from end of dialogue to start of verb for the speaker 
   
      return speaker
   return 0   
 
def check_speakers(dialogue_array, characters):

   pronouns = ["he", "she", "they"]
   
   for index in range(0, len(dialogue_array)):
      if dialogue_array[index][2] == 'NS':       #speaker wasn't found
         for character in characters:
         #      print(dialogue_array[index][3], character)
            if character in dialogue_array[index][3] and character != 'he': 
               # print("new c", character)
               dialogue_array[index][2] = character
               # print("OOOO", dialogue_array[index][2])
               break
      else:
         for pn in pronouns:
            if pn == dialogue_array[index][2]:
               speaker = pronoun_to_speaker(pn, dialogue_array[index][3], dialogue_array, index, characters)
               dialogue_array[index][2] = speaker
               break
               
 #   print("updated,", dialogue_array)
   return dialogue_array


def pronoun_to_speaker(pronoun, line, dialogue_array, index,characters):
   #dialogue = 0, reason = 1, speaker = 2, entire line = 3 
   print(pronoun, line, characters)
   if pronoun in characters: characters.remove(pronoun)
   #check next speaker, pick alternate 
   speaker = ""
   next_speaker = dialogue_array[index+1][2]
   
   if len(characters) == 2:
      if characters[0] == next_speaker:
         speaker = characters[1]
      else:
         speaker = characters[0]
         
   print("spea,", speaker)
   return speaker


menu()