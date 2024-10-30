class Itemize:
    def __init__(
        self, 
        in_itemize = False,
        activation = False,
        deactivation = False,
    ):
        self.in_itemize = in_itemize
        self.activation = activation
        self.deactivation = deactivation

    def resetActivation(self):
        self.activation = False
        self.deactivation = False

    def activate(self):
        self.in_itemize = True
        self.activation = True

    def write(self, file, stripped_line):
        if self.activation:
            file.write(f"<ul>\n")
        elif self.deactivation:
            file.write(f"</ul>\n")
        else:
            file.write(f"<li>this will be an item</li>\n")
        
