class Dimension:
  def __init__(self, type, constructor=None):
    self.type = type

    if constructor == None:
      self.constructor = type
    else:
      self.constructor = constructor

  def __repr__(self):
    return "Dimension(type=%s, constructor=%s)" % (self.type, self.constructor)