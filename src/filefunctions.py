import os, shutil

def list_dir_files(path):
    #return a list of lists of the path and directories and files found
    file_list = []

    for file_name in os.listdir(path):
        file_list.append([path + "/", file_name])
        current_node = path + "/" + file_name
        if not os.path.isfile(current_node):
            #this is a folder. update path and call this function recursively
            sub_dir = list_dir_files(current_node)
            for rec in sub_dir:
                file_list.append(rec)
    
    return file_list

def move_files(file_list, path_from, path_to):

    #first creating directories
    for file_name in file_list:
        node_path = file_name[0] + file_name[1]
        new_path = path_to + node_path[len(path_from)::]
        if os.path.isfile (node_path):
            #This is a file
            print(f"Moving: {node_path}")
            shutil.copy(node_path, new_path)
        else:
            #This is a directory, create it.
            #print(f"Directory Found! {node_path}")
            new_path = path_to + node_path[len(path_from)::]
            print(f"Creating: {new_path}")
            os.mkdir(new_path)

    pass
