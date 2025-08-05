def is_tag(pos, html_text):
    if pos + 1 >= len(html_text):  # Check if next char exists
        return False
    next_char = html_text[pos + 1]
    return(
        next_char.isalpha() or  # <div
        next_char == '/' or     # </div
        next_char == '!' or     # <!-- or <!DOCTYPE
        next_char == '?'        # <?xml
    ) 
def read_until_tag(pos, html_text):
    content = ""
    while pos < len(html_text):
        if html_text[pos] == '<' and is_tag(pos, html_text):
            break
        content += html_text[pos]
        
        pos += 1
        
    return content


def read_tag(pos, html_text):
    tag_name = ""
    pos += 1
    while html_text[pos] != ">" :
        tag_name += html_text[pos]
        pos += 1
        
        if pos > len(html_text):
            raise ValueError
            
    return tag_name, pos + 1
    
    




def main():
    html_stack = []
    text = " <html> <p1> hello </p1> </html> "
    indices = [i for i, char in enumerate(text) if char == "<"]
    for i in indices:
        tag, closing_char = read_tag(i, text)
        html_stack.append(tag)
        content = read_until_tag(closing_char, text)
        html_stack.append(content)
    for i in html_stack:
        print(i)



