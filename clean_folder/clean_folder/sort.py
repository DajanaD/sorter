import re
import sys
import os
from pathlib import Path
import shutil


CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

TRANS = dict()

for cyrillic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyrillic)] = latin
    TRANS[ord(cyrillic.upper())] = latin.upper()


def normalize(name):
    translate_name = re.sub(r'\W', '_', name.translate(TRANS))
    return translate_name

JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []
DOC_DOCUMENT = []
DOCX_DOCUMENT = []
TXT_DOCUMENT = []
PDF_DOCUMENT = []
XLSX_DOCUMENT = []
PPTX_DOCUMENT = []
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []
MY_OTHER = []
ARCHIVES = []

REGISTER_EXTENSION = {
    'JPEG': JPEG_IMAGES,
    'JPG': JPG_IMAGES,
    'PNG': PNG_IMAGES,
    'SVG': SVG_IMAGES,
    'MP3': MP3_AUDIO,
    'AVI': AVI_VIDEO,
    'MP4': MP4_VIDEO,
    'MOV': MOV_VIDEO,
    'MKV': MKV_VIDEO,
    'DOC': DOC_DOCUMENT,
    'DOCX': DOCX_DOCUMENT,
    'TXT': TXT_DOCUMENT,
    'PDF': PDF_DOCUMENT,
    'XLSX': XLSX_DOCUMENT,
    'PPTX': PPTX_DOCUMENT,
    'MP3': MP3_AUDIO,
    'OGG': OGG_AUDIO,
    'WAV': WAV_AUDIO,
    'AMR': AMR_AUDIO,
    'ZIP': ARCHIVES,
    'GZ': ARCHIVES,
    'TAR': ARCHIVES,
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()


def get_extension(name):
    return Path(name).suffix[1:].upper()  # suffix[1:] -> .jpg -> jpg

def scan(folder):
    for item in folder.iterdir():
        # Робота з папкою
        if item.is_dir():  # перевіряємо чи обєкт папка
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHER'):
                FOLDERS.append(item)
                scan(item)
            continue

        # Робота з файлом
        extension = get_extension(item.name)  # беремо розширення файлу
        full_name = folder / item.name  # беремо повний шлях до файлу
        if not extension:
            MY_OTHER.append(full_name)
        else:
            try:
                REGISTER_EXTENSION[extension]
                EXTENSIONS.add(extension)
            except KeyError:
                UNKNOWN.add(extension)  # .mp4, .mov, .avi
                MY_OTHER.append(full_name)

def handle_media(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    file_name.replace(target_folder / normalize(file_name.name))

def handle_archive(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(file_name.name.replace(file_name.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute()))
    except shutil.ReadError:
        folder_for_file.rmdir()
        return
    file_name.unlink()


def main(folder):
    scan = scan(folder)
    for file in scan(JPEG_IMAGES):
        handle_media(file, folder / 'images' / 'JPEG')
    for file in scan(JPG_IMAGES):
        handle_media(file, folder / 'images' / 'JPG')
    for file in scan(PNG_IMAGES):
        handle_media(file, folder / 'images' / 'PNG')
    for file in scan(SVG_IMAGES):
        handle_media(file, folder / 'images' / 'SVG')
    for file in scan(SVG_IMAGES):
        handle_media(file, folder / 'video' / 'AVI')
    for file in scan(SVG_IMAGES):
        handle_media(file, folder / 'video' / 'MP4')
    for file in scan(SVG_IMAGES):
        handle_media(file, folder / 'video' / 'MOV')
    for file in scan(SVG_IMAGES):
        handle_media(file, folder / 'video' / 'MKV')
    for file in scan(SVG_IMAGES):
        handle_media(file, folder / 'documents' / 'DOC')
    for file in scan(SVG_IMAGES):
        handle_media(file, folder / 'documents' / 'DOCX') 
    for file in scan(SVG_IMAGES):
        handle_media(file, folder / 'documents' / 'TXT')
    for file in scan(SVG_IMAGES):
        handle_media(file, folder / 'documents' / 'PDF')
    for file in scan(SVG_IMAGES):
        handle_media(file, folder / 'documents' / 'XLSX')
    for file in scan(SVG_IMAGES):
        handle_media(file, folder / 'documents' / 'PPTX') 
    for file in scan(MP3_AUDIO):
        handle_media(file, folder / 'audio' / 'MP3')
    for file in scan(SVG_IMAGES):
        handle_media(file, folder / 'audio' / 'OGG')
    for file in scan(SVG_IMAGES):
        handle_media(file, folder / 'audio' / 'WAV') 
    for file in scan(SVG_IMAGES):
        handle_media(file, folder / 'audio' / 'AMR')
    for file in scan(MY_OTHER):
        handle_media(file, folder / 'MY_OTHER')
    for file in scan(ARCHIVES):
        handle_archive(file, folder / 'ARCHIVES')

    for folder in scan(FOLDERS[::-1]):
        # Видаляємо пусті папки після сортування
        try:
            folder.rmdir()
        except OSError:
            print(f'Error during remove folder {folder}')

def run():
    folder_process = Path(sys.argv[1])
    main(folder_process)


if __name__ == '__main__':
    run()