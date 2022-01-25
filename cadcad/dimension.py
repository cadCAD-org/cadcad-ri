class Dimension:
  def __init__(self, type, constructor):
    self.type = type
    self.constructor = constructor

  def __repr__(self):
    return "Dimension(type=%s, constructor=%s)" % (self.type, self.constructor)