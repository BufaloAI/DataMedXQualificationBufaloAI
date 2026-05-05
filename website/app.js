const TARGET_COLUMN = "ölüm durumu";
const DEATH_DATE_COLUMN = "ölüm tarihi";
const DERIVED_SIGNAL_COLUMN = "olum_tarihi_var";

const CORE_COLUMNS = [
	"kanser_turu",
	"cinsiyet",
	"doğum tarihi",
	"department",
	"oluşturma tarihi",
	"epikriz",
	"atc kod",
	"işlem tipi",
];

const LAB_COLUMNS = [
	"hba1c_mean",
	"hba1c_last",
	"hba1c_count",
	"hba1c_slope",
	"üre_mean",
	"üre_last",
	"üre_count",
	"üre_slope",
	"kreatinin_mean",
	"kreatinin_last",
	"kreatinin_count",
	"kreatinin_slope",
	"bun_mean",
	"bun_last",
	"bun_count",
	"bun_slope",
	"alt_mean",
	"alt_last",
	"alt_count",
	"alt_slope",
	"alp_mean",
	"alp_last",
	"alp_count",
	"alp_slope",
	"ast_mean",
	"ast_last",
	"ast_count",
	"ast_slope",
	"ggt_mean",
	"ggt_last",
	"ggt_count",
	"ggt_slope",
	"bilirubin_mean",
	"bilirubin_last",
	"bilirubin_count",
	"bilirubin_slope",
	"potasyum_mean",
	"potasyum_last",
	"potasyum_count",
	"potasyum_slope",
	"kalsiyum_mean",
	"kalsiyum_last",
	"kalsiyum_count",
	"kalsiyum_slope",
	"magnezyum_mean",
	"magnezyum_last",
	"magnezyum_count",
	"magnezyum_slope",
	"klor_mean",
	"klor_last",
	"klor_count",
	"klor_slope",
	"albumin_mean",
	"albumin_last",
	"albumin_count",
	"albumin_slope",
	"crp_mean",
	"crp_last",
	"crp_count",
	"crp_slope",
	"ldh_mean",
	"ldh_last",
	"ldh_count",
	"ldh_slope",
	"sodyum_mean",
	"sodyum_last",
	"sodyum_count",
	"sodyum_slope",
];

const BASE_FEATURE_COLUMNS = [...CORE_COLUMNS, ...LAB_COLUMNS];
const TRAINING_COLUMNS = [...BASE_FEATURE_COLUMNS, TARGET_COLUMN];

const FEATURE_LABELS = {
	kanser_turu: "Kanser türü",
	cinsiyet: "Cinsiyet",
	"doğum tarihi": "Doğum tarihi",
	department: "Bölüm",
	"oluşturma tarihi": "Oluşturma tarihi",
	epikriz: "Epikriz",
	"atc kod": "ATC kod",
	"işlem tipi": "İşlem tipi",
	hba1c_mean: "HbA1c ortalama",
	hba1c_last: "HbA1c son",
	hba1c_count: "HbA1c sayısı",
	hba1c_slope: "HbA1c eğimi",
	üre_mean: "Üre ortalama",
	üre_last: "Üre son",
	üre_count: "Üre sayısı",
	üre_slope: "Üre eğimi",
	kreatinin_mean: "Kreatinin ortalama",
	kreatinin_last: "Kreatinin son",
	kreatinin_count: "Kreatinin sayısı",
	kreatinin_slope: "Kreatinin eğimi",
	bun_mean: "BUN ortalama",
	bun_last: "BUN son",
	bun_count: "BUN sayısı",
	bun_slope: "BUN eğimi",
	alt_mean: "ALT ortalama",
	alt_last: "ALT son",
	alt_count: "ALT sayısı",
	alt_slope: "ALT eğimi",
	alp_mean: "ALP ortalama",
	alp_last: "ALP son",
	alp_count: "ALP sayısı",
	alp_slope: "ALP eğimi",
	ast_mean: "AST ortalama",
	ast_last: "AST son",
	ast_count: "AST sayısı",
	ast_slope: "AST eğimi",
	ggt_mean: "GGT ortalama",
	ggt_last: "GGT son",
	ggt_count: "GGT sayısı",
	ggt_slope: "GGT eğimi",
	bilirubin_mean: "Bilirubin ortalama",
	bilirubin_last: "Bilirubin son",
	bilirubin_count: "Bilirubin sayısı",
	bilirubin_slope: "Bilirubin eğimi",
	potasyum_mean: "Potasyum ortalama",
	potasyum_last: "Potasyum son",
	potasyum_count: "Potasyum sayısı",
	potasyum_slope: "Potasyum eğimi",
	kalsiyum_mean: "Kalsiyum ortalama",
	kalsiyum_last: "Kalsiyum son",
	kalsiyum_count: "Kalsiyum sayısı",
	kalsiyum_slope: "Kalsiyum eğimi",
	magnezyum_mean: "Magnezyum ortalama",
	magnezyum_last: "Magnezyum son",
	magnezyum_count: "Magnezyum sayısı",
	magnezyum_slope: "Magnezyum eğimi",
	klor_mean: "Klor ortalama",
	klor_last: "Klor son",
	klor_count: "Klor sayısı",
	klor_slope: "Klor eğimi",
	albumin_mean: "Albumin ortalama",
	albumin_last: "Albumin son",
	albumin_count: "Albumin sayısı",
	albumin_slope: "Albumin eğimi",
	crp_mean: "CRP ortalama",
	crp_last: "CRP son",
	crp_count: "CRP sayısı",
	crp_slope: "CRP eğimi",
	ldh_mean: "LDH ortalama",
	ldh_last: "LDH son",
	ldh_count: "LDH sayısı",
	ldh_slope: "LDH eğimi",
	sodyum_mean: "Sodyum ortalama",
	sodyum_last: "Sodyum son",
	sodyum_count: "Sodyum sayısı",
	sodyum_slope: "Sodyum eğimi",
	[DERIVED_SIGNAL_COLUMN]: "Ölüm tarihi sinyali",
	[TARGET_COLUMN]: "Hedef sütun",
};

