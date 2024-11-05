class Table:
    def __init__(
        self, 
        containsATable = False,
        in_table = False,
        activation = False,
        deactivation = False,
        firstLine = True,
        tableName = "",
        caption = ""
    ):
        self.containsATable = containsATable
        self.in_table = in_table
        self.activation = activation
        self.deactivation = deactivation
        self.tableName = tableName
        self.caption = caption 

    def resetActivation(self):
        self.activation = False
        self.deactivation = False

    def activate(self):
        self.in_table = True
        self.activation = True
        self.containsATable = True
        self.firstLine = True


    def write(self, file, stripped_line):
        if self.activation:
            file.write(f"\n<center>\n")
            file.write(f"<table style=\"width:80%;\">\n")
            self.activation = False

        elif self.deactivation:
            file.write(f"</table>\n")
            file.write(f"</center>\n")
            self.deactivation = False
            self.in_table = False

        else:
            if "\\centering" not in stripped_line \
            and "\\begin{tabular" not in stripped_line \
            and "\\end{tabular" not in stripped_line \
            and "\\hline" not in stripped_line:
            
                file.write("<tr>\n")
                columns = stripped_line.split('&')
                for column in columns:
                    column = column.strip().replace('\\', '').replace('$', '')
                    # Handle subscript notation
                    while '_' in column:
                        start = column.index('_')
                        if column[start+1] == '{':
                            end = column.find('}', start)
                            if end == -1:
                                break
                            subscript = column[start+2:end]
                            column = column[:start] + '<sub>' + subscript + '</sub>' + column[end+1:]
                        else:
                            subscript = column[start+1]
                            column = column[:start] + '<sub>' + subscript + '</sub>' + column[start+2:]
                    if self.firstLine:
                        file.write(f"  <th>{column}</th>\n")
                    else:
                        file.write(f"  <td>{column}</td>\n")

                file.write("</tr>\n")
                self.firstLine = False



    def createStyle(self,file):
        file.write("<style>\n")
        file.write("table {\n")
        file.write("  border: 2px solid rgb(140 140 140);\n")
        file.write("  font-family: arial, sans-serif;\n")
        file.write("  #border-collapse: collapse;\n")
        file.write("}\n")

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


        
        


'''
###### LATEX

\begin{table}[]
\centering
\begin{tabular}{l c c c l l l}
\hline
Patch  & $U_x$ [m/s] & $p$ [Pa] & $T_{in}$ [K] & $Y_{C_8H_18}$ [-]  & $Y_{O_2}$ [-] & $Y_{N_2}$ [-] \\
\hline
\hline
Inlet  & 3.0         & -        & 1000         &                    &               &               \\
Outlet & -           & 101325   & -            &                    &               &               \\
\hline
\end{tabular}
\end{table}



###### HTML

<center>
<table style="width:80%;">
  <tr>
    <th>Company</th>
    <th>Contact</th>
    <th>Country</th>
  </tr>
  <tr>
    <td>Alfreds Futterkiste</td>
    <td>Maria Anders</td>
    <td>Germany</td>
  </tr>
  <tr>
    <td>Centro comercial Moctezuma</td>
    <td>Francisco Chang</td>
    <td>Mexico</td>
  </tr>
</table>
</center>
'''
