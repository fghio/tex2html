class Table:
    def __init__(
        self, 
        containsATable = False,
        in_table = False,
        in_tabular = False,
        activation = False,
        deactivation = False,
        rows = [],
        caption = ""
    ):
        self.containsATable = containsATable
        self.in_table = in_table
        self.in_tabular = in_tabular
        self.activation = activation
        self.deactivation = deactivation
        self.rows = rows
        self.caption = caption

    def resetActivation(self):
        self.activation = False
        self.deactivation = False

    def activate(self):
        self.in_table = True
        self.activation = True
        self.containsATable = True

    def _write_table(self, file):
        file.write("\n<div class=\"table-container\">\n")
        file.write("<table class=\"table is-bordered is-striped is-hoverable is-fullwidth\"") 
        file.write("style=\"border: 2px solid rgb(140 140 140); font-family: arial, sans-serif; #border-collapse: collapse;\">\n")

        for i, row in enumerate(self.rows):
            file.write("<tr>\n")
            for cell in row:
                if i == 0:
                    file.write(f"<th>{cell}</th>\n")
                else:
                    file.write(f"<td>{cell}</td>\n")
            file.write("</tr>\n")

        file.write("</table>\n")

        if self.caption:
            file.write(f"<p class=\"has-text-centered is-size-6 caption\">{self.caption}</p>\n")

        file.write("</div>\n")

        self.rows = []
        self.caption = ""

    def _fix_math(self, text):
        # Replace $<equation>$ with $$<equation>$$ inside each cell
        if text.count('$') >= 2:
            new_text = ""
            inside_math = False
            for char in text:
                if char == '$':
                    if not inside_math:
                        new_text += "$$"
                        inside_math = True
                    else:
                        new_text += "$$"
                        inside_math = False
                else:
                    new_text += char
            return new_text
        else:
            return text

    def write(self, file, stripped_line):
        # Check for \caption
        if r'\caption{' in stripped_line:
            self.caption = stripped_line[len("\\caption{"):-1].strip()

        # Activate tabular
        elif r'\begin{tabular}' in stripped_line:
            self.in_tabular = True

        # Deactivate tabular
        elif r'\end{tabular}' in stripped_line:
            self.in_tabular = False

        # Collect rows ONLY inside tabular
        elif self.in_tabular and '&' in stripped_line and r'\\' in stripped_line:
            clean_line = stripped_line.replace(r'\\', '').strip()
            cells = [self._fix_math(cell.strip()) for cell in clean_line.split('&')]
            self.rows.append(cells)

        # At the end of table
        if self.deactivation:
            self._write_table(file)
            self.in_table = False


    def createStyle(self,file):
        file.write("<style>\n")
        file.write("th,\n")
        file.write("td {\n")
        file.write("  border: 1px solid rgb(160 160 160);\n")
        file.write("}\n")

        file.write("td, th {\n")
        file.write("  border: 1px solid #dddddd;\n")
        file.write("  text-align: left;\n")
        file.write("  padding: 8px;\n")
        file.write("}\n")

        file.write("tr:nth-child(even) {\n")
        file.write("  background-color: #dddddd;\n")
        file.write("}\n")
        file.write("</style>\n")


