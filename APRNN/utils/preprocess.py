import os

# def time2id(file_path):
#     with open(file_path + '.out', 'w') as f_out:
#         with open(file_path, 'r') as f_in:
#             i = 0
#             for line in f_in:
#                 if line.startswith('Time'):
#                     print(line.strip(), file=f_out)
#                 else:
#                     print("{0},{1}".format(i, line[11:].strip()), file=f_out)
#                 i += 1


def load_label():
    file_path = '/Users/hsh/Documents/2015/AnomalyClassifier/y_out/te/label'
    list_file = os.listdir(file_path)
    _dict = {}
    for item in list_file:
        a_file_path = file_path + '/' + item
        with open(a_file_path, 'r') as f_in:
            for line in f_in:
                tokens = line.split(',')
                id = int(tokens[0])
                if float(tokens[-2]) > 0:
                    _dict[id] = '2'
                    for i in range(id - 6, id):
                        if i >= 0:
                            _dict[i] = '1'
    print(len(_dict))
    return _dict

def merge_data():
    _dict = load_label()
    file_path = '/Users/hsh/Documents/2015/AnomalyClassifier/y_out/te/data'
    list_file = os.listdir(file_path)
    _data = []
    for item in list_file:
        a_file_path = file_path + '/' + item
        one_data = []
        with open(a_file_path, 'r') as f_in:
            for line in f_in:
                l = line.replace(',', '').strip()
                one_data.append(l)
        _data.append(one_data)
    print(len(_data))
    with open(file_path + '.data', 'w') as f_out:
        i = 1
        while True:
            one_line = [str(i)]
            for j in range(0, 8):
                if i - 1 == len(_data[j]):
                    print(i)
                    return
                one_line.append(_data[j][i-1])
            if (i-1) in _dict:
                one_line.append(_dict[i-1])
            else:
                one_line.append('0')
            print >>f_out, ','.join(one_line)
            i += 1
        print i

if __name__ == "__main__":
    # file_path = '../data/rubis/rubis.txt'
    # file_path = 'C:\\Users\\Shaohan\\Desktop\\ibm_t\\all.data'
    # time2id(file_path)
    merge_data()