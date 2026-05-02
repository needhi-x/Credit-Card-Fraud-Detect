import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE

# -----------------------------
# 🔥 FIX 1: SAFE CSV LOADING
# -----------------------------
df = pd.read_csv(
    "data/creditcard.csv",
    low_memory=True,      # reduces RAM usage
    memory_map=True       # safer loading
)

print("Dataset shape:", df.shape)

# -----------------------------
# SPLIT
# -----------------------------
X = df.drop("Class", axis=1)
y = df["Class"]

# -----------------------------
# SCALE
# -----------------------------
scaler = StandardScaler()
X["Amount"] = scaler.fit_transform(X[["Amount"]])
X["Time"] = scaler.fit_transform(X[["Time"]])

# convert to numpy (IMPORTANT)
X = X.values
y = y.values

# -----------------------------
# TRAIN TEST SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -----------------------------
# 🔥 FIX 2: LIGHT SMOTE (SAFE)
# -----------------------------
smote = SMOTE(
    sampling_strategy=0.1,  # even lighter → prevents memory crash
    random_state=42,
    k_neighbors=3
)

X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

print("After SMOTE:", np.bincount(y_train_res))

# -----------------------------
# MODEL (LIGHT + STABLE)
# -----------------------------
model = RandomForestClassifier(
    n_estimators=30,   # reduced
    max_depth=8,       # controlled
    n_jobs=1,          # safe for Windows
    random_state=42
)

model.fit(X_train_res, y_train_res)

# -----------------------------
# EVALUATION
# -----------------------------
y_pred = model.predict(X_test)

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# -----------------------------
# SAVE MODEL
# -----------------------------
joblib.dump(model, "models/fraud_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")

print("Model saved successfully ✅")


joblib.dump(model, "models/fraud_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")

# 🔥 ADD THIS (MISSING PART)
joblib.dump(df.drop("Class", axis=1).columns.tolist(), "models/columns.pkl")

print("All files saved ✅")