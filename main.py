from geneticAlgorithm import executeGeneticAlgorithm
from geneticOperators import initCities

if __name__ == '__main__':
  cities = initCities()
  
  population, generation, bigHorse = executeGeneticAlgorithm(cities, 5, 5)

  print(f"\n\nPopulação final após {generation} gerações")
  for pop in population:
    print(f"{pop}: ( ", end="")
    for neighbor in population[pop]['path']:
      print(f"{neighbor['city'].getId()}", end=" ")
    print(") - Aptidão: ", population[pop]['fitness'])

  print("\nMelhor solução encontrada:")
  print(f"( ", end="")
  for neighbor in bigHorse['path']:
    print(f"{neighbor['city'].getId()}", end=" ")
  print(") - Aptidão: ", bigHorse['fitness'])

