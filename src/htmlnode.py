import re

#define some constants
#block_types
block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

#List of the block types so I can iterate through them
block_types = [
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list
]

###### HTML Node Classes ######

class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag  
        self.value = value
        self.children = children
        self.props = props
        pass

    def to_html(self):
        raise NotImplementedError
        pass

    def props_to_html(self):
        html = ""
        if self.props != {}:
            for prop in self.props:
                html = html + " " + prop + '="' + self.props[prop] + '"' 
        return html
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    pass

class LeafNode(HTMLNode):
    
    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag, value, None, props)
        pass

    def to_html(self):
        if self.value == None:
            raise ValueError("No Value Given")
        if self.tag == None:
            return self.value
        if self.tag == "p" or self.tag == "b" or self.tag =="i" or self.tag =="code":
            return f"<{self.tag}>{self.value}</{self.tag}>"
        if self.tag == "a":
            return f'<a href="{self.props}">{self.value}</a>'
        if self.tag == "img":
            return f'<img src="{self.props}" alt="{self.value}"></img>'
        raise ValueError("Invalid Leaf Node Tag")

    pass

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag, None, children, props)
        pass

    def to_html(self):
        if self.tag == None or self.tag == "":
            raise ValueError("No Tag Provided")
        if self.children == None or self.children == []:
            raise ValueError("No Children Given")
        html = f"<{self.tag}>"
        for child in self.children:
            html = html + child.to_html()
        html = html + f"</{self.tag}>"
        return html

    pass

class TextNode:
    def __init__(self, text, text_type, *args) -> None:
        self.text = text
        self.text_type = text_type
        self.url = None
        #print(f"args: {args}")
        if len(args) >= 1:
            self.url = args[0]
        pass

    def __eq__(self, value: object) -> bool:
        if self.text == value.text and self.text_type == value.text_type and self.url == value.url:
            return True
        return False

    def __repr__(self) -> str:
        if self.url == None:
            return f'TextNode("{self.text}", {self.text_type})'
        return f'TextNode("{self.text}", {self.text_type}, {self.url})'

pass

def text_node_to_html_node(text_node):
    text_types = {
        "text": None,
        "bold": "b",
        "italic": "i",
        "code": "code",
        "link": "a",
        "image": "img"
    }
    
    #print(text_node)

    prop = None
    if text_node.text_type == "link" or text_node.text_type =="image":
        prop = text_node.url
    return LeafNode(text_types[text_node.text_type], text_node.text, prop)
    
pass

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    if type(old_nodes) != TextNode:
        new_nodes.append(old_nodes)
    else:
        split_of_old_nodes = old_nodes.text.split(delimiter)
        #print(f"split_of_old_nodes: {split_of_old_nodes}: {len(split_of_old_nodes)}")
        if len(split_of_old_nodes) % 2 == 0:
             raise ValueError("Invalid markdown, formatted sectoin not close. Do you need to escape a special character?")
        for i in range(0, len(split_of_old_nodes)):
            if split_of_old_nodes[i] != "": #skip empty sectoins
                if i % 2 == 0:
                    new_nodes.append(TextNode(split_of_old_nodes[i], "text"))
                else:
                    new_nodes.append(TextNode(split_of_old_nodes[i], text_type))
    #print(f"new nodes in def: {new_nodes}")
    return new_nodes

pass

