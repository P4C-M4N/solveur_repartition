from domain.domain import sixieme, cinquieme, quatrieme, troisieme, all_levels, Teacher
import gurobipy as gp
from gurobipy import GRB


# Creation of the  teachers
fred = Teacher("fred",15, 17, [sixieme, troisieme])
sandra = Teacher("sandra", 18, 20, [sixieme, cinquieme, troisieme])
jerome = Teacher("jerome", 18, 20, [sixieme, cinquieme, quatrieme, troisieme])
myriam = Teacher("myriam", 18, 20, [sixieme, cinquieme, quatrieme])
mary = Teacher("mary", 18, 20, [sixieme, cinquieme, troisieme])
bmp = Teacher("bmp", 7, 13, [cinquieme, quatrieme])

all_teachers = [fred, sandra, jerome, myriam, mary, bmp]

# Initialize the model
model = gp.Model("Repartition Problem")

# Define the variables of the model
# for all teachers, all levels, the repartition for the current level is a variable added to the model
for teacher in all_teachers:
    for level in all_levels:
        var_name = f"{teacher.name}_{level.name}"
        teacher.repartition[level.name] = model.addVar(vtype=GRB.INTEGER, name=var_name, lb=0)

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

# Add constraints for the maximum number of groups in 6eme and 5eme: a teacher can teach at most 2 groups in 6eme and 5eme
for teacher in all_teachers:
    model.addConstr(teacher.repartition[sixieme.name] <= 2, f"max_6eme_{teacher.name}")
    model.addConstr(teacher.repartition[cinquieme.name] <= 2, f"max_5eme_{teacher.name}")

# Found all the solutions
model.optimize()

# Print all the solutions: for each teacher and each level, print the number of classes taught and 
# for each teacher the total of hours taught
for teacher in all_teachers:
    print(f"Teacher {teacher.name}")
    for level in all_levels:
        print(f"Level {level.name}: {teacher.repartition[level.name].x}")
    print(f"Total hours: {sum(teacher.repartition[level.name].x * level.volume_hours for level in teacher.wanted_levels_taught)}")
    print()

