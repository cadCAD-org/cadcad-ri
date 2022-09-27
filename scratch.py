from cadcad.points import Point, block
from cadcad.spaces import Real, space


@space
class MySavanah:
    savanah: Savanah
    real: Real


Point(Savanah, {'prey_population': 10, 'predator_population': 5})

MS = Savanah + Real
MS = Savanah * Real

@block
def fun(point_domain: Point[Savanah]) -> Point[Savanah]:
    ...

A B C D

A -> (B | C) -> D


MySavanah : Savanah | Real -> Savanah + Real -> MySavanah


Real^3:

@space
class 3-Real:
    my_real: Real
    real: Real
    real: Real



# Spaces have to be collection of dimensions.
# Dimension is a pair name (str) and type|Space
# Spaces have to +, *, ^, .name, .dimensions, deepcopy, rename_dims, is_empty, unroll_schema, is_equivalent
# Spaces must have constraints
