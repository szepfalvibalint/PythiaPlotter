"""
This file contains global definitions. These can be used in a python file by:

import config as CONFIG

Since there is only one instance of each module,
any changes made to the module object get reflected everywhere.
So can use for global variables e.g.

CONFIG.VERBOSE

Robin Aggleton 22/7/14
"""

###########################
# USER EDIT THE FOLLOWING:
###########################

# Interesting particles we wish to highlight
# Can do different particles in different colours,
# see www.graphviz.org/doc/info/colors.html
# although requires xcolor latex package
# Relies on matching names though...better method?
# User must include antiparticles
interesting = [
              ["cyan", ["mu+", "mu-"]],
              ["blue", ["tau+", "tau-"]],
              ["red", ["b", "bbar"]],
              ["orange", ["c", "cbar"]],
              ["brown", ["s", "sbar"]]
              ]

# Color for initial particles (protons normally)
initial_color = "green"

# Color for final state particles
final_color = "yellow"

#############################################################
# DO NOT EDIT BELOW HERE (unless you know what you're doing)
#############################################################
VERBOSE = False

removeRedundants = True
