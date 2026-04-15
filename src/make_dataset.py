import os
from collections import Counter

import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

BASE = "../data/raw/a-labelled-version-of-the-ADFA-LD-dataset-master/ADFA-LD"
TRAIN_DIR = os.path.join(BASE, "Training_Data_Master")      # 正常
VAL_DIR   = os.path.join(BASE, "Validation_Data_Master")    # 正常
ATT_DIR   = os.path.join(BASE, "Attack_Data_Master")        # 攻击(恶意)

def read_seq(path: str):
    with open(path, "r") as f:
        return f.read().strip().split()

def load_dir_as_counts(dir_path: str, label: int):
    X_dicts, y = [], []
    for root, _, files in os.walk(dir_path):  # 递归遍历
        for fn in files:
            if not fn.endswith(".txt"):
                continue
            fp = os.path.join(root, fn)
            seq = read_seq(fp)
from itertools import tee

def bigrams(seq):
    a, b = tee(seq)
    next(b, None)
    return [f"{x}_{y}" for x, y in zip(a, b)]

def trigrams(seq):
    return [f"{seq[i]}_{seq[i+1]}_{seq[i+2]}" for i in range(len(seq) - 2)]

def load_dir_as_counts(dir_path: str, label: int):
    X_dicts, y = [], []
    for root, _, files in os.walk(dir_path):
        for fn in files:
            if not fn.endswith(".txt"):
                continue
            fp = os.path.join(root, fn)
            seq = read_seq(fp)

            features = Counter(seq)      # 1-gram
            features.update(Counter(bigrams(seq)))  # 2-gram
            features.update(Counter(trigrams(seq))) # 3-gram

            X_dicts.append(features)
            y.append(label)
    return X_dicts, y

# 正常样本：Training + Validation
Xn1, yn1 = load_dir_as_counts(TRAIN_DIR, 0)
Xn2, yn2 = load_dir_as_counts(VAL_DIR, 0)
# 恶意样本：Attack
Xa, ya = load_dir_as_counts(ATT_DIR, 1)

X_dicts = Xn1 + Xn2 + Xa
y = np.array(yn1 + yn2 + ya)

print("normal:", len(yn1) + len(yn2), "attack:", len(ya), "total:", len(y))

# 向量化：把 Counter 变成稀疏向量
vec = DictVectorizer(sparse=True)
X = vec.fit_transform(X_dicts)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

clf = LogisticRegression(
    solver="saga",
    penalty="l2",
    max_iter=20000,
    class_weight="balanced",
    n_jobs=-1,
)
rf = RandomForestClassifier(
    n_estimators=200,
    class_weight="balanced",
    n_jobs=-1,
    random_state=42
)
print("Logistic Regression")
clf.fit(X_train, y_train)
pred = clf.predict(X_test)
print(classification_report(y_test, pred, digits=4))

print("Random Forest")
rf.fit(X_train, y_train)
pred_rf = rf.predict(X_test)
print(classification_report(y_test, pred_rf, digits=4))
