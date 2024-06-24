# Class file for the domain layer
# Author: Francky

# class Teacher describing some teachers characteristics: min_hours_of_work, max_hours_of_work, levels_taught, and the number of levels taught, a repartition as a map where keys are the levels and values are the number of class taught for each level
class Teacher:
    def __init__(self, name, min_hours_of_work, wanted_max_hours_of_work, wanted_levels_taught):
        self.name = name
        self.min_hours_of_work = min_hours_of_work
        self.max_hours_of_work = wanted_max_hours_of_work
        self.wanted_levels_taught = wanted_levels_taught
        self.nb_levels_taught = len(wanted_levels_taught)
        self.repartition = {
            level.name: 0 for level in all_levels
        }

        

# Enumeration of possible levels: 6_eme, 5_eme, 4_eme, 3_eme. Each level is characterized by a name and a volume of hours
class Level:
    def __init__(self, name, volume_hours, nb_groups=1):
        self.name = name
        self.volume_hours = volume_hours
        self.nb_groups = nb_groups


# Creation of the levels as constants
sixieme = Level("6_eme", 4.5, 7)
cinquieme = Level("5_eme", 3.5, 9)
quatrieme =  Level("4_eme", 3.5, 6)
troisieme = Level("3_eme", 4, 5)

all_levels = [sixieme, cinquieme, quatrieme, troisieme]

