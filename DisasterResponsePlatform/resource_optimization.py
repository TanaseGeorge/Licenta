from pulp import LpMinimize, LpProblem, LpVariable, lpSum, value
import MySQLdb

db = MySQLdb.connect(host="localhost", user="root", passwd="Sqluser1", db="disaster_response")
cursor = db.cursor()

cursor.execute("SELECT id, type, quantity, lat, lon FROM resources")
resources_data = cursor.fetchall()

cursor.execute("SELECT id, lat, lon FROM incidents")
incidents_data = cursor.fetchall()

prob = LpProblem("Resource_Optimization", LpMinimize)

routes = [(r[0], i[0]) for r in resources_data for i in incidents_data]
route_vars = LpVariable.dicts("Route", routes, lowBound=0, cat='Continuous')

total_transport_cost = lpSum([route_vars[(r[0], i[0])] * (abs(r[3]-i[1]) + abs(r[4]-i[2])) for r in resources_data for i in incidents_data])
prob += total_transport_cost

for r in resources_data:
    supply_constraint = lpSum([route_vars[(r[0], i[0])] for i in incidents_data]) <= r[2]
    prob += supply_constraint, f"Supply_Constraint_{r[0]}"

for i in incidents_data:
    demand_constraint = lpSum([route_vars[(r[0], i[0])] for r in resources_data]) >= 1
    prob += demand_constraint, f"Demand_Constraint_{i[0]}"

prob.solve()

print("Optimal Allocation and Routing Plan for Resources:")
for r in resources_data:
    for i in incidents_data:
        if route_vars[(r[0], i[0])].varValue > 0:
            print(f"Resource {r[1]} (ID: {r[0]}) -> Incident {i[0]}: {route_vars[(r[0], i[0])].varValue} units")

print("\nTotal Transportation Cost:", value(prob.objective))

db.close()
