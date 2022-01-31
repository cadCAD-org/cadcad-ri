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

# Our block logic which gets applied to a point. At the moment, the
# "logic" is simply to append a new dimension (length) which should
# satisfy the schema requirements of s3 (our codomain). No check
# happens to ensure the generated point doesn't violate the schema
# requirements but it could be added pretty easily.
def calculate_length(point):
  return {"name": point["name"], "length": len(point["name"]), "data": point["data"]}

# A sample point (p1). It MUST adhere to the dimensions specified in s1
# as that statespace serves as our blocks domain.
#
# Notes: If you do not include all keys that were defined in s1, this
# point is seen as invalid. If you include extra keys in your point,
# that too is seen as invalid. Lastly, if you do not use the correct
# datatype as defined in s1, this point is seen as invalid.
#
# Examples (using state schema: {"name": str, "data": numpy.ndarray}):
# {"name": "Tyler"} -- Invalid point (missing key: data)
# {"name": "Tyler", "data": 12} -- Invalid point (type mismatch: data)
# {"name": "Tyler", "data": numpy.ndarray((1, 1))} -- Valid point
# {"name": "Tyler", "data": numpy.ndarray((1, 1)), "a": 1} -- Invalid point (extra key: a)
p1 = {"name": "Tyler", "data": np.ndarray((1, 1))}

# Our block (b1) which specifies s1 as our domain, s3 as our codomain,
# and calculate_length as our block logic.
b1 = Block(s1, s3, calculate_length)

# Our new point which should satisfy the requirements of s3 though
# there are currently no checks for this.
p2 = b1.run([p1])