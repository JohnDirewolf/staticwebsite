import os
from generatepage import extract_title, generate_page

def main():

    #print(os.getcwd())
    os.chdir("./github.com/JohnDirewolf/staticwebsite")
    #print(os.getcwd())
    generate_page("./content/index.md", "./template.html", "./public/index.html")
    return

main()