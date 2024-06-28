
class Teacher:
    """
    Représente un enseignant et ses contraintes
    """
    def __init__(self, name, min_hours_of_work, wanted_max_hours_of_work, wanted_levels_taught, minimize_hours=False, minimize_levels=False):
        self.name = name
        self.min_hours_of_work = min_hours_of_work
        self.wanted_max_hours_of_work = wanted_max_hours_of_work
        self.wanted_levels_taught = wanted_levels_taught
        self.minimize_hours = minimize_hours
        self.minimize_levels = minimize_levels

        self.repartition = {}

class Level:
    """
    Représente un niveau et ses contraintes
    """
    def __init__(self, name, volume_hours, nb_groups, max_group_teacher):
        self.name = name
        self.volume_hours = volume_hours
        self.nb_groups = nb_groups
        self.max_group_teacher = max_group_teacher
