# load data from the data folder
import os

def load_data(file_name):
    with open("data/"+file_name, "r", encoding='utf-8') as f:
        return f.read()


if __name__ == "__main__":
    md_data = load_data()
    print(md_data[:200])