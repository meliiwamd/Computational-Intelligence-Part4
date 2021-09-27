import random
import operator

# Soling Traveling Salesman Problem using genetic algorithm.
# There is 5 main steps doing this algorithm:

# 1.Creating initial population.
# 2.Calculating fitness.
# 3.Selecting the best genes.
# 4.Crossing over.
# 5.Mutating to introduce variations.

# So as mentioned above we'll start with creating the initial population.
# We'll save chromosomes in arrays ith size of cities + 1.

# Make graph.
CityNumber = 7

Graph = {
    '1': {'2': 12, '3': 10, '7': 12},
    '2': {'1': 12, '3': 8, '4': 12},
    '3': {'1': 10, '2': 8, '4': 11, '5': 3, '7': 9},
    '4': {'2': 12, '3': 11, '5': 11, '6': 10},
    '5': {'3': 3, '4': 11, '6': 6, '7': 7},
    '6': {'4': 10, '5': 6, '7': 9},
    '7': {'1': 12, '3': 9, '5': 7, '6': 9}
}

class Individual:
    def __init__(self):
        self.Chromosome = [None] * (CityNumber + 1)
        self.Fitness = 0
    
    def Initialize(self):

        StartCity = 3
        Numbers = [1, 2, 4, 5, 6, 7]

        # Numbers = [1, 2, 3, 4, 5, 6, 7]
        # Index = random.randint(0, len(Numbers) - 1)
        # StartCity = Numbers[Index]
        # del Numbers[Index]
        
        self.Chromosome[0] = self.Chromosome[-1] = StartCity
        for x in range(1, CityNumber):
            Index = random.randint(0, len(Numbers) - 1)
            self.Chromosome[x] = Numbers[Index]
            del Numbers[Index]

        return self.Chromosome

    def CalculateFitness(self):
        self.Fitness = 0
        for x in range(CityNumber):
            Value = Graph[str(self.Chromosome[x])]
            if str(self.Chromosome[x + 1]) in Value:
                NextValue = Value[str(self.Chromosome[x + 1])]
                self.Fitness += NextValue
            else:
                self.Fitness = 999999
                return self.Fitness
        return self.Fitness

    def Set(self, Chro):
        self.Chromosome = Chro

def SelectParents(Population, SizeOfSelection):
    Selected = []
    # Sort by their fitness.
    for i in range(SizeOfSelection):
        Selected.append(Population[i])
    return Selected

def GeneticChange(MutationRate, Best):
    # Crossover at first.
    NewPop = []

    # With some probability we have mutation.
    for i in range(len(Best) - 2):
        Child1 = CrossOverTwoPoint(Best[i], Best[i + 1])
        Child2 = CrossOverTwoPoint(Best[i], Best[i + 2])
        Prob = random.random() / 10
        if Prob < MutationRate:
            NewPop.append(Mutate(Child1))
            NewPop.append(Mutate(Child2))
        else:
            NewPop.append(Child1)
            NewPop.append(Child2)
    return NewPop

def Mutate(Parent):
    # Just swapping.
    Index1 = random.randint(1, len(Parent.Chromosome) - 2)
    Index2 = random.randint(1, len(Parent.Chromosome) - 2)
    while Index1 is Index2:
        Index2 = random.randint(1, len(Parent.Chromosome) - 2)

    Temp = Parent.Chromosome[Index1]
    Parent.Chromosome[Index1] = Parent.Chromosome[Index2]
    Parent.Chromosome[Index2] = Temp

    Parent.CalculateFitness()
    return Parent

def CrossOverTwoPoint(Mom, Dad):
    # Two point.
    Child = [-1] * len(Mom.Chromosome)
    Index1 = random.randint(1, len(Dad.Chromosome) - 2)
    Index2 = random.randint(1, len(Dad.Chromosome) - 2)

   
    Child[0] = Child[-1] = Dad.Chromosome[0]

    if Index1 < Index2:
        for i in range(Index1, Index2):
            Child[i] = Dad.Chromosome[i]
        for i in range(1, Index1):
            for j in range(1, len(Mom.Chromosome) - 1):
                if Mom.Chromosome[j] not in Child:
                    Child[i] = Mom.Chromosome[j]
                    break
        for i in range(Index2, len(Child) - 1):
            for j in range(1, len(Mom.Chromosome) - 1):
                if Mom.Chromosome[j] not in Child:
                    Child[i] = Mom.Chromosome[j]
                    break
    else:
        for i in range(Index2, Index1):
            Child[i] = Dad.Chromosome[i]
        for i in range(1, Index2):
            for j in range(1, len(Mom.Chromosome) - 1):
                if Mom.Chromosome[j] not in Child:
                    Child[i] = Mom.Chromosome[j]
                    break
        for i in range(Index1, len(Child) - 1):
            for j in range(1, len(Mom.Chromosome) - 1):
                if Mom.Chromosome[j] not in Child:
                    Child[i] = Mom.Chromosome[j]
                    break
                    
    ChildInd = Individual()
    ChildInd.Set(Child)
    ChildInd.CalculateFitness()
 
    return ChildInd


# Now it's time to create the initial population.
Population = []
InitialPopulation = 1000
UpperBound = 200
Iteration = 0
Mutation = 0.05
SizeOfSelection = 75

for i in range(InitialPopulation):
    Ind = Individual()
    Ind.Initialize()
    Ind.CalculateFitness()
    Population.append(Ind)

while Iteration < UpperBound:
    # Sort.
    Population.sort(key=operator.attrgetter('Fitness'), reverse=False)
    # Select individuals with better fitnesses.
    Best = SelectParents(Population, SizeOfSelection)

    # It supports both mutation and crossover.
    Population = GeneticChange(Mutation, Best)
    Iteration += 1

