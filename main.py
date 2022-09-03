


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
  
  initialPopulation = foo.getInitialPopulation(cities)
  for pop in initialPopulation:
    print(f"{pop}: ( ", end="")
    for neighbor in initialPopulation[pop]:
      print(f"{neighbor['city'].getId()}", end=" ")
    
    print(")")

  # os.system("pause")

  fitness = foo.calculateFitness(initialPopulation)
  for fit in fitness:
    print(f"{fit}: {fitness[fit]}")

  parents = foo.selectParents(fitness)



