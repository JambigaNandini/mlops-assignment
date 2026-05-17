import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

# 1. Load and clean dataset
df = pd.read_csv('feature_repo/data/adult.csv')

# Clean column names
df.columns = df.columns.str.strip()

# Clean all string columns
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].str.strip()

# Drop rows with missing/corrupted values
df = df.replace('?', pd.NA).dropna()

print("Clean Shape:", df.shape)
print("Columns:", list(df.columns))

# 2. Prepare features
features = ['age', 'education.num', 'hours.per.week',
            'capital.gain', 'capital.loss']
X = df[features].apply(pd.to_numeric, errors='coerce').dropna()
df = df.loc[X.index]
y = LabelEncoder().fit_transform(df['income'])

# 3. Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. MLflow Tracking
mlflow.set_experiment("adult_income_experiment")

with mlflow.start_run():
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)

    mlflow.log_param("model", "RandomForest")
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("test_size", 0.2)
    mlflow.log_param("features", str(features))
    mlflow.log_metric("accuracy", acc)
    mlflow.sklearn.log_model(model, "model")

    print("=== Results ===")
    print(f"Training rows: {len(X_train)}")
    print(f"Testing rows:  {len(X_test)}")
    print(f"Accuracy: {acc:.4f} ({acc*100:.2f}%)")
    print(classification_report(y_test, y_pred,
          target_names=['<=50K', '>50K']))
    print("Run logged to MLflow successfully!")