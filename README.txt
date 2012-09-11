(I expect this README file to live in a directory called PyMMT, next to things like actuators.py and tracker.py. If that's how it is, great! You're looking at the right file!)

This directory contains a Python package (and some Java it relies on) which provides classes/functions to help control the "morphable mirror telescope" (MMT), a big flexible telescope mirror. It also contains a Python script that presents a user interface with buttons and stuff for communicating with the other hardware components (a laser tracker and a set of linear actuators).

I've tried to document everything pretty well, both by commenting my code and by writing the files in the PyMMT/help directory. Check that out if you're new -- hopefully, this is arranged so that any technically literate person who's fairly good with Python can go from never having seen the MMT project to having a pretty good understanding of it by just looking at the things in this directory.

The help directory contains:
 - totally_new.txt: fills in basic background information.
 - images/: contains a bunch of pictures/illustrations of various parts of the project.
 - installation.txt: tells you what you'll need to get this package working.
 - py4j.txt: a short introduction to Py4J, a library we use to use Java stuff from Python.
 - how_to_not_break_anything.txt: how to treat the hardware right.
 - tracker.txt: about the FARO laser tracker.
 - actuators.txt: about the actuators and how we control them.
 - actuator_protocol.pdf: describes the communications protocol used by the actuator-controlling boards.
 - d2xx.txt: describes what little I know of the D2XX USB-to-serial setup.