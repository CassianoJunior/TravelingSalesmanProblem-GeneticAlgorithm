from classes import City
from geneticAlgorithm import executeGeneticAlgorithm
from geneticOperators import initCities

if __name__ == '__main__':
  cities = initCities()
  
  executeGeneticAlgorithm(cities, 2, 5)
