# This subpackage holds a bunch of functions culminating in the
# "recompute" function, which solves the following problem: if you
# have a rigid structure whose shape is known but position is not, and
# you are told the positions of three points on that structure, find
# the positions of several other points on the structure.
#
# For example, you know what a face looks like. If I tell you where
# somebody's eyes and the tip of their nose are, you should be able to
# tell me the positions of their ears, mouth, chin, etc.
#
# Similarly, if I give you a list of (name, x, y, z) quadruplets,
# describing the positions of various points in one coordinate system,
# and then I give you three quadruplets corresponding to the positions
# of some of those points in a different coordinate system, you should
# be able to figure out how to transform all the rest of the points
# into the new system.
#
# But you don't have to, because I already did.

from . import repositioning
from . import mathystuff
from . import io

from .io import save, load
from .repositioning import recompute
