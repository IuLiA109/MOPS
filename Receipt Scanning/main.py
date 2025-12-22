import cv2 as cv
import numpy as np
import pytesseract
import re
from thefuzz import fuzz
from category import *
from image_processing import *
from text_processing import *
from dotenv import load_dotenv

load_dotenv()

base_path = rf"{os.getenv('TESSERACT_PATH')}"
TESSERACT_CMD = base_path + r"Tesseract-OCR/tesseract.exe"
IMAGINE_BON = 'bon1.jpeg'
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def afisare_rezultate(rezultate, rand_total):
    data = {
        "produse": [
            {
                "produs": r["produs"],
                "pret": r["pret"],
                "categorie": r["categorie"]
            }
            for r in rezultate
        ]
    }

    if rand_total is not None:
        data["total"] = rand_total

    print(json.dumps(data, indent=4, ensure_ascii=False))

def main():
    img = cv.imread(IMAGINE_BON)
    if img is None:
        print(f"Eroare: Imaginea '{IMAGINE_BON}' nu exista sau nu a putut fi citita.")
        return

    bon = extrage_bon(img)
    # show_image("Bon Decupat", bon)
    
    gray_upscaled, binary_map = preprocesare_generala(bon)
    # show_image("Binarizare pentru Linii", binary_map)
    
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