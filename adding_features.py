import ast

import numpy as np
import pandas as pd


# (Eren) I will read the paired time-value dataset and turn those sequences into simple numeric features.
df = pd.read_csv('list_ordered_veriseti.csv')


# (Eren) These columns contain numeric measurements, so I can safely compute mean, last, count, and slope.
NUMERIC_PAIR_COLUMNS = [
	'hba1c_list',
	'üre_list',
	'kreatinin_list',
	'bun_list',
	'alt_list',
	'alp_list',
	'ast_list',
	'ggt_list',
	'bilirubin_list',
	'potasyum_list',
	'kalsiyum_list',
	'magnezyum_list',
	'klor_list',
	'albumin_list',
	'crp_list',
	'ldh_list',
	'sodyum_list',
]


def parse_pair_list(cell) -> list:
	"""Turn a stored string representation of [(time, value), ...] into a Python list."""

	if pd.isna(cell) or str(cell).strip() in ['', '[]']:
		return []
	if isinstance(cell, list):
		return cell
	try:
		parsed = ast.literal_eval(cell)
	except (ValueError, SyntaxError):
		return []
	return parsed if isinstance(parsed, list) else []


def compute_pair_features(cell) -> tuple:
	"""Extract mean, last value, count, and slope from one time-value sequence."""

	pairs = parse_pair_list(cell)
	if not pairs:
		return np.nan, np.nan, 0, np.nan

	timestamps = []
	values = []

	for pair in pairs:
		if not isinstance(pair, (tuple, list)) or len(pair) != 2:
			continue

		time_raw, value_raw = pair

		try:
			timestamp = pd.to_datetime(time_raw)
			value = float(value_raw)
		except (ValueError, TypeError):
			continue

		timestamps.append(timestamp)
		values.append(value)

	if not values:
		return np.nan, np.nan, 0, np.nan

	order = np.argsort(timestamps)
	timestamps = [timestamps[i] for i in order]
	values = [values[i] for i in order]

	mean_value = float(np.mean(values))
	last_value = float(values[-1])
	measurement_count = int(len(values))

	if len(values) < 2:
		slope = 0.0
	else:
		x = np.array([(ts - timestamps[0]).total_seconds() / 86400.0 for ts in timestamps], dtype=float)
		y = np.array(values, dtype=float)
		if np.allclose(x, x[0]):
			slope = 0.0
		else:
			try:
				slope = float(np.polyfit(x, y, 1)[0])
			except Exception:
				slope = np.nan

	return mean_value, last_value, measurement_count, slope


# (Eren) I will create the new feature columns first, then remove the complicated sequence columns.
for source_column in NUMERIC_PAIR_COLUMNS:
	if source_column not in df.columns:
		continue

	feature_prefix = source_column.removesuffix('_list')
	features = df[source_column].apply(compute_pair_features)

	df[f'{feature_prefix}_mean'] = features.apply(lambda item: item[0])
	df[f'{feature_prefix}_last'] = features.apply(lambda item: item[1])
	df[f'{feature_prefix}_count'] = features.apply(lambda item: item[2])
	df[f'{feature_prefix}_slope'] = features.apply(lambda item: item[3])


# (Eren) Empty measurements should not stay as missing values if I want a clean ML table.
feature_columns = [column for column in df.columns if column.endswith(('_mean', '_last', '_count', '_slope'))]
for column in feature_columns:
	if column.endswith('_count'):
		df[column] = df[column].fillna(0).astype(int)
	else:
		fill_value = df[column].median()
		if pd.isna(fill_value):
			fill_value = 0.0
		df[column] = df[column].fillna(fill_value)


# (Eren) I will drop the original pair columns now that the core features are extracted.
pair_columns = [column for column in df.columns if column.endswith('_list')]
df.drop(columns=pair_columns, inplace=True)


# (Eren) Finally, I will save the cleaned feature table for modeling.
df.to_csv('final_veriseti.csv', index=False)