Answer = min(Population, key=operator.attrgetter('Fitness'))
print(Answer.Chromosome, "Fitness: ", Answer.Fitness)

import random
import operator
# Same as previous question.
# The sole difference is about the genes and orientation of chromosome.

# Here we use our unknown values as the genes.
# So our chromosome would be unknown values of the equation.

# Equation = 9x^5 − 194.7x^4 + 1680.1x^3 − 7227.94x^2 + 15501.2x − 13257.2
# We consider our answer to be in range of [-9, 9]
# Ans we also accept 4 numbers of fraction.

Coefficients = [9, -194.7, 1680.1, -7227.94, 15501.2, -13257.2]
ChromosomeSize = 6

class Individual:
    def __init__(self):
        self.Chromosome = [None] * ChromosomeSize
        self.Fitness = 0
        self.Answer = 0
        self.Neg = random.randint(0, 1)
    
    def Initialize(self):
        String = ""
        for i in range(ChromosomeSize):
            if i is 1:
                self.Chromosome[i] = '.'
            else:
                self.Chromosome[i] = random.randint(0, 9)
            String += str(self.Chromosome[i])
        if self.Neg is 0:
            self.Answer = float(String) 
        else:
            self.Answer = float(String) * -1

    def CalculateFitness(self):
        Value = 0
        for i in range(len(Coefficients)):
            Value += Coefficients[i] * pow(self.Answer, 5 - i)
        self.Fitness = abs(Value)

    def Set(self, Chro):
        self.Chromosome = Chro
    
    def SwapDot(self):
        DotInd = 0
        String = ""
        for i in range(ChromosomeSize):
            if self.Chromosome[i] is '.':
                DotInd = i
                break
        if DotInd is not 1:
            self.Chromosome[DotInd] = self.Chromosome[1]
            self.Chromosome[1] = '.'

        for i in range(ChromosomeSize):
            String += str(self.Chromosome[i])
        if self.Neg is 0:
            self.Answer = float(String) 
        else:
            self.Answer = float(String) * -1
        
def SelectParents(Population, SizeOfSelection):
    Selected = []
    # Sort by their fitness.
    for i in range(SizeOfSelection):
        Selected.append(Population[i])
    return Selected

def GeneticChange(MutationRate, Best):
    # Crossover at first.
    NewPop = []

    # With some probability we have mutation.
    for i in range(len(Best) - 2):
        Child1 = CrossOverTwoPoint(Best[i], Best[i + 1])
        Child2 = CrossOverTwoPoint(Best[i], Best[i + 2])
        Prob = random.random() / 10
        if Prob < MutationRate:
            NewPop.append(Mutate(Child1))
            NewPop.append(Mutate(Child2))
        else:
            NewPop.append(Child1)
            NewPop.append(Child2)
    return NewPop

def Mutate(Parent):
    # Just swapping.
    Index1 = random.randint(0, len(Parent.Chromosome) - 1)
    Index2 = random.randint(0, len(Parent.Chromosome) - 1)
    while Index1 == 2 or Index2 == 2:
        if Index1 == 2:
            Index1 = random.randint(0, len(Parent.Chromosome) - 1)
        else:
            Index2 = random.randint(0, len(Parent.Chromosome) - 1)

    Temp = Parent.Chromosome[Index1]
    Parent.Chromosome[Index1] = Parent.Chromosome[Index2]
    Parent.Chromosome[Index2] = Temp
    Parent.SwapDot()
    Parent.CalculateFitness()
    return Parent

def CrossOverTwoPoint(Mom, Dad):
    # Two point.
    Child = [0] * ChromosomeSize
    Index1 = random.randint(0, len(Dad.Chromosome) - 1)
    Index2 = random.randint(0, len(Dad.Chromosome) - 1)
   
    if Index1 < Index2:
        for i in range(Index1, Index2):
            Child[i] = Dad.Chromosome[i]
        for i in range(0, Index1):
            for j in range(0, len(Mom.Chromosome)):
                if Mom.Chromosome[j] not in Child:
                    Child[i] = Mom.Chromosome[j]
                    break
        for i in range(Index2, len(Child)):
            for j in range(0, len(Mom.Chromosome)):
                if Mom.Chromosome[j] not in Child:
                    Child[i] = Mom.Chromosome[j]
                    break
    else:
        for i in range(Index2, Index1):
            Child[i] = Dad.Chromosome[i]
        for i in range(0, Index2):
            for j in range(0, len(Mom.Chromosome)):
                if Mom.Chromosome[j] not in Child:
                    Child[i] = Mom.Chromosome[j]
                    break
        for i in range(Index1, len(Child)):
            for j in range(0, len(Mom.Chromosome)):
                if Mom.Chromosome[j] not in Child:
                    Child[i] = Mom.Chromosome[j]
                    break
                    
    ChildInd = Individual()
    ChildInd.Set(Child)
    ChildInd.SwapDot()
    ChildInd.CalculateFitness()
 
    return ChildInd


# Now it's time to create the initial population.
Population = []
InitialPopulation = 1000
UpperBound = 200
Iteration = 0
Mutation = 0.05
SizeOfSelection = 75

for i in range(InitialPopulation):
    Ind = Individual()
    Ind.Initialize()
    Ind.CalculateFitness()
    Population.append(Ind)

while Iteration < UpperBound:
    # Sort.
    Population.sort(key=operator.attrgetter('Fitness'), reverse=False)
    # Select individuals with better fitnesses.
    Best = SelectParents(Population, SizeOfSelection)

    # It supports both mutation and crossover.
    Population = GeneticChange(Mutation, Best)
    Iteration += 1

Answer = min(Population, key=operator.attrgetter('Fitness'))
print(Answer.Chromosome, Answer.Answer, "Fitness: ", Answer.Fitness)

