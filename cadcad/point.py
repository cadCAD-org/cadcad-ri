class Point:
  def __init__(self, space, point):
    self.space = space
    self.point = point

  def __repr__(self):
    return "Point(space=%s)" % self.space