# image_browser.py
import os
import glob
import PySimpleGUI as sg
from PIL import Image, ImageTk
import shutil

def GetImages(path):
    images = glob.glob(f'{path}/*.jpg') + glob.glob(f'{path}/*.jpeg')
    return images

def UpdateImage(paths, window, prefex):
    try:
        for i in range(6):
            if i<len(paths):
                image = Image.open(paths[i])
                image.thumbnail((250, 250))
                photo_img = ImageTk.PhotoImage(image)
                window[f"{prefex}-IMAGE-{i}"].update(data=photo_img)
            else:
                window[f"{prefex}-IMAGE-{i}"].update(data=None)
    except:
        print(f"Unable to open {paths[0]}!")

def CombineFolders(baseFolsder, dir1, dir2):
    newDir=os.path.join(baseFolsder, f"{dir1}+{dir2}")
    os.makedirs(newDir)
    dir1=os.path.join(baseFolsder, f"{dir1}")
    imgFromDir1=GetImages(dir1)
    for file in imgFromDir1:
        shutil.move(file, newDir)
    if len(os.listdir(dir1))==0:
        os.removedirs(dir1)
    dir2=os.path.join(baseFolsder, f"{dir2}")
    imgFromDir2=GetImages(dir2)
    for file in imgFromDir2:
        shutil.move(file, newDir)
    if len(os.listdir(dir2))==0:
        os.removedirs(dir2)


def GetFolders(path):
    contents = os.listdir(path)
    folders = []
    for name in contents:
        if os.path.isdir(os.path.join(path, name)):
            folders.append(name)
    return folders

def main():
    folder_path = r"C:/DATA/AI/Test/"
    folders = GetFolders(folder_path)

    elements = [
        [sg.Button("Combine folders", size=(400,1), disabled=True)],
        [sg.Column([
                [sg.Listbox(values=folders, enable_events=True, size=(80, 5), key="L-FOLDERS")],
                [sg.Image(key=f"L-IMAGE-{i}", size=(100, 100)) for i in range(2)],
                [sg.Image(key=f"L-IMAGE-{i}", size=(100, 100)) for i in range(2, 4)],
                [sg.Image(key=f"L-IMAGE-{i}", size=(100, 100)) for i in range(4, 6)],
            ],
            pad=(0, 0),  # Убираем отступы
            vertical_alignment="top",  # Выравнивание по верхнему краю
        ),
        sg.VSeparator(),
        sg.Column([
            [sg.Listbox(values=folders, enable_events=True, size=(80, 5), key="R-FOLDERS")],
            [sg.Image(key=f"R-IMAGE-{i}", size=(100, 100)) for i in range(2)],
            [sg.Image(key=f"R-IMAGE-{i}", size=(100, 100)) for i in range(2, 4)],
            [sg.Image(key=f"R-IMAGE-{i}", size=(100, 100)) for i in range(4, 6)],
        ],
            pad=(0, 0),  # Убираем отступы
            vertical_alignment="top",  # Выравнивание по верхнему краю
        )
        ]
    ]

    window = sg.Window("Image Viewer", elements, size=(1200, 800))
    images = []
    left_dir = None
    right_dir = None

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "L-FOLDERS":
            left_dir=values["L-FOLDERS"][0]
            images = GetImages(os.path.join(folder_path, left_dir))
            UpdateImage(images, window, "L")
        if event == "R-FOLDERS":
            right_dir=values["R-FOLDERS"][0]
            images = GetImages(os.path.join(folder_path, right_dir))
            UpdateImage(images, window, "R")
        if event == "Combine folders":
            CombineFolders(folder_path, left_dir, right_dir)
            folders = GetFolders(folder_path)
            window["L-FOLDERS"].update(values=folders)
            window["R-FOLDERS"].update(values=folders)
            UpdateImage([], window, "L")
            UpdateImage([], window, "R")

        window["Combine folders"].update(disabled=(left_dir is None)or(right_dir is None)or(left_dir == right_dir))
    window.close()

if __name__ == "__main__":
    main()