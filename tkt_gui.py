import PySimpleGUI as sg
from pathlib import Path

filePath_s = r'C:\temp\etf'
text = sg.PopupGetFile('Please enter a file name',
                       default_path = filePath_s,
                       initial_folder = filePath_s,
                       file_types = (("Normal text file","*.txt"),("All types","*.*")))
sg.Popup('Results', 'The value returned from PopupGetFile', text)
filename = Path(text)
print(text)
print(filename.stem)
print(filename.suffix)