def time2id(file_path):
    with open(file_path + '.out', 'w') as f_out:
        with open(file_path, 'r') as f_in:
            i = 0
            for line in f_in:
                if line.startswith('Time'):
                    print(line.strip(), file=f_out)
                else:
                    print("{0},{1}".format(i, line[11:].strip()), file=f_out)
                i += 1

if __name__ == "__main__":
    file_path = '../data/rubis/rubis.txt'
    time2id(file_path)