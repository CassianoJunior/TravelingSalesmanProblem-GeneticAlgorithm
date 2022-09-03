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

    population[f"indivíduo{str(city.getId())}"] = path

  return population

def cityIsInPath(city, path):
  for pathCity in path:
    if pathCity["city"].getId() == city.getId():
      return True

  return False


def calculateFitness(population: dict):
  fitness = {}

  control = 1
  fitness["sum"] = 0
  for individual in population:
    fitness[individual] = 0

    for i in range(len(population[individual])):
      fitness[individual] += population[individual][i]["distance"]
    
      print(f"Aptidão parcial da indivíduo {control}, até cidade {population[individual][i]['city'].getId()}: {fitness[individual]}")

    print(f"Aptidão final da indivídual {control}: {fitness[individual]}")
    print()
    control += 1

    fitness["sum"] += fitness[individual]

  return fitness
# python -u "c:\Users\cassi\Documents\UFPI\Disciplinas\5P\InteligenciaArtificial\Trabalhos\TrabalhoPratico2\TravelingSalesmanProblem-GeneticAlgorithm\main.py"

def selectParents(fitness: dict):
  parents = []
  weights = []
  values = []
  for fit in fitness:
    if fit != "sum":
      weights.append(fitness["sum"] - fitness[fit])
      values.append(fitness[fit])

  while len(parents) != 2:
    parent = random.choices(values, weights=weights, k=1)
    parents.append(parent[0])

  return parents
