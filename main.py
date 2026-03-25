import sys
import os
import locale
from PyPDF2 import PdfWriter, PdfReader
import pikepdf
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QFileDialog, QMessageBox, QRadioButton
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap

# Diccionario de traducciones
LANGUAGES = {
    "es": {
        "title": "PDF Tools - Combinar, Dividir y Comprimir",
        "option_merge": "Combinar PDFs",
        "option_split": "Separar PDF",
        "option_compress": "Comprimir PDF",
        "btn_select_multiple": "Seleccionar archivos",
        "btn_select_single": "Seleccionar archivo",
        "btn_reset_tooltip": "Limpiar selección",
        "label_range": "Rango de páginas (inicio-fin):",
        "label_selected": "Archivos cargados:",
        "btn_process": "Procesar",
        "warning_no_files": "No hay archivos PDF seleccionados.",
        "warning_not_enough_files": "Selecciona al menos 2 PDFs para combinar.",
        "success_merged": "PDF combinado guardado en:",
        "error_merge": "No se pudo combinar los PDFs.",
        "error_invalid_range": "Formato de rango inválido. Usa: inicio-fin (ej: 1-5)",
        "error_out_of_range": "Páginas fuera de rango.",
        "success_split": "PDF separado guardado en:",
        "success_compressed": "PDF comprimido guardado en:",
        "error_compress": "No se pudo comprimir el PDF.",
        "default_name_compressed": "_comprimido"
    },
    "en": {
        "title": "PDF Tools - Merge, Split and Compress",
        "option_merge": "Merge PDFs",
        "option_split": "Split PDF",
        "option_compress": "Compress PDF",
        "btn_select_multiple": "Select files",
        "btn_select_single": "Select file",
        "btn_reset_tooltip": "Clear selection",
        "label_range": "Page range (start-end):",
        "label_selected": "Loaded files:",
        "btn_process": "Process",
        "warning_no_files": "No PDF files selected.",
        "warning_not_enough_files": "Select at least 2 PDFs to merge.",
        "success_merged": "Merged PDF saved at:",
        "error_merge": "Could not merge PDFs.",
        "error_invalid_range": "Invalid range format. Use: start-end (e.g. 1-5)",
        "error_out_of_range": "Pages out of range.",
        "success_split": "Split PDF saved at:",
        "success_compressed": "Compressed PDF saved at:",
        "error_compress": "Could not compress PDF.",
        "default_name_compressed": "_compressed"
    }
}

# Estilo oscuro para toda la aplicación
DARK_STYLE = """
QMainWindow, QMessageBox {
    background-color: #2b2b2b;
}
QRadioButton {
    color: white;
    font-size: 18px;
    spacing: 5px;
}
QRadioButton::indicator {
    width: 20px;
    height: 20px;
}
QPushButton {
    background-color: #b50f00;
    color: white;
    border: none;
    padding: 10px;
    border-radius: 6px;
    font-size: 18px;
}
QPushButton:hover {
    background-color: #bf2315;
}
QPushButton#circle {
    border-radius: 20px;
    width: 40px;
    height: 40px;
    padding: 0;
    border: none;
    background-color: #444;
}
QPushButton#circle:hover {
    background-color: #555;
}
QLineEdit {
    background-color: #3c3c3c;
    color: white;
    padding: 8px;
    border: 1px solid #555;
    border-radius: 4px;
    font-size: 18px;
}
QLabel {
    color: #ffffff;
    font-size: 18px;
}
QLabel#files_label {
    color: #a0a0a0;
    font-size: 14px;
    font-style: italic;
}

QPushButton#reset_button {
    background-color: transparent;
    border: none;
    padding: 0;
}
QPushButton#reset_button:hover {
    background-color: rgba(255, 255, 255, 30);
    border-radius: 20px;
}
"""

class PDFToolApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Idioma del sistema detectado automáticamente
        lang_code = locale.getdefaultlocale()[0][:2]
        self.lang = LANGUAGES.get(lang_code, LANGUAGES["es"])

        self.setWindowTitle(self.lang["title"])
        self.setGeometry(100, 100, 500, 480)
        self.setFixedSize(450, 650)
        self.setWindowIcon(QIcon("iconv2.png"))
        self.setStyleSheet(DARK_STYLE)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ===== BOTONES DE IDIOMA =====
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 5, 4, 0)
        top_layout.setSpacing(5)

        self.btn_en = QPushButton()
        self.btn_en.setIcon(QIcon("us_flag.png"))
        self.btn_en.setObjectName("circle")
        self.btn_en.setFixedSize(40, 40)
        self.btn_en.clicked.connect(lambda: self.change_language("en"))

        self.btn_es = QPushButton()
        self.btn_es.setIcon(QIcon("es_flag.png"))
        self.btn_es.setObjectName("circle")
        self.btn_es.setFixedSize(40, 40)
        self.btn_es.clicked.connect(lambda: self.change_language("es"))

        top_layout.addStretch()
        top_layout.addWidget(self.btn_en)
        top_layout.addWidget(self.btn_es)

        main_layout.addLayout(top_layout)

        # ===== CONTENIDO CENTRADO =====
        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        content_layout.setContentsMargins(0, 50, 0, 0)
        
        self.banner_label = QLabel()
        pixmap = QPixmap("banner.png")
        if not pixmap.isNull():
            self.banner_label.setPixmap(
                pixmap.scaled(375, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            )
        self.banner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.banner_label)

        options_layout = QHBoxLayout()
        
        # Creación de RadioButtons
        self.radio_merge = QRadioButton(self.lang["option_merge"])
        self.radio_split = QRadioButton(self.lang["option_split"])
        self.radio_compress = QRadioButton(self.lang["option_compress"])
        self.radio_merge.setChecked(True)

        options_layout.addWidget(self.radio_merge)
        options_layout.addWidget(self.radio_split)
        options_layout.addWidget(self.radio_compress)

        # Conexión limpia
        self.radio_merge.toggled.connect(self.on_mode_changed)
        self.radio_split.toggled.connect(self.on_mode_changed)
        self.radio_compress.toggled.connect(self.on_mode_changed)

