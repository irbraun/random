import glob
import os
import sys
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", dest="input", help="path to the input parent directory", required=True)
parser.add_argument("-o", "--output", dest="output", help="path of the output text file", required=False)
args = parser.parse_args()
input_dir = args.input
output_path = args.output




def handle_stmt(s):
    s = s.strip()
    if (len(s.split(" ")) == 1) or (len(s.split(" ")) == 3):
        return(s.split(" ")[0])
    else:
        raise ValueError("unrecognized as import statement {}".format(s))

    

# Find a list of all the modules names that might need to be mocked.
module_names = set()
for filename in glob.glob(os.path.join(input_dir,"**","*.py")):

    # Open the file and get all the import statement lines without tabs or newlines characters.
    f = open(filename, "r")
    lines = f.readlines()
    imports = [line.rstrip("\n").replace("\t","") for line in lines if "import" in line]

    for line in imports:
        
        # Remove trailing comments from the line.
        line = "".join(line.split("#")[0])
        
        # Handling regular import statements.
        if line.split(" ")[0] == "import":
            modules =  " ".join(line.split(" ")[1:])
            stmts = modules.split(",")
            for stmt in stmts:
                module_names.add(handle_stmt(stmt))
                
        # Handling import statements starting with 'from'.
        if line.split(" ")[0] == "from":
            module_names.add(line.split(" ")[1])
            modules = " ".join(line.split(" ")[3:])
            stmts = modules.split(",")
            for stmt in stmts:
                module_names.add(line.split(" ")[1] + "." + handle_stmt(stmt))
    
    
# Remove duplicates and sort the list of modules names.
module_names = list(module_names)    
module_names.sort()
module_names = [m for m in module_names if not "oats" in m]
        
# Write the the module names in list syntax to a text file.
outf = open(output_path, "w")
outf.write("MOCK_MODULES = [\n")
for s in module_names:
    outf.write("'"+s+"'"+", ")
outf.write("]")
outf.close()