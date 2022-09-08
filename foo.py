import random

from classes import City


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
    
      print(f"Aptidão parcial da indivíduo {control}, até cidade {populationWithFitness[individual]['path'][i]['city'].getId()}: {populationWithFitness[individual]['fitness']}")

    print(f"Aptidão final do indivíduo {control}: {populationWithFitness[individual]['fitness']}\n")
    control += 1

    sum += 1/populationWithFitness[individual]["fitness"]

  return populationWithFitness, sum
# python -u "c:\Users\cassi\Documents\UFPI\Disciplinas\5P\InteligenciaArtificial\Trabalhos\TrabalhoPratico2\TravelingSalesmanProblem-GeneticAlgorithm\main.py"

def selectParents(population: dict, sumOfFitness):
  parents = []
  weights = []
  values = []

  for pop in population:
    for neighbor in population[pop]['path']:
      absoluteFitness = 1 / population[pop]["fitness"]
      weights.append(absoluteFitness/sumOfFitness)
      values.append(population[pop]["path"]) 
  print(len(list(population.keys())))
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
  validsSolutions = 0
  print(len(parents))
  while len(childrens) < len(parents) - 1:
    parent1 = random.choice(parents)
    parent2 = random.choice(parents)

    cutoff = random.randint(0, len(parent1) - 1)

    child1 = parent1[:cutoff] + parent2[cutoff:]
    child2 = parent1[cutoff:] + parent2[:cutoff]

    if isValidSolution(child1) and len(childrens) <= len(parents) - 2:
      childrens.append(child1)
      for city in child1:
        print(city['city'].getId(), end=" ")
      print()
      validsSolutions += 1
    if isValidSolution(child2) and len(childrens) <= len(parents) - 2:
      childrens.append(child2)
      for city in child2:
        print(city['city'].getId(), end=" ")
      print()
      validsSolutions += 1

  print(f"Quantidade de soluções válidas: {validsSolutions}")
  print(len(childrens))
  return childrens

def mutation(childrens: list):
  for child in childrens:
    if random.random() <= 0.05:
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

