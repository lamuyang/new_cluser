def open_pkl(pkl):
    import pickle
    with open(f"{pkl}", 'rb') as fp:
        sorted = pickle.load(fp)
    fp.close()
    return sorted
def read_to_txt(pkl,file_name):
    import pickle
    with open(f"{pkl}", 'rb') as fp:
        sorted = pickle.load(fp)
    with open(file_name,"w") as file:
        for i in sorted:
            file.write(f"{i}\n")
