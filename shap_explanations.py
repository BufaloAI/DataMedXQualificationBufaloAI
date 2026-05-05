# pyright: reportMissingImports=false

import json
import pickle
from pathlib import Path

import pandas as pd
import shap


MODEL_PATH = Path("rf_non_absolute_survival_model.pkl")
GLOBAL_JSON_PATH = Path("shap_global_importance.json")
LOCAL_JSON_PATH = Path("shap_local_explanations.json")
GLOBAL_CSV_PATH = Path("shap_global_importance.csv")
FORCE_HTML_PATH = Path("shap_force_plot_sample0.html")
MAX_LOCAL_SAMPLES = 5


def _extract_positive_class_shap(shap_values):
	# (Eren) SHAP output format can change by version, so I normalize it to positive class contributions.
	if isinstance(shap_values, list):
		if len(shap_values) == 2:
			return shap_values[1]
		return shap_values[0]

	if hasattr(shap_values, "shape") and len(shap_values.shape) == 3:
		return shap_values[:, :, 1]

	return shap_values


def generate_shap_explanations() -> None:
	# (Eren) I load the leakage-safe trained model and holdout samples for SHAP.
	if not MODEL_PATH.exists():
		raise FileNotFoundError(
			"rf_non_absolute_survival_model.pkl was not found. Run non_absolute_death.py first."
		)

	with MODEL_PATH.open("rb") as f:
		model_bundle = pickle.load(f)

	pipeline = model_bundle["pipeline"]
	X_test = model_bundle["X_test"]
	feature_columns = model_bundle["feature_columns"]

	preprocessor = pipeline.named_steps["preprocessor"]
	forest_model = pipeline.named_steps["model"]

	X_test_transformed = preprocessor.transform(X_test)
	transformed_feature_names = preprocessor.get_feature_names_out().tolist()

	# (Eren) I use TreeExplainer because Random Forest is a tree model.
	explainer = shap.TreeExplainer(forest_model)
	raw_shap_values = explainer.shap_values(X_test_transformed)
	positive_shap_values = _extract_positive_class_shap(raw_shap_values)

	global_importance = (
		pd.Series(abs(positive_shap_values).mean(axis=0), index=transformed_feature_names)
		.sort_values(ascending=False)
		.reset_index()
	)
	global_importance.columns = ["feature", "mean_abs_shap"]

	# (Eren) I save global importance in both JSON and CSV to make website integration easier.
	global_importance.to_csv(GLOBAL_CSV_PATH, index=False)
	with GLOBAL_JSON_PATH.open("w", encoding="utf-8") as f:
		json.dump(global_importance.to_dict(orient="records"), f, ensure_ascii=False, indent=2)

	local_payload = []
	sample_count = min(MAX_LOCAL_SAMPLES, len(X_test))

	for i in range(sample_count):
		row_values = positive_shap_values[i]
		pred_prob = float(pipeline.predict_proba(X_test.iloc[[i]])[0][1])

		top_local = (
			pd.Series(row_values, index=transformed_feature_names)
			.reindex(pd.Series(abs(row_values), index=transformed_feature_names).sort_values(ascending=False).index)
			.head(12)
		)

		local_payload.append(
			{
				"sample_index": int(X_test.index[i]),
				"prediction_probability_death": pred_prob,
				"top_contributors": [
					{"feature": feat, "shap_value": float(val)} for feat, val in top_local.items()
				],
				"original_input": {
					col: (None if pd.isna(X_test.iloc[i][col]) else str(X_test.iloc[i][col]))
					for col in feature_columns
				},
			}
		)

	with LOCAL_JSON_PATH.open("w", encoding="utf-8") as f:
		json.dump(local_payload, f, ensure_ascii=False, indent=2)

	# (Eren) I also save one interactive force plot that can be embedded directly in a website.
	expected_value = explainer.expected_value
	if isinstance(expected_value, list):
		expected_value = expected_value[1] if len(expected_value) > 1 else expected_value[0]

	force_plot = shap.force_plot(
		expected_value,
		positive_shap_values[0],
		feature_names=transformed_feature_names,
	)
	shap.save_html(str(FORCE_HTML_PATH), force_plot)

	print("SHAP explanation files were created successfully.")
	print(f"Global importance JSON: {GLOBAL_JSON_PATH}")
	print(f"Global importance CSV: {GLOBAL_CSV_PATH}")
	print(f"Local explanations JSON: {LOCAL_JSON_PATH}")
	print(f"Force plot HTML: {FORCE_HTML_PATH}")


if __name__ == "__main__":
	generate_shap_explanations()
