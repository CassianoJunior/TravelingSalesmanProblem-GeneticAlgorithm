class City:
  def __init__(self, id):
    self.id = id
    self.neighborhood = []
  
  def setNeighborhood(self, neighborhood):
    self.neighborhood = neighborhood

  def getNeighborhood(self):
    return self.neighborhood
  
  def getId(self):
    return self.id

  def __iter__(self):
    pass
