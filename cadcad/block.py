class Block():
  def __init__(self, domain, codomain, fn):
    self.domain = domain
    self.codomain = codomain
    self.fn = fn

  def __repr__(self):
    return "Block(domain=%s, codomain=%s, fn=%s)" % (self.domain, self.codomain, self.fn)

  def do_keys_match(self, points):
    return all(self.domain.dimensions.keys() == p.keys() for p in points)

  def do_types_match(self, points):
    for p in points:
      for key in p:
        if self.domain.dimensions[key].type != type(p[key]):
          return False

    return True

  def check_points(self, points):
    if self.do_keys_match(points):
      if self.do_types_match(points):
        return True
      else:
        raise TypeError("Point type mismatch.")
    else:
      raise Exception("Point key mismatch.")

  def run(self, points):
    try:
      self.check_points(points)
      return list(map(self.fn, points))
    except (Exception, TypeError) as e:
      print("Invalid point(s): %s" % (e))
      
