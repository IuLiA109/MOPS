import cv2 as cv
import numpy as np
import pytesseract
import re
from thefuzz import fuzz
from category import *
from image_processing import *
from text_processing import *

base_path = r""
TESSERACT_CMD = base_path + r"Tesseract-OCR/tesseract.exe"
IMAGINE_BON = 'bon1.jpeg'
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def afisare_rezultate(rezultate, rand_total):
    print("REZULTAT FINAL CLASIFICARE BON")
    print("="*50)
    for r in rezultate:
        print(f"| {r['categorie']:<20} | {r['produs']:<25} | {r['pret']:<6} RON |")
    if rand_total:
        print("TOTAL BON (Text extras):", rand_total)
    print("="*50)

def main():
    img = cv.imread(IMAGINE_BON)
    if img is None:
        print(f"Eroare: Imaginea '{IMAGINE_BON}' nu exista sau nu a putut fi citita.")
        return

    bon = extrage_bon(img)
    show_image("Bon Decupat", bon)
    
    gray_upscaled, binary_map = preprocesare_generala(bon)
    show_image("Binarizare pentru Linii", binary_map)
    
    slices_linii = extrage_linii_text(gray_upscaled, binary_map)
    text_integral = ""
    
    for i, slice_img in enumerate(slices_linii):
        text_raw = proceseaza_linie_ocr(slice_img)
        if len(text_raw) < 3: 
            continue 
        text_integral += text_raw.upper().strip() + "\n"

    randuri = text_integral.split('\n')
    date_brute_produse, rand_total = extrage_date_produse(randuri)
    
    if not date_brute_produse:
        print("Nu s-au putut extrage datele de produse pentru clasificare.")
        return
        
    lista_produse_finale = procesare_date_brute(date_brute_produse)
    rezultate = clasifica_produse(lista_produse_finale)
    afisare_rezultate(rezultate, rand_total)

if __name__ == "__main__":
    main()