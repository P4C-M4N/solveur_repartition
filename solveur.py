import gurobipy as gp
from gurobipy import GRB
import pandas as pd

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

# Initialize the model
model = gp.Model("Repartition Problem")

# Define the variables
variables = {}
k_variables = {}
prefixes = ['fred', 'TP1', 'TP2', 'TP3', 'TP4', 'BMP']
levels = ['6eme', '5eme', '4eme', '3eme']

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
model.addConstr(gp.quicksum(k_variables[f"k_{prefix}_6eme"] for prefix in prefixes) == 7, f"total_6eme")
model.addConstr(gp.quicksum(k_variables[f"k_{prefix}_5eme"] for prefix in prefixes) == 9, f"total_5eme")
model.addConstr(gp.quicksum(k_variables[f"k_{prefix}_4eme"] for prefix in prefixes) == 6, f"total_4eme")
model.addConstr(gp.quicksum(k_variables[f"k_{prefix}_3eme"] for prefix in prefixes) == 5, f"total_3eme")



# Add constraints for maximum k variables in 6eme and 5eme
for prefix in prefixes:
    model.addConstr(k_variables[f"k_{prefix}_6eme"] <= 2, f"max_6eme_{prefix}")
    model.addConstr(k_variables[f"k_{prefix}_5eme"] <= 2, f"max_5eme_{prefix}")

# Define maximum and minimum hours constraints for each prefix
model.addConstr(gp.quicksum(variables[f"fred_{level}"] for level in levels) <= 17, "fred_max")
model.addConstr(gp.quicksum(variables[f"fred_{level}"] for level in levels) >= 15, "fred_min")

for prefix in ['TP1', 'TP2', 'TP3', 'TP4']:
    model.addConstr(gp.quicksum(variables[f"{prefix}_{level}"] for level in levels) <= 20, f"{prefix}_max")
    model.addConstr(gp.quicksum(variables[f"{prefix}_{level}"] for level in levels) >= 18, f"{prefix}_min")

model.addConstr(k_variables[f"k_BMP_3eme"] == 0, "BMP_3eme_NO")
model.addConstr(k_variables[f"k_BMP_4eme"] == 0, "BMP_3eme_NO")
model.addConstr(k_variables[f"k_BMP_5eme"]+k_variables[f"k_BMP_6eme"] == 3, "BMP_5eme_6eme")

# Define binary variables to indicate if TP2 teaches at a level
binary_FRED = {level: model.addVar(vtype=GRB.BINARY, name=f"binary_FRED_{level}") for level in levels}

# Link binary variables with the actual teaching hours
for level in levels:
    model.addConstr(k_variables[f"k_fred_{level}"] <= 4 * binary_FRED[level], f"link_FRED_{level}")

# Ensure TP2 teaches at exactly two levels
model.addConstr(gp.quicksum(binary_FRED[level] for level in levels) == 2, "FRED_two_levels")

model.addConstr(k_variables[f"k_fred_3eme"] >= 1, "fred 3eme oui")

# Define binary variables to indicate if TP2 teaches at a level
binary_TP2 = {level: model.addVar(vtype=GRB.BINARY, name=f"binary_TP2_{level}") for level in levels}

# Link binary variables with the actual teaching hours
for level in levels:
    model.addConstr(k_variables[f"k_TP2_{level}"] <= 5 * binary_TP2[level], f"link_TP2_{level}")

# Ensure TP2 teaches at exactly two levels
model.addConstr(gp.quicksum(binary_TP2[level] for level in levels) == 2, "TP2_two_levels")

# Define binary variables to indicate if TP3 teaches at a level
binary_TP3 = {level: model.addVar(vtype=GRB.BINARY, name=f"binary_TP3_{level}") for level in levels}

# Link binary variables with the actual teaching hours
for level in levels:
    model.addConstr(k_variables[f"k_TP3_{level}"] <= 5 * binary_TP3[level], f"link_TP3_{level}")

# Ensure TP3 teaches at exactly two levels
model.addConstr(gp.quicksum(binary_TP3[level] for level in levels) == 2, "TP3_two_levels")

# # Define binary variables to indicate if TP4 teaches at a level
# binary_TP4 = {level: model.addVar(vtype=GRB.BINARY, name=f"binary_TP4_{level}") for level in levels}

# # Link binary variables with the actual teaching hours
# for level in levels:
#     model.addConstr(k_variables[f"k_TP4_{level}"] <= 5 * binary_TP4[level], f"link_TP4_{level}")

# # Ensure TP4 teaches at exactly two levels
# model.addConstr(gp.quicksum(binary_TP4[level] for level in levels) == 2, "TP4_two_levels")


model.addConstr(k_variables[f"k_TP4_4eme"] == 1, "TP4 3eme oui")




# Define the objective function (minimization of the sum of TP variables)
objective = gp.quicksum(variables[var] for var in variables if "TP" in var and "TP1" not in var)
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
