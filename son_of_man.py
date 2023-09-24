

import vulkanese as ve
import bookofjulian as J

class SonOfMan(ve.graph):

    def __init__(self, depth = 0, **kwargs):
        ve.graph.__init__(self, **kwargs)

        # generate our own brain
        self.brain = ve.ai.humanBrain()

        # generate the hierarchy
        if depth < self.maxdepth:
            for i in range(self.fanout):
                self.children += [SonOfMan(depth=depth+1, **kwargs)]


    def run(self, depth = 0,indata):

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