# Importation des modules
import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget, QMessageBox, QListWidgetItem
from PyQt5.QtCore import Qt
from styles import global_stylesheet

class LevelsRepartitionPage(QWidget):
    """
    Représente la page de répartition des niveaux en fonction des enseignants 
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
        self.setStyleSheet(global_stylesheet.stylesheet)
        layout = QHBoxLayout()

        # Partie gauche
        left_layout = QVBoxLayout()
        buttons_layout = QHBoxLayout()
        self.delete_button = QPushButton("Delete")
        self.modify_button = QPushButton("Modify")       
        self.constraint_list = QListWidget()
        self.constraint_list.itemClicked.connect(self.select_constraint)
        # Ajout des boutons à partie gauche
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addWidget(self.modify_button)
        left_layout.addLayout(buttons_layout)
        left_layout.addWidget(self.constraint_list)

        # Partie droite
        right_layout = QVBoxLayout()
        teacher_label = QLabel("Teacher")
        self.teacher_list = QListWidget()
        levels_label = QLabel("Levels")
        self.levels_list = QListWidget()
        self.levels_list.setSelectionMode(QListWidget.MultiSelection)
        min_group_label = QLabel("Min groups")
        self.min_group_input = QLineEdit()
        self.min_group_input.setPlaceholderText("Min groups")
        max_group_label = QLabel("Max groups")
        self.max_group_input = QLineEdit()
        self.max_group_input.setPlaceholderText("Max groups")
        self.add_button = QPushButton("Add constraint")
        self.add_button.clicked.connect(self.add_constraint)
        # Ajout des éléments à la partie droite
        right_layout.addWidget(teacher_label)
        right_layout.addWidget(self.teacher_list)
        right_layout.addWidget(levels_label)
        right_layout.addWidget(self.levels_list)
        right_layout.addWidget(min_group_label)
        right_layout.addWidget(self.min_group_input)
        right_layout.addWidget(max_group_label)
        right_layout.addWidget(self.max_group_input)
        right_layout.addWidget(self.add_button)

        right_layout.addStretch(1)
        
        # Ajout des parties gauche et droite à la page
        layout.addLayout(left_layout, 1)
        layout.addLayout(right_layout, 1)
        self.setLayout(layout)
        self.load_constraints()
        self.load_teachers()
        self.load_levels()
        self.delete_button.clicked.connect(self.delete_constraint)
        self.modify_button.clicked.connect(self.modify_constraint)
        self.current_constraint = None

    def load_constraints(self):
        """
        Fonction permettant de charger les contraintes de niveau depuis le fichier de configuration
        En entrée : Aucune
        En sortie : Aucune
        """
        try:
            with open('config.json', 'r') as file:
                config = json.load(file)
                constraints = config.get('level_constraints', [])
                self.constraint_list.clear()
                for constraint in constraints:
                    item_text = f"{constraint['teacher']} : {constraint['levels']} (Min: {constraint['min_groups']}, Max: {constraint['max_groups']})"
                    self.constraint_list.addItem(item_text)
            print("Log : Récupération des contraintes de niveaux depuis levels_repartition_window.py")
        except FileNotFoundError:
            with open('config.json', 'w') as file:
                json.dump({"teachers": [], "levels": [], "level_constraints": []}, file)

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
                    item = QListWidgetItem(teacher['name'])
                    self.teacher_list.addItem(item)
            print("Log : Récupération des enseignants depuis levels_repartition_window.py")
        except FileNotFoundError:
            with open('config.json', 'w') as file:
                json.dump({"teachers": [], "levels": [], "level_constraints": []}, file)

    def load_levels(self):
        """
        Fonction permettant de charger les niveaux depuis le fichier de configuration
        En entrée : Aucune
        En sortie : Aucune
        """
        try:
            with open('config.json', 'r') as file:
                config = json.load(file)
                levels = config.get('levels', [])
                self.levels_list.clear()
                for level in levels:
                    item = QListWidgetItem(level['name'], self.levels_list)
                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                    item.setCheckState(Qt.Unchecked)
                    self.levels_list.addItem(item)
            print("Log : Récupération des niveaux depuis levels_repartition_window.py")
        except FileNotFoundError:
            with open('config.json', 'w') as file:
                json.dump({"teachers": [], "levels": [], "level_constraints": []}, file)

    def add_constraint(self):
        """
        Fonction permettant d'ajouter une contrainte de niveau 
        En entrée : Aucune
        En sortie : Aucune
        """
        selected_teacher_item = self.teacher_list.selectedItems()
        selected_levels_items = self.levels_list.selectedItems()
        min_groups = self.min_group_input.text()
        max_groups = self.max_group_input.text()
        
        if not selected_teacher_item or not selected_levels_items or not min_groups or not max_groups:
            QMessageBox.warning(self, "Erreur de saisie", "Merci de saisir tous les champs.")
            return

        teacher = selected_teacher_item[0].text()
        levels = [item.text() for item in selected_levels_items]
        
        new_constraint = {
            "teacher": teacher,
            "levels": levels,
            "min_groups": int(min_groups),
            "max_groups": int(max_groups)
        }
        
        try:
            with open('config.json', 'r+') as file:
                config = json.load(file)
                
                # Ensure 'level_constraints' exists in the config
                if 'level_constraints' not in config:
                    config['level_constraints'] = []
                
                config['level_constraints'].append(new_constraint)
                file.seek(0)
                file.truncate()
                json.dump(config, file, indent=4)
                
            self.load_constraints()
            self.clear_inputs()
            print("Log : Ajout d'une contrainte de niveau depuis levels_repartition_window.py")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", "Une erreur est survenue lors de l'ajout de la contrainte.")

    def select_constraint(self, item):
        """
        Fonction permettant de sélectionner une contrainte de niveau
        En entrée : item (QListWidgetItem) : L'élément sélectionné
        En sortie : Aucune
        """
        try:
            with open('config.json', 'r') as file:
                config = json.load(file)
                constraints = config.get('level_constraints', [])
                for constraint in constraints:
                    item_text = f"{constraint['teacher']} : {constraint['levels']} (Min: {constraint['min_groups']}, Max: {constraint['max_groups']})"
                    if item.text() == item_text:
                        self.current_constraint = constraint
                        self.clear_selection()
                        self.teacher_list.findItems(constraint['teacher'], Qt.MatchExactly)[0].setSelected(True)
                        for level in constraint['levels']:
                            self.levels_list.findItems(level, Qt.MatchExactly)[0].setCheckState(Qt.Checked)
                        self.min_group_input.setText(str(constraint['min_groups']))
                        self.max_group_input.setText(str(constraint['max_groups']))
                        break
        except Exception as e:
            QMessageBox.critical(self, "Erreur", "Une erreur est survenue lors de la sélection de la contrainte.")

    def modify_constraint(self):
        """
        Fonction permettant de modifier une contrainte de niveau
        En entrée : Aucune
        En sortie : Aucune
        """
        if self.current_constraint is None:
            QMessageBox.warning(self, "Erreur de sélection", "Merci saisir une contrainte à modifier.")
            return
        
        selected_teacher_item = self.teacher_list.selectedItems()
        selected_levels_items = self.levels_list.selectedItems()
        min_groups = self.min_group_input.text()
        max_groups = self.max_group_input.text()
        
        if not selected_teacher_item or not selected_levels_items or not min_groups or not max_groups:
            QMessageBox.warning(self, "Erreur de saisie", "Merci de saisir tous les champs.")
            return

        teacher = selected_teacher_item[0].text()
        levels = [item.text() for item in selected_levels_items]

        try:
            with open('config.json', 'r+') as file:
                config = json.load(file)
                for constraint in config['level_constraints']:
                    if constraint == self.current_constraint:
                        constraint['teacher'] = teacher
                        constraint['levels'] = levels
                        constraint['min_groups'] = int(min_groups)
                        constraint['max_groups'] = int(max_groups)
                        self.current_constraint = constraint
                        break
                file.seek(0)
                file.truncate()
                json.dump(config, file, indent=4)
                
            self.load_constraints()
            self.clear_inputs()
            print("Log : Modification d'une contrainte de niveau depuis levels_repartition_window.py")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", "Une erreur est survenue lors de la modification de la contrainte.")

    def delete_constraint(self):
        """
        Fonction permettant de supprimer une contrainte de niveau
        En entrée : Aucune
        En sortie : Aucune
        """
        if self.current_constraint is None:
            QMessageBox.warning(self, "Erreur de sélection", "Merci de sélectionner une contrainte à supprimer.")
            return
        
        try:
            with open('config.json', 'r+') as file:
                config = json.load(file)
                config['level_constraints'] = [constraint for constraint in config['level_constraints'] if constraint != self.current_constraint]
                file.seek(0)
                file.truncate()
                json.dump(config, file, indent=4)
                
            self.load_constraints()
            self.clear_inputs()
            self.current_constraint = None
            print("Log : Suppression d'une contrainte de niveau depuis levels_repartition_window.py")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", "Une erreur est survenue lors de la suppression de la contrainte.")

    def clear_inputs(self):
        """
        Fonction permettant de vider les champs de saisie
        En entrée : Aucune
        En sortie : Aucune
        """
        self.clear_selection()
        self.min_group_input.clear()
        self.max_group_input.clear()

    def clear_selection(self):
        """
        Fonction permettant de désélectionner les éléments sélectionnés
        En entrée : Aucune
        En sortie : Aucune
        """
        self.teacher_list.clearSelection()
        for i in range(self.levels_list.count()):
            item = self.levels_list.item(i)
            item.setCheckState(Qt.Unchecked)