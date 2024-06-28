# Importation des modules
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QSizePolicy
import solver.solver as solver

class ResultPage(QWidget):
    """
    Représente la page d'affichage des résultats
    """
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Fonction permettant d'initialiser l'interface graphique de la page de répartition des niveaux
        En entrée : Aucune
        En sortie : Aucune
        """
        layout = QVBoxLayout()
        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.run_solver)
        layout.addWidget(self.run_button)
        self.result_table = QTableWidget()
        self.result_table.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        layout.addWidget(self.result_table)
        self.setLayout(layout)

    def run_solver(self):
        """
        Fonction permettant de lancer le solveur et d'afficher les résultats
        En entrée : Aucune
        En sortie : Aucune
        """
        self.result_table.clear()
        try:
            results = solver.solve()
        except Exception as e:
            QMessageBox.critical(self, "Erreur : ", "Aucune solution trouvée")
            return

        if results:
            levels = list(next(iter(results.values())).keys())
            levels.remove('total_hours')
            num_rows = len(results)
            num_cols = len(levels) + 1
            self.result_table.setColumnCount(num_cols)
            self.result_table.setRowCount(num_rows)
            header_labels = levels + ['Total Hours']
            self.result_table.setHorizontalHeaderLabels(header_labels)
            font = self.result_table.font()
            font.setPointSize(10)
            self.result_table.setFont(font)

            # Remplissage des lignes
            for i, (teacher_name, teacher_result) in enumerate(results.items()):
                total_hours = teacher_result.get('total_hours', 0)
                teacher_name_item = QTableWidgetItem(teacher_name)
                self.result_table.setVerticalHeaderItem(i, teacher_name_item)

                # Remplissage des colonnes
                for j, level in enumerate(levels):
                    value = teacher_result.get(level, 0)
                    item = QTableWidgetItem(str(round(value, 2)))
                    self.result_table.setItem(i, j, item)

                item_total = QTableWidgetItem(str(round(total_hours, 2)))
                self.result_table.setItem(i, num_cols - 1, item_total)

            self.result_table.resizeColumnsToContents()

            # Ajustement de la taille des colonnes et des lignes
            width = self.width()
            height = self.height()
            num_columns = self.result_table.columnCount()
            column_width = width / (num_columns + 1)
            for j in range(num_columns):
                self.result_table.setColumnWidth(j, int(column_width))

            num_rows = self.result_table.rowCount()
            row_height = height / (num_rows + 2)
            for i in range(num_rows):
                self.result_table.setRowHeight(i, int(row_height))