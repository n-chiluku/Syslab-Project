import sys, os, time, subprocess, webbrowser

# filename = fd.askopenfilename(title='Open a file', filetypes=filetypes)
# book_title = filename[filename.rfind("/")+1:len(filename)-4]
filename = "C:\Users\1504522\Desktop\Syslab Project\Quotes\Metamorphosis"

f = open(filename)
global text_array
text_array = f.read().splitlines() #array of each line in the text
print("text_array", text_array)
f.close()




