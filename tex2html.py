import os
from supportFunctions import convert_line
from myMath import Math
from myItemize import Itemize


def tex_to_html(tex_file, html_file):

    paragraphStyle = "align=\"justify\""
    
    # open tex file and load all lines
    with open(tex_file, 'r') as file:
        lines = file.readlines()

    # set a math environment for when it's needed
    math = Math()
    itemize = Itemize(math)

    # Open the HTML file
    with open(html_file, 'w') as file:

        # these go away when defined in respective class at init
        in_table = False
        in_figure = False

        # iterate over the lines
        for line in lines:
            stripped_line = line.strip()

            # not begin nor end of equation env.
            math.resetActivation()
            itemize.resetActivation()

            # Check for environment start
            if r'\begin{equation' in stripped_line:
                math.activate()
            elif r'\begin{itemize}' in stripped_line:
                itemize.activate()
            elif r'\begin{table}' in stripped_line:
                in_table = True
                activation = True
            elif r'\begin{figure}' in stripped_line:
                in_figure = True
                activation = True

            # write the paragraphs which are not in strange env.
            if not math.in_equation \
                and not itemize.in_itemize \
                and not in_table \
                and not in_figure:
                
                # if the line is empty, write a space
                if stripped_line == "":
                    file.write("\n")
                else:
                    converted_line = convert_line(stripped_line)
                    file.write(f"<p {paragraphStyle}>\n{converted_line}\n</p>\n")


            # end is checked at the end: avoids to include end tag wrongly
            if r'\end{equation' in stripped_line:
                math.deactivation = True
            elif r'\end{itemize' in stripped_line:
                itemize.deactivation = True
            elif r'\end{table}' in stripped_line:
                in_table = False
                deactivation = True
            elif r'\end{figure}' in stripped_line:
                in_figure = False
                deactivation = True

            # when not \begin or \end, but while in math mode, write the line            
            if math.in_equation:
                math.write(file, stripped_line)

            # the check against not math.deactivation avoids to write the line
            # \end{equation} in the output file
            if itemize.in_itemize and not math.deactivation:
                itemize.write(file, stripped_line)


        if math.containsAnEquation:
            math.createScript(file)
            




if __name__ == "__main__":

    # Remove the output.html file if it exists
    if os.path.exists('html/output.html'):
        os.remove('html/output.html')

    tex_to_html('latex/text.tex', 'html/output.html')
