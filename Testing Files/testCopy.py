import sys, os, time
import tkinter as tk
from tkinter import *
# import tkSnack
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from backEnd import TestingClass
# import pygame
import vlc
# import play_mp3
import Play_mp3 
# play_mp3.play(filename)
# C:\Users\1504522\Desktop\Syslab Project
# C:\Users\1504522 
# os.system('pip install play-mp3 --C:\Users\1504522\Desktop\Syslab Project')
# import subprocess
# subprocess.call('pip install play-mp3 --target=C:\Users\1504522\Desktop\Syslab Project', shell=True)

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
file_menu = None
speaker_file = "speakerCues.txt"

# p = vlc.MediaPlayer("AndrewNeil.mp3")
# p.play()

import playsound
from playsound import playsound
# playsound.playsound('AndrewNeil.mp3')

def menu():
   file_menu = tk.Tk()
   file_menu.title("Menu")
   file_menu.geometry('500x500')
   
   ttk.Button(text='Open a Text File', command=select_file()) #open the file 

   ttk.Button(text="Get the information", command=lambda: show_extraction_details(file_menu)).grid(row=100, column=0, columnspan=1, sticky=tk.W+tk.E+tk.N+tk.S)

   file_menu.mainloop()

def show_extraction_details(file_menu):

   
   #for each line, give it a different voice in the mp3 after being able to play it
   
   book_array, dialogue_array = identify_dialogue(text_array)
   
   tk.Label(text="Breakdown of dialogue extraction", font=("Arial", 10), fg=grey).grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
   tk.Label(text="", font=("Arial", 10), fg=grey).grid(row=1, column=0, sticky=tk.W+tk.E+tk.N+tk.S)

  #  tk.Label(text="Dialogue: ", font=("Arial", 10), fg=grey).grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
  #  for x in range(0, len(book_array)):
#       if book_array[x][0] == 'd':      # it's dialogue
# 
#          tk.Label(text=book_array[x][1:], font=("Arial", 10), fg=grey).grid(row=x+1, column=1, sticky=tk.W+tk.E+tk.N+tk.S) # print dialogue
#          line_info = []

   count = 2
   for x in range(0, len(dialogue_array)):
      tk.Label(text="Dialogue: ", font=("Arial", 10), fg=grey).grid(row=count, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
      tk.Label(text='"' + dialogue_array[x][0] + '"', font=("Arial", 10), fg=grey).grid(row=count, column=1, sticky=tk.W+tk.E+tk.N+tk.S)
      tk.Label(text="Reason for extraction: ", font=("Arial", 10), fg=grey).grid(row=count+1, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
      tk.Label(text=dialogue_array[x][1], font=("Arial", 10), fg=grey).grid(row=count+1, column=1, sticky=tk.W+tk.E+tk.N+tk.S)
      tk.Label(text="Speaker: ", font=("Arial", 10), fg=grey).grid(row=count+2, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
      tk.Label(text=dialogue_array[x][2], font=("Arial", 10), fg=grey).grid(row=count+2, column=1, sticky=tk.W+tk.E+tk.N+tk.S)
      
      tk.Label(text="", font=("Arial", 10), fg=grey).grid(row=count+3, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
      
      count+=4
      
      # tk.Label(text=book_array[x][1:], font=("Arial", 10), fg=grey).grid(row=x, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
      
      ttk.Button(text="Get the audio", command=lambda: open_Audio_real(file_menu)).grid(row=100, column=1, columnspan=1, sticky=tk.W+tk.E+tk.N+tk.S)

def open_Audio_real(file_menu):

   playsound('C:/Users/1504522/Desktop/Syslab Project/AndrewNeil.mp3')
  #  ttk.Button(text="Exit", command=lambda: exit_program(file_menu)).grid(row=100, column=2, columnspan=1, sticky=tk.W+tk.E+tk.N+tk.S)
   
# def exit_program(file_menu):
#    return True   

def collect_text(filename):
   f = open(filename)
   global text_array
   text_array = f.read().splitlines() #array of each line in the text
   f.close()
      
def select_file():
   filetypes = (('text files', '*.txt'),('All files', '*.*'))

   global filename
   filename = fd.askopenfilename(title='Open a file', filetypes=filetypes)
   
   collect_text(filename)
   
   
def identify_dialogue(text_array):                    #returns an array with smaller arrays of each dialogue within quotations, reason, and speaker
   
   dialogue_array = [] #[dialogue, reason, speaker]
#    narration_array = []
   
   book_array = [] 
  #  thought_keywords = ['wondered', 'thought']
   
   for element in text_array:
      print("line", element)
      if element.find('"') != -1:         # it has quotations and is dialogue, so find the closing, then add to array followed by narration
         starting_index = int(element.find('"')) + 1
         closing_index = int(element.find('"', starting_index+1))
         
         dialogue_piece = "d " + element[starting_index:closing_index]
         
         
         speaker = find_speaker(element, closing_index)
         
         
         dialogue_array.append([element[starting_index:closing_index],"quotations", speaker])
         book_array.append(dialogue_piece)
         # print("dialogue", dialogue_array)
         # print("book", book_array)
         narration_piece = "n " + element[closing_index+1:]
         # narration_array.append(narration_piece)
         book_array.append(narration_piece)
         
      else:                               #it doesn't have quotations and is not dialogue, so assign it the narrator voice
         # for word in thought_keywords:
      #             if word in element:           # it is a thought, so counts as dialogue
      #                
         book_array.append("n " + element)
          
   return book_array, dialogue_array

def find_speaker(line, dialogue_closing_index): # make an array of all the speakers of the text
 #   for index in range(0,len(book_array)):
 #      if book_array[index] == 'n' && book_array[index-1]: #it's narration and there's dialogue before
         
   f = open(speaker_file)
   
   verb_array = f.read().splitlines() #array of each line in the text
   speaker = ""
   
   characters = []
   
   for verb in verb_array:
      if verb in line:
         speaker = line[dialogue_closing_index+1: line.index(verb)]
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
   
   
   # speaker = book_array[index+1:
 
   
menu()