def remove(fileName):
    a_file = open("sample.txt", "r")
    get list of lines
    lines = a_file.readlines()
    a_file.close()

    del lines[1]
    delete lines


    new_file = open("sample.txt", "w+")
    write to file without line

    for line in lines:
    new_file.write(line)

    new_file.close()