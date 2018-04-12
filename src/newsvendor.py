from pyomo.environ import *
from pyomo.opt import SolverFactory



class Newsvendor(object):
    
    
    def __init__(self, price, cost, salvage_value, quantity_start):
        self.price = price
        self.cost = cost
        self.salvage_value = salvage_value
        self.quantity_start = quantity_start
        self.underage_cost = self.price - self.cost
        self.overage_cost = self.cost - self.salvage_value
        
        
    def objective_deterministic(self, model):
        '''
        Define and return a Pyomo expression representing the following objective function:
        C(q, d) = co * s + cu * t
        '''
        return model.overage_cost * model.s + model.underage_cost * model.t
        
        
    def model_deterministic(self, demand):
        # Create an optimization model.
        model = ConcreteModel()
        
        # Define parameters in model representing underage cost (cu), overage cost (co), and certain demand (d).
        # Pass validation functions that check that parameter values are positive real, i.e. continuous.
        model.underage_cost = Param(initialize=self.underage_cost, within=PositiveReals)
        model.overage_cost = Param(initialize=self.overage_cost, within=PositiveReals)
        model.demand = Param(initialize=demand, within=PositiveReals)
        
        # Define our decision variables, inventory quantity, s, and t.
        # Only allow our decision variables to take on non-negative real, i.e. continuous, values.
        model.quantity = Var(initialize=self.quantity_start, domain=NonNegativeReals)
        model.s = Var(initialize=0, domain=NonNegativeReals)
        model.t = Var(initialize=0, domain=NonNegativeReals)
        
        # Define an objective function in model representing cost.
        # Tell Pyomo our goal is to minimize this function.
        model.cost = Objective(rule=self.objective_deterministic, sense=minimize)
        
        # Define a constraint in model requiring that s be greater than or equal to quantity minus demand.
        # Define a constraint in model requiring that t be greater than or equal to demand minus quantity.
        model.constraint_1 = Constraint(expr=model.s >= (model.quantity - model.demand))
        model.constraint_2 = Constraint(expr=model.t >= (model.demand - model.quantity))
        
        return model
        

    def solve_deterministic(self, model):
        solver = SolverFactory('glpk')
        results = solver.solve(model)
        print(results)
        print("Optimal quantity (deterministic): ", model.quantity.value)
        print("Optimal cost (deterministic): ", model.cost())
        
        
    def objective_stochastic(self, model):
        '''
        Define and return a Pyomo expression representing the 'Newsvendor as LP (stochastic)' objective function.
        '''
        part_1 = (model.overage_cost * model.s_1 + model.underage_cost * model.t_1) * model.proba_1
        part_2 = (model.overage_cost * model.s_2 + model.underage_cost * model.t_2) * model.proba_2
        part_3 = (model.overage_cost * model.s_3 + model.underage_cost * model.t_3) * model.proba_3
        return part_1 + part_2 + part_3
      
      
    def model_stochastic(self, demand):
        '''
        Define and return a Pyomo model representing the 'Newsvendor as LP (stochastic)' problem.
        '''
        # Create an optimization model.
        model = ConcreteModel()
        
        # Define parameters in model.
        model.underage_cost = Param(initialize=self.underage_cost, within=PositiveReals)
        model.overage_cost = Param(initialize=self.overage_cost, within=PositiveReals)
        model.demand_1 = Param(initialize=demand[0][0], within=PositiveReals)
        model.demand_2 = Param(initialize=demand[1][0], within=PositiveReals)
        model.demand_3 = Param(initialize=demand[2][0], within=PositiveReals)
        model.proba_1 = Param(initialize=demand[0][1], within=PositiveReals)
        model.proba_2 = Param(initialize=demand[1][1], within=PositiveReals)
        model.proba_3 = Param(initialize=demand[2][1], within=PositiveReals)
        
        # Define our decision variables.
        model.quantity = Var(initialize=self.quantity_start, domain=NonNegativeReals)
        model.s_1 = Var(initialize=0, domain=NonNegativeReals)
        model.s_2 = Var(initialize=0, domain=NonNegativeReals)
        model.s_3 = Var(initialize=0, domain=NonNegativeReals)
        model.t_1 = Var(initialize=0, domain=NonNegativeReals)
        model.t_2 = Var(initialize=0, domain=NonNegativeReals)
        model.t_3 = Var(initialize=0, domain=NonNegativeReals)
        
        # Define an objective function in model representing expected cost.
        model.expected_cost = Objective(rule=self.objective_stochastic, sense=minimize)
        
        # Define constraints in model.
        model.constraint_s_1 = Constraint(expr=model.s_1 >= (model.quantity - model.demand_1))
        model.constraint_s_2 = Constraint(expr=model.s_2 >= (model.quantity - model.demand_2))
        model.constraint_s_3 = Constraint(expr=model.s_3 >= (model.quantity - model.demand_3))
        model.constraint_t_1 = Constraint(expr=model.t_1 >= (model.demand_1 - model.quantity))
        model.constraint_t_2 = Constraint(expr=model.t_2 >= (model.demand_2 - model.quantity))
        model.constraint_t_3 = Constraint(expr=model.t_3 >= (model.demand_3 - model.quantity))
        
        return model
        

    def solve_stochastic(self, model):
        '''
        Solve the 'Newsvendor as LP (stochastic)' problem using the glpk solver.
        '''
        solver = SolverFactory('glpk')
        results = solver.solve(model)
        print(results)
        print("Optimal quantity (stochastic): ", model.quantity.value)
        print("Optimal cost (stochastic): ", model.expected_cost())
        
        
    def objective_stochastic_generalized(self, model):
        '''
        Define and return a Pyomo expression representing the 'Newsvendor as LP (stochastic)' objective function.
        '''
        return sum((model.overage_cost * model.s[i] + model.underage_cost * model.t[i]) * model.proba[i] for i in model.I)
        
        
    def s_constraint_generator(self, model, i):
        '''
        '''
        return model.s[i] >= (model.quantity - model.demand[i])
        
        
    def t_constraint_generator(self, model, i):
        '''
        '''
        return model.t[i] >= (model.demand[i] - model.quantity)
      
      
    def model_stochastic_generalized(self, demand):
        '''
        Define and return a Pyomo model representing the 'Newsvendor as LP (stochastic)' problem.
        '''
        # Create an optimization model.
        model = ConcreteModel()
        
        model.I = Set(initialize=[i + 1 for i in range(len(demand))])
        
        # Define parameters.
        model.underage_cost = Param(initialize=self.underage_cost, within=PositiveReals)
        model.overage_cost = Param(initialize=self.overage_cost, within=PositiveReals)
        
        # Define parameters with index set I.
        model.demand = Param(model.I, initialize={i + 1: demand[i][0] for i in range(len(demand))}, within=PositiveReals)
        model.proba = Param(model.I, initialize={i + 1: demand[i][1] for i in range(len(demand))}, within=PositiveReals)
        
        # Define our decision variables.
        model.quantity = Var(domain=NonNegativeReals)
        model.s = Var(model.I, domain=NonNegativeReals)
        model.t = Var(model.I, domain=NonNegativeReals)
        
        # Define an objective function in model representing expected cost.
        model.expected_cost = Objective(rule=self.objective_stochastic_generalized, sense=minimize)
        
        # Define constraints in model.
        model.constraint_s = Constraint(model.I, rule=self.s_constraint_generator)
        model.constraint_t = Constraint(model.I, rule=self.t_constraint_generator)
        
        return model
        

    def solve_stochastic_generalized(self, model):
        '''
        Solve the 'Newsvendor as LP (stochastic)' problem using the glpk solver.
        '''
        solver = SolverFactory('glpk')
        results = solver.solve(model)
        print(results)
        print("Optimal quantity (stochastic): ", model.quantity.value)
        print("Optimal cost (stochastic): ", model.expected_cost())

        