const MODEL_SUMMARIES = {
	normal: {
		id: "normal",
		title: "Normal model",
		description: "Ölüm tarihi sinyalini de kullanan, karşılaştırma amaçlı hızlı model.",
		accuracy: 1.0,
		confusionMatrix: [
			[66, 0],
			[0, 34],
		],
		classDistribution: { 0: 331, 1: 169 },
		trainSize: 400,
		testSize: 100,
		featureCount: 77,
		modelMode: "absolute_death_normal",
		warning:
			"Bu mod ölüm tarihi sinyalini türettiği için klinik kullanım için değil, kıyaslama için düşünülmelidir.",
		badge: "Karşılaştırma modeli",
	},
	until_time: {
		id: "until_time",
		title: "Until_time model",
		description: "Ölüm tarihi sızıntısı çıkarılmış, SHAP yorumuna uygun model.",
		accuracy: 0.85,
		confusionMatrix: [
			[58, 8],
			[7, 27],
		],
		classDistribution: { 0: 331, 1: 169 },
		trainSize: 400,
		testSize: 100,
		featureCount: 76,
		modelMode: "leakage_safe_non_absolute_death",
		warning: "Bu mod üretim benzeri yorum için önerilen seçenektir.",
		badge: "Önerilen model",
	},
};

const SHAP_GLOBAL_IMPORTANCE = [
	{ feature: "num__albumin_last", meanAbsShap: 0.0615378425451346 },
	{ feature: "num__üre_last", meanAbsShap: 0.04843766411183214 },
	{ feature: "num__crp_last", meanAbsShap: 0.0340623608418963 },
	{ feature: "num__kalsiyum_last", meanAbsShap: 0.030195368782847554 },
	{ feature: "num__albumin_slope", meanAbsShap: 0.025763316521666094 },
	{ feature: "num__crp_slope", meanAbsShap: 0.025043914278078026 },
	{ feature: "num__üre_slope", meanAbsShap: 0.02483932658992029 },
	{ feature: "num__albumin_mean", meanAbsShap: 0.024465697160830156 },
	{ feature: "num__ldh_last", meanAbsShap: 0.02310135382096082 },
	{ feature: "num__kreatinin_last", meanAbsShap: 0.022980597386853974 },
	{ feature: "num__ast_last", meanAbsShap: 0.021613495568404 },
	{ feature: "num__ldh_mean", meanAbsShap: 0.015250953350992198 },
];

