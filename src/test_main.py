from htmlnode import TextNode
from filefunctions import move_files, list_dir_files
import os, shutil
from generatepage import extract_title, generate_page

def main():
    """
    print("Hello World")
    node = TextNode("This is a text node", "bold")
    node.url = "https://www.boot.dev"
    print(node)

    node2 = TextNode("This is not a text node", "bold", "https://www.boot.dev")

    print(node==node2)

    print("File Copy\n")

    #if os.path.exists("./public/public"):
    #    os.rmdir("./public/public")
    #    print("Directory Removed")    
    #os.mkdir ("./public/public")
    #print("Directory Created")

    #for file_name in list_dir_files("./public/static"):
    #    print(f"{file_name[0]}{file_name[1]}")

    print("removing old files if needed")
    #destroy any current files in ./public/public/
    if os.path.exists("./public/public/"):
        shutil.rmtree("./public/public/")
    os.mkdir("./public/public/")
    print("moving files")
    move_files(list_dir_files("./public/static"), "./public/static", "./public/public")
    """

    #test_markdown = "This is **bolded** paragraph\n\n## This is a header\n\nThis is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line"
    
    #try:
    #    print(extract_title(test_markdown))
    #except Exception as inst:
    #    print(inst)

    #print(os.listdir("./github.com/JohnDirewolf/public/"))

    generate_page("./github.com/JohnDirewolf/public/content/index.md", "./github.com/JohnDirewolf/public/template.html", "./github.com/JohnDirewolf/public/public/index.html")


    return

main()