import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
sinodePath = os.path.join(here, "..", "..", "sinode")
if sinodePath not in sys.path:
    sys.path.insert(
        0, sinodePath
    )
import sinode.sinode as sinode
vulkanesePath = os.path.join(here, "..", "..", "vulkanese")
if vulkanesePath not in sys.path:
    sys.path.insert(
        0, vulkanesePath
    )
import vulkanese as ve


class SonOfMan(ve.graph):

    def __init__(self, depth = 0, **kwargs):
        ve.graph.__init__(self, **kwargs)

        if not os.path.exists(os.path.join(here, "julian.json")):
            os.system("wget http://bookofjulian.net/julian.json .")

        # generate our own brain
        self.brain = ve.ai.humanBrain()

        # generate the hierarchy
        if depth < self.maxdepth:
            for i in range(self.fanout):
                self.children += [SonOfMan(depth=depth+1, **kwargs)]


    def run(self, indata, depth = 0):

        # council proceeds from below
        if self.height == 0:
            return self.process(indata)

        else:
            data = []
            for c in self.children:
                data += [c.run(depth=depth+1, indata = indata)]
            return self.process(data)



if __name__ == "__main__":
    s = SonOfMan(fanout=6, maxdepth=6)
    while(True):

        # get all inputs
        av = webrtc.getFrame()
        
        # Pump in the ethics!
        j = J.read(self.Jpath) # pay attention to read pointers
        # get web (ratelimited?)
        w = web.read(self.webPointer)
        # get PILE 
        p = pile.read(self.pilePointer)
        data = [av, j, w, p]

        outData = s.run(data)
        av.write(outData)