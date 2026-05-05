import json
import pickle
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder


RANDOM_STATE = 42
TEST_SIZE = 0.20

DATA_PATH = Path("final_veriseti.csv")
MODEL_PATH = Path("rf_non_absolute_survival_model.pkl")
METADATA_PATH = Path("rf_non_absolute_survival_metadata.json")


def build_and_train_model() -> None:
	# (Eren) I load the dataset and keep only valid binary values in the target.
	df = pd.read_csv(DATA_PATH)

	if "ölüm durumu" not in df.columns:
		raise ValueError("'ölüm durumu' column was not found in final_veriseti.csv")

	df = df.dropna(subset=["ölüm durumu"]).copy()
	df["ölüm durumu"] = pd.to_numeric(df["ölüm durumu"], errors="coerce")
	df = df[df["ölüm durumu"].isin([0, 1])].copy()
	df["ölüm durumu"] = df["ölüm durumu"].astype(int)

	# (Eren) This is the leakage-safe setup: I remove death date and any derivative of death date.
	leakage_columns = ["ölüm tarihi", "olum_tarihi_var"]
	feature_columns = [col for col in df.columns if col not in ["ölüm durumu"] + leakage_columns]

	X = df[feature_columns].copy()
	y = df["ölüm durumu"].copy()

	numeric_columns = X.select_dtypes(include=["number"]).columns.tolist()
	categorical_columns = [col for col in X.columns if col not in numeric_columns]

	numeric_pipeline = Pipeline(
		steps=[
			("imputer", SimpleImputer(strategy="median")),
		]
	)

	categorical_pipeline = Pipeline(
		steps=[
			("imputer", SimpleImputer(strategy="most_frequent")),
			(
				"encoder",
				OrdinalEncoder(
					handle_unknown="use_encoded_value",
					unknown_value=-1,
				),
			),
		]
	)

	preprocessor = ColumnTransformer(
		transformers=[
			("num", numeric_pipeline, numeric_columns),
			("cat", categorical_pipeline, categorical_columns),
		],
		remainder="drop",
	)

	model = RandomForestClassifier(
		n_estimators=700,
		max_depth=None,
		min_samples_split=2,
		min_samples_leaf=1,
		class_weight="balanced_subsample",
		random_state=RANDOM_STATE,
		n_jobs=-1,
	)

	pipeline = Pipeline(
		steps=[
			("preprocessor", preprocessor),
			("model", model),
		]
	)

	X_train, X_test, y_train, y_test = train_test_split(
		X,
		y,
		test_size=TEST_SIZE,
		random_state=RANDOM_STATE,
		stratify=y,
	)

	pipeline.fit(X_train, y_train)

	y_pred = pipeline.predict(X_test)
	accuracy = accuracy_score(y_test, y_pred)
	report_text = classification_report(y_test, y_pred, digits=4)
	cm = confusion_matrix(y_test, y_pred).tolist()

	print("Leakage-safe model performance on 80/20 split")
	print(f"Accuracy: {accuracy:.4f}")
	print("Confusion matrix:")
	print(cm)
	print("Classification report:")
	print(report_text)

	# (Eren) I save the model bundle with train/test data for SHAP and website usage.
	model_bundle = {
		"pipeline": pipeline,
		"feature_columns": feature_columns,
		"target_column": "ölüm durumu",
		"train_size": len(X_train),
		"test_size": len(X_test),
		"accuracy": float(accuracy),
		"random_state": RANDOM_STATE,
		"X_train": X_train,
		"X_test": X_test,
		"y_train": y_train,
		"y_test": y_test,
	}

	with MODEL_PATH.open("wb") as f:
		pickle.dump(model_bundle, f)

	metadata = {
		"data_file": str(DATA_PATH),
		"model_file": str(MODEL_PATH),
		"target_column": "ölüm durumu",
		"feature_columns": feature_columns,
		"leakage_columns_removed": [c for c in leakage_columns if c in df.columns],
		"model_mode": "leakage_safe_non_absolute_death",
		"train_test_ratio": "80/20",
		"train_size": len(X_train),
		"test_size": len(X_test),
		"class_distribution": y.value_counts().to_dict(),
		"accuracy": float(accuracy),
		"confusion_matrix": cm,
		"model_name": "RandomForestClassifier",
		"model_params": model.get_params(),
		"random_state": RANDOM_STATE,
	}

	with METADATA_PATH.open("w", encoding="utf-8") as f:
		json.dump(metadata, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
	build_and_train_model()
