import geneticOperators
from classes import City


def executeGeneticAlgorithm(cities, generations, populationSize = 10, mutationRate = 0.05):
  initialPopulation = geneticOperators.generateInitialPopulation(cities, populationSize)
  iterations = 1

  bigHorse = {'path': [], 'fitness': 0}
  while iterations <= generations:
    print(f"Geração: {iterations}\n")
    iterations += 1
    print("População")
    for pop in initialPopulation:
      print(f"{pop}: ( ", end="")
      for neighbor in initialPopulation[pop]['path']:
        print(f"{neighbor['city'].getId()}", end=" ")
      
      print(")")

    print("Garanhão: ( ", end="")
    for neighbor in bigHorse['path']:
      print(f"{neighbor['city'].getId()}", end=" ")
    print(f") - Aptidão: {bigHorse['fitness']}\n")

    # os.system("pause")

    populationWithFitness, sumOfFitness = geneticOperators.calculateFitness(initialPopulation)
    for pop in populationWithFitness:
      print(f"{pop}: ( ", end="")
      for neighbor in populationWithFitness[pop]['path']:
        print(f"{neighbor['city'].getId()}", end=" ")
      
      print(f") - Aptidão: {populationWithFitness[pop]['fitness']} - Probabilidade: {((1/populationWithFitness[pop]['fitness'])/sumOfFitness*100):.2f}%")

    parents = geneticOperators.selectParents(populationWithFitness, sumOfFitness)
    
    print("Seleção dos pais")
    for parent in parents:
      print(f"( ", end="")
      for neighbor in parent['path']:
        print(f"{neighbor['city'].getId()}", end=" ")
      
      print(f") - Aptidão: {parent['fitness']} - Probabilidade: {((1/parent['fitness'])/sumOfFitness*100):.2f}%")
    
    childrens = geneticOperators.crossover(parents)
    
    bestSolution = populationWithFitness[list(populationWithFitness.keys())[0]]

    for population in populationWithFitness:
      if populationWithFitness[population]["fitness"] < bestSolution["fitness"]:
        bestSolution = populationWithFitness[population]
        bigHorse = bestSolution

    print("Filhos resultantes do cruzamento:")
    for child in childrens:
      print(f"( ", end="")
      for neighbor in child:
        print(f"{neighbor['city'].getId()}", end=" ")
      
      print(")")
    print()

    childrensCopy = childrens
    childrens = geneticOperators.mutation(childrens, mutationRate)

    mutateds = listOfChildsMutateds(childrens, childrensCopy)
    if len(mutateds) > 0:
      print("Indivíduos que sofreram mutação:")
      for child in mutateds:
        print(f"( ", end="")
        for neighbor in child:
          print(f"{neighbor['city'].getId()}", end=" ")
        
        print(")\n")
    else:
      print("Nenhum indivíduo sofreu mutação")
    
    newPopulation = {}
    for i in range(len(childrens)):
      newPopulation[f'indivíduo{i+1}'] = {
        "path": childrens[i],
        "fitness": 0
      }
    newPopulation[f'indivíduo{len(childrens) + 1} (GARANHÃO)'] = {
      "path": bestSolution["path"],
      "fitness": 0
    }
    
    initialPopulation = newPopulation

def listOfChildsMutateds(childrens, oldChildrens):
  mutateds = []
  for child in range(len(childrens)):
    for neighbor in range(len(childrens[child])):
      if childrens[child][neighbor]["city"].getId() != oldChildrens[child][neighbor]["city"].getId():
        mutateds.append(child)
  
  return mutateds