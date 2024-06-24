from domain.domain import sixieme, cinquieme, quatrieme, troisieme, all_levels, Teacher
import gurobipy as gp
from gurobipy import GRB


# Creation of the  teachers
fred = Teacher(15, 17, [sixieme, troisieme])
sandra = Teacher(18, 20, [sixieme, cinquieme, troisieme])
jerome = Teacher(18, 18.5, [sixieme, cinquieme, quatrieme, troisieme])
myriam = Teacher(18, 20, [sixieme, cinquieme, quatrieme])
mary = Teacher(18, 19, [sixieme, cinquieme, troisieme])
bmp = Teacher(7, 13, [cinquieme, quatrieme])

all_teachers = [fred, sandra, jerome, myriam, mary, bmp]

# Initialize the model
model = gp.Model("Repartition Problem")

# Define the variables of the model
# for all teachers, all levels, the repartition for the current level is a variable added to the model
for teacher in all_teachers:
    for level in all_levels:
        var_name = f"{teacher.name}_{level.name}"
        teacher.repartition[level.name] = model.addVar(vtype=GRB.CONTINUOUS, name=var_name, lb=0)

# Add constraints for each teacher based on the number of hours taught
for teacher in all_teachers:
    model.addConstr(gp.quicksum(teacher.repartition[level.name] * level.volume_hours for level in teacher.wanted_levels_taught) <= teacher.max_hours_of_work, f"{teacher.name}_max")
    model.addConstr(gp.quicksum(teacher.repartition[level.name] * level.volume_hours for level in teacher.wanted_levels_taught) >= teacher.min_hours_of_work, f"{teacher.name}_min")

# Add constraints for each teacher based on the wanted levels taught
for teacher in all_teachers:
    for level in all_levels:
        if level in teacher.wanted_levels_taught:
            model.addConstr(teacher.repartition[level.name] >= 0, f"{teacher.name}_{level.name}_min")
        else:
            model.addConstr(teacher.repartition[level.name] == 0, f"{teacher.name}_{level.name}_max")

# Add constraints for the total number of groups per level
for level in all_levels:
    model.addConstr(gp.quicksum(teacher.repartition[level.name] for teacher in all_teachers) == level.nb_groups, f"total_{level.name}")

