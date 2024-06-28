# Importation des modules
import json
from .domain import Teacher, Level
import gurobipy as gp
from gurobipy import GRB

def solve():
    """
    Fonction permettant d'ajouter toutes les contraintes et de résoudre le problème de répartition des enseignants
    En entrée : Aucune
    En sortie : Un dictionnaire contenant la répartition des enseignants sur les différents niveaux
    """
    with open('config.json', 'r') as file:
        config = json.load(file)
    all_levels = []
    level_dict = {}
    # Récupération des niveaux
    for level_data in config['levels']:
        level = Level(
            name=level_data['name'],
            volume_hours=float(level_data['volume_hour']),
            nb_groups=int(level_data['num_groups']),
            max_group_teacher=int(level_data['max_group_teacher'])
        )
        all_levels.append(level)
        level_dict[level.name] = level
    all_teachers = []

    # Récupération des enseignants
    for teacher_data in config['teachers']:
        levels_taught = [level_dict[level] for level in teacher_data['levels']]
        teacher = Teacher(
            name=teacher_data['name'],
            min_hours_of_work=float(teacher_data['min_hour']),
            wanted_max_hours_of_work=float(teacher_data['max_hour']),
            wanted_levels_taught=levels_taught,
            minimize_hours=teacher_data.get('minimize_hours', False),
            minimize_levels=teacher_data.get('minimize_levels', False)
        )
        all_teachers.append(teacher)
    model = gp.Model("Repartition Problem")

    # Définition des variables de décision
    for teacher in all_teachers:
        for level in all_levels:
            var_name = f"{teacher.name}_{level.name}"
            teacher.repartition[level.name] = model.addVar(vtype=GRB.INTEGER, name=var_name, lb=0)

    # Ajout de la contrainte pour chaque enseignant sur le nombre d'heures de travail
    for teacher in all_teachers:
        model.addConstr(gp.quicksum(teacher.repartition[level.name] * level.volume_hours for level in teacher.wanted_levels_taught) <= teacher.wanted_max_hours_of_work, f"{teacher.name}_max")
        model.addConstr(gp.quicksum(teacher.repartition[level.name] * level.volume_hours for level in teacher.wanted_levels_taught) >= teacher.min_hours_of_work, f"{teacher.name}_min")

    # Ajout de la contrainte pour chaque enseignant sur les niveaux enseignés
    for teacher in all_teachers:
        for level in all_levels:
            if level in teacher.wanted_levels_taught:
                model.addConstr(teacher.repartition[level.name] >= 0, f"{teacher.name}_{level.name}_min")
            else:
                model.addConstr(teacher.repartition[level.name] == 0, f"{teacher.name}_{level.name}_max")

    # Ajout de la contrainte pour chaque niveau sur le nombre de groupes
    for level in all_levels:
        model.addConstr(gp.quicksum(teacher.repartition[level.name] for teacher in all_teachers) == level.nb_groups, f"total_{level.name}")

    # Ajout de la contrainte pour chaque enseignant sur le nombre de groupes maximum
    for teacher in all_teachers:
        for level_data in config['levels']:
            level = level_dict[level_data['name']]
            model.addConstr(teacher.repartition[level.name] <= int(level_data['max_group_teacher']), f"max_{level.name}_{teacher.name}")
            
    # Ajout des contraintes de niveau pour chaque enseignant (nombre minimum et maximum de groupes)
    level_constraints = config.get('level_constraints', [])
    for constraint in level_constraints:
        teacher = next(teacher for teacher in all_teachers if teacher.name == constraint['teacher'])
        levels = [level_dict[level] for level in constraint['levels']]
        min_groups = constraint['min_groups']
        max_groups = constraint['max_groups']
        model.addConstr(gp.quicksum(teacher.repartition[level.name] for level in levels) >= min_groups, f"{teacher.name}_min_groups")
        model.addConstr(gp.quicksum(teacher.repartition[level.name] for level in levels) <= max_groups, f"{teacher.name}_max_groups")

    # Ajout de la fonction objectif pour minimiser les heures et les niveaux enseignés
    objective_terms = []
    for teacher in all_teachers:
        if teacher.minimize_hours:
            objective_terms.append(gp.quicksum(teacher.repartition[level.name] * level.volume_hours for level in teacher.wanted_levels_taught))
        if teacher.minimize_levels:
            objective_terms.append(gp.quicksum(teacher.repartition[level.name] for level in teacher.wanted_levels_taught))

    model.setObjective(gp.quicksum(objective_terms), GRB.MINIMIZE)
    model.optimize()

    # Récupération des résultats
    results = {}
    for teacher in all_teachers:
        teacher_result = {
            'total_hours': sum(max(0, teacher.repartition[level.name].x) * level.volume_hours for level in teacher.wanted_levels_taught)
        }
        for level in all_levels:
            teacher_result[level.name] = max(0, teacher.repartition[level.name].x)
        results[teacher.name] = teacher_result

    return results
