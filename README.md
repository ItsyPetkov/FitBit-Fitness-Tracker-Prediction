# FFTP: FitBit Fitness Tracker Prediction of High-Intensity Physical Activity

## Table of Contents

- [Project Background and Overview](#project-background-and-overview)
- [Data Structure Overview](#data-structure-overview)
- [Results and Evaluation Overview](#results-and-evaluation-overview)
  - [Scenario 1 - Baseline Models: Logistic Regression and SVC](#scenario-1---baseline-models-logistic-regression-and-svc)
  - [Scenario 2 - Random Forest and the Target Leakage Investigation](#scenario-2---random-forest-and-the-target-leakage-investigation)
- [EDA-based Insights and Predictive Features](#eda-based-insights-and-predictive-features)
  - [Initial Exploratory Data Analysis](#initial-exploratory-data-analysis)
  - [Data Pipeline and Transformation](#data-pipeline-and-transformation)
  - [Post-Transformation EDA and Correlation Analysis](#post-transformation-eda-and-correlation-analysis)
  - [Feature Engineering](#feature-engineering)
  - [Feature Selection](#feature-selection)
- [Business Intelligence Dashboards and Marketing Insights](#business-intelligence-dashboards-and-marketing-insights)
- [Code Quality and Engineering Practices](#code-quality-and-engineering-practices)
- [Recommendations](#recommendations)
- [Limitations](#limitations)
- [Future Work and Considerations](#future-work-and-considerations)

## Project Background and Overview

This project builds on the well-known Bellabeat / FitBit Fitness Tracker Data case study frequently used in data-analytics coursework, extending it from a descriptive BI exercise into a full data engineering and machine-learning pipeline. The underlying data is the public FitBit Fitness Tracker Data set (Kaggle, via Möbius, CC0), covering minute-, hourly- and daily-level activity, calorie, intensity and sleep data submitted by FitBit users across two survey windows in early 2016.

The raw survey exports are loaded into Google BigQuery and modelled with dbt (staging → intermediate → marts) into a single analysis-ready fact table. That table feeds a Python/scikit-learn pipeline that trains and compares three classifiers.

**Project goal**: given an hour of a user's wearable-device activity (steps, calories, movement intensity, and time-of-day context), predict whether that hour qualifies as "high intensity", without relying on the device's own on-board intensity classification.

This project can be divided into the following workflow stages:

* **Data Engineering**: Raw per-minute, per-hour and per-day FitBit exports are merged across survey waves and modelled through a layered dbt project (staging, intermediate, marts) into `fct_data_analysis_table`, with column-level dbt tests (`not_null`, `accepted_range`, `accepted_values`) enforced throughout.
* **Exploratory Data Analysis and Feature Selection**: Correlation and feature-importance analysis across 22 candidate features narrowed the predictor set down to the 11 most informative raw columns.
* **Feature Engineering**: Five additional ratio/interaction features (e.g. calories per step, steps × calories) were derived from the selected columns.
* **Modelling and Evaluation**: Logistic Regression, a Support Vector Classifier, and a Random Forest were trained on an identical 70/30 stratified split and compared using accuracy, precision, recall, F1, ROC-AUC and PR-AUC.
* **Critical Review**: An independent audit re-executed the entire pipeline end-to-end, uncovered and helped resolve two engineering bugs, and investigated why the Random Forest's near-perfect score should not be taken at face value.
* **Business Intelligence and Reporting**: Three Looker Studio dashboards and a marketing-facing insights report translate the same underlying data into consumer-behaviour findings and Bellabeat-specific recommendations.

A detailed technical audit report (architecture review, reproduced results, and the target-leakage investigation) can be found [here](https://github.com/ItsyPetkov/FitBit-Fitness-Tracker-Prediction/blob/main/reports/Data_Science_Project_Report.pdf).

A marketing-facing Insights and Recommendations report can be found [here](https://github.com/ItsyPetkov/FitBit-Fitness-Tracker-Prediction/blob/main/reports/Insights%20%26%20Recommendations%20Report.pdf).

The dbt data models (staging, intermediate and marts layers) can be found [here](https://github.com/ItsyPetkov/FitBit-Fitness-Tracker-Prediction/tree/main/models).

The Python ML pipeline source code can be found [here](https://github.com/ItsyPetkov/FitBit-Fitness-Tracker-Prediction/tree/main/src).

Feature engineering and feature selection logic can be found [here](https://github.com/ItsyPetkov/FitBit-Fitness-Tracker-Prediction/tree/main/src/features) and [here](https://github.com/ItsyPetkov/FitBit-Fitness-Tracker-Prediction/tree/main/src/notebooks).

Model training and evaluation code can be found [here](https://github.com/ItsyPetkov/FitBit-Fitness-Tracker-Prediction/tree/main/src/models).

The automated unit test suite can be found [here](https://github.com/ItsyPetkov/FitBit-Fitness-Tracker-Prediction/tree/main/src/tests).

BI dashboards (Activity Patterns, User Engagement, Consumer Behaviour Overview) can be found [here](https://github.com/ItsyPetkov/FitBit-Fitness-Tracker-Prediction/tree/main/dashboards).

## Data Structure Overview

The primary data set is the public FitBit Fitness Tracker Data set, submitted by consenting FitBit users via Amazon Mechanical Turk and covering two overlapping survey windows between 2016-03-12 and 2016-05-12. Minute-, hourly- and daily-level exports for steps, calories, intensity, METs and sleep are loaded into BigQuery as raw source tables, then modelled through dbt's staging and intermediate layers before being merged into `fct_data_analysis_table` via inner joins across the hourly, minute, daily and user-dimension fact tables.

That join is intentionally strict: a user only appears in the final analysis table if they have matching records across all four source tables for a given hour. As a result, the modelling table retains **24 users** with complete records, out of a broader raw panel of up to 35 users visible in the hourly-only BI dashboards.

The resulting table (`dataset/ml_dataset.csv`) has **574,807 rows and 30 columns** at hourly granularity, with no missing values and no duplicate rows. Below is the data dictionary for the final analysis table, adapted from the project's own dbt column documentation.

| Column | Type | Description | Used in model? |
|---|---|---|---|
| user_id | int | Unique identifier for each FitBit user. | No — identifier |
| activity_hour | timestamp | Hour-level timestamp of recorded activity data. | No |
| steps_per_hour | int | Total steps taken during the given hour. | Yes |
| calories_per_hour | int | Calories burned during the given hour. | Yes |
| total_intensities_per_hour | int | Total number of intensity units recorded during the given hour. | Yes |
| average_intensities_per_hour | float | Average intensity during the given hour (total ÷ 60). | Yes |
| hour_of_day | int | Hour number (0–23). | Yes |
| day_of_week | int | Day-of-week number (1–7). | Yes |
| day_name | string | Name of day (Monday–Sunday). | No — dropped at feature-selection stage |
| day_type | string | Weekday or Weekend. | No — dropped at feature-selection stage |
| time_of_day | string | Morning, Afternoon, Evening or Night. | No — dropped at feature-selection stage |
| activity_date | date | Date of recorded activity. | No |
| month | int | Month number (1–12). | No |
| activity_minute | timestamp | Minute-level timestamp for each recorded data point. | No |
| steps_per_minute | int | Steps taken during the given minute. | Yes |
| calories_per_minute | float | Calories burned during the given minute. | Yes |
| intensity_type | int | FitBit's own per-minute intensity classification (0–3), sourced independently from the device's accelerometer-based algorithm. | No — this is what the target is derived from |
| total_steps_per_day | int | Total steps taken during the day. | Yes |
| total_calories_per_day | int | Calories burned during the day. | Yes |
| total_distance_per_day | float | Total distance covered during the day. | No |
| very_active_minutes | int | Minutes classified as highly active during the day. | No |
| fairly_active_minutes | int | Minutes classified as fairly active during the day. | No |
| lightly_active_minutes | int | Minutes classified as lightly active during the day. | No |
| sedentary_minutes | int | Minutes classified as sedentary during the day. | No |
| total_minutes_asleep | int | Total minutes asleep per day. | No |
| total_time_in_bed | int | Total minutes in bed per day. | No |
| first_activity_date | date | First recorded date of user activity. | No |
| last_activity_date | date | Most recent recorded date of user activity. | No |
| days_recorded | int | Number of distinct days the user has recorded activity. | Yes |
| high_intensity | int | Binary target: 1 if intensity_type is 2 or 3, else 0. | Target variable |

The exact join logic that produces this table can be inspected [here](https://github.com/ItsyPetkov/FitBit-Fitness-Tracker-Prediction/blob/main/models/marts/fct_data_analysis_table.sql).

## Results and Evaluation Overview

Three classifiers were trained on an identical 70/30 stratified split (402,364 training rows, 172,443 test rows) and evaluated on the same held-out test set:

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|---|
| Logistic Regression | 98.88% | 0.803 | 0.737 | 0.769 | 0.996 | 0.851 |
| Support Vector Classifier | 98.94% | 0.835 | 0.727 | 0.777 | 0.983 | 0.846 |
| Random Forest | 99.995% | 0.999 | 0.999 | 0.999 | 1.000 | 1.000 |

Precision/recall/F1 are reported for the positive class (`high_intensity = 1`), which makes up only 2.5% of the data — a class distribution under which accuracy alone is a misleading headline number.

### Scenario 1 - Baseline Models: Logistic Regression and SVC

Logistic Regression and the RBF-kernel SVC were trained on scaled features and used as the baseline comparison against the more flexible Random Forest.

**Key findings**:
* Both models land in a similar, believable range: ~98.9% accuracy but only 72.7–73.7% recall and 80.3–83.5% precision on the minority "high intensity" class.
* In absolute terms, Logistic Regression misses 1,151 of 4,373 true high-intensity hours and raises 788 false alarms — a real, plausible error pattern for a genuinely learned linear/kernel decision boundary.
* Neither model is prone to the extreme overfitting seen in Scenario 2, which is itself informative about how separable the underlying classes really are.

### Scenario 2 - Random Forest and the Target Leakage Investigation

The Random Forest's headline numbers (99.995% accuracy, F1 = 0.999, 8 total errors out of 172,443 test rows) are unusual enough on a real-world behavioural dataset to warrant scrutiny before being taken at face value. An independent audit investigated this directly.

**Key findings**:
* An earlier version of the pipeline had a scaling bug — the Random Forest was trained on unscaled features but evaluated on scaled test data — which silently collapsed real-world recall to 6.2% while accuracy still looked plausible (97.6%). **This has since been fixed** in `main.py`.
* Tracing the dbt lineage resolves the open question the audit report could not answer from the data alone: `intensity_type` is not computed from `steps_per_minute` or `calories_per_minute` anywhere in this pipeline — it is FitBit's own independent, accelerometer-based per-minute intensity classification, joined in from `minuteIntensitiesNarrow_merged` (see [`fct_data_analysis_table.sql`](https://github.com/ItsyPetkov/FitBit-Fitness-Tracker-Prediction/blob/main/models/marts/fct_data_analysis_table.sql)).
* Even so, that classification is derived from the same physical exertion that `steps_per_minute` and `calories_per_minute` measure, so the two are extremely tightly correlated — the Random Forest's own feature importances put `calories_per_minute` and its engineered derivatives ahead of everything else combined.
* Retraining on a reduced 8-feature set with the most suspicious per-minute and hourly-intensity columns removed brought performance down to a more believable 99.73% accuracy, F1 = 0.944, and 89.8% recall — still ahead of the linear/kernel baselines, but no longer implausibly close to perfect.
* The takeaway is not that the Random Forest is broken, but that the reported 99.995% figure specifically should be treated as inflated, and the reduced-feature model is a more honest estimate of real predictive skill.

The full investigation, including the confirmatory experiment and supporting evidence tables, is documented in the [technical audit report](https://github.com/ItsyPetkov/FitBit-Fitness-Tracker-Prediction/blob/main/reports/Data_Science_Project_Report.pdf).

## EDA-based Insights and Predictive Features

This section summarises the exploratory analysis carried out on the analysis-ready table to inform feature engineering and selection for the classification task above.

### Initial Exploratory Data Analysis

The 574,807-row, 30-column analysis table contains no missing values and no duplicate rows. The target class is heavily imbalanced: 97.46% of hours are labelled "not high intensity" (560,229 rows) versus 2.54% labelled "high intensity" (14,578 rows) — a model predicting the majority class every time would already score 97.5% accuracy, which is why precision/recall are reported alongside accuracy throughout this project.

Descriptive statistics for the final 16 modelling features:

| Feature | Mean | Std | Min | Median | Max |
|---|---|---|---|---|---|
| steps_per_hour | 332.3 | 640.2 | 0 | 74.0 | 7,801 |
| calories_per_hour | 97.0 | 60.1 | 42 | 81.0 | 669 |
| total_intensities_per_hour | 12.7 | 21.2 | 0 | 5.0 | 180 |
| average_intensities_per_hour | 0.21 | 0.35 | 0 | 0.08 | 3.00 |
| hour_of_day | 11.5 | 6.9 | 0 | 11.0 | 23 |
| day_of_week | 4.0 | 2.0 | 1 | 4.0 | 7 |
| steps_per_minute | 5.5 | 17.5 | 0 | 0.0 | 186 |
| calories_per_minute | 1.6 | 1.4 | 0.7 | 1.17 | 19.3 |
| total_steps_per_day | 8,260 | 4,294 | 0 | 8,585 | 22,770 |
| total_calories_per_day | 2,318.7 | 808.0 | 0 | 2,180 | 4,900 |
| days_recorded | 59.1 | 5.6 | 30 | 61.0 | 61 |
| hourly_steps_calories* | 60,158 | 188,426 | 0 | 5,459 | 4,975,593 |
| minute_steps_calories* | 27.9 | 118.4 | 0 | 0.0 | 2,905.7 |
| calories_per_step_hour* | 24.0 | 40.8 | 0.05 | 1.03 | 669.0 |
| calories_per_step_minute* | 1.0 | 0.67 | 0.04 | 1.01 | 19.3 |
| daily_calories_per_step* | 0.76 | 3.66 | 0 | 0.30 | 49.6 |

_\* Engineered feature — see [Feature Engineering](#feature-engineering)._

### Data Pipeline and Transformation

Unlike a project working from a single flat CSV, this data arrives as ten separate per-metric FitBit exports, split across two overlapping survey waves. The dbt project resolves this in three layers:

* **Staging**: each metric (steps, calories, intensities, METs, sleep) has its own staging model that unions and de-duplicates the two survey-wave source tables for that metric.
* **Intermediate**: minute-level metrics are joined together into a single per-minute activity table, and daily activity and sleep are combined into a per-day table.
* **Marts**: hourly, minute, daily and user-dimension fact tables are built and finally merged into `fct_data_analysis_table`.

Because the underlying Kaggle export is already fairly clean, the dbt layer's main role is consolidation and validation rather than heavy outlier removal — every column in the final table carries `not_null` and range/accepted-value tests (e.g. `hour_of_day` between 0–23, `day_type` restricted to Weekday/Weekend), which double as living documentation of what "clean" means for this dataset.

### Post-Transformation EDA and Correlation Analysis

A correlation heatmap of the 11 raw selected features surfaces a clear redundancy: `total_intensities_per_hour` and `average_intensities_per_hour` correlate at 1.00, since the latter is simply the former divided by 60. `steps_per_hour`, `calories_per_hour`, and both intensity columns also cluster tightly together (r ≈ 0.88), reflecting that they are all different views of the same underlying physical exertion.

### Feature Engineering

Five features were derived on top of the 11 selected raw columns:

* `hourly_steps_calories` = steps_per_hour × calories_per_hour
* `minute_steps_calories` = steps_per_minute × calories_per_minute
* `calories_per_step_hour` = calories_per_hour ÷ (steps_per_hour + 1)
* `calories_per_step_minute` = calories_per_minute ÷ (steps_per_minute + 1)
* `daily_calories_per_step` = total_calories_per_day ÷ (total_steps_per_day + 1)

The `+1` denominators avoid division-by-zero for the many hours with zero recorded steps (the median `steps_per_hour` is 74, with a floor of 0).

### Feature Selection

Starting from 22 candidate features (numeric and one-hot-encoded categorical), a Random Forest importance ranking showed every categorical level (`day_name`, `day_type`, `time_of_day`) scoring below 0.005 importance, while `calories_per_minute` (0.314) and `steps_per_minute` (0.227) dominated. Applying a 0.01 importance threshold removed all categorical columns, leaving the 11 numeric features used throughout this project. As in comparable prediction tasks, the categorical/calendar context added little once continuous activity signal was available.

## Business Intelligence Dashboards and Marketing Insights

Alongside the ML pipeline, three Looker Studio dashboards (Activity Patterns, User Engagement, Consumer Behaviour Overview) surface the same underlying data for a non-technical, marketing-facing audience, summarised in the [Insights and Recommendations report](https://github.com/ItsyPetkov/FitBit-Fitness-Tracker-Prediction/blob/main/reports/Insights%20%26%20Recommendations%20Report.pdf).

Headline figures from that report: 24 total users, 8,259.99 average daily steps, 252.44 average active minutes, 419.57 minutes (~7 hours) average sleep duration, and 94.04% of users classified as highly engaged based on 59.12 average recorded days (61-day median).

Five recommended marketing actions came out of this analysis:

1. **Use time-based activity messaging** — align prompts with each user's actual active hours rather than sending identical messages throughout the day.
2. **Promote small, achievable movement goals** — personalised nudges rather than one universal step target.
3. **Position Bellabeat as a holistic wellness companion** — combine activity and sleep content rather than treating steps as the only outcome.
4. **Build on existing engagement** — reinforce the already-high engagement rate with streaks, milestones and weekly summaries.
5. **Personalize by engagement stage** — different messaging for newer versus long-term users.

## Code Quality and Engineering Practices

The Python pipeline is organised into clearly separated modules (data ingestion, feature engineering, model training, evaluation, orchestration) and backed by a six-file `unittest` suite that mocks the BigQuery client, verifies the exact arithmetic of every engineered feature, and confirms the logging setup writes to disk. This is complemented on the data side by dbt's own column-level tests, so both the SQL and Python layers of the pipeline are independently validated.

An independent audit of this codebase identified the following issues:

| Issue | Status |
|---|---|
| Random Forest evaluated on mismatched (scaled) test data, silently collapsing real recall to 6.2% | ✅ Fixed |
| Function name typo (`train_rondom_forest_classifier`) | ✅ Fixed |
| No pinned dependency file | ✅ Fixed — `pyproject.toml` and `requirements.txt` added |
| Metrics are `print()`-ed rather than logged or persisted | Open |
| No model persistence in the pipeline (`save_model_state` defined but unused) | Open |
| Hardcoded relative paths (`../data_raw/data.csv`) | Open |
| `matplotlib.pyplot.show()` calls block in headless/CI environments | Open |
| Hyperparameter-tuning notebook (`GridSearchCV`) has no execution output | Open |

The full audit, including how each issue was confirmed, is available in the [technical report](https://github.com/ItsyPetkov/FitBit-Fitness-Tracker-Prediction/blob/main/reports/Data_Science_Project_Report.pdf).

## Recommendations

Based on the modelling results and the code quality review, it is recommended to treat the **reduced-feature Random Forest (F1 = 0.944)** from Scenario 2 as the honest performance benchmark for this task, rather than the unqualified 99.995% headline figure. Applying `class_weight="balanced"` or a resampling strategy (SMOTE, undersampling) to the baseline models, and reporting precision-recall curves as the primary evaluation view given the 97.5/2.5 class split, would likely narrow the gap further while keeping results trustworthy.

## Limitations

Despite the relatively thorough analysis provided above, this project is still prone to the following limitations:

* **Small, short panel**: the analysis-ready table retains only 24 users with complete cross-table records, tracked over roughly two months — patterns may not generalise to a larger or more diverse population.
* **Severe class imbalance**: only 2.5% of hours are labelled "high intensity", which limits how much can be learned about that class even with careful handling.
* **Near-tautological prediction task**: because FitBit's own intensity label is highly correlated with the steps/calories features used to predict it, this task is inherently easier than most behavioural-prediction problems, which caps how much the modelling results can be generalised to less closely related targets.
* **Compute-constrained reproduction**: the SVC's audited results were reproduced on a stratified 12,000-row subsample rather than the full training set, due to the RBF kernel's poor scaling on the single-core audit environment.

## Future Work and Considerations

To build upon this work, the following steps could be considered:

* **Persist metrics and models**: log evaluation metrics to a file per run and call the existing `save_model_state`/`load_model_state` helpers so results and trained models survive a pipeline run.
* **Address the class imbalance directly**: apply class weighting or resampling and re-evaluate all three models under identical conditions.
* **Adopt the reduced feature set as default**: make the leakage-aware, 8-feature Random Forest the pipeline's primary reported model, with the full 16-feature version retained for comparison only.
* **Execute the hyperparameter study**: run the existing `GridSearchCV` notebook and feed its winning configuration back into `train_model.py`.
* **Connect the ML signal to the BI layer**: feed the "high intensity" classifier's output into the Activity Patterns dashboard to power the context-aware activity prompts recommended in the Insights and Recommendations report.
* **Expand the panel**: incorporate additional users and a longer time window to test whether the current findings hold at scale.
