from myMath import Math

class Itemize:
    def __init__(
        self, 
        math : Math,
        in_itemize = False,
        activation = False,
        deactivation = False,
        counter = 0
    ):
        self.math = math
        self.in_itemize = in_itemize
        self.activation = activation
        self.deactivation = deactivation
        self.counter = counter

    def resetActivation(self):
        self.activation = False
        self.deactivation = False

    def activate(self):
        self.in_itemize = True
        self.activation = True

    def write(self, file, stripped_line):
        
        if self.activation:
            file.write(f"<ul>\n")
            file.write(f"<li>")
                   
        elif self.deactivation:
            file.write(f"</li>\n")
            file.write(f"</ul>\n")
            self.counter = 0

        else:
            if not self.math.in_equation:

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

                
                    
                
        
