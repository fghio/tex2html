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
        elif line[i] == '$':
            result.append('$$')
            i += 1
        else:
            result.append(line[i])
            i += 1

    return ''.join(result)
