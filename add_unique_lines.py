import sys
import os

def add_unique_lines(source_file, destination_file):

    # if destination_file does not exist, create it
    if not os.path.exists(destination_file):
        open(destination_file, 'w').close()
    

    unique_lines_counter = 0

    line_dict = {}

    sf = open(source_file, 'r')
    df = open(destination_file, 'r') # first open it in read mode and generate the dictionary
    

    for line in df.readlines():
        line_dict[line.strip()] = True

    df.close()
    df = open(destination_file, 'a+') # then open it in append mode and add the new lines
    
    for line in sf.readlines():

        if line_dict.get(line.strip()): # line_dict[line] 
            continue
        else:
            line_dict[line] = True
            unique_lines_counter += 1
            df.write(f"{line}")
            print(line.replace("\n",""))

    df.close()
    sf.close()

    return unique_lines_counter

if __name__ == "__main__":
    
    if len(sys.argv) < 3:
        print("Usage: python3 add_unique_lines.py source_file destination_file")
        sys.exit(1)

    add_unique_lines(sys.argv[1], sys.argv[2])
