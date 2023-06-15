#!/usr/bin/env python
# coding: utf-8

# In[7]:


from pulp import LpVariable, LpProblem, LpMaximize, LpStatus, value, LpMinimize
# Holdings
hUSD = 2000000
hEUR = 5000000
hGBP = 1000000
hHKD = 3000000
hJPY = 30000000

# Transaction Rates (to USD)
r1 = 1.5593    # GBP to USD
r2 = 0.12812   # HKD to USD
r3 = 0.00843   # JPY to USD
r4 = 0.9724    # EUR to USD

# Transaction Costs (Parameters)
c1 = 0.00947446
c2 = 0.01917605
c3 = 0.00176192
c4 = 0.0006235
c5 = 0.001162
c6 = 0.0063871

# declare your variables
x1 = LpVariable("x1", 0, None) # USD for EUR
x2 = LpVariable("x2", 0, None) # GBP for EUR
x3 = LpVariable("x3", 0, None) # HKD for EUR
x4 = LpVariable("x4", 0, None) # USD for JPY
x5 = LpVariable("x5", 0, None) # GBP for JPY
x6 = LpVariable("x6", 0, None) # HKD for JPY

# defines the problem
prob = LpProblem("problem", LpMinimize)

# defines the constraints
prob += hUSD - (x1 + x4) >= 250000
prob += hGBP*r1 - (x2 + x5) >= 250000
prob += hHKD*r2 - (x3 + x6) >= 250000
prob += hJPY*r3 + (x1 + x2 + x3) >= 54000000*r3
prob += hEUR*r4 + (x4 + x5 + x6) >= 8000000*r4


# defines the objective function to maximize
prob += c1*x1 + c2*x2 + c3*x3 + c4*x4 + c5*x5 + c6*x6

# solve the problem
status = prob.solve()
LpStatus[status]

print(prob)

# print the results
print("Pulp Solution for Baldwin Enterprise Foreign Currency Exchange:\n")
print("x1:", value(x1))
print("x2:", value(x2))
print("x3:", value(x3))
print("x4:", value(x4))
print("x5:", value(x5))
print("x6:", value(x6))
print("Minimized Costs in US Dollars:", c1*value(x1) + c2*value(x2) + c3*value(x3) + c4*value(x4) + c5*value(x5) + c6*value(x6))


# In[8]:


from pulp import LpVariable, LpProblem, LpMaximize, LpStatus, value, LpMinimize
# Holdings
hUSD = 2000000
hEUR = 5000000
hGBP = 1000000
hHKD = 3000000
hJPY = 30000000

# Transaction Rates (to USD)
r1 = 1.5593    # GBP to USD
r2 = 0.12812   # HKD to USD
r3 = 0.00843   # JPY to USD
r4 = 0.9724    # EUR to USD

# Transaction Costs (Parameters)
c1 = 0.00947446
c2 = 0.01917605
c3 = 0.00176192
c4 = 0.0006235
c5 = 0.001162
c6 = 0.0063871

# declare your variables
x1 = LpVariable("x1", 0, None) # USD for EUR
x2 = LpVariable("x2", 0, None) # GBP for EUR
x3 = LpVariable("x3", 0, None) # HKD for EUR
x4 = LpVariable("x4", 0, None) # USD for JPY
x5 = LpVariable("x5", 0, None) # GBP for JPY
x6 = LpVariable("x6", 0, None) # HKD for JPY

# defines the problem
prob = LpProblem("problem", LpMinimize)

# defines the constraints
prob += hUSD - (x1 + x4) >= 50000
prob += hGBP*r1 - (x2 + x5) >= 50000
prob += hHKD*r2 - (x3 + x6) >= 50000
prob += hJPY*r3 + (x1 + x2 + x3) >= 54000000*r3
prob += hEUR*r4 + (x4 + x5 + x6) >= 8000000*r4


# defines the objective function to maximize
prob += c1*x1 + c2*x2 + c3*x3 + c4*x4 + c5*x5 + c6*x6

# solve the problem
status = prob.solve()
LpStatus[status]

print(prob)

# print the results
print("Pulp Solution for Baldwin Enterprise Foreign Currency Exchange:\n")
print("x1:", value(x1))
print("x2:", value(x2))
print("x3:", value(x3))
print("x4:", value(x4))
print("x5:", value(x5))
print("x6:", value(x6))
print("Minimized Costs in US Dollars:", c1*value(x1) + c2*value(x2) + c3*value(x3) + c4*value(x4) + c5*value(x5) + c6*value(x6))

