class Math:
    def __init__(
        self, 
        containsAnEquation = False,
        eqTagID = 0,
        completeEquation = "",
        in_equation = False,
        activation = False,
        deactivation = False,
    ):
        self.containsAnEquation = containsAnEquation
        self.eqTagID = eqTagID
        self.completeEquation = completeEquation
        self.in_equation = in_equation
        self.activation = activation
        self.deactivation = deactivation

    def resetActivation(self):
        self.activation = False
        self.deactivation = False

    def activate(self):
        self.in_equation = True
        self.containsAnEquation = True
        self.eqTagID = self.eqTagID +1 
        self.activation = True

    def write(self, file, stripped_line):
        if not self.activation:
            if not self.deactivation:
                self.completeEquation = self.completeEquation + " " + stripped_line
            else:
                file.write(f"$${self.completeEquation} \\tag{ {self.eqTagID} }$$\n")
                self.completeEquation = ""
                self.in_equation = False

    def createScript(self,file):
        file.write(f"\n<script id=\"MathJax-script\" async src=\"https://cdn.jsdelivr.net/npm/mathjax@3.0.1/es5/tex-mml-chtml.js\"></script> \n")
