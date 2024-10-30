import os


def tex_to_html(tex_file, html_file):

    paragraphStyle = "align=\"justify\""
    

    def convert_line(line):
        bold_active = False
        italic_active = False
        result = []

        i = 0
        while i < len(line):
            if line[i:i+8] == r'\textbf{':
                result.append('<b>')
                bold_active = True
                i += 8
            elif line[i:i+8] == r'\textit{':
                result.append('<i>')
                italic_active = True
                i += 8
            elif line[i] == '}' and bold_active:
                result.append('</b>')
                bold_active = False
                i += 1
            elif line[i] == '}' and italic_active:
                result.append('</i>')
                italic_active = False
                i += 1
            else:
                result.append(line[i])
                i += 1

        return ''.join(result)

    with open(tex_file, 'r') as file:
        lines = file.readlines()

    # useful key for Equation
    containsAnEquation = False
    eqTagID = 0
    completeEquation = ""

    # Open the HTML file
    with open(html_file, 'w') as file:

        in_equation = False
        in_table = False
        in_figure = False
        
        # iterate over the lines
        for line in lines:
            stripped_line = line.strip()

            activation=False
            deactivation=False

            # Check for environment start
            if r'\begin{equation' in stripped_line:
                in_equation = True
                activation = True
                containsAnEquation = True
                eqTagID = eqTagID +1 
            elif r'\begin{table}' in stripped_line:
                in_table = True
                activation = True
            elif r'\begin{figure}' in stripped_line:
                in_figure = True
                activation = True

            if not in_equation and not in_table and not in_figure:

                # if the line is empty, write a space
                if stripped_line == "":
                    file.write("\n")
                else:
                    converted_line = convert_line(stripped_line)
                    file.write(f"<p {paragraphStyle}>\n{converted_line}\n</p>\n")

            # end is checked at the end: avoids to include end tag wrongly
            if r'\end{equation' in stripped_line:
                deactivation = True
            elif r'\end{table}' in stripped_line:
                in_table = False
                deactivation = True
            elif r'\end{figure}' in stripped_line:
                in_figure = False
                deactivation = True

            # when not \begin or \end, but while in math mode, write the line            
            if in_equation and not activation:
                if not deactivation:
                    completeEquation = completeEquation + " " + stripped_line
                else:
                    print("nowWriting")
                    file.write(f"$${completeEquation} \\tag{ {eqTagID} }$$\n")
                    completeEquation = ""
                    in_equation = False


        if containsAnEquation:
            file.write(f"\n<script id=\"MathJax-script\" async src=\"https://cdn.jsdelivr.net/npm/mathjax@3.0.1/es5/tex-mml-chtml.js\"></script> \n")
            




if __name__ == "__main__":

    # Remove the output.html file if it exists
    if os.path.exists('html/output.html'):
        os.remove('html/output.html')

    tex_to_html('latex/text.tex', 'html/output.html')