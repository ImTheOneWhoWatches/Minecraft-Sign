import sys
import random
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDialog, QTextBrowser

def apply_color_codes(text):
    color_mapping = {
        '§0': '<font color="#000000">',  # black
        '§1': '<font color="#0000AA">',  # dark_blue
        '§2': '<font color="#00AA00">',  # dark_green
        '§3': '<font color="#00AAAA">',  # dark_aqua
        '§4': '<font color="#AA0000">',  # dark_red
        '§5': '<font color="#AA00AA">',  # dark_purple
        '§6': '<font color="#FFAA00">',  # gold
        '§7': '<font color="#AAAAAA">',  # gray
        '§8': '<font color="#555555">',  # dark_gray
        '§9': '<font color="#5555FF">',  # blue
        '§a': '<font color="#55FF55">',  # green
        '§b': '<font color="#55FFFF">',  # aqua
        '§c': '<font color="#FF5555">',  # red
        '§d': '<font color="#FF55FF">',  # light_purple
        '§e': '<font color="#FFFF55">',  # yellow
        '§f': '<font color="#FFFFFF">',  # white
        '§r': '</font>',  # reset
        '§l': '<b>',  # bold
        '§o': '<i>',  # italic
        '§n': '<u>',  # underline
        '§m': '<s>',  # strikethrough
    }

    formatted_text = text
    for code, color in color_mapping.items():
        formatted_text = formatted_text.replace(code, color)

    return formatted_text

def apply_obfuscated(text):
    obfuscated_text = ''.join(random.sample(text, len(text)))
    return obfuscated_text

class ObfuscatedLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_obfuscated_text)
        self.timer.start(100)  # Update text every 100 milliseconds
        self.original_text = ""
        self.obfuscate = False

    def setText(self, text):
        self.original_text = text
        self.obfuscate = '§k' in text
        super().setText(text)

    def update_obfuscated_text(self):
        if self.obfuscate:
            obfuscated_text = apply_obfuscated(self.original_text)
            super().setText(obfuscated_text)

class MOTDFormatter(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Sign Generator')
        self.setFixedSize(250, 200)  # Set fixed size for the main window

        layout = QVBoxLayout()

        motd_label = QLabel('         Enter your Minecraft Sign color code:')
        layout.addWidget(motd_label)

        self.motd_input = QLineEdit()
        layout.addWidget(self.motd_input)

        insert_button = QPushButton('Insert §')
        insert_button.clicked.connect(self.insert_section_symbol)
        layout.addWidget(insert_button)

        self.format_button = QPushButton('Format Sign')
        self.format_button.clicked.connect(self.format_and_display)
        layout.addWidget(self.format_button)

        self.formatted_motd_label = ObfuscatedLabel()
        layout.addWidget(self.formatted_motd_label)

        self.info_button = QPushButton('§ Codes Info')
        self.info_button.clicked.connect(self.open_info_window)
        layout.addWidget(self.info_button)

        self.setLayout(layout)

        # Apply styles
        self.setStyleSheet("""
            QWidget {
                background-color: #212121;
                border-radius: 10px;
            }
            QLineEdit, QPushButton {
                background-color: #E2E2E2;
                border-radius: 5px;
                border: 2px solid #424242;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #424242;
            }
        """)

    def format_and_display(self):
        motd_input_text = self.motd_input.text()
        formatted_motd = apply_color_codes(motd_input_text)
        self.formatted_motd_label.setText(formatted_motd)
        if '§k' in formatted_motd:
            self.formatted_motd_label.obfuscate = True
        else:
            self.formatted_motd_label.obfuscate = False

    def insert_section_symbol(self):
        cursor_position = self.motd_input.cursorPosition()
        current_text = self.motd_input.text()
        new_text = current_text[:cursor_position] + "§" + current_text[cursor_position:]
        self.motd_input.setText(new_text)
        self.motd_input.setCursorPosition(cursor_position + 1)

    def open_info_window(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("§ Codes Info")
        dialog.setFixedSize(200, 260)  # Set fixed size for the information dialog
        dialog.setModal(False)
        dialog_layout = QVBoxLayout()

        info_text = QTextBrowser()
        info_text.setOpenExternalLinks(True)
        info_text.setHtml("""
        <h3>§ Codes Information</h3>
        <p><b>§0</b>: <font color="#000000">Black</font></p>
        <p><b>§1</b>: <font color="#0000AA">Dark Blue</font></p>
        <p><b>§2</b>: <font color="#00AA00">Dark Green</font></p>
        <p><b>§3</b>: <font color="#00AAAA">Dark Aqua</font></p>
        <p><b>§4</b>: <font color="#AA0000">Dark Red</font></p>
        <p><b>§5</b>: <font color="#AA00AA">Dark Purple</font></p>
        <p><b>§6</b>: <font color="#FFAA00">Gold</font></p>
        <p><b>§7</b>: <font color="#AAAAAA">Gray</font></p>
        <p><b>§8</b>: <font color="#555555">Dark Gray</font></p>
        <p><b>§9</b>: <font color="#5555FF">Blue</font></p>
        <p><b>§a</b>: <font color="#55FF55">Green</font></p>
        <p><b>§b</b>: <font color="#55FFFF">Aqua</font></p>
        <p><b>§c</b>: <font color="#FF5555">Red</font></p>
        <p><b>§d</b>: <font color="#FF55FF">Light Purple</font></p>
        <p><b>§e</b>: <font color="#FFFF55">Yellow</font></p>
        <p><b>§f</b>: <font color="#FFFFFF">White</font></p>
        <p><b>§r</b>: Reset Color</p>
        <p><b>§l</b>: Bold</p>
        <p><b>§o</b>: Italic</p>
        <p><b>§n</b>: Underline</p>
        <p><b>§m</b>: Strikethrough</p>
        <p><b>§k</b>: Obfuscated Text</p>
        """)
        dialog_layout.addWidget(info_text)

        made_by_label = QLabel("Made by TheOneWhoWatches")
        made_by_label.setFont(QFont('Arial', 8))
        dialog_layout.addWidget(made_by_label, alignment=Qt.AlignRight)

        dialog.setLayout(dialog_layout)
        dialog.show()

def main():
    app = QApplication(sys.argv)
    formatter = MOTDFormatter()
    formatter.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
