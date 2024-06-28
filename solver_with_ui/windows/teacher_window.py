import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget, QMessageBox, QListWidgetItem, QCheckBox
from PyQt5.QtCore import Qt

class TeacherPage(QWidget):
    """
    Représente la page de gestion des enseignants
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
        layout = QHBoxLayout()

        # Partie gauche
        left_layout = QVBoxLayout()
        buttons_layout = QHBoxLayout()
        self.delete_button = QPushButton("Delete")
        self.modify_button = QPushButton("Modify")
        self.teacher_list = QListWidget()
        self.teacher_list.itemClicked.connect(self.select_teacher)
        # Ajout des éléments à la partie de gauche
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addWidget(self.modify_button)        
        left_layout.addLayout(buttons_layout)
        left_layout.addWidget(self.teacher_list)
        
        # Partie droite
        right_layout = QVBoxLayout()
        name_label = QLabel("Name")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")
        min_hour_label = QLabel("Min hour")
        self.min_hour_input = QLineEdit()
        self.min_hour_input.setPlaceholderText("Min hour")
        max_hour_label = QLabel("Max hour")
        self.max_hour_input = QLineEdit()
        self.max_hour_input.setPlaceholderText("Max hour")
        levels_label = QLabel("Levels")
        self.levels_list = QListWidget()
        self.levels_list.setSelectionMode(QListWidget.MultiSelection)
        try:
            with open('config.json', 'r') as file:
                config = json.load(file)
                levels = config.get('levels', [])
                for level in levels:
                    item = QListWidgetItem(level['name'])
                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                    item.setCheckState(Qt.Unchecked)
                    self.levels_list.addItem(item)
        except FileNotFoundError:
            with open('config.json', 'w') as file:
                json.dump({"teachers": [], "levels": []}, file)
        self.minimize_hours_checkbox = QCheckBox("Minimize Hours")
        self.minimize_levels_checkbox = QCheckBox("Minimize Levels")
        minimize_label = QLabel("Minimize")
        self.add_button = QPushButton("Add teacher")
        self.add_button.clicked.connect(self.add_teacher)
        # Ajout des éléments à la partie de droite
        right_layout.addWidget(name_label)
        right_layout.addWidget(self.name_input)
        right_layout.addWidget(min_hour_label)
        right_layout.addWidget(self.min_hour_input)
        right_layout.addWidget(max_hour_label)
        right_layout.addWidget(self.max_hour_input)
        right_layout.addWidget(levels_label)
        right_layout.addWidget(self.levels_list)
        right_layout.addWidget(minimize_label)
        right_layout.addWidget(self.minimize_hours_checkbox)
        right_layout.addWidget(self.minimize_levels_checkbox)
        right_layout.addWidget(self.add_button)
        
        right_layout.addStretch(1)
        
        layout.addLayout(left_layout, 1)
        layout.addLayout(right_layout, 1)
        
        self.setLayout(layout)
        self.load_teachers()
        self.current_teacher = None

        self.delete_button.clicked.connect(self.delete_teacher)
        self.modify_button.clicked.connect(self.modify_teacher)

    def load_teachers(self):
        """
        Fonction permettant de charger les enseignants depuis le fichier de configuration
        En entrée : Aucune
        En sortie : Aucune
        """
        try:
            with open('config.json', 'r') as file:
                config = json.load(file)
                teachers = config.get('teachers', [])
                self.teacher_list.clear()
                for teacher in teachers:
                    self.teacher_list.addItem(teacher['name'])
            print("Log : Récupération des enseignants depuis teacher_window.py")
        except FileNotFoundError:
            with open('config.json', 'w') as file:
                json.dump({"teachers": [], "levels": []}, file)

    def add_teacher(self):
        """
        Fonction permettant d'ajouter un enseignant
        En entrée : Aucune
        En sortie : Aucune
        """
        name = self.name_input.text()
        min_hour = self.min_hour_input.text()
        max_hour = self.max_hour_input.text()
        levels = [self.levels_list.item(i).text() for i in range(self.levels_list.count()) if self.levels_list.item(i).checkState() == Qt.Checked]
        minimize_hours = self.minimize_hours_checkbox.isChecked()
        minimize_levels = self.minimize_levels_checkbox.isChecked()
        if not name or not min_hour or not max_hour or not levels:
            QMessageBox.warning(self, "Erreur de saisie", "Merci de saisir tous les champs.")
            return
        new_teacher = {
            "name": name,
            "min_hour": min_hour,
            "max_hour": max_hour,
            "levels": levels,
            "minimize_hours": minimize_hours,
            "minimize_levels": minimize_levels
        }
        try:
            with open('config.json', 'r+') as file:
                config = json.load(file)
                config['teachers'].append(new_teacher)
                file.seek(0)
                file.truncate()
                json.dump(config, file, indent=4)
                
            self.teacher_list.addItem(name)
            self.clear_inputs()
            print("Log : Ajout de l'enseignant depuis teacher_window.py")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", "Une erreur est survenue lors de l'ajout de l'enseignant.")

    def select_teacher(self, item):
        """
        Fonction permettant de sélectionner un enseignant
        En entrée : L'item sélectionné
        En sortie : Aucune
        """
        try:
            with open('config.json', 'r') as file:
                config = json.load(file)
                teachers = config.get('teachers', [])
                for teacher in teachers:
                    if teacher['name'] == item.text():
                        self.current_teacher = teacher
                        self.name_input.setText(teacher['name'])
                        self.min_hour_input.setText(teacher['min_hour'])
                        self.max_hour_input.setText(teacher['max_hour'])
                        self.minimize_hours_checkbox.setChecked(teacher.get('minimize_hours', False))
                        self.minimize_levels_checkbox.setChecked(teacher.get('minimize_levels', False))
                        for i in range(self.levels_list.count()):
                            if self.levels_list.item(i).text() in teacher['levels']:
                                self.levels_list.item(i).setCheckState(Qt.Checked)
                            else:
                                self.levels_list.item(i).setCheckState(Qt.Unchecked)
                        break
        except Exception as e:
            QMessageBox.critical(self, "Erreur", "Une erreur est survenue lors de la sélection de l'enseignant.")

    def modify_teacher(self):
        """
        Fonction permettant de modifier un enseignant
        En entrée : Aucune
        En sortie : Aucune
        """
        if self.current_teacher is None:
            QMessageBox.warning(self, "Erreur de sélection", "Merci de sélectionner un enseignant à modifier.")
            return
        
        new_name = self.name_input.text()
        min_hour = self.min_hour_input.text()
        max_hour = self.max_hour_input.text()
        levels = [self.levels_list.item(i).text() for i in range(self.levels_list.count()) if self.levels_list.item(i).checkState() == Qt.Checked]
        minimize_hours = self.minimize_hours_checkbox.isChecked()
        minimize_levels = self.minimize_levels_checkbox.isChecked()
        
        if not new_name or not min_hour or not max_hour or not levels:
            QMessageBox.warning(self, "Erreur de saisie", "Merci de saisir tous les champs.")
            return
        
        try:
            with open('config.json', 'r+') as file:
                config = json.load(file)
                for teacher in config['teachers']:
                    if teacher['name'] == self.current_teacher['name']:
                        teacher['name'] = new_name
                        teacher['min_hour'] = min_hour
                        teacher['max_hour'] = max_hour
                        teacher['levels'] = levels
                        teacher['minimize_hours'] = minimize_hours
                        teacher['minimize_levels'] = minimize_levels
                        self.current_teacher = teacher
                        break
                file.seek(0)
                file.truncate()
                json.dump(config, file, indent=4)
                
            self.load_teachers()
            self.clear_inputs()
            print("Log : Modification de l'enseignant depuis teacher_window.py")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", "Une erreur est survenue lors de la modification de l'enseignant.")

    def delete_teacher(self):
        """
        Fonction permettant de supprimer un enseignant
        En entrée : Aucune
        En sortie : Aucune
        """
        if self.current_teacher is None:
            QMessageBox.warning(self, "Erreur de sélection", "Merci de sélectionner un enseignant à supprimer.")
            return
        
        try:
            with open('config.json', 'r+') as file:
                config = json.load(file)
                config['teachers'] = [teacher for teacher in config['teachers'] if teacher['name'] != self.current_teacher['name']]
                file.seek(0)
                file.truncate()
                json.dump(config, file, indent=4)
                
            self.load_teachers()
            self.clear_inputs()
            self.current_teacher = None
            print("Log : Suppression de l'enseignant depuis teacher_window.py")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", "Une erreur est survenue lors de la suppression de l'enseignant.")

    def clear_inputs(self):
        """
        Fonction permettant de vider les champs de saisie
        En entrée : Aucune
        En sortie : Aucune
        """
        self.name_input.clear()
        self.min_hour_input.clear()
        self.max_hour_input.clear()
        for i in range(self.levels_list.count()):
            self.levels_list.item(i).setCheckState(Qt.Unchecked)
        self.minimize_hours_checkbox.setChecked(False)
        self.minimize_levels_checkbox.setChecked(False)
