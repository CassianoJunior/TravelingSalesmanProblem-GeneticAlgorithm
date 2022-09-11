import geneticOperators
from classes import City
from colorVariables import *
from unionTypes import *


def executeGeneticAlgorithm(cities: list[City], generations: int, populationSize:int = 10, mutationRate:float = 0.05) -> tuple[dict[str, IndividualType], int, PathDictionaryType]:
  actualPopulation = geneticOperators.generateInitialPopulation(cities, populationSize)
  iterations = 1
  isPausedExecution = False

  bigHorse = {'path': [], 'fitness': 0}
  while iterations < generations:
    isPausedExecution = showPausedMode(isPausedExecution)

    print(f"{BOLD + RED}\nGeração: {iterations} {RESET}\n")
    iterations += 1
    print(f"{BOLD}População{RESET}")
    for pop in actualPopulation:
      print(f"{pop}: ( ", end="")
      for neighbor in actualPopulation[pop]['path']:
        print(f"{neighbor['city'].getId()}", end=" ")
      
      print(")")

    print(f"{BOLD + CYAN}Garanhão: ( ", end="")
    for neighbor in bigHorse['path']:
      print(f"  {neighbor['city'].getId()}", end=" ")
    print(f") - Aptidão: {bigHorse['fitness']} {RESET}\n")

    if isPausedExecution: pauseCode("Pressione qualquer tecla para prosseguir para o cálculo da aptidão da população")

    populationWithFitness, sumOfFitness = geneticOperators.calculateFitness(actualPopulation)
    for pop in populationWithFitness:
      print(f"{pop}: ( ", end="")
      for neighbor in populationWithFitness[pop]['path']:
        print(f"{neighbor['city'].getId()}", end=" ")
      
      print(f") - Aptidão: {populationWithFitness[pop]['fitness']} - Probabilidade: {((1/populationWithFitness[pop]['fitness'])/sumOfFitness*100):.2f}%")
    print()

    if isPausedExecution: pauseCode("Pressione qualquer tecla para prosseguir para a seleção dos pais (Seleção natural - Método: roleta)")

    parents = geneticOperators.selectParents(populationWithFitness, sumOfFitness)
    
    print(f"{BOLD}Seleção dos pais{RESET}")
    for parent in parents:
      print(f"( ", end="")
      for neighbor in parent['path']:
        print(f"{neighbor['city'].getId()}", end=" ")
      
      print(f") - Aptidão: {parent['fitness']} - Probabilidade: {((1/parent['fitness'])/sumOfFitness*100):.2f}%")
    
    if isPausedExecution: pauseCode("Pressione qualquer tecla para prosseguir para a geração dos filhos (crossover)")

    bestSolution = populationWithFitness[list(populationWithFitness.keys())[0]]

    for population in populationWithFitness:
      if populationWithFitness[population]["fitness"] < bestSolution["fitness"]:
        bestSolution = populationWithFitness[population]
        bigHorse = bestSolution

    childrens = geneticOperators.crossover(parents, cities)
    
    print(f"{BOLD}Filhos resultantes do cruzamento:{RESET}")
    for child in childrens:
      print(f"( ", end="")
      for neighbor in child:
        print(f"{neighbor['city'].getId()}", end=" ")
      
      print(")")
    print()
    
    childrensCopy = childrens
    
    bestSolution = populationWithFitness[list(populationWithFitness.keys())[0]]

    for population in populationWithFitness:
      if populationWithFitness[population]["fitness"] < bestSolution["fitness"]:
        bestSolution = populationWithFitness[population]
        bigHorse = bestSolution

    if isPausedExecution: pauseCode("Pressione qualquer tecla para prosseguir para a mutação dos filhos")

    childrens = geneticOperators.mutation(childrens, mutationRate)

    mutateds = listOfChildsMutateds(childrens, childrensCopy)
    if len(mutateds) > 0:
      print(f"{BOLD}Indivíduos que sofreram mutação:{RESET} (Taxa de mutação: {mutationRate}%)")
      for child in mutateds:
        print(f"( ", end="")
        for neighbor in child:
          print(f"{neighbor['city'].getId()}", end=" ")
        
        print(")\n")
    else:
      print(f"{BOLD}Nenhum indivíduo sofreu mutação.{RESET} (Taxa de mutação: {mutationRate}%)")
    
    newPopulation = {}
    for i in range(len(childrens)):
      newPopulation[f'indivíduo{i+1}'] = {
        "path": childrens[i],
        "fitness": 0
      }
    newPopulation[f'indivíduo{len(childrens) + 1}*'] = {
      "path": bestSolution["path"],
      "fitness": 0
    }
    
    if isStagnant(actualPopulation, bigHorse['fitness']) or iterations >= generations : break

    actualPopulation = newPopulation

  return actualPopulation, iterations, bigHorse

def listOfChildsMutateds(childrens: list[IndividualType], oldChildrens: list[IndividualType]) -> list[IndividualType]:
  mutateds = []
  for child in range(len(childrens)):
    for neighbor in range(len(childrens[child])):
      if childrens[child][neighbor]["city"].getId() != oldChildrens[child][neighbor]["city"].getId():
        mutateds.append(child)
  
  return mutateds

def isStagnant(population: dict[str, IndividualType], bestFitness: int) -> bool:
  allFitness = []
  for pop in population:
    allFitness.append(population[pop]['fitness'])

  for fitness in allFitness:
    quant = allFitness.count(fitness)
    if quant >= len(list(population.keys()))*0.8 and fitness <= bestFitness and bestFitness != 0:
      return True

  return False

def showPausedMode(isPausedExecution: bool) -> bool:
  if isPausedExecution:
      answer = input("\nDeseja executar o programa de forma pausada?\n")
      if(answer.lower() == 'n' or answer.lower() == 'nao' or answer.lower() == 'não'):
        isPausedExecution = False
  return isPausedExecution

def pauseCode(msg: str):
  input(f"\n{msg}...\n")
