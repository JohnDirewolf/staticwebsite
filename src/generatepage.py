from htmlnode import markdown_to_html_node
from filefunctions import list_dir_files 
import os

##### Generate Page #####

# Extract Title Function

def extract_title(markdown):
    markdown_split = markdown.split("\n\n")

    for each_line in markdown_split:
        if each_line[0:2:] == "# ":
            return each_line[2::]
    raise Exception("All pages need a single h1 header")
    
    pass

def generate_page(from_path, template_path, dest_path):

    #Print a message to console
    print(f"<<< Generating page from {from_path} to {dest_path} using {template_path} >>>\n")

    #Read markdown file
    file_markdown = open(from_path)
    file_markdown_contents = file_markdown.read()
    file_markdown.close()

    #Read the template file
    file_template = open(template_path)
    file_template_contents = file_template.read()
    file_template.close()

    #Convert markdown file to HTML
    HTML_to_add = markdown_to_html_node(file_markdown_contents)

    #Extract the title
    page_title = extract_title(file_markdown_contents)

    #Replace Title and Content sections
    file_template_contents = file_template_contents.replace("{{ Title }}", page_title)
    file_template_contents = file_template_contents.replace("{{ Content }}", HTML_to_add)

    #Create a new HTML to the destination path
    print(f"dest_path: {dest_path}")
    file_html = open(dest_path, "w")
    file_html.write(file_template_contents)
    file_html.close

    pass

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    #Print a message to console
    print(f"<<< Generating pages from all directories under {dir_path_content} to {dest_dir_path} using {template_path} >>>\n")

    dir_list = list_dir_files(dir_path_content)

    for node in dir_list:
        path_file = node[0] + node[1]
        # print(path_file)
        destination_path = dest_dir_path + path_file[len(dir_path_content):-3:] + ".html"
        if os.path.isfile (path_file):
            destination_path = dest_dir_path + path_file[len(dir_path_content):-3:] + ".html"
            #This is a file, so process
            #print(f"Processing File: {path_file}")
            #remove the from path and change to the destination path.
            #print(f"Printing file to: {destination_path}")
            generate_page(path_file, template_path, destination_path)
        else:
            destination_path = dest_dir_path + path_file[len(dir_path_content)::]
            #directory, if it does not exist, create it.
            #print(destination_path)
            #print(os.path.isdir(destination_path))
            if not os.path.isdir(destination_path):
                os.mkdir(destination_path)

    print(f"<<< Done! >>>")

    pass



    