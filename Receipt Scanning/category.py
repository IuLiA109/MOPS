import json
import os
from thefuzz import process, fuzz

DB_FILE = "baza_date_produse.json"

def incarca_baza_date():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {
            "Bauturi": ["cola", "apa", "suc", "bere"],
            "Panificatie": ["paine", "franzela", "covrig"],
            "Lactate": ["lapte", "branza", "unt"]
        }

def salveaza_baza_date(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4, ensure_ascii=False)

def cere_categorie_manual(produs, db):
    print(f"\n" + "="*50)
    print(f"[?] NU recunosc produsul: '{produs}'")
    print("-" * 50)
    categorii_existente = ", ".join(sorted(db.keys()))
    print(f"Categorii existente: {categorii_existente}")
    print("-" * 50)
    
    while True:
        raspuns = input(f">> Scrie categoria pentru '{produs}' (sau una NOUA): ").strip()
        
        if not raspuns:
            print("Te rog scrie un nume de categorie.")
            continue
            
        categorie_aleasa = raspuns.title()
        
        if categorie_aleasa in db:
            print(f"Adaug '{produs}' in categoria existenta: {categorie_aleasa}")
        else:
            db[categorie_aleasa] = []
            
        cuvant_cheie = produs.lower()
        if cuvant_cheie not in db[categorie_aleasa]:
            db[categorie_aleasa].append(cuvant_cheie)
            salveaza_baza_date(db)
            
        return categorie_aleasa

def clasifica_produse(lista_produse, prag_siguranta=85):
    db = incarca_baza_date()
    rezultate_finale = []

    for nume_produs, pret in lista_produse:
        best_score = 0
        categorie_gasita = None
        
        cheie_produs = nume_produs.lower()

        for cat, keywords in db.items():
            match = process.extractOne(cheie_produs, keywords, scorer=fuzz.partial_ratio)
            if match:
                if match[1] > best_score:
                    best_score = match[1]
                    categorie_gasita = cat

        if best_score >= prag_siguranta:
            rezultate_finale.append({
                "produs": nume_produs, 
                "pret": pret, 
                "categorie": categorie_gasita
            })
        else:
            cat_manuala = cere_categorie_manual(nume_produs, db)
            rezultate_finale.append({
                "produs": nume_produs,
                "pret": pret,
                "categorie": cat_manuala
            })

            db = incarca_baza_date()

    return rezultate_finale
