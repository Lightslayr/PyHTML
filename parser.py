import re
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Node:
    tag: str
    attrs: Optional[List[str]] = field(default_factory=list)
    children: Optional[List[str]] = field(default_factory=list)
    parent: Optional['Node'] = None

elements_with_children = set(
    'a', 'abbr', 'address', 'article', 'aside', 'audio', 'b', 'bdi', 'bdo', 'blockquote', 
    'body', 'button', 'canvas', 'caption', 'cite', 'code', 'colgroup', 'data', 'datalist', 
    'dd', 'del', 'details', 'dfn', 'dialog', 'div', 'dl', 'dt', 'em', 'fieldset', 
    'figcaption', 'figure', 'footer', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head', 
    'header', 'hgroup', 'html', 'i', 'iframe', 'ins', 'kbd', 'label', 'legend', 'li', 
    'main', 'map', 'mark', 'menu', 'meter', 'nav', 'noscript', 'object', 'ol', 'optgroup', 
    'option', 'output', 'p', 'picture', 'pre', 'progress', 'q', 'rp', 'rt', 'ruby', 's', 
    'samp', 'script', 'section', 'select', 'small', 'span', 'strong', 'style', 'sub', 
    'summary', 'sup', 'svg', 'table', 'tbody', 'td', 'template', 'textarea', 'tfoot', 
    'th', 'thead', 'time', 'title', 'tr', 'u', 'ul', 'var', 'video'
)
def attributes_to_dict(html_tag):
    attr_pattern = r'([a-zA-Z_-]+)\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+))|\b([a-zA-Z_-]+)\b'
    matches = re.finditer(attr_pattern, html_tag)
    
    attrs_dict = {}
    for match in matches:
        if match.group(1):  
            name = match.group(1)
            value = match.group(2) or match.group(3) or match.group(4)
            attrs_dict[name] = value
        elif match.group(5):  
            attrs_dict[match.group(5)] = True  
    return attrs_dict
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
    text = " <html> <img src=https.com/> <p1> hello </p1> </html> "
    indices = [i for i, char in enumerate(text) if char == "<"]
    for i in indices:
        tag, closing_char = read_tag(i, text)
        html_stack.append(tag)
        content = read_until_tag(closing_char, text)
        html_stack.append(content)
    for i in html_stack:
        print(i)



