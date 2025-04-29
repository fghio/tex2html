def convert_line(line):
    bold_active = False
    italic_active = False
    href_active = False
    href_url = ""
    href_text = ""
    collecting_url = False
    collecting_text = False
    
    result = []
    i = 0
    while i < len(line):
        # Handle the href command \href{url}{text}
        if line[i:i+6] == r'\href{':
            href_active = True
            collecting_url = True
            href_url = ""
            href_text = ""
            i += 6
        elif collecting_url and line[i] == '}':
            collecting_url = False
            collecting_text = True
            if i + 1 < len(line) and line[i+1] == '{':
                i += 2  # jump '}' and '{'
            else:
                i += 1  # jump only '}'
        elif collecting_text and line[i] == '}':
            collecting_text = False
            href_active = False
            # add the complete link
            result.append(f'<a href="{href_url}" target="_blank">{href_text}</a>')
            i += 1
        elif collecting_url:
            href_url += line[i]
            i += 1
        elif collecting_text:
            href_text += line[i]
            i += 1
        # other commands to be handled
        elif line[i:i+8] == r'\textbf{':
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
