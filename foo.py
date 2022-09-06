import random

from classes import City


def getInitialPopulation(cities):
  citiesCopy = cities
  population = {}

  for city in citiesCopy:
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

    population[f"indivíduo{str(city.getId())}"] = {"path": path, "fitness": 0}

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
  
  while len(parents) != 4:
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
  for i in range(0, len(parents), 2):
    child1 = parents[i][:3] + parents[i+1][3:]
    child2 = parents[i][3:] + parents[i+1][:3]
    childrens.append(child1)
    childrens.append(child2)
    for child in childrens:
      for city in child:
        print(city['city'].getId(), end=" ")
      print()
    print(isValidSolution(child1))
    print(isValidSolution(child2))
  
  return childrens