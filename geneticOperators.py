import random

from classes import City


def initCities():
  city1 = City(1)
  city2 = City(2)
  city3 = City(3)
  city4 = City(4)
  city5 = City(5)
  city1.setNeighborhood([
    {"city": city2, "distance": 2},
    {"city": city4, "distance": 3},
    {"city": city5, "distance": 6}
  ])
  city2.setNeighborhood([
    {"city": city1, "distance": 2},
    {"city": city3, "distance": 4},
    {"city": city4, "distance": 3}
  ])
  city3.setNeighborhood([
    {"city": city2, "distance": 4},
    {"city": city4, "distance": 7},
    {"city": city5, "distance": 3}
  ])

  city4.setNeighborhood([
    {"city": city1, "distance": 3},
    {"city": city2, "distance": 3},
    {"city": city3, "distance": 7},
    {"city": city5, "distance": 3}
  ])

  city5.setNeighborhood([
    {"city": city1, "distance": 6},
    {"city": city3, "distance": 3},
    {"city": city4, "distance": 3}
  ])

  return [city1, city2, city3, city4, city5]

def generateInitialPopulation(cities, populationSize=10):
  citiesCopy = cities
  population = {}

  for i in range(populationSize):
    city = random.choice(citiesCopy)
    path = [{"city": city, "distance": 0}]
    actualCity = city
    while len(path) != 5:
      citiesInNeighborhood = actualCity.getNeighborhood()
      randomNeighbor = random.choice(citiesInNeighborhood)
      allInPath = True

      for cityInNeighborhood in citiesInNeighborhood:
        if not cityIsInPath(cityInNeighborhood["city"], path):
          allInPath = False
          break
      
      if allInPath:
        path = [{"city": city, "distance": 0}]
        actualCity = city
        continue
      
      if not cityIsInPath(randomNeighbor["city"], path):
        path.append(randomNeighbor)
        actualCity = randomNeighbor["city"]

    population[f"indivíduo{i+1}"] = {"path": path, "fitness": 0}

  return population

def cityIsInPath(city, path):
  for pathCity in path:
    if pathCity["city"].getId() == city.getId():
      return True

  return False


def calculateFitness(population: dict):
  populationWithFitness = population
  control = 1
  sum = 0
  for individual in populationWithFitness:
  
    for i in range(len(populationWithFitness[individual]['path'])):
      populationWithFitness[individual]["fitness"] += populationWithFitness[individual]["path"][i]["distance"]
    
      print(f"Aptidão parcial do indivíduo {control}, até cidade {populationWithFitness[individual]['path'][i]['city'].getId()}: {populationWithFitness[individual]['fitness']}")

    print(f"Aptidão final do indivíduo {control}: {populationWithFitness[individual]['fitness']}\n")
    control += 1

    sum += 1/populationWithFitness[individual]["fitness"]

  return populationWithFitness, sum

def selectParents(population: dict, sumOfFitness):
  parents = []
  weights = []
  values = []

  for pop in population:
    for neighbor in population[pop]['path']:
      absoluteFitness = 1 / population[pop]["fitness"]
      weights.append(absoluteFitness/sumOfFitness)
      values.append(population[pop]) 

  while len(parents) <= len(list(population.keys())) - 1:
    parent = random.choices(values, weights=weights, k=1)
    parents.append(parent[0])

  return parents

def isValidSolution(solution):
  citiesIds = []
  for neighbor in solution:
    citiesIds.append(neighbor["city"].getId())
  
  for id in citiesIds:
    if citiesIds.count(id) > 1:
      return False

  for i in range(len(solution) - 1):
    isNeighbor = False
    for neighbor in solution[i]["city"].getNeighborhood():
      if solution[i+1]["city"].getId() == neighbor["city"].getId():
        isNeighbor = True
        break
    if not isNeighbor:
      return False

  return True

def crossover(parents: list):
  childrens = []
  while len(childrens) < len(parents) - 1:
    parent1 = random.choice(parents)
    parent2 = random.choice(parents)

    cutoff = random.randint(1, len(parent1) - 1)

    print(f"Ponto de corte: {cutoff}")
    print("Pais selecionados:")
    control = 0
    for city in parent1['path']:
      if control == cutoff: print("|", end=" ")
      print(city["city"].getId(), end=" ")
      control += 1
    print()
    control = 0
    for city in parent2['path']:
      if control == cutoff: print("|", end=" ")
      print(city["city"].getId(), end=" ")
      control += 1
    print()

    child1 = parent1['path'][:cutoff] + parent2['path'][cutoff:]
    child2 = parent1['path'][cutoff:] + parent2['path'][:cutoff]

    print("Filho(s) gerado(s):") if isValidSolution(child1) or isValidSolution(child2) else print("Filhos gerados inválidos!")
    
    if isValidSolution(child1) and len(childrens) <= len(parents) - 2:
      for city in child1:
        print(city["city"].getId(), end=" ")
      print()
      childrens.append(child1)

    if not (isValidSolution(child2) and len(childrens) <= len(parents) - 2): print()

    if isValidSolution(child2) and len(childrens) <= len(parents) - 2:
      for city in child2:
        print(city["city"].getId(), end=" ")
      print("\n")
      childrens.append(child2)
      

  return childrens

def mutation(childrens: list, mutationRate = 0.05):
  for child in childrens:
    if random.random() <= mutationRate:
      while True:
        city1 = random.choice(child)
        city2 = random.choice(child)

        index1 = child.index(city1)
        index2 = child.index(city2)

        child[index1] = city2
        child[index2] = city1

        if isValidSolution(child): break
        child[index1] = city1
        child[index2] = city2

  return childrens

