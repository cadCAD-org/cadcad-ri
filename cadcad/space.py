from dimension import Dimension

class Space:
  def __init__(self, dimensions={}):
    self.dimensions = dimensions

    for key in dimensions:
      if isinstance(dimensions[key], Dimension):
        self.dimensions[key] = dimensions[key]

  def __repr__(self):
    return "Space(dimensions=%s)" % (self.dimensions)

  def __mul__(self, space):
    return Space({**self.dimensions, **space.dimensions})

  def __imul__(self, space):
    return Space({**self.dimensions, **space.dimensions})

  def add_dimension(self, key, value):
    if isinstance(value, Dimension):
      self.dimensions[key] = value