const SHAP_LOCAL_EXPLANATIONS = [
	{
		sampleIndex: 498,
		predictionProbabilityDeath: 0.047142857142857146,
		profile: {
			kanser_turu: "Prostat kanseri",
			cinsiyet: "erkek",
			doğum_tarihi: "1954",
			department: "Kardiyoloji / takip polikliniği",
		},
		topContributors: [
			{ feature: "num__albumin_last", shapValue: -0.06860809154276482 },
			{ feature: "num__üre_last", shapValue: -0.05477307568708991 },
			{ feature: "num__crp_last", shapValue: -0.042704253348564966 },
			{ feature: "num__albumin_mean", shapValue: -0.03498081986932331 },
			{ feature: "num__kalsiyum_last", shapValue: -0.033890887102407584 },
			{ feature: "num__üre_slope", shapValue: -0.028247958968285025 },
			{ feature: "num__albumin_slope", shapValue: -0.025218756963244507 },
			{ feature: "num__crp_slope", shapValue: -0.023448962385344604 },
			{ feature: "num__bilirubin_last", shapValue: 0.017158151479811506 },
			{ feature: "num__ldh_last", shapValue: 0.014828060486464926 },
		],
	},
	{
		sampleIndex: 143,
		predictionProbabilityDeath: 0.08571428571428572,
		profile: {
			kanser_turu: "Meme Kanseri",
			cinsiyet: "kadın",
			doğum_tarihi: "1974",
			department: "Medikal onkoloji",
		},
		topContributors: [
			{ feature: "num__üre_last", shapValue: -0.06404260228218034 },
			{ feature: "num__ldh_last", shapValue: -0.04354614703990013 },
			{ feature: "num__albumin_last", shapValue: -0.042553004425543446 },
			{ feature: "num__kalsiyum_last", shapValue: -0.03168934229710563 },
			{ feature: "num__kreatinin_last", shapValue: -0.03127818846480091 },
			{ feature: "num__crp_last", shapValue: 0.02554723180332655 },
			{ feature: "num__crp_slope", shapValue: -0.02491340716422332 },
			{ feature: "num__ast_last", shapValue: -0.024760005832183157 },
			{ feature: "num__üre_slope", shapValue: -0.023495552975791947 },
			{ feature: "num__ldh_mean", shapValue: -0.021209746779528704 },
		],
	},
];

const SHAP_ACTION_MAP = [
	{ match: ["albumin"], positive: "Albumin artışı ve nedeninin araştırılması için beslenme, karaciğer ve böbrek değerlendirmesi yapılmalı.", negative: "Albumin şu anda koruyucu görünüyor; yine de trend izlenmeli." },
	{ match: ["üre", "kreatinin"], positive: "Böbrek fonksiyonları, hidrasyon ve ilaçlar tekrar gözden geçirilmeli.", negative: "Böbrek parametreleri şu anda baskılayıcı görünmüyor; takip sürmeli." },
	{ match: ["crp"], positive: "Enflamasyon/infeksiyon odağı aranmalı ve uygun tetkikler tekrarlanmalı.", negative: "Enflamatuvar yük azalmış görünüyor; trend kontrol edilmeli." },
	{ match: ["ldh"], positive: "Tümör yükü veya doku hasarı açısından onkoloji değerlendirmesi düşünülmeli.", negative: "LDH tarafı yatıştırıcı görünüyor; yine de seri ölçüm önemli." },
	{ match: ["kalsiyum"], positive: "Kalsiyum dengesi ve kemik metabolizması klinik bağlamda yeniden değerlendirilmeli.", negative: "Kalsiyum şu anda destekleyici bir işaret veriyor." },
	{ match: ["bilirubin", "ast", "alt", "alp", "ggt"], positive: "Karaciğer fonksiyonları ve ilaç yükü birlikte değerlendirilmelidir.", negative: "Karaciğer enzimleri şu anda daha sakin görünüyor." },
];

function normalizeFeatureName(featureName) {
	return featureName.replace(/^(num__|cat__)/, "");
}

function humanizeFeatureName(featureName) {
	const normalized = normalizeFeatureName(featureName);
	const label = FEATURE_LABELS[normalized] || normalized;
	return label.replace(/_/g, " ");
}

function formatProbability(probability) {
	return `${(probability * 100).toFixed(1)}%`;
}

function formatDecimal(value, digits = 4) {
	return Number(value).toFixed(digits);
}

