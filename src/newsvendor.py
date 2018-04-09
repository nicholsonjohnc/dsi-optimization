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
        
        # Define our decision variable, inventory quantity.
        # Only allow our decision variable to take on non-negative real, i.e. continuous, values.
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
        # YOUR CODE HERE
        pass
      
      
    def model_stochastic(self, mu, sigma):
        '''
        Define and return a Pyomo model representing the 'Newsvendor as LP (stochastic)' problem.
        '''
        # YOUR CODE HERE
        pass
        

    def solve_stochastic(self, model):
        '''
        Solve the 'Newsvendor as LP (stochastic)' problem using the glpk solver.
        '''
        # YOUR CODE HERE
        pass

        
if __name__ == '__main__':
    newsvendor = Newsvendor(price=150, cost=100, salvage_value=70, quantity_start=1)
    model = newsvendor.model_deterministic(demand=3940)
    newsvendor.solve_deterministic(model)
    
    # newsvendor = Newsvendor(price=150, cost=100, salvage_value=70, quantity_start=5000)
    # model = newsvendor.model_stochastic(mu=3649, sigma=926)
    # newsvendor.solve_stochastic(model)
    