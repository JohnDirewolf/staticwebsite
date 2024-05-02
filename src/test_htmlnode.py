from htmlnode import HTMLNode, LeafNode, ParentNode, TextNode, text_node_to_html_node, split_nodes_delimiter

def main():
    text_types = [
        "text",
        "bold",
        "italic",
        "code",
        "link",
        "image"
    ]
    
    print("HTMLNode Test")
    HTMLChild = HTMLNode(tag="underline", value="true", props={"href": "https://boot.dev"})
    HTML1 = HTMLNode("bold","value here" , HTMLChild, {"href": "https://www.google.com", "target": "_blank"})
    print(HTML1.props_to_html())
    print(HTML1)

    #test a LeafNode

    print("\nLeafNode Test")
    pLeaf = LeafNode("p", "This is a paragraph of text.")
    print(pLeaf.to_html())
    aLeaf = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    print(aLeaf.to_html())
    try:
        badLeaf = LeafNode("b", "Text here", None)
        print(badLeaf.to_html())
    except Exception as inst:
        print(type(inst))
        print(inst.args)

    print("\nParentNode Test")
    try:
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        print(node.to_html())
    except Exception as inst:
        print(inst.args)

    print("\nParentNode Nested Test")
    nested_node = ParentNode(
        "div",
        [
            LeafNode("p", "Nesting Time!!!"),
            node,
            LeafNode("a", "Click Here!", {"href": "https://www.google.com"})
        ],                     
    )

    print(nested_node.to_html())


    print("\nTestNode To HTMLNode Test")
    
    #html_node = text_node_to_html_node(TextNode("Hello World", "bold"))
    #print(html_node.to_html())
    try:
        for type in range(0, 6):
            #print(text_types[type])
            url = None
            if text_types[type] == "image":
                url = {"url": "http://url.google.com"}
            elif text_types[type] == "link":
                url = {"href": "http://href.boot.dev"}
            html_node = text_node_to_html_node(TextNode("Hello World", text_types[type], url))
            print(html_node.to_html())
    except ValueError as inst:
        print(inst.args)

    print("\nTest of splitting nodes")

    text_type_text = "text"
    text_type_code = "code"
    #node = TextNode("This is text with a `code block` word", text_type_text)
    old_node = LeafNode("p", "Hello World")
    print(split_nodes_delimiter(old_node, "`", text_type_text))
    old_node = TextNode("This is text with a `code block` word", "code")
    print(split_nodes_delimiter(old_node, "`", text_type_code))
    old_node = TextNode("This is text with a **bold block** word", "bold")
    print(split_nodes_delimiter(old_node, "**", "bold"))
    old_node = TextNode("This is text with a *italic block* word", "italic")
    print(split_nodes_delimiter(old_node, "*", "italic"))
    try:
        old_node = TextNode("This is text with an unclosed tag *italic block word", "italic")
        print(split_nodes_delimiter(old_node, "*", "italic"))
    except Exception as inst:
        print(inst.args)
    old_node = LeafNode("b", "Goodbye World")
    print(split_nodes_delimiter(old_node, "`", "bold"))

    pass
pass


main()

