# Importation des modules 
from PyQt5.QtWidgets import QMainWindow, QAction, QDesktopWidget, QWidget
from PyQt5.QtGui import QIcon
from windows.teacher_window import TeacherPage
from windows.levels_window import LevelsPage
from windows.result_window import ResultPage
from windows.levels_repartition_window import LevelsRepartitionPage
from utils import getScreenDimensions
from styles import global_stylesheet

class MainWindow(QMainWindow):
    """ 
    Représente la fenêtre principale de l'application
    """
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initMenuBar()
    
    def initUI(self):
        """
        Fonction permettant d'initialiser l'interface graphique de la page de répartition des niveaux
        En entrée : Aucune
        En sortie : Aucune
        """
        print("Initialisation des paramètres de la fenêtre principale")
        self.setWindowTitle('Solver - App')
        screen_width, screen_height = getScreenDimensions()
        self.setGeometry(0, 0, screen_width-15, screen_height)
        self.setStyleSheet(global_stylesheet.stylesheet)
        self.setWindowIcon(QIcon('./pictures/logo_app.jpg'))
    
    def initMenuBar(self):
        """
        Fonction permettant d'initialiser la barre de menu
        En entrée : Aucune
        En sortie : Aucune
        """
        print("Initialisation de la barre de menu")
        menubar = self.menuBar()
        
        # Home page
        home_action = QAction('Home', self)
        home_action.triggered.connect(self.show_home)
        menubar.addAction(home_action)
        # Levels page
        levels_action = QAction('Levels', self)
        levels_action.triggered.connect(self.show_levels)
        menubar.addAction(levels_action)
        # Teacher page
        teacher_action = QAction('Teacher', self)
        teacher_action.triggered.connect(self.show_teacher)
        menubar.addAction(teacher_action)
        # Levels repartition page
        levels_repartition_action = QAction('Levels Repartition', self)
        levels_repartition_action.triggered.connect(self.show_levels_repartition)
        menubar.addAction(levels_repartition_action)
        # Result page
        result_action = QAction('Result', self)
        result_action.triggered.connect(self.show_result)
        menubar.addAction(result_action)

        
    def show_home(self):
        """
        Fonction permettant d'afficher la page d'accueil
        En entrée : Aucune
        En sortie : Aucune
        """
        print("Page 'home' affichée")
        self.setCentralWidget(QWidget())

    def show_levels(self):
        """
        Fonction permettant d'afficher la page de répartition des niveaux
        En entrée : Aucune
        En sortie : Aucune
        """
        print("Page 'levels' affichée")
        self.levels_page = LevelsPage()
        self.setCentralWidget(self.levels_page)

    def show_teacher(self):
        """
        Fonction permettant d'afficher la page des enseignants
        En entrée : Aucune
        En sortie : Aucune
        """
        print("Page 'teacher' affichée")
        self.teacher_page = TeacherPage()
        self.setCentralWidget(self.teacher_page)

    def show_levels_repartition(self):
        """
        Fonction permettant d'afficher la page contraintes spécifiques des niveaux
        En entrée : Aucune
        En sortie : Aucune
        """
        print("Page 'levels repartition' affichée")
        self.levels_repartition_page = LevelsRepartitionPage()
        self.setCentralWidget(self.levels_repartition_page)

    def show_result(self):
        """
        Fonction permettant d'afficher la page de résultat du solveur
        En entrée : Aucune
        En sortie : Aucune
        """
        print("Page 'result' affichée")
        self.result_page = ResultPage()
        self.setCentralWidget(self.result_page)

