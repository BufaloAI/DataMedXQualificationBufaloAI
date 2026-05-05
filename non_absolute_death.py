import argparse
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
TARGET_COLUMN = "ölüm durumu"
DEATH_DATE_COLUMN = "ölüm tarihi"
ABSOLUTE_SIGNAL_COLUMN = "olum_tarihi_var"

DATA_PATH = Path("final_veriseti.csv")
MODEL_PATH = Path("rf_non_absolute_survival_model.pkl")
METADATA_PATH = Path("rf_non_absolute_survival_metadata.json")


MODE_CONFIG = {
	"normal": {
		"model_path": Path("rf_survival_model.pkl"),
		"metadata_path": Path("rf_survival_metadata.json"),
		"model_mode": "absolute_death_normal",
	},
	"until_time": {
		"model_path": MODEL_PATH,
		"metadata_path": METADATA_PATH,
		"model_mode": "leakage_safe_non_absolute_death",
	},
}


def _resolve_training_source(data_path: Path, external_training_data: str | None) -> Path:
	if external_training_data:
		return Path(external_training_data)
	return data_path


def _clean_target(df: pd.DataFrame) -> pd.DataFrame:
	if TARGET_COLUMN not in df.columns:
		raise ValueError(f"'{TARGET_COLUMN}' column was not found in final_veriseti.csv")

	df = df.dropna(subset=[TARGET_COLUMN]).copy()
	df[TARGET_COLUMN] = pd.to_numeric(df[TARGET_COLUMN], errors="coerce")
	df = df[df[TARGET_COLUMN].isin([0, 1])].copy()
	df[TARGET_COLUMN] = df[TARGET_COLUMN].astype(int)
	return df


def _prepare_dataset(df: pd.DataFrame, mode: str) -> tuple[pd.DataFrame, list[str], list[str]]:
	if mode not in MODE_CONFIG:
		raise ValueError("mode must be either 'normal' or 'until_time'")

	df = _clean_target(df)
	leakage_columns: list[str] = []

	if mode == "normal" and DEATH_DATE_COLUMN in df.columns:
		df[ABSOLUTE_SIGNAL_COLUMN] = df[DEATH_DATE_COLUMN].notna().astype(int)
		leakage_columns = [DEATH_DATE_COLUMN]
	elif mode == "until_time":
		leakage_columns = [DEATH_DATE_COLUMN, ABSOLUTE_SIGNAL_COLUMN]

	feature_columns = [col for col in df.columns if col not in [TARGET_COLUMN] + leakage_columns]
	return df, feature_columns, [col for col in leakage_columns if col in df.columns]


def _build_pipeline(X: pd.DataFrame) -> Pipeline:
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

	return Pipeline(
		steps=[
			("preprocessor", preprocessor),
			("model", model),
		]
	)


def build_and_train_model(
	mode: str = "until_time",
	data_path: Path = DATA_PATH,
	external_training_data: str | None = None,
) -> None:
	# (Eren) I load either the bundled dataset or an external CSV supplied by the doctor.
	training_source = _resolve_training_source(data_path, external_training_data)
	df = pd.read_csv(training_source)
	df, feature_columns, leakage_columns = _prepare_dataset(df, mode)

	X = df[feature_columns].copy()
	y = df[TARGET_COLUMN].copy()
	pipeline = _build_pipeline(X)

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

	print(f"Model mode: {mode}")
	print(f"Training source: {training_source}")
	print("Model performance on 80/20 split")
	print(f"Accuracy: {accuracy:.4f}")
	print("Confusion matrix:")
	print(cm)
	print("Classification report:")
	print(report_text)

	model_bundle = {
		"pipeline": pipeline,
		"feature_columns": feature_columns,
		"target_column": TARGET_COLUMN,
		"train_size": len(X_train),
		"test_size": len(X_test),
		"accuracy": float(accuracy),
		"random_state": RANDOM_STATE,
		"mode": mode,
		"training_source": str(training_source),
		"X_train": X_train,
		"X_test": X_test,
		"y_train": y_train,
		"y_test": y_test,
	}

	model_path = MODE_CONFIG[mode]["model_path"]
	metadata_path = MODE_CONFIG[mode]["metadata_path"]

	with model_path.open("wb") as f:
		pickle.dump(model_bundle, f)

	metadata = {
		"data_file": str(training_source),
		"model_file": str(model_path),
		"target_column": TARGET_COLUMN,
		"feature_columns": feature_columns,
		"leakage_columns_removed": leakage_columns,
		"model_mode": MODE_CONFIG[mode]["model_mode"],
		"train_test_ratio": "80/20",
		"train_size": len(X_train),
		"test_size": len(X_test),
		"class_distribution": y.value_counts().to_dict(),
		"accuracy": float(accuracy),
		"confusion_matrix": cm,
		"model_name": "RandomForestClassifier",
		"model_params": pipeline.named_steps["model"].get_params(),
		"random_state": RANDOM_STATE,
	}

	with metadata_path.open("w", encoding="utf-8") as f:
		json.dump(metadata, f, ensure_ascii=False, indent=2)

	print(f"Model saved to: {model_path}")
	print(f"Metadata saved to: {metadata_path}")

	if accuracy < 0.90:
		print("Warning: Accuracy is below 90%. Consider feature refinement or hyperparameter tuning.")


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Train the cancer survival model.")
	parser.add_argument(
		"--mode",
		choices=["normal", "until_time"],
		default="until_time",
		help="normal uses the absolute-death signal, until_time removes leakage.",
	)
	parser.add_argument(
		"--data-path",
		default=str(DATA_PATH),
		help="Path to the training CSV file.",
	)
	parser.add_argument(
		"--external-training-data",
		default=None,
		help="Optional external CSV path supplied by the doctor.",
	)
	return parser.parse_args()


if __name__ == "__main__":
	args = parse_args()
	build_and_train_model(
		mode=args.mode,
		data_path=Path(args.data_path),
		external_training_data=args.external_training_data,
	)