##### Markdown Extraction Functoins #####

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    image_tups = extract_markdown_images(old_nodes.text)
    if len(image_tups) == 0:
        #print("No further Image found")
        return [old_nodes]
    split_nodes = old_nodes.text.split(f"![{image_tups[0][0]}]({image_tups[0][1]})", 1)
    new_nodes.append(TextNode(split_nodes[0], "text"))
    new_nodes.append(TextNode(image_tups[0][0], "image", image_tups[0][1]))
    if split_nodes[1] != "":
        rec_nodes = split_nodes_image(TextNode(split_nodes[1], "text"))
        for each_node in rec_nodes:
            new_nodes.append(each_node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    link_tups = extract_markdown_links(old_nodes.text)
    if len(link_tups) == 0:
        # print("No further links found")
        return [old_nodes]
    split_nodes = old_nodes.text.split(f"[{link_tups[0][0]}]({link_tups[0][1]})", 1)
    new_nodes.append(TextNode(split_nodes[0], "text"))
    new_nodes.append(TextNode(link_tups[0][0], "link", link_tups[0][1]))
    if split_nodes[1] != "":
        rec_nodes = split_nodes_link(TextNode(split_nodes[1], "text"))
        for each_node in rec_nodes:
            new_nodes.append(each_node)
    return new_nodes

def text_to_textnodes(text):
    image_nodes = split_nodes_image(TextNode(text, "text"))
    # print(image_nodes)
    new_nodes = []
    for each_node in image_nodes:
        #print(each_node)
        link_nodes = split_nodes_link(each_node)
        for each_node in link_nodes:
            new_nodes.append(each_node)
    
    bold_nodes = []
    for each_new_node in new_nodes:
        #print(f"each_new_node: {each_new_node}")
        if each_new_node.text_type != "text":
            bold_nodes.append(each_new_node)
        else:
            new_bold_nodes = []
            new_bold_nodes = split_nodes_delimiter(TextNode(each_new_node.text, "text"), "**", "bold")
            for new_bold_node in new_bold_nodes:
                bold_nodes.append(new_bold_node)
    
    italic_nodes = []
    for each_bold_node in bold_nodes:
        #print(f"each_new_node: {each_new_node}")
        if each_bold_node.text_type != "text":
            italic_nodes.append(each_bold_node)
        else:
            new_italic_nodes = []
            new_italic_nodes = split_nodes_delimiter(TextNode(each_bold_node.text, "text"), "*", "italic")
            for new_italic_node in new_italic_nodes:
                italic_nodes.append(new_italic_node)
    
    code_nodes = []
    for each_italic_node in italic_nodes:
        #print(f"each_italic_node: {each_italic_node}")
        if each_italic_node.text_type != "text":
            code_nodes.append(each_italic_node)
        else:
            new_code_nodes = []
            new_code_nodes = split_nodes_delimiter(TextNode(each_italic_node.text, "text"), "`", "code")
            #print(f"Just after split new_code_nodes in text_to_textnodes: {new_code_nodes}")
            for new_code_node in new_code_nodes:
                code_nodes.append(new_code_node)

    return(code_nodes)

##### MARKDOWN BLOCK FUNCTIONS ##### 

def markdown_to_blocks(markdown):
    block_strings = []
    stripped_strings = []

    block_strings = markdown.split("\n\n")
    for block_string in block_strings:
        if block_string != "":
            stripped_strings.append(block_string.strip("\n "))
    return stripped_strings

def block_to_block_type(block):
    #paragraph is apparently the default
    block_type = block_type_paragraph
    
    #check for heading
    pound = " "
    for i in range(0, 6):
        pound = "#" + pound
        if block[0:i + 2] == pound:
            return block_type_heading
    #check for code block
    code_ticks = "```" 
    if block[0:3] == code_ticks and block[-3::] == code_ticks:
        return block_type_code 
    #for the next three we are doing a line by line check, so split
    line_check = block.split("\n")
    #check for quote block
    found = True #We assume we have all the line types here, if any fail they change to false
    found_quote = True
    found_ulist = True
    found_olist = True
    for line in line_check:
        if line[0] != ">":
            found_quote = False #If ANY line does not start with > then it is NOT a quote
        if line[0] != "*" and line[0] != "-":
            found_ulist = False #If ANY line does not start with * or - it is not an unordered list
        if re.search("[0-9]. ", line[0:3]) == None:
            found_olist = False #If ANY line does not start with 0-9 a dot and a space then itis not an ordered list
    if found_quote:
        return block_type_quote
    if found_ulist:
        return block_type_unordered_list
    if found_olist:
        return block_type_ordered_list

    #we default to paragraph
    return block_type

def to_html_paragraph(markdown):
    markdown_split = markdown.split("\n")

    html_block = ""

    for each_line in markdown_split:
        html_block = html_block + each_line + "<br/>"

    #remove the last br
    html_block = html_block[0:-5:]

    #process text for inline style
    inline_html_block = ""
    for node in text_to_textnodes(html_block):
        inline_html_block = inline_html_block + text_node_to_html_node(node).to_html()

    html_block = f"<p>{inline_html_block}</p>"
    return html_block

def to_html_heading(markdown):
    'count and remove the #'
    pound_count = 0
    
    for i in markdown[0:6]:
        if i == "#":
            pound_count += 1

    #done checking # so stripping
    markdown = markdown.lstrip("# ")

    #process the text for inline style
    inline_markdown = ""
    
    for node in text_to_textnodes(markdown):
        inline_markdown = inline_markdown + text_node_to_html_node(node).to_html()

    return f"<h{pound_count}>{inline_markdown}</h{pound_count}>"

def to_html_blockquote(markdown):
    html_block = ""

    #split the quote at the linebreaks as we will need to strip the leading > each line and add a <br/>
    markdown_split = markdown.split("\n")
    
    for each_line in markdown_split:
        html_block = html_block + each_line.lstrip("> ") + "<br/>"
    
    #remove the last br
    html_block = html_block[0:-5:]

    inline_markdown = ""
    #process the inline styles
    for node in text_to_textnodes(html_block):
        inline_markdown = f"{inline_markdown}{text_node_to_html_node(node).to_html()}"

    return f"<blockquote>{inline_markdown}</blockquote>"

def to_html_code(markdown):

    markdown = markdown.strip("```")
    #Not sure if there is actually an inline code as it is the code itself unprossessed, but will add a process, but probably disable it.
    inline_html_block = ""
    for node in text_to_textnodes(markdown):
        inline_html_block = inline_html_block = text_node_to_html_node(node).to_html()

    return f"<pre><code>{inline_html_block}</code></pre>"

def to_html_ulist(markdown):
    #split on \n and add <li>
    html_block = ""
    
    list_split = markdown.split("\n")
    #print(list_split)
    for list_item in list_split:
        list_item = list_item[1::].lstrip(" ")
        #inline style processing for each item
        #processor does not like f statments with the functions so breaking down
        inline_markdown = text_to_textnodes(list_item)
        #clear list_item so we can rebuild with the inline_markdown
        list_item = ""
        for node in inline_markdown:
            list_item = list_item + text_node_to_html_node(node).to_html()  
        
        html_block = html_block + f"<li>{list_item}</li>"

    html_block = "<ul>" + html_block + "</ul>"
    return html_block

def to_html_olist(markdown):
    #split on \n and add <li>
    html_block = ""

    list_split = markdown.split("\n")
    for list_item in list_split:
        list_item = list_item[2::].lstrip(" ")
        #inline style processing for each item
        #processor does not like f statments with the functions so breaking down
        inline_markdown = text_to_textnodes(list_item)

        #print(inline_markdown)

        #clear list_item so we can rebuild with the inline_markdown
        list_item = ""
        for node in inline_markdown:
            list_item = list_item + text_node_to_html_node(node).to_html()  
        
        html_block = html_block + f"<li>{list_item}</li>"

    html_block = "<ol>" + html_block + "</ol>"

    return html_block

def markdown_to_html_node(markdown):
    htmldocument = ""

    #outer div wrapper
    htmldocument = "<div>"

    # First split the markdown into discreet blocks
    markdown_blocks = markdown_to_blocks(markdown)

    for each_block in markdown_blocks:
        each_block_type = block_to_block_type(each_block)
        if each_block_type == block_type_paragraph:
            htmldocument = htmldocument + to_html_paragraph(each_block)
        elif each_block_type == block_type_heading:
            htmldocument = htmldocument + to_html_heading(each_block)
        elif each_block_type == block_type_quote:
            htmldocument = htmldocument + to_html_blockquote(each_block)
        elif each_block_type == block_type_code:
            htmldocument = htmldocument + to_html_code(each_block)
        elif each_block_type == block_type_unordered_list:
            htmldocument = htmldocument + to_html_ulist(each_block)
        elif each_block_type == block_type_ordered_list:
            htmldocument = htmldocument + to_html_olist(each_block)
        else:
            htmldocument = htmldocument

    #close outer div wrapper
    htmldocument = htmldocument + "</div>"

    #print(htmldocument)
    return htmldocument
        