function scoreLabel(probability) {
	if (probability < 0.15) {
		return "Düşük risk";
	}
	if (probability < 0.4) {
		return "Orta risk";
	}
	return "Yüksek risk";
}

function shapActionForFeature(featureName, shapValue) {
	const normalized = normalizeFeatureName(featureName).toLowerCase();
	const rule = SHAP_ACTION_MAP.find((item) => item.match.some((match) => normalized.includes(match)));
	if (!rule) {
		return shapValue >= 0
			? "Bu değişken riski yukarı çekiyor; klinik bağlamda doğrulanmalı."
			: "Bu değişken riski aşağı çekiyor; yine de trend takibi gerekli.";
	}

	return shapValue >= 0 ? rule.positive : rule.negative;
}

function parseCsv(text) {
	const source = text.replace(/^\uFEFF/, "");
	const rows = [];
	let row = [];
	let field = "";
	let inQuotes = false;

	for (let index = 0; index < source.length; index += 1) {
		const character = source[index];
		const nextCharacter = source[index + 1];

		if (inQuotes) {
			if (character === '"') {
				if (nextCharacter === '"') {
					field += '"';
					index += 1;
				} else {
					inQuotes = false;
				}
			} else {
				field += character;
			}
			continue;
		}

		if (character === '"') {
			inQuotes = true;
			continue;
		}

		if (character === ',') {
			row.push(field);
			field = "";
			continue;
		}

		if (character === "\n") {
			row.push(field);
			rows.push(row);
			row = [];
			field = "";
			continue;
		}

		if (character === "\r") {
			continue;
		}

		field += character;
	}

	row.push(field);
	if (row.length > 1 || row[0] !== "") {
		rows.push(row);
	}

	return rows;
}

function unique(values) {
	return [...new Set(values)];
}

function validateColumns(headers, kind, mode) {
	const required = kind === "patient" ? BASE_FEATURE_COLUMNS : TRAINING_COLUMNS;
	const missing = required.filter((column) => !headers.includes(column));
	let extra = headers.filter((column) => !required.includes(column));
	const warnings = [];

	if (kind === "patient" && headers.includes(TARGET_COLUMN)) {
		warnings.push("Bu dosya hedef sütun içeriyor; bu, hasta veri önizlemesinden çok eğitim verisine benziyor.");
	}

	if (kind === "training" && mode === "until_time" && headers.includes(DEATH_DATE_COLUMN)) {
		warnings.push("Until_time modunda ölüm tarihi kullanılamaz; script bu sütunu sızıntı olmaması için düşürür.");
	}

	if (kind === "training" && mode === "normal" && !headers.includes(DEATH_DATE_COLUMN)) {
		warnings.push("Normal modda ölüm tarihi varsa model otomatik sinyal üretir; yoksa model yine çalışır ama normal modun anlamı zayıflar.");
	}

	if (kind === "training" && mode === "normal" && headers.includes(DEATH_DATE_COLUMN)) {
		extra = extra.filter((column) => column !== DEATH_DATE_COLUMN);
		warnings.push("Normal modda ölüm tarihi isteğe bağlıdır; model bunu otomatik olarak sinyale dönüştürür.");
	}

	if (headers.includes(DERIVED_SIGNAL_COLUMN)) {
		warnings.push("olum_tarihi_var sütunu elle eklenmiş; bunu scriptin üretmesi daha güvenlidir.");
	}

	return {
		missing,
		extra,
		warnings,
		isValid: missing.length === 0,
	};
}

function renderChips(columns) {
	return columns
		.map((column) => `<span class="chip">${column}</span>`)
		.join("");
}

function renderSchemaSections(container) {
	const html = `
		<div class="schema-grid">
			<section class="panel soft-panel">
				<h3>Zorunlu hasta özellikleri</h3>
				<p>Bu alanlar hasta verisi için gerekli temel giriş sütunlarıdır.</p>
				<div class="chip-grid">${renderChips(BASE_FEATURE_COLUMNS)}</div>
			</section>
			<section class="panel soft-panel">
				<h3>Eğitim verisi şablonu</h3>
				<p>Eğitim CSV dosyası aynı özellikleri ve hedef sütunu <strong>${TARGET_COLUMN}</strong> içermelidir.</p>
				<div class="chip-grid">${renderChips(TRAINING_COLUMNS)}</div>
			</section>
		</div>
	`;
	container.innerHTML = html;
}

function renderMetrics(model) {
	const metrics = document.querySelector("[data-role='metrics']");
	const matrix = document.querySelector("[data-role='confusion-matrix']");
	const status = document.querySelector("[data-role='model-status']");
	const command = document.querySelector("[data-role='command']");
	const note = document.querySelector("[data-role='model-note']");

	if (!metrics || !matrix) {
		return;
	}

	const summary = MODEL_SUMMARIES[model];
	metrics.innerHTML = `
		<div class="metric-card">
			<span>Doğruluk</span>
			<strong>${formatProbability(summary.accuracy)}</strong>
		</div>
		<div class="metric-card">
			<span>Eğitim satırı</span>
			<strong>${summary.trainSize}</strong>
		</div>
		<div class="metric-card">
			<span>Test satırı</span>
			<strong>${summary.testSize}</strong>
		</div>
		<div class="metric-card">
			<span>Özellik sayısı</span>
			<strong>${summary.featureCount}</strong>
		</div>
	`;

	matrix.innerHTML = `
		<div class="matrix-cell matrix-head">Tahmin 0</div>
		<div class="matrix-cell matrix-head">Tahmin 1</div>
		<div class="matrix-cell matrix-head">Gerçek 0</div>
		<div class="matrix-cell">${summary.confusionMatrix[0][0]}</div>
		<div class="matrix-cell">${summary.confusionMatrix[0][1]}</div>
		<div class="matrix-cell matrix-head">Gerçek 1</div>
		<div class="matrix-cell">${summary.confusionMatrix[1][0]}</div>
		<div class="matrix-cell">${summary.confusionMatrix[1][1]}</div>
	`;

	if (status) {
		status.textContent = summary.badge;
		status.className = `status-pill ${model === "until_time" ? "status-good" : "status-warn"}`;
	}

	if (command) {
		command.textContent = `python non_absolute_death.py --mode ${model}`;
	}

	if (note) {
		note.textContent = summary.warning;
	}
}

function renderGlobalShap(container) {
	container.innerHTML = SHAP_GLOBAL_IMPORTANCE.map((item, index) => {
		return `
			<div class="importance-row">
				<div class="importance-index">${index + 1}</div>
				<div class="importance-body">
					<strong>${humanizeFeatureName(item.feature)}</strong>
					<span>${item.feature}</span>
				</div>
				<div class="importance-value">${formatDecimal(item.meanAbsShap, 4)}</div>
			</div>
		`;
	}).join("");
}

function renderLocalCases(container) {
	container.innerHTML = SHAP_LOCAL_EXPLANATIONS.map((sample) => {
		const topFeatures = sample.topContributors
			.map((item) => {
				const className = item.shapValue >= 0 ? "shap-positive" : "shap-negative";
				return `
					<li class="shap-row ${className}">
						<div>
							<strong>${humanizeFeatureName(item.feature)}</strong>
							<p>${shapActionForFeature(item.feature, item.shapValue)}</p>
						</div>
						<span>${item.shapValue >= 0 ? "+" : ""}${formatDecimal(item.shapValue, 4)}</span>
					</li>
				`;
			})
			.join("");

		const recommendations = unique(sample.topContributors.slice(0, 4).map((item) => shapActionForFeature(item.feature, item.shapValue)));

		return `
			<article class="patient-card panel">
				<div class="patient-card-head">
					<div>
						<p class="eyebrow">Hasta ${sample.sampleIndex}</p>
						<h3>${sample.profile.kanser_turu}</h3>
						<p>${sample.profile.cinsiyet} · ${sample.profile.doğum_tarihi} doğumlu · ${sample.profile.department}</p>
					</div>
					<div class="risk-badge ${sample.predictionProbabilityDeath < 0.15 ? "risk-low" : "risk-medium"}">
						${scoreLabel(sample.predictionProbabilityDeath)}
					</div>
				</div>
				<div class="patient-score">
					<strong>${formatProbability(sample.predictionProbabilityDeath)}</strong>
					<span>ölüm olasılığı tahmini</span>
				</div>
				<div class="columns-grid">
					<div>
						<h4>SHAP etkileri</h4>
						<ul class="shap-list">${topFeatures}</ul>
					</div>
					<div>
						<h4>Bu hasta için ne yapılmalı?</h4>
						<ul class="recommendation-list">
							${recommendations.map((item) => `<li>${item}</li>`).join("")}
						</ul>
					</div>
				</div>
			</article>
		`;
	}).join("");
}

function renderCommandHint(container, mode, fileName = "<eğitim.csv>") {
	container.textContent = `python non_absolute_death.py --mode ${mode} --external-training-data ${fileName}`;
}

function makeTemplateCsv(mode) {
	const header = [...BASE_FEATURE_COLUMNS, TARGET_COLUMN];
	if (mode === "normal") {
		header.push(DEATH_DATE_COLUMN);
	}
	return `${header.join(",")}\n`;
}

function displayFileSummary(target, title, result, warnings = []) {
	const warningHtml = warnings.length
		? `<ul class="warning-list">${warnings.map((warning) => `<li>${warning}</li>`).join("")}</ul>`
		: "";

	target.innerHTML = `
		<div class="upload-result ${result.isValid ? "result-good" : "result-bad"}">
			<h4>${title}</h4>
			<p>${result.isValid ? "Şema eşleşti." : "Şema eksikleri var."}</p>
			<p><strong>Eksik:</strong> ${result.missing.length ? result.missing.map((item) => FEATURE_LABELS[item] || item).join(", ") : "Yok"}</p>
			<p><strong>Fazla:</strong> ${result.extra.length ? result.extra.map((item) => FEATURE_LABELS[item] || item).join(", ") : "Yok"}</p>
			${warningHtml}
		</div>
	`;
}

function updateTemplatePreview(container, mode) {
	const headers = [...BASE_FEATURE_COLUMNS, TARGET_COLUMN];
	if (mode === "normal") {
		headers.push(DEATH_DATE_COLUMN);
	}

	container.textContent = headers.join(",");
}

async function handleUpload(fileInput, outputElement, kind, mode, commandElement, templateElement) {
	const file = fileInput.files?.[0];
	if (!file) {
		return;
	}

	const text = await file.text();
	const rows = parseCsv(text);
	const headers = rows[0] || [];
	const result = validateColumns(headers, kind, mode);
	const extraWarnings = [...result.warnings];
	if (kind === "training") {
		extraWarnings.push(`Bu dosya ${rows.length - 1} kayıt satırı içeriyor.`);
	}
	if (kind === "patient") {
		extraWarnings.push(`Bu dosya ${rows.length - 1} kayıt satırı içeriyor.`);
	}

	displayFileSummary(outputElement, file.name, result, extraWarnings);
	renderCommandHint(commandElement, mode, file.name);
	updateTemplatePreview(templateElement, mode);
}

function setupMainPage() {
	const modelToggles = document.querySelectorAll("[data-model-toggle]");
	const shapContainer = document.querySelector("[data-role='shap-global']");
	const localContainer = document.querySelector("[data-role='shap-local']");
	const schemaContainer = document.querySelector("[data-role='schema']");
	const modeLabel = document.querySelector("[data-role='mode-label']");
	const commandElement = document.querySelector("[data-role='command']");
	const templateElement = document.querySelector("[data-role='template-preview']");
	const trainingStatus = document.querySelector("[data-role='training-status']");
	const patientStatus = document.querySelector("[data-role='patient-status']");
	const patientInput = document.querySelector("#patient-csv");
	const trainingInput = document.querySelector("#training-csv");
	const patientValidateButton = document.querySelector("#validate-patient");
	const trainingValidateButton = document.querySelector("#validate-training");
	const templateDownload = document.querySelector("#download-template");
	let activeMode = "until_time";

	if (!shapContainer || !localContainer || !schemaContainer) {
		return;
	}

	renderGlobalShap(shapContainer);
	renderLocalCases(localContainer);
	renderSchemaSections(schemaContainer);
	renderMetrics(activeMode);
	if (modeLabel) {
		modeLabel.textContent = MODEL_SUMMARIES[activeMode].title;
	}
	renderCommandHint(commandElement, activeMode, "<eğitim.csv>");
	updateTemplatePreview(templateElement, activeMode);

	const activateMode = (mode) => {
		activeMode = mode;
		renderMetrics(activeMode);
		if (modeLabel) {
			modeLabel.textContent = MODEL_SUMMARIES[activeMode].title;
		}
		updateTemplatePreview(templateElement, activeMode);
		renderCommandHint(commandElement, activeMode, trainingInput?.files?.[0]?.name || "<eğitim.csv>");
		if (trainingStatus && trainingInput?.files?.[0]) {
			handleUpload(trainingInput, trainingStatus, "training", activeMode, commandElement, templateElement);
		}
		if (patientStatus && patientInput?.files?.[0]) {
			handleUpload(patientInput, patientStatus, "patient", activeMode, commandElement, templateElement);
		}
	};

	modelToggles.forEach((button) => {
		button.addEventListener("click", () => {
			modelToggles.forEach((item) => item.classList.remove("is-active"));
			button.classList.add("is-active");
			activateMode(button.dataset.modelToggle || "until_time");
		});
	});

	patientValidateButton?.addEventListener("click", () => {
		handleUpload(patientInput, patientStatus, "patient", activeMode, commandElement, templateElement);
	});

	trainingValidateButton?.addEventListener("click", () => {
		handleUpload(trainingInput, trainingStatus, "training", activeMode, commandElement, templateElement);
	});

	templateDownload?.addEventListener("click", () => {
		const csv = makeTemplateCsv(activeMode);
		const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
		const url = URL.createObjectURL(blob);
		const link = document.createElement("a");
		link.href = url;
		link.download = `egitim_sablonu_${activeMode}.csv`;
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
		setTimeout(() => URL.revokeObjectURL(url), 1000);
	});
}

function setupModelPage() {
	const page = document.querySelector("[data-role='model-page']");
	if (!page) {
		return;
	}

	page.innerHTML = `
		<section class="hero hero-compact">
			<div>
				<p class="eyebrow">Model açıklaması</p>
				<h1>Model nasıl çalışıyor?</h1>
				<p>
					Bu sayfa, Random Forest tabanlı ölüm durumu modelinin veri akışı, sızıntı farkı ve SHAP yorumunu özetler.
				</p>
			</div>
			<a class="ghost-link" href="index.html">Ana sayfaya dön</a>
		</section>

		<section class="panel narrative">
			<h2>İki modun farkı</h2>
			<div class="mode-comparison">
				<article>
					<h3>Normal model</h3>
					<p>Ölüm tarihi sinyalinden türetilen ek bilgiyle öğrenir. Skor yüksek görünse de bu akış gerçek klinik kullanım için fazla iyimser olabilir.</p>
				</article>
				<article>
					<h3>Until_time model</h3>
					<p>Ölüm tarihi ve türevlerini dışarıda bırakır. SHAP yorumları bu modda daha güvenlidir ve yorumlanabilirliği daha yüksektir.</p>
				</article>
			</div>
		</section>

		<section class="panel narrative">
			<h2>Teknik akış</h2>
			<ol class="steps-list">
				<li>CSV okunur ve <strong>${TARGET_COLUMN}</strong> sütunu temizlenir.</li>
				<li>Sayısal alanlara medyan, kategorik alanlara en sık değer ile doldurma uygulanır.</li>
				<li>Kategorik alanlar OrdinalEncoder ile sayısallaştırılır.</li>
				<li>Random Forest tahmin yapar; SHAP TreeExplainer ise ağaç tabanlı açıklama üretir.</li>
			</ol>
		</section>

		<section class="panel narrative">
			<h2>CSV şeması</h2>
			<p>Hasta verisi için yalnızca özellik sütunları gerekir. Eğitim verisi için aynı sütunlara ek olarak hedef sütun gerekir.</p>
			<div class="schema-grid" data-role="schema"></div>
		</section>

		<section class="panel narrative">
			<h2>SHAP neden önemli?</h2>
			<p>
				SHAP, modelin tahmini yükselten ve düşüren etkileri her örnek için ayrıştırır. Bu projede öne çıkan ana faktörler albumin, üre, CRP, kalsiyum, LDH ve böbrek fonksiyonlarıdır.
			</p>
			<p>
				Önemli not: SHAP açıklamaları bir tedavi reçetesi değildir. Klinik ekip, bu işaretleri laboratuvar trendi, görüntüleme ve hasta öyküsüyle birlikte yorumlamalıdır.
			</p>
		</section>
	`;

	const schemaContainer = page.querySelector("[data-role='schema']");
	if (schemaContainer) {
		renderSchemaSections(schemaContainer);
	}
}

document.addEventListener("DOMContentLoaded", () => {
	setupMainPage();
	setupModelPage();
});
