
import foo
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
    {"city": city3, "distance":4},
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

if __name__ == '__main__':
  cities = initCities()
  
  initialPopulation = foo.generateInitialPopulation(cities, 5)
  for pop in initialPopulation:
    print(f"{pop}: ( ", end="")
    for neighbor in initialPopulation[pop]['path']:
      print(f"{neighbor['city'].getId()}", end=" ")
    
    print(")")

  # os.system("pause")
  populationWithFitness, sumOfFitness = foo.calculateFitness(initialPopulation)
  for pop in populationWithFitness:
    print(f"{pop}: ( ", end="")
    for neighbor in populationWithFitness[pop]['path']:
      print(f"{neighbor['city'].getId()}", end=" ")
    
    print(f"), {populationWithFitness[pop]['fitness']}")

  parents = foo.selectParents(populationWithFitness, sumOfFitness)
  
  for parent in parents:
    print(f"( ", end="")
    for neighbor in parent:
      print(f"{neighbor['city'].getId()}", end=" ")
    
    print(")")
  
  childrens = foo.crossover(parents)
  
  bestSolution = populationWithFitness[list (populationWithFitness.keys())[0]]
  for population in populationWithFitness:
    if populationWithFitness[population]["fitness"] < bestSolution["fitness"]:
      bestSolution = populationWithFitness[population]

  for child in childrens:
    print(f"( ", end="")
    for neighbor in child:
      print(f"{neighbor['city'].getId()}", end=" ")
    
    print(")")

  childrens = foo.mutation(childrens)

  print("Mutateds:")
  for child in childrens:
    print(f"( ", end="")
    for neighbor in child:
      print(f"{neighbor['city'].getId()}", end=" ")
    
    print(")")

  newPopulation = {}
  for i in range(len(childrens)):
    newPopulation[f'indivíduo{i+1}'] = {
      "path": childrens[i],
      "fitness": 0
    }
  newPopulation[f'indivíduo{len(childrens) + 1}(GARANHÃO)'] = {
    "path": bestSolution["path"],
    "fitness": bestSolution["fitness"]
  }

  print("New Population:")
  for pop in newPopulation:
    print(f"{pop}: ( ", end="")
    for neighbor in newPopulation[pop]['path']:
      print(f"{neighbor['city'].getId()}", end=" ")
    
    print(f") - fitness: {newPopulation[pop]['fitness']}")