# ===== SECCIÓN DE SELECCIÓN DE ARCHIVOS Y BOTÓN DE RESET ACTUALIZADA =====
        selection_layout = QHBoxLayout()
        selection_layout.setSpacing(10)
        
        self.btn_select = QPushButton(self.lang["btn_select_multiple"])
        self.btn_select.clicked.connect(self.select_files)

        self.btn_reset = QPushButton()
        self.btn_reset.setIcon(QIcon("reiniciar.png")) 
        self.btn_reset.setObjectName("reset_button")
    
        self.btn_reset.setFixedSize(40, 40)
        self.btn_reset.setIconSize(QSize(33, 33))
        
        self.btn_reset.setToolTip(self.lang["btn_reset_tooltip"])
        self.btn_reset.clicked.connect(self.clear_selection)

        selection_layout.addWidget(self.btn_select)
        selection_layout.addWidget(self.btn_reset)

        # Etiqueta para mostrar los archivos seleccionados
        self.label_selected_files = QLabel("")
        self.label_selected_files.setObjectName("files_label")
        self.label_selected_files.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_selected_files.setWordWrap(True)

        self.label_range = QLabel(self.lang["label_range"])
        self.label_range.setVisible(False)

        self.entry_range = QLineEdit()
        self.entry_range.setVisible(False)
        self.entry_range.setMaximumWidth(150)

        self.btn_process = QPushButton(self.lang["btn_process"])
        self.btn_process.clicked.connect(self.process_action)

        content_layout.addLayout(options_layout)
        content_layout.addLayout(selection_layout)
        content_layout.addWidget(self.label_selected_files)
        content_layout.addWidget(self.label_range)
        content_layout.addWidget(self.entry_range)
        content_layout.addWidget(self.btn_process)

        main_layout.addLayout(content_layout)

        self.selected_paths = []

    def change_language(self, lang_code):
        self.lang = LANGUAGES[lang_code]
        self.setWindowTitle(self.lang["title"])
        self.radio_merge.setText(self.lang["option_merge"])
        self.radio_split.setText(self.lang["option_split"])
        self.radio_compress.setText(self.lang["option_compress"])
        self.label_range.setText(self.lang["label_range"])
        self.btn_process.setText(self.lang["btn_process"])
        self.btn_reset.setToolTip(self.lang["btn_reset_tooltip"])
        self.update_ui_state()
        self.update_files_label()

    def on_mode_changed(self, checked=False):
        """Maneja de forma segura cualquier cambio en los RadioButtons."""
        self.update_ui_state()
        self.clear_selection()

    def update_ui_state(self):
        """Actualiza textos y visibilidad según el modo seleccionado."""
        is_merge = self.radio_merge.isChecked()
        is_split = self.radio_split.isChecked()

        self.btn_select.setText(self.lang["btn_select_multiple"] if is_merge else self.lang["btn_select_single"])
        
        self.label_range.setVisible(is_split)
        self.entry_range.setVisible(is_split)

    def select_files(self):
        if self.radio_merge.isChecked():
            files, _ = QFileDialog.getOpenFileNames(self, "", "", "PDF Files (*.pdf)")
            self.selected_paths = files if files else []
        else:
            file, _ = QFileDialog.getOpenFileName(self, "", "", "PDF Files (*.pdf)")
            self.selected_paths = [file] if file else []
        
        self.update_files_label()

    def update_files_label(self):
        """Actualiza el texto del label para mostrar los nombres de los PDFs cargados."""
        if not self.selected_paths:
            self.label_selected_files.setText("")
        else:
            names = [os.path.basename(p) for p in self.selected_paths]
            text = f"{self.lang['label_selected']} " + ", ".join(names)
            self.label_selected_files.setText(text)

    def clear_selection(self):
        """Limpia los archivos cargados."""
        self.selected_paths = []
        self.update_files_label()
        self.entry_range.clear()

    def process_action(self):
        if not self.selected_paths:
            QMessageBox.warning(self, "Error", self.lang["warning_no_files"])
            return
        
        if self.radio_merge.isChecked():
            self.merge_pdfs()
        elif self.radio_split.isChecked():
            self.split_pdf()
        else:
            self.compress_pdf()

    def merge_pdfs(self):
        if len(self.selected_paths) < 2:
            QMessageBox.critical(self, "Error", self.lang["warning_not_enough_files"])
            return

        base_names = [os.path.splitext(os.path.basename(p))[0] for p in self.selected_paths]
        suggested_name = "_".join(base_names) + ".pdf"

        output, _ = QFileDialog.getSaveFileName(self, "", suggested_name, "PDF Files (*.pdf)")
        if not output:
            return

        writer = PdfWriter()
        try:
            for path in self.selected_paths:
                reader = PdfReader(path)
                for page in reader.pages:
                    writer.add_page(page)

            with open(output, "wb") as f:
                writer.write(f)

            QMessageBox.information(self, "", f"{self.lang['success_merged']}\n{output}")
            self.clear_selection()
        except Exception as e:
            QMessageBox.critical(self, "", str(e))

    def split_pdf(self):
        input_path = self.selected_paths[0]
        reader = PdfReader(input_path)

        try:
            start, end = map(int, self.entry_range.text().split("-"))
        except:
            QMessageBox.critical(self, "", self.lang["error_invalid_range"])
            return

        if start < 1 or end > len(reader.pages):
            QMessageBox.critical(self, "", self.lang["error_out_of_range"])
            return

        base_name = os.path.splitext(os.path.basename(input_path))[0]
        suggested_name = f"{base_name}_{start}-{end}.pdf"

        output, _ = QFileDialog.getSaveFileName(self, "", suggested_name, "PDF Files (*.pdf)")
        if not output:
            return

        writer = PdfWriter()
        for i in range(start - 1, end):
            writer.add_page(reader.pages[i])

        try:
            with open(output, "wb") as f:
                writer.write(f)

            QMessageBox.information(self, "", f"{self.lang['success_split']}\n{output}")
            self.clear_selection()
        except Exception as e:
            QMessageBox.critical(self, "", str(e))

    def compress_pdf(self):
        input_path = self.selected_paths[0]
        
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        suffix = self.lang["default_name_compressed"]
        suggested_name = f"{base_name}{suffix}.pdf"

        output, _ = QFileDialog.getSaveFileName(self, "", suggested_name, "PDF Files (*.pdf)")
        if not output:
            return

        try:
            with pikepdf.open(input_path) as pdf:
                pdf.save(output, compress_streams=True)
            QMessageBox.information(self, "", f"{self.lang['success_compressed']}\n{output}")
            self.clear_selection()
        except Exception as e:
            QMessageBox.critical(self, "", str(e))


def main():
    app = QApplication(sys.argv)
    window = PDFToolApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()