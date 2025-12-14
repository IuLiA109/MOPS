import re

def extrage_date_produse(randuri):
    rand_start = -1
    rand_final = -1
    
    randuri_filtrate = [
        r for r in randuri 
        if len(r) > 0 and not (
            (r[0].isdigit() and "BUC." not in r) or 
            "REDUCERE" in r or 
            ("TOTAL" in r and not r.startswith("TOTAL")) or 
            "DISCOUNT" in r
        )
    ]

    for i, rand in enumerate(randuri_filtrate):
        if rand_start == -1 and ("BUC." in rand):
            rand_start = i
        if rand_final == -1 and rand.startswith("TOTAL"):
            rand_final = i
            break
    
    if rand_start == -1 or rand_final == -1:
        print("Avertisment: Nu s-au putut gasi limitele 'BUC.' si 'TOTAL'.")
        return [], None
        
    rand_total = randuri_filtrate[rand_final]
    data_bruta = []
    i = rand_start

    while i < rand_final:
        produs_curent = randuri_filtrate[i]
        
        if i + 1 < len(randuri_filtrate):
            rand_urmator = randuri_filtrate[i+1]
            
            if "BUC." in produs_curent:
                data_bruta.append((produs_curent, rand_urmator))
                i += 2
            else:
                data_bruta.append(("", produs_curent)) 
                i += 1
        else:
            data_bruta.append((produs_curent, ""))
            i += 1
            
    return data_bruta, rand_total

def procesare_pret(data_pret):
    pret = 0
    cantitate = 1
    cuvinte_pret = data_pret.split()

    if(data_pret!=""):
        index_buc = -1
        for i, cuvant in enumerate(cuvinte_pret):
            if "BUC" in cuvant: 
                index_buc = i
                break
        if index_buc > 0:
            raw_cantitate = cuvinte_pret[index_buc - 1]
            cantitate_clean = re.sub(r"[^0-9,.]", "", raw_cantitate)
            
            try:
                cantitate = float(cantitate_clean.replace(',', '.'))
            except ValueError:
                cantitate = 1.0 

            for cuvant in reversed(cuvinte_pret):
                if any(c.isdigit() for c in cuvant):
                    pret_clean = re.sub(r"[^0-9,.]", "", cuvant)
                    try:
                        pret = float(pret_clean.replace(',', '.'))
                        break
                    except ValueError:
                        continue

    return cantitate * pret

def procesare_produs(data_produs):
    cuvinte_produs = data_produs.split()
    second_pret = 0.0
    nume_parts = []

    for cuvant in cuvinte_produs:
        if cuvant[0].isdigit():
            break 
        nume_parts.append(cuvant)

    for cuvant in reversed(cuvinte_produs):
        if sum(1 for c in cuvant if c.isdigit()) >= 2:
            pret_clean = re.sub(r"[^0-9,.]", "", cuvant)
            pret_clean = pret_clean.replace(',', '.')
            try:
                second_pret = float(pret_clean)
                break 
            except ValueError:
                continue 

    nume_produs = " ".join(nume_parts)
    return nume_produs, second_pret

def procesare_date_brute(date_brut):
    lista_produse_finale = []
    for d in date_brut:
        data_pret = d[0]
        data_produs = d[1]
        produs = ""
        first_pret = 0
        pret_final = 0.0
        
        first_pret = procesare_pret(data_pret)
        produs, second_pret = procesare_produs(data_produs)
        pret_final = second_pret

        if(first_pret != second_pret and first_pret != 0.0):
                pret_final = first_pret

        lista_produse_finale.append((produs, pret_final))

    return lista_produse_finale