if __name__ == '__main__':
    # newsvendor = Newsvendor(price=15.99, cost=7.99, salvage_value=6.99, quantity_start=5000)
    # model = newsvendor.model_deterministic(demand=8200)
    # newsvendor.solve_deterministic(model)
    
    # newsvendor = Newsvendor(price=15.99, cost=7.99, salvage_value=6.99, quantity_start=5000)
    # model = newsvendor.model_stochastic(demand=[(5400, 0.1), (7800, 0.4), (8200, 0.5)])
    # newsvendor.solve_stochastic(model)
    
    # newsvendor = Newsvendor(price=15.99, cost=7.99, salvage_value=6.99, quantity_start=5000)
    # model = newsvendor.model_stochastic_generalized(demand=[(5400, 0.1), (7800, 0.4), (8200, 0.5)])
    # newsvendor.solve_stochastic_generalized(model)
    
    # Solve test problem from the literature and compare our solution to the analytical one.
    import numpy as np
    demand=np.random.normal(loc=3649, scale=926, size=5000)
    # NOTE: Both Pyomo and numpy use operator overloading. So cast numpy floats to Python floats before passing into Pyomo.
    demand_proba_pairs = [(np.float64(demand[i]).item(), 0.0002) for i in range(5000)]
    newsvendor = Newsvendor(price=150, cost=100, salvage_value=70, quantity_start=5000)
    model = newsvendor.model_stochastic_generalized(demand=demand_proba_pairs)
    newsvendor.solve_stochastic_generalized(model)
    # Compute analytical quantity.
    import scipy.stats as stats
    dist = stats.norm(loc=3649, scale=926)
    print('Optimal quantity (analytical): ', dist.ppf((150-100) / ((150-100) + (100-70))))
    
    


    