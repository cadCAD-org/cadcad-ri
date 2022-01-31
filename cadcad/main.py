from block import Block
from dimension import Dimension
from space import Space

import numpy as np

# Define some dimensions. d1 and d2 will belong to our first space,
# while d3 will belong to a second space. No constructor functions
# have needed to be specified in my testing thus far.
d1 = Dimension(str)
d2 = Dimension(np.ndarray)
d3 = Dimension(int)

# Our first space (s1) with .add_dimension() used to add d1 and d2
s1 = Space()
s1.add_dimension("name", d1)
s1.add_dimension("data", d2)

# An alternative way to create state dimensions ...
s2dimensions = {
  "length": d3
}

# Our second space (s2) which is instantiated using the above dimensions.
s2 = Space(s2dimensions)

# Our third space (s3) which will serve as the codomain of our block.
s3 = s1 * s2

# Our block logic which gets applied to a point.
def calculate_length(point):
  return {"name": point["name"], "length": len(point["name"]), "data": point["data"]}

# A sample point (p1). It MUST adhere to the dimensions specified in s1
# as that statespace serves as our blocks domain.
p1 = {"name": "Tyler", "data": np.ndarray((1, 1))}

# Our block (b1) which specifies s1 as our domain, s3 as our codomain,
# and calculate_length as our block logic.
b1 = Block(s1, s3, calculate_length)

# Our new point which should satisfy the requirements of s3 though
# there are currently no checks for this.
p2 = b1.run([p1])