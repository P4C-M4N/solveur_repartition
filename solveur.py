import gurobipy as gp
from gurobipy import GRB
import pandas as pd

prefixes = ['fred', 'mary', 'myriame', 'sandra', 'jerome', 'BMP']
levels = ['6eme', '5eme', '4eme', '3eme']

# Define the number of hours for each level
nbH = {
    '6eme': 31.5,
    '5eme': 31.5,
    '4eme': 21,
    '3eme': 20
}

# Define the volume hours for each level
vol_h = {
    '6eme': 4.5,
    '5eme': 3.5,
    '4eme': 3.5,
    '3eme': 4
}

bmp_nb_grp = 3
bmp_levels_allow = ['6eme', '5eme']

bmp_levels_forbidden = [level for level in levels if level not in bmp_levels_allow]

# Initialize the model
model = gp.Model("Repartition Problem")

# Define the variables
variables = {}
k_variables = {}


for prefix in prefixes:
    for level in levels:
        var_name = f"{prefix}_{level}"
        k_var_name = f"k_{var_name}"
        variables[var_name] = model.addVar(vtype=GRB.CONTINUOUS, name=var_name, lb=0)
        k_variables[k_var_name] = model.addVar(vtype=GRB.INTEGER, name=k_var_name, lb=0)

# Add constraints for each prefix and level based on volume hours
for prefix in prefixes:
    for level in levels:
        var_name = f"{prefix}_{level}"
        k_var_name = f"k_{var_name}"
        model.addConstr(variables[var_name] == k_variables[k_var_name] * vol_h[level], var_name)

# # Add constraints for total hours per level
model.addConstr(gp.quicksum(k_variables[f"k_{prefix}_6eme"] for prefix in prefixes) == nbH['6eme']/vol_h['6eme'], f"total_6eme")
model.addConstr(gp.quicksum(k_variables[f"k_{prefix}_5eme"] for prefix in prefixes) == nbH['5eme']/vol_h['5eme'], f"total_5eme")
model.addConstr(gp.quicksum(k_variables[f"k_{prefix}_4eme"] for prefix in prefixes) == nbH['4eme']/vol_h['4eme'], f"total_4eme")
model.addConstr(gp.quicksum(k_variables[f"k_{prefix}_3eme"] for prefix in prefixes) == nbH['3eme']/vol_h['3eme'], f"total_3eme")



# Add constraints for maximum k variables in 6eme and 5eme
for prefix in prefixes:
    model.addConstr(k_variables[f"k_{prefix}_6eme"] <= 2, f"max_6eme_{prefix}")
    model.addConstr(k_variables[f"k_{prefix}_5eme"] <= 2, f"max_5eme_{prefix}")

# Define maximum and minimum hours constraints for each professor

# Fred
model.addConstr(gp.quicksum(variables[f"fred_{level}"] for level in levels) <= 17, "fred_max")
model.addConstr(gp.quicksum(variables[f"fred_{level}"] for level in levels) >= 15, "fred_min")
model.addConstr(k_variables[f"k_fred_3eme"] >= 1, "fred 3eme yes")

# Mary
model.addConstr(gp.quicksum(variables[f"mary_{level}"] for level in levels) <= 20, "mary_max")
model.addConstr(gp.quicksum(variables[f"mary_{level}"] for level in levels) >= 18, "mary_min")

# Myriame
model.addConstr(gp.quicksum(variables[f"myriame_{level}"] for level in levels) <= 20, "myriame_max")
model.addConstr(gp.quicksum(variables[f"myriame_{level}"] for level in levels) >= 18, "myriame_min")
model.addConstr(k_variables[f"k_myriame_3eme"] == 0, "myriame 3eme no")

# Sandra
model.addConstr(gp.quicksum(variables[f"sandra_{level}"] for level in levels) <= 20, "sandra_max")
model.addConstr(gp.quicksum(variables[f"sandra_{level}"] for level in levels) >= 18, "sandra_min")

# Jerome
model.addConstr(gp.quicksum(variables[f"jerome_{level}"] for level in levels) <= 20, "jerome_max")
model.addConstr(gp.quicksum(variables[f"jerome_{level}"] for level in levels) >= 18, "jerome_min")

# BMP
for level in bmp_levels_forbidden:
    model.addConstr(k_variables[f"k_BMP_{level}"] == 0, f"BMP_{level}_no")
model.addConstr(gp.quicksum(k_variables[f"k_BMP_{level}"] for level in levels) == bmp_nb_grp, "BMP_contrainte_nb_grp")






# Define binary variables to indicate if professors teaches at a level
binary_fred = {level: model.addVar(vtype=GRB.BINARY, name=f"binary_fred_{level}") for level in levels}
binary_mary = {level: model.addVar(vtype=GRB.BINARY, name=f"binary_mary_{level}") for level in levels}
binary_myriame = {level: model.addVar(vtype=GRB.BINARY, name=f"binary_myriame_{level}") for level in levels}
binary_sandra = {level: model.addVar(vtype=GRB.BINARY, name=f"binary_sandra_{level}") for level in levels}
binary_jerome = {level: model.addVar(vtype=GRB.BINARY, name=f"binary_jerome_{level}") for level in levels}
binary_BMP = {level: model.addVar(vtype=GRB.BINARY, name=f"binary_BMP_{level}") for level in levels}

# Link binary variables with the actual teaching hours
for level in levels:
    model.addConstr(k_variables[f"k_fred_{level}"] <= 100 * binary_fred[level], f"link_fred_{level}")
    model.addConstr(k_variables[f"k_fred_{level}"] >= 0.1 * binary_fred[level], f"link_fred_{level}")

    model.addConstr(k_variables[f"k_mary_{level}"] <= 100 * binary_mary[level], f"link_mary_{level}")
    model.addConstr(k_variables[f"k_mary_{level}"] >= 0.1 * binary_mary[level], f"link_mary_{level}")

    model.addConstr(k_variables[f"k_myriame_{level}"] <= 100 * binary_myriame[level], f"link_myriame_{level}")
    model.addConstr(k_variables[f"k_myriame_{level}"] >= 0.1 * binary_myriame[level], f"link_myriame_{level}")

    model.addConstr(k_variables[f"k_sandra_{level}"] <= 100 * binary_sandra[level], f"link_sandra_{level}")
    model.addConstr(k_variables[f"k_sandra_{level}"] >= 0.1 * binary_sandra[level], f"link_sandra_{level}")

    model.addConstr(k_variables[f"k_jerome_{level}"] <= 100 * binary_jerome[level], f"link_jerome_{level}")
    model.addConstr(k_variables[f"k_jerome_{level}"] >= 0.1 * binary_jerome[level], f"link_jerome_{level}")

    model.addConstr(k_variables[f"k_BMP_{level}"] <= 100 * binary_BMP[level], f"link_BMP_{level}")
    model.addConstr(k_variables[f"k_BMP_{level}"] >= 0.1 * binary_BMP[level], f"link_BMP_{level}")

# Setup level constraints
model.addConstr(gp.quicksum(binary_fred[level] for level in levels) == 2, "fred_levels")
model.addConstr(gp.quicksum(binary_mary[level] for level in levels) <= 3, "mary_levels")
model.addConstr(gp.quicksum(binary_myriame[level] for level in levels) <= 3, "myriame_levels")
model.addConstr(gp.quicksum(binary_sandra[level] for level in levels) <= 3, "sandra_levels")
#model.addConstr(gp.quicksum(binary_jerome[level] for level in levels) == 2, "jerome_levels")
#model.addConstr(gp.quicksum(binary_BMP[level] for level in levels) <= 2, "BMP_levels")



# Define the objective function (minimization of the sum of TP variables)
prefixes_to_minimize = ['mary', 'myriame', 'jerome']

objective = gp.quicksum(variables[f"{prefix}_{level}"] for prefix in prefixes_to_minimize for level in levels)
model.setObjective(objective, GRB.MINIMIZE)

# Optimize the model
model.optimize()


# Check if the optimization was successful
if model.Status == GRB.OPTIMAL:
    # Create a dictionary to hold the results
    results = {prefix: {level: 0 for level in levels} for prefix in prefixes}

    # Store the values in the dictionary
    for v in model.getVars():
        if v.VarName.startswith('k_'):
            prefix, level = v.VarName.split('_')[1:]
            results[prefix][level] = v.X

    # Create a DataFrame from the dictionary
    df = pd.DataFrame(results).T

    # Calculate the total hours for each professor
    df['Total'] = sum(df[level] * vol_h[level] for level in levels)

    # Print the DataFrame
    print(df)
else:
    print(f"Optimization was unsuccessful. Status: {model.Status}")
