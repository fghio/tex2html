from myMath import Math
from myFigure import Figure

class Itemize:
    def __init__(
        self, 
        math : Math,
        figure : Figure,
        in_itemize = False,
        activation = False,
        deactivation = False,
        isEnumeration = False,
        counter = 0
    ):
        self.math = math
        self.figure = figure
        self.in_itemize = in_itemize
        self.activation = activation
        self.deactivation = deactivation
        self.isEnumeration = isEnumeration
        self.counter = counter

    def resetActivation(self):
        self.activation = False
        self.deactivation = False

    def activate(self):
        self.in_itemize = True
        self.activation = True

    def write(self, file, stripped_line):
        
        if self.activation:
            if self.isEnumeration:
                file.write(f"<ol>\n")
            else:
                file.write(f"<ul>\n")
    
            file.write(f"<li>")

        elif self.deactivation:
            file.write(f"</li>\n")
            
            if self.isEnumeration:
                file.write(f"</ol>\n")
            else:
                file.write(f"</ul>\n")
            self.counter = 0
            self.in_itemize = False

        else:
            if not self.math.in_equation and not self.figure.in_figure:

                if self.counter == 0:
                    stripped_line = stripped_line[len("\\item"):].strip()
                    file.write(f"{stripped_line}")
                    self.counter += 1
                    
                else:
                    if stripped_line.startswith("\\item"):
                        stripped_line = stripped_line[len("\\item"):].strip()
                        file.write(f"</li>\n")
                        file.write(f"<li>{stripped_line}")
                    else:  
                        file.write(f" {stripped_line}")
