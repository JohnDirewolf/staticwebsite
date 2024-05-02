import os
from generatepage import extract_title, generate_page, generate_pages_recursive

def main():

    #print(os.getcwd())
    os.chdir("./github.com/JohnDirewolf/staticwebsite")
    #print(os.getcwd())
    #generate_page("./content/index.md", "./template.html", "./public/index.html")
    generate_pages_recursive("./content", "./template.html", "./public")



    return

main()