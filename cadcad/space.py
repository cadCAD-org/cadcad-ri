from dimension import Dimension

class Space:
  def __init__(self, name):
    self.name = name
    self.dimensions = {}

  def __repr__(self):
    return "Space(name=%s, dimensions=%s" % (self.name, self.dimensions)

  def add_dimension(self, key, type, constructor):
    self.dimensions[key] = Dimension(type, constructor)
    return self.dimensions[key]

  def get_dimensions(self):
    return self.dimensions

  def remove_dimension(self, key):
    self.dimensions.pop(key)
    return self.dimensions