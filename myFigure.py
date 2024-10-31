class Figure:
    def __init__(
        self, 
        in_figure = False,
        activation = False,
        deactivation = False,
        figureName = "",
        caption = "",
        size = 1080
    ):
        self.in_figure = in_figure
        self.activation = activation
        self.deactivation = deactivation
        self.figureName = figureName
        self.caption = caption 
        self.size = size

    def resetActivation(self):
        self.activation = False
        self.deactivation = False

    def activate(self):
        self.in_figure = True
        self.activation = True

    def write(self, file, stripped_line):
        
        if r'\includegraphics' in stripped_line:
            startFigPath = stripped_line.find("{") + 1
            endFigPath = stripped_line.find("}")
            self.figureName = stripped_line[startFigPath:endFigPath].strip()

#            startDim = stripped_line.find("[") + 1
#            endFigDim = stripped_line.find("]")
            self.size = 900
            
        if r'\caption{'  in stripped_line:
            self.caption = stripped_line[len("\\caption{"):-1].strip()

        # at the end, let's write the figure
        if self.deactivation:

            file.write(f"\n<img src=\"{self.figureName}\" ")
            file.write(f"class=\"box px-0 py-0 ml-auto mr-auto\" ")
            file.write(f"width=\"{self.size}\" ")
            file.write(f"title=\"{self.caption}\" ")
            file.write(f"alt=\"{self.caption}\">\n")

            #file.write(f"<p class=\"has-text-centered is-size-6 caption\">")
            #file.write(f"{self.caption}</p>\n")

            self.in_figure = False
        


'''
example:

<img src="./assets/images/spreadsheet/firstRowListaMovimenti.webp" 
    class="box px-0 py-0 ml-auto mr-auto" 
    width="1080" 
    title="A screenshot." 
    alt="A screenshot.">

<p class="has-text-centered is-size-6 caption">A screenshot.</p>

'''
