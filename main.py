from classes import City
from geneticAlgorithm import executeGeneticAlgorithm
from geneticOperators import initCities

if __name__ == '__main__':
  cities = initCities()
  
  population, generation = executeGeneticAlgorithm(cities, 10, 10)

  print(f"População final após {generation} gerações")
  for pop in population:
    print(f"{pop}: ( ", end="")
    for neighbor in population[pop]['path']:
      print(f"{neighbor['city'].getId()}", end=" ")
    print(") - Aptidão: ", population[pop]['fitness'])

