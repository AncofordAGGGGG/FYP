import os

data_dir = "../data/raw/a-labelled-version-of-the-ADFA-LD-dataset-master/ADFA-LD/Training_Data_Master"

files = os.listdir(data_dir)

print("number of training samples:", len(files))

# 读取一个样本
sample_file = os.path.join(data_dir, files[0])

with open(sample_file, "r") as f:
    seq = f.read().strip().split()

print("first file:", files[0])
print("sequence length:", len(seq))
print("first 20 syscalls:", seq[:20])