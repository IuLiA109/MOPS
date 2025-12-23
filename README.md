# OCR Receipt Processing

## Requirements
### Software

- Python 3.10.x
- Tesseract OCR 5.x
- Romanian language data for Tesseract (`ron`)

### Python Dependencies

All Python dependencies are listed in `requirements.txt`.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/IuLiA109/MOPS.git
cd mops
```

### 2. Install Tesseract OCR

#### Windows

1. Download the 64-bit installer from:
   https://github.com/UB-Mannheim/tesseract/wiki

2. Run the installer.

3. During installation, make sure to install the Romanian language pack (`ron`), under "Additional Language Data".
   This is required for correct diacritics and receipt formatting.

4. Note the installation directory. Common paths include:
   - `C:\Program Files\Tesseract-OCR`
   - `C:\Users\<User>\AppData\Local\Programs\Tesseract-OCR`

#### Linux
Install Tesseract using your package manager and include the Romanian language pack.

Ubuntu:
```bash
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-ron
```

Verify:
```bash
tesseract --version
```

### 3. Install dependancies

```
pip install -r requirements.txt
```

## Configuration

### Tesseract Path Configuration
### Windows Only
Because Tesseract is not always available in the system PATH on Windows, the project requires manual configuration.
1.  Create a .env file
2. Include the variable ```TESSERACT_PATH=<path to Tesseract-OCR>```
    - e.g. ```TESSERACT_PATH=C:/Program Files/```

The script will automatically append Tesseract-OCR/tesseract.exe

### Linux
No path configuration is required as long as Tesseract is installed system-wide and accessible from the command line.


## Running the Project
After installation and configuration, run: 
```bash
python main.py
```

Make sure input images are placed in the expected directory structure defined by the project.