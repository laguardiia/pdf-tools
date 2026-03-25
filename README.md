# PDF Tools 🛠️

Una herramienta de escritorio sencilla para combinar, separar y comprimir archivos PDF, con interfaz gráfica en español e inglés.

---

## Funcionalidades

- **Combinar PDFs** — Seleccioná múltiples archivos y unilos en uno solo
- **Separar PDF** — Extraé un rango de páginas de un PDF existente
- **Comprimir PDF** — Reducí el tamaño de un archivo PDF manteniendo su contenido
- **Interfaz bilingüe** — Cambiá entre español e inglés con un clic
- **Detección automática de idioma** — La app detecta el idioma del sistema al iniciar

---

## 📋 Requisitos

- Python 3.8 o superior
- Las dependencias listadas en `requirements.txt`

---

## 🚀 Instalación

1. Cloná el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/pdf-tools.git
   cd pdf-tools
   ```

2. Instalá las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecutá la aplicación:
   ```bash
   python main.py
   ```

---

## 📦 Generar ejecutable (opcional)

Podés crear un `.exe` (Windows) o binario (Linux/Mac) con PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=iconv2.png main.py
```

El ejecutable se genera en la carpeta `dist/`.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Podés abrir un issue para reportar bugs o proponer mejoras, o directamente hacer un pull request.

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Consultá el archivo [LICENSE](LICENSE) para más detalles.

---

---

# PDF Tools 🛠️

A simple desktop tool to merge, split, and compress PDF files, with a graphical interface in Spanish and English.

---

##  Features

- **Merge PDFs** — Select multiple files and combine them into one
- **Split PDF** — Extract a page range from an existing PDF
- **Compress PDF** — Reduce the file size of a PDF while preserving its content
- **Bilingual interface** — Switch between Spanish and English with one click
- **Automatic language detection** — The app detects the system language on startup

---

## 📋 Requirements

- Python 3.8 or higher
- Dependencies listed in `requirements.txt`

---

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/pdf-tools.git
   cd pdf-tools
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

---

## 🖼️ Required Assets

The application uses the following image files, which must be in the same directory as `main.py`:

| File | Description |
|---|---|
| `banner.png` | Top banner of the app |
| `iconv2.png` | Window icon |
| `us_flag.png` | Flag icon to switch to English |
| `es_flag.png` | Flag icon to switch to Spanish |
| `reiniciar.png` | Reset button icon |

---

## 📦 Build Executable (optional)

You can create a `.exe` (Windows) or binary (Linux/Mac) with PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=iconv2.png main.py
```

The executable will be generated in the `dist/` folder.

---

## 🤝 Contributing

Contributions are welcome. You can open an issue to report bugs or suggest improvements, or submit a pull request directly.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
