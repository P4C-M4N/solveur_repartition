# Constantes de couleurs 
RICH_BLACK = "#0D1F2D" # BLeu foncé
CORAL = "#F37748" # Orange
BABY_POWDER = "#FDFFF7" # Blanc
VERDIGRIS = "#38A3A5" # Bleu 
SHAMROCK_GREEN = "#169873" # Vert

stylesheet = """
QWidget {
    background-color: """ + RICH_BLACK + """;
}

QMenuBar {
    font-size: 20px;
    spacing: 25px;
    background-color: """ + SHAMROCK_GREEN + """;
    color: """ + BABY_POWDER + """;
}


QMenuBar::item:selected {
    background-color: """ + VERDIGRIS + """;
    color: """ + BABY_POWDER + """;
}

QLabel {
    color: """ + BABY_POWDER + """;
    font-size: 30px;
}


QPushButton {
    background-color: """ + VERDIGRIS + """;
    color: """ + BABY_POWDER + """;
    border: none;
    padding: 10px;
    height: 50px;
    font-size: 20px;
}

QPushButton:hover {
    background-color: """ + CORAL + """;
}

QLineEdit {
    background-color: """ + VERDIGRIS + """;
    color: """ + BABY_POWDER + """;
    font-size: 20px;
    height: 50px;
    margin-bottom : 25px;
}

QListWidget {
    background-color: """ + VERDIGRIS + """;
    color: """ + BABY_POWDER + """;
    font-size: 20px;
}

QListWidget::item {
    border: 1px solid """ + VERDIGRIS + """;
    font-size: 20px;
    margin-bottom: 20px;
}

QListWidgetItem {
    background-color: """ + BABY_POWDER + """;
    color: """ + RICH_BLACK + """;
    font-size: 20px;
}


QTextEdit {
    background-color: """ + VERDIGRIS + """;
    color: """ + BABY_POWDER + """;
    font-size: 20px;
    margin-bottom: 20px;
}

QTableWidget::item {
    background-color: """ + VERDIGRIS + """;
    color: """ + BABY_POWDER + """;
    border: 1px solid """ + CORAL + """;
    font-size: 20px;
    font-weight: bold;
    padding-left: 10px;
}

QCheckBox {
    color: """ + BABY_POWDER + """;
    background-color: """ + VERDIGRIS + """;
    font-size: 20px;
}

"""