from block import Block
from dimension import Dimension
from space import Space

import numpy as np

d1 = Dimension(str)
d2 = Dimension(np.ndarray)
d3 = Dimension(int)

s1 = Space()
s1.add_dimension("name", d1)
s1.add_dimension("data", d2)

s2dimensions = {
  "length": d3
}

s2 = Space(s2dimensions)

s3 = s1 * s2

def calculate_length(point):
  return {"name": point["name"], "length": len(point["name"]), "data": point["data"]}

p1 = {"name": "Tyler", "data": np.ndarray((1, 1))}
p2 = {"name": "Zargham", "data": np.ndarray((3, 3))}

b1 = Block(s1, s3, calculate_length)
p2 = b1.run([p1, p2])

print(p2)