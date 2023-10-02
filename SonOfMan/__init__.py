import os 
import sys
here = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(
    0, os.path.join(here, "..", "..", "sinode")
)
import sinode.sinode as sinode
sys.path.insert(
    0, os.path.join(here, "..", "..", "vulkanese")
)
import vulkanese as ve