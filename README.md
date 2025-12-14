# MOPS

## ⚙️ Cerințe Preliminare

* **Limbaj:** Python **3.10.7**
* **OS:** Windows (recomandat pentru acest ghid de instalare)

---

## 🚀 Ghid de Instalare

Pentru a rula acest proiect, este necesară o configurare în doi pași: instalarea motorului OCR extern și instalarea bibliotecilor Python.

### Pasul 1: Instalarea Tesseract-OCR (Obligatoriu)

Librăria Python `pytesseract` este doar o interfață. Pentru a funcționa, trebuie instalat motorul OCR pe sistem.

1.  **Descarcă Tesseract:**
    * Accesează [UB Mannheim Tesseract Wiki](https://github.com/UB-Mannheim/tesseract/wiki).
    * Descarcă versiunea **64-bit** (ex: `tesseract-ocr-w64-setup-v5.x.x.exe`).

2.  **Instalează-l:**
    * Rulează installer-ul descărcat.
    * ⚠️ **IMPORTANT:** La pasul **"Additional Script Data"** (sau "Additional Language Data"), derulează și bifează **Romanian (ron)**.
    * *Notă: Implicit vine doar cu engleză, dar aplicația necesită limba română pentru a citi corect diacriticele și formatul bonurilor.*

3.  **Reține calea de instalare:**
    * Calea standard este: `C:\Program Files\Tesseract-OCR` sau `C:\Users\Nume\AppData\Local\Programs\Tesseract-OCR`.
    * Vei avea nevoie de folderul părinte la **Pasul 3**.

### Pasul 2: Instalarea Dependențelor Python

Deschide terminalul (CMD, PowerShell sau terminalul din VS Code) în folderul proiectului și rulează comanda:

```bash
pip install opencv-python numpy pytesseract thefuzz python-Levenshtein
```

### Pasul 3: Configurarea (Foarte Important)

Deoarece calea de instalare a Tesseract diferă de la un calculator la altul, trebuie să setezi locația corectă în codul sursă.

1.  Deschide fișierul `main.py` într-un editor de text.
2.  La începutul fișierului, caută variabila `base_path`:

    ```python
    # Așa arată linia în codul original
    base_path = r""
    ```

3.  Introdu calea către **folderul părinte** (cel care conține folderul `Tesseract-OCR`).

    > **💡 Notă:** Nu trebuie să pui calea completă până la `tesseract.exe`, ci doar folderul în care ai instalat programul. Scriptul va adăuga automat sufixul `Tesseract-OCR/tesseract.exe`.

    #### Exemple de configurare:
      **Dacă ai instalat în `AppData`, linia va arăta aproximativ așa (înlocuiește `NumeUser`):**
        ```python
        base_path = r"C:/Users/NumeUser/AppData/Local/Programs/"
        ```
