class City:
  def __init__(self, id):
    self.id = id
    self.neighborhood = []
  
  def setNeighborhood(self, neighborhood: list[dict]):
    self.neighborhood = neighborhood

  def getNeighborhood(self) -> list[dict]:
    return self.neighborhood

  def getNeighbor(self, neighborId):
    for neighbor in self.neighborhood:
      if neighbor['city'].getId() == neighborId:
        return neighbor
    return None
  
  def getId(self) -> int:
    return self.id

  def __str__(self):
    return f"City {self.id}"

  def __iter__(self):
    pass
