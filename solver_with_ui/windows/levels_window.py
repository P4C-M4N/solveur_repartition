# Importation des modules
import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget, QMessageBox
from styles import global_stylesheet
from utils import *

class LevelsPage(QWidget):
    """
    Représente la page de gestion des niveaux
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
        self.levels_list = QListWidget()
        self.levels_list.itemClicked.connect(self.select_level)
        # Ajout des éléments à la partie de gauche 
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addWidget(self.modify_button)
        left_layout.addLayout(buttons_layout)
        left_layout.addWidget(self.levels_list)
        
        # Partie droite
        right_layout = QVBoxLayout()
        name_label = QLabel("Name")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")
        volume_hour_label = QLabel("Volume hour")
        self.volume_hour_input = QLineEdit()
        self.volume_hour_input.setPlaceholderText("Volume hour")
        num_groups_label = QLabel("Number groups")
        self.num_groups_input = QLineEdit()
        self.num_groups_input.setPlaceholderText("Number groups")
        max_group_teacher_label = QLabel("Max Group Teacher")
        self.max_group_teacher_input = QLineEdit()
        self.max_group_teacher_input.setPlaceholderText("Max Group Teacher")
        self.add_button = QPushButton("Add level")
        self.add_button.clicked.connect(self.add_level)
        # Ajout des éléments à la partie de droite
        right_layout.addWidget(name_label)
        right_layout.addWidget(self.name_input)
        right_layout.addWidget(volume_hour_label)
        right_layout.addWidget(self.volume_hour_input)
        right_layout.addWidget(num_groups_label)
        right_layout.addWidget(self.num_groups_input)
        right_layout.addWidget(max_group_teacher_label)
        right_layout.addWidget(self.max_group_teacher_input)
        right_layout.addWidget(self.add_button)
        
        right_layout.addStretch(1)
        
        layout.addLayout(left_layout, 1)
        layout.addLayout(right_layout, 1)
        
        self.setLayout(layout)
        self.load_levels()

        self.delete_button.clicked.connect(self.delete_level)
        self.modify_button.clicked.connect(self.modify_level)
        self.current_level = None

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
                    self.levels_list.addItem(level['name'])
            print("Log : Récupération des niveaux depuis levels_window.py")
        except FileNotFoundError:
            with open('config.json', 'w') as file:
                json.dump({"teachers": [], "levels": []}, file)

    def add_level(self):
        """
        Fonction permettant d'ajouter un niveau
        En entrée : Aucune
        En sortie : Aucune
        """
        name = self.name_input.text()
        volume_hour = self.volume_hour_input.text()
        num_groups = self.num_groups_input.text()
        max_group_teacher = self.max_group_teacher_input.text()
        
        if not name or not volume_hour or not num_groups or not max_group_teacher:
            QMessageBox.warning(self, "Erreur de saisie", "Merci de saisir tous les champs.")
            return
        
        new_level = {
            "name": name,
            "volume_hour": volume_hour,
            "num_groups": num_groups,
            "max_group_teacher": max_group_teacher
        }
        
        try:
            with open('config.json', 'r+') as file:
                config = json.load(file)
                config['levels'].append(new_level)
                file.seek(0)
                file.truncate()
                json.dump(config, file, indent=4)
                
            self.levels_list.addItem(name)
            self.clear_inputs()
            print("Log : Ajout du niveau depuis levels_window.py")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", "Une erreur est survenue lors de l'ajout du niveau")

    def select_level(self, item):
        """
        Fonction permettant de sélectionner un niveau
        En entrée : item (QListWidgetItem) : L'item sélectionné
        En sortie : Aucune
        """
        try:
            with open('config.json', 'r') as file:
                config = json.load(file)
                levels = config.get('levels', [])
                for level in levels:
                    if level['name'] == item.text():
                        self.current_level = level
                        self.name_input.setText(level['name'])
                        self.volume_hour_input.setText(level['volume_hour'])
                        self.num_groups_input.setText(level['num_groups'])
                        self.max_group_teacher_input.setText(level['max_group_teacher'])
                        break
        except Exception as e:
            QMessageBox.critical(self, "Erreur", "Une erreur est survenue lors de la sélection du niveau")

    def modify_level(self):
        """
        Fonction permettant de modifier un niveau 
        En entrée : Aucune
        En sortie : Aucune
        """
        if self.current_level is None:
            QMessageBox.warning(self, "Erreur de sélection", "Merci de saisir un niveau à modifier.")
            return
        
        new_name = self.name_input.text()
        volume_hour = self.volume_hour_input.text()
        num_groups = self.num_groups_input.text()
        max_group_teacher = self.max_group_teacher_input.text()
        
        if not new_name or not volume_hour or not num_groups or not max_group_teacher:
            QMessageBox.warning(self, "Erreur de saisie", "Merci de saisir tous les champs.")
            return
        
        try:
            with open('config.json', 'r+') as file:
                config = json.load(file)
                for level in config['levels']:
                    if level['name'] == self.current_level['name']:
                        level['name'] = new_name
                        level['volume_hour'] = volume_hour
                        level['num_groups'] = num_groups
                        level['max_group_teacher'] = max_group_teacher
                        self.current_level = level
                        break
            with open('config.json', 'w') as file:
                json.dump(config, file, indent=4)
                
            self.load_levels()
            self.clear_inputs()
            print("Log : Modification du niveau depuis levels_window.py")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", "Une erreur est survenue lors de la modification du niveau")

    def delete_level(self):
        """
        Fonction permettant de supprimer un niveau
        En entrée : Aucune
        En sortie : Aucune
        """
        if self.current_level is None:
            QMessageBox.warning(self, "Erreur de sélection", "Merci de saisir un niveau à supprimer.")
            return
        
        try:
            with open('config.json', 'r+') as file:
                config = json.load(file)
                config['levels'] = [level for level in config['levels'] if level['name'] != self.current_level['name']]
                
            with open('config.json', 'w') as file:
                json.dump(config, file, indent=4)
                
            self.load_levels()
            self.clear_inputs()
            self.current_level = None
            print("Log : Suppression du niveau depuis levels_window.py")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", "Une erreur est survenue lors de la suppression du niveau")

    def clear_inputs(self):
        """
        Fonction permettant de vider les champs de saisie
        En entrée : Aucune
        En sortie : Aucune
        """
        self.name_input.clear()
        self.volume_hour_input.clear()
        self.num_groups_input.clear()
        self.max_group_teacher_input.clear()
