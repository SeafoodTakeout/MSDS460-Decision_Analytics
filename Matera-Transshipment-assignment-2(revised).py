# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 16:40:17 2022

@author: 16095
"""

# to explore alternative levels of demand by customers
# select an integer value for the demand multiplier
demand_multiplier = 4.7  # default is 1   

import regex as re # regular expresstions used in manipulating output for reporting solution
import pulp # mathematical programming
prob = pulp.LpProblem("Distribution_1", pulp.LpMinimize)
solver = pulp.getSolver("PULP_CBC_CMD") 

# report the solver being used
print()
print("Solver settings for this problem:")
print(solver.toDict())
print()

# Names for Breweries
brewery = ["b1", "b2", "b3", "b4"]

# Dictionary for maximumn units/capacity
brewery_maximum = {"b1": 2000,
                   "b2": 2500,
                   "b3": 3500,
                   "b4": 2000}

# Dictionary for minimum units/capacity
brewery_minimum = {"b1": 100,
                   "b2": 150,
                   "b3": 200,
                   "b4": 100}

# Names for Packaging Facilities
packaging = ["p1", "p2", "p3"]

# Dictionary for maximum number of units packaging facilities
packaging_maximum = {"p1": 500,
                     "p2": 1500,
                     "p3": 2500}

# Dictionary for minimum number of units packaging facilities
packaging_minimum = {"p1": 50,
                     "p2": 100,
                     "p3": 150}

# Names of Demand Points
demand_point = ["d1", "d2", "d3", "d4", "d5", "d6",
          "d7", "d8", "d9", "d10", "d11", "d12",
          "d13", "d14", "d15"]

# Dictionary for aggregate demand at each demand point in tons
demand_input = {"d1": 48, "d2": 84, "d3": 64, 
               "d4": 106, "d5": 47, "d6": 57, 
               "d7": 64, "d8": 93, "d9": 74, 
               "d10": 41, "d11": 61, "d12": 42,
               "d13": 57, "d14": 70, "d15": 41,}

# use demand_multiplier to increase demand
demand = demand_input # dictionary with the same structure as base demend
for key in list(demand_input.keys()):
    demand[key] = demand_multiplier * demand_input[key]
    
d1_demand = demand['d1'] 
d2_demand = demand['d2'] 
d3_demand = demand['d3'] 
d4_demand = demand['d4'] 
d5_demand = demand['d5'] 
d6_demand = demand['d6'] 
d7_demand = demand['d7'] 
d8_demand = demand['d8'] 
d9_demand = demand['d9'] 
d10_demand = demand['d10'] 
d11_demand = demand['d11'] 
d12_demand = demand['d12'] 
d13_demand = demand['d13'] 
d14_demand = demand['d14'] 
d15_demand = demand['d15']      
    
total_demand = sum(demand.values())

# Create a list of costs of transportation paths 
# between breweries and packaging facilities
# for routes not possible set cost to 9999
brewery_to_packaging_shipping_costs = [
      
         [1.55,0.51,0.9],
         [0.81,3.18,0.65],
         [2.13,0.97,0.51],
         [1.23,2.15,2.08]
         ]

# Create another list of transportation costs
# This one is between packaging facilities to demand points
# for routes not possible set cost to 9999
packaging_to_demand_shipping_costs = [
    [4.82,  2.05, 4.42, 3.83, 0.97, 3.04, 3.91, 4.03, 5.11, 0.90, 4.39, 0.85, 2.81, 3.94, 1.04], # "Newcastle"
    [1.83,  4.03, 3.95, 4.21, 4.78, 3.20, 1.88, 2.96, 5.11, 2.67, 4.14, 1.22, 5.10, 3.47, 1.92], # "Birmingham"
    [2.66,  0.95, 3.94, 2.04, 2.35, 1.42, 3.60, 3.17, 1.34, 4.51, 0.74, 0.94, 1.98, 4.77, 2.04], # "London"
    ]

# The cost data are made into dictionaries
first_costs = pulp.makeDict([brewery,packaging],brewery_to_packaging_shipping_costs,0)
second_costs = pulp.makeDict([packaging,demand_point],packaging_to_demand_shipping_costs,0)

# Create the 'prob' variable to contain the problem data
prob = pulp.LpProblem("Distribution_1",pulp.LpMinimize)

# Create list of tuples containing all the possible brewery-to-packaging routes for transport
first_routes = [(i,j) for i in brewery for j in packaging]
# A dictionary called 'Vars' is created to contain the referenced variables(the routes)
first_vars = pulp.LpVariable.dicts("route",(brewery,packaging),0,None,pulp.LpInteger)

# Create list of tuples containing all the possible packaging-to-demand points for transport
second_routes = [(j,k) for j in packaging for k in demand_point]
# A dictionary called 'Vars' is created to contain the referenced variables(the routes)
second_vars = pulp.LpVariable.dicts("route",(packaging,demand_point),0,None,pulp.LpInteger)

# brewery constaints for maxiumum production
for i in brewery:
    prob += (pulp.lpSum([first_vars[i][j] for j in packaging])) <= brewery_maximum[i], "Brewery_Maximum_Capacity%s"%i
    
for i in brewery:
    prob += (pulp.lpSum([first_vars[i][j] for j in packaging])) >= brewery_minimum[i], "Brewery_Minimum_Capacity%s"%i
    
# quantities into packaging    
for j in packaging:
    prob += pulp.lpSum([first_vars[i][j] for i in brewery]) <= packaging_maximum[j], "Packaging_Maximum_Capacity%s"%j
        
for j in packaging:
    prob += pulp.lpSum([first_vars[i][j] for i in brewery]) >= packaging_minimum[j], "Packaging_Minimum_Capacity%s"%j
    
# must satisfy the orders placed by demand points
# using shipments from packaging facilities
for k in demand_point:
    prob += pulp.lpSum([second_vars[j][k] for j in packaging]) >= demand[k], "Meet_or_exceed_demand_input%s"%k

# packaging input must be equal to packaging output in this problem
# in other problems, it may be OK to hold inventory at a packaging or distribution facility
for j in packaging:
   prob += pulp.lpSum([first_vars[i][j] for i in brewery]) == pulp.lpSum([second_vars[j][k] for k in demand_point]), "Packaging_in_out%s"%j
    
# total brewery output should exceed total demand

# set selected decision variables to zero to accommodate explicit constraints  
# brewery-to-packaging
prob += pulp.LpVariable("route_b1_p1", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_b1_p2", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_b1_p3", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_b2_p1", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_b2_p2", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_b2_p3", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_b3_p1", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_b3_p2", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_b3_p3", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_b4_p1", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_b4_p2", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_b4_p3", lowBound=0, upBound=0, cat = 'Integer')
# packaging 1 to demand points
prob += pulp.LpVariable("route_p1_d1", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p1_d2", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p1_d3", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p1_d4", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p1_d5", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p1_d6", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p1_d7", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p1_d8", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p1_d9", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p1_d10", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p1_d11", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p1_d12", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p1_d13", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p1_d14", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p1_d15", lowBound=0, upBound=0, cat = 'Integer')
# packaging 2 to demand points
prob += pulp.LpVariable("route_p2_d1", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p2_d2", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p2_d3", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p2_d4", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p2_d5", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p2_d6", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p2_d7", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p2_d8", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p2_d9", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p2_d10", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p2_d11", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p2_d12", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p2_d13", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p2_d14", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p2_d15", lowBound=0, upBound=0, cat = 'Integer')
# packaging 2 to demand points
prob += pulp.LpVariable("route_p3_d1", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p3_d2", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p3_d3", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p3_d4", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p3_d5", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p3_d6", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p3_d7", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p3_d8", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p3_d9", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p3_d10", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p3_d11", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p3_d12", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p3_d13", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p3_d14", lowBound=0, upBound=0, cat = 'Integer')
prob += pulp.LpVariable("route_p3_d15", lowBound=0, upBound=0, cat = 'Integer')

# The objective function for all transportation costs
prob += pulp.lpSum([first_vars[i][j]*first_costs[i][j] for (i,j) in first_routes]) + pulp.lpSum([second_vars[j][k]*second_costs[j][k] for (j,k) in second_routes]), "All_Tansportation_Costs"

# solve the linear programming problem
# as this is a transshipment problem, we expect integer decision variable values
prob.solve()

# The status of the solution is printed to the screen
print("Status:", pulp.LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimal value
for v in prob.variables():
    print(v.name, "=", round(v.varValue))

# Sum across route variables to obtain brewery totals
b1_output = 0
b2_output = 0
b3_output = 0
b4_output = 0

# Sum across route variables to obtain packaging totals
p1_output = 0
p2_output = 0
p3_output = 0

# Sum across route variables to obtain demand point totals
d1_input = 0
d2_input = 0
d3_input = 0
d4_input = 0
d5_input = 0
d6_input = 0
d7_input = 0
d8_input = 0
d9_input = 0
d10_input = 0 
d11_input = 0 
d12_input = 0
d13_input = 0 
d14_input = 0 
d15_input = 0

for v in prob.variables():
    if re.search("route_b1_..",v.name):
        b1_output += round(v.varValue)
    if re.search("route_b2_..",v.name):
        b2_output += round(v.varValue)
    if re.search("route_b3_..",v.name):
        b3_output += round(v.varValue)
    if re.search("route_b4_..",v.name):
        b4_output += round(v.varValue)            
        
    if re.search("route_p1_..",v.name):
        p1_output += round(v.varValue)     
    if re.search("route_p2_..",v.name):
        p2_output += round(v.varValue)
    if re.search("route_p3_..",v.name):
        p3_output += round(v.varValue)  
        
    if re.search("_d1",v.name):
        d1_input += round(v.varValue)  
    if re.search("_d2",v.name):
        d2_input += round(v.varValue)  
    if re.search("_d3",v.name):
        d3_input += round(v.varValue)  
    if re.search("_d4",v.name):
        d4_input += round(v.varValue)  
    if re.search("_d5",v.name):
        d5_input += round(v.varValue)  
    if re.search("_d6",v.name):
        d6_input += round(v.varValue) 
    if re.search("_d7",v.name):
        d7_input += round(v.varValue)  
    if re.search("_d8",v.name):
        d8_input += round(v.varValue)  
    if re.search("_d9",v.name):
        d9_input += round(v.varValue)  
    if re.search("_d10",v.name):
        d10_input += round(v.varValue)  
    if re.search("_d11",v.name):
        d11_input += round(v.varValue)  
    if re.search("_d12",v.name):
        d12_input += round(v.varValue)  
    if re.search("_d13",v.name):
        d13_input += round(v.varValue)  
    if re.search("_d14",v.name):
        d14_input += round(v.varValue)  
    if re.search("_d15",v.name):
        d15_input += round(v.varValue)  

total_brewery_output = b1_output + b2_output + b3_output + b4_output  
total_packaging_output = p1_output + p2_output + p3_output 
total_demand_point_input = d1_input + d2_input + d3_input + d4_input + d5_input + d6_input + d7_input + d8_input + d9_input + d10_input + d11_input + d12_input + d13_input + d14_input + d15_input

print()
print("b1_output:",b1_output)     
print("b2_output:",b2_output)
print("b3_output:",b3_output)     
print("b4_output:",b4_output)  
print("total_brewery_output:", total_brewery_output) 

print()
print("p1_output:",p1_output)  
print("p2_output:",p2_output) 
print("p3_output:",p3_output)  
print("total_packaging_output:", total_packaging_output)

print()
print("total demand in problem set-up:", total_demand)
if (total_demand_point_input < total_demand):
    print("customer demand requirements not met")
if (total_demand_point_input >= total_demand):
    print("customer demand requirements met")
print("d1_demand:", d1_demand, "d1_input:",d1_input) 
print("d2_demand:", d2_demand, "d2_input:",d2_input) 
print("d3_demand:", d3_demand, "d3_input:",d3_input) 
print("d4_demand:", d4_demand, "d4_input:",d4_input) 
print("d5_demand:", d5_demand, "d5_input:",d5_input) 
print("d6_demand:", d6_demand, "d6_input:",d6_input)
print("d7_demand:", d7_demand, "d7_input:",d7_input) 
print("d8_demand:", d8_demand, "d8_input:",d8_input) 
print("d9_demand:", d9_demand, "d9_input:",d9_input) 
print("d10_demand:", d10_demand, "d10_input:",d10_input) 
print("d11_demand:", d11_demand, "d11_input:",d11_input) 
print("d12_demand:", d12_demand, "d12_input:",d12_input)  
print("d13_demand:", d13_demand, "d13_input:",d13_input) 
print("d14_demand:", d14_demand, "d14_input:",d14_input) 
print("d15_demand:", d15_demand, "d15_input:",d15_input)    
print("total demand point input:", total_demand_point_input)
    
print()
# The optimised objective function value is printed to the screen    
print("Total Cost of Transportation = ", round(pulp.value(prob.objective)))

