import os

FILES_TO_RENAME_PATH = r'C:\Users\jeron\Google Drive\trading\kirk\2022\listas'
PREFIX_TO_CHECK = '2018'
PREFIX_TO_CHANGE = '2022'
FILENAME_SEPARATOR = '_'

os.chdir(FILES_TO_RENAME_PATH)

# dirs=directories
for (root, dirs, file) in os.walk(FILES_TO_RENAME_PATH):
    for f in file:
        print(f)
        filename_lst = f.split('_')
        prefix_file = filename_lst[0]
        if prefix_file == PREFIX_TO_CHECK:
            filename_lst[0] = PREFIX_TO_CHANGE
            newFilename = FILENAME_SEPARATOR.join(filename_lst)
            os.rename(f, newFilename)
