def time2id(file_path):
    with open(file_path + 'out', 'w') as f_out:
        with open(file_path, 'r') as f_in:
            for line in f_in:
                n