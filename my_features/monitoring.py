import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset

# Load data
df = pd.read_csv('feature_repo/data/adult.csv')
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].str.strip()
df = df.replace('?', pd.NA).dropna()

# Features
features = ['age', 'education.num', 'hours.per.week', 'capital.gain', 'capital.loss']
X = df[features].apply(pd.to_numeric, errors='coerce').dropna()

# Split reference and current data
reference = X.iloc[:5000]
current = X.iloc[5000:10000]

# Create drift report
report = Report(metrics=[DataDriftPreset()])
my_run = report.run(reference_data=reference, current_data=current)
my_run.save_html('drift_report.html')
print("Drift report saved!")