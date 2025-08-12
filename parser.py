import re
from dataclasses import dataclass, field
from typing import List, Optional



intilist = [
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
]
ELEMENT_PARENT_SET = set()

for i in intilist:
    ELEMENT_PARENT_SET.add(i)
    
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
def read_until_tag(pos, html_text, tag):
    content = ""
    while pos < len(html_text):
        if html_text[pos] == '<' and is_tag(pos, html_text):
            break
        content += html_text[pos]
        
        pos += 1
    glyph = " glyph="
    glyph += content.strip()
    tag += glyph

    return html_text, pos + len(glyph), tag


def read_tag(pos, html_text):
    tag_name = ""
    pos += 1
    while html_text[pos] != ">" :
        tag_name += html_text[pos]
        pos += 1
        
        if pos > len(html_text):
            raise ValueError
            
    return tag_name, pos + 1
     
    



def print_tree(node, indent=0):
    prefix = '  ' * indent
    
    print(f"{prefix}- TAG: <{node.tag}>")
    if "glyph" in node.attrs:
        print(f" {prefix}- CONTENT: {node.attrs.get('glyph')}")



    for child in node.children:
        print_tree(child, indent + 1)
def main():
    html_stack = []
    text = " <html> <body> <head> hello </head> </body> <ruby> goodbye </html> "
    pos = 0
    while pos < len(text):
        if text[pos] == "<" and is_tag(pos, text):
            tag, closing_char = read_tag(pos, text)
            text, new_pos, tag = read_until_tag(closing_char, text, tag)
            html_stack.append(tag)
            pos = new_pos  
        else:
            pos += 1 

        
    for i in html_stack:
        print(i)
    read_to_rendertree(html_stack, ELEMENT_PARENT_SET)

@dataclass
class Node:
    tag: Optional['str'] 
    attrs: dict = field(default_factory=dict)
    children: list['Node'] = field(default_factory=list)
    parent: Optional['Node'] = None
def read_to_rendertree(html_stack, parent_List: set):
    current_parent = list()
    current_parent_node = list()   
    current_parent.append("html")
    root = Node("html")
    root.tag = "html"
    root.parent = None
    
    root.attrs = {}
    current_parent_node.append(root)
    current_parent.append("html")
    html_stack = html_stack[1:]
    for el in html_stack:
        tag = ""
        i = 0
        while i < len(el) and el[i] != " ":
            tag += el[i]
            i += 1
        if tag.strip() == "":
            continue

        node = Node(tag)
        
        node.parent  = current_parent[-1]
        if el.startswith("/"):
            if current_parent_node:
                current_parent_node.pop()
            continue

        if not current_parent_node:
    # This means there's no valid parent to attach to — skip or handle gracefully
            break
        current_parent_node[-1].children.append(node)
        

        

        if tag in parent_List:
            current_parent.append(el)
            current_parent_node.append(node)
        node.attrs = attributes_to_dict(el)
        
        
    print_tree(root)


        
        

    


