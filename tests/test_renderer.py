# Tests basic renderer operation by running the renderers sample
# rendering.

import os
import sys
sys.path.append(os.path.abspath('..'))

import p5py as p

p.sketch._initialize()
p.sketch._run()
exit()
