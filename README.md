# Malware Detection Using Machine Learning

## Project Overview
This project aims to detect malicious programs using machine learning techniques based on system call sequences.

Programs are represented as sequences of system calls, and n-gram features are extracted to capture behavioral patterns. Different machine learning models are then applied to classify programs as normal or malicious.

---

## Dataset
The project uses the **ADFA-LD dataset**, which contains:

- Training_Data_Master (normal programs)
- Validation_Data_Master (normal programs)
- Attack_Data_Master (malicious programs)

Each file represents a sequence of system calls generated during program execution.

---

## Methodology

### 1. Feature Extraction
System call sequences are transformed into n-gram features:

- **1-gram**: individual system calls
- **2-gram**: pairs of consecutive calls
- **3-gram**: triplets of consecutive calls

These features capture the behavioral patterns of program execution.

---

### 2. Feature Representation
The extracted n-gram features are converted into numerical vectors using:

- `DictVectorizer` (bag-of-n-gram representation)

---

### 3. Models
Two machine learning models are used:

- Logistic Regression
- Random Forest

---

### 4. Evaluation Metrics
Model performance is evaluated using:

- Precision
- Recall
- F1-score
- Accuracy

---

## Experimental Results

The results show that increasing the n-gram size improves detection performance:

| Features | Attack F1 | Accuracy |
|---------|--------|---------|
| 1-gram | 0.7025 | 0.9118 |
| 1+2-gram | 0.7592 | 0.9286 |
| 1+2+3-gram | **0.7710** | **0.9337** |

Random Forest achieves the best overall performance with higher accuracy and F1-score.

---

## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

---

### 2. Run the program
```bash
python src/make_dataset.py
```

---

## Project Structure
```
malware-detection/
│
├── src/
│   ├── make_dataset.py
│   ├── load_adfa.py
│
├── data/ (not included)
│
├── requirements.txt
├── README.md
```
