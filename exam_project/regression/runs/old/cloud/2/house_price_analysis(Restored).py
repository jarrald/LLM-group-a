#House Price Prediction - King County

# Target: price

# ~4600 rows, 18 features



import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

import seaborn as sns

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV

from sklearn.preprocessing import StandardScaler, OneHotEncoder

from sklearn.compose import ColumnTransformer

from sklearn.pipeline import Pipeline

from sklearn.impute import SimpleImputer

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

from sklearn.linear_model import Ridge

from sklearn.metrics import mean_squared_error, r2_score

import warnings

warnings.filterwarnings("ignore")



# ── Load ──────────────────────────────────────────────────────────────────────

df = pd.read_csv("regression/house_prices.csv")



# ── Inspect ───────────────────────────────────────────────────────────────────

print(f"Shape: {df.shape}")

print(f"\nMissing per column:\n{df.isnull().sum()}")

print(f"\nData types:\n{df.dtypes}")

print(f"\nBasic stats:\n{df.describe()}")

print(f"\nDuplicates: {df.duplicated().sum()}")



# ── Clean ─────────────────────────────────────────────────────────────────────

df = df.drop(columns=["date", "street", "country", "statezip"])

df = df.drop_duplicates()



# ── Data quality checks ───────────────────────────────────────────────────────

print("\n=== Data quality ===")

print(f"Zero bedrooms: {(df['bedrooms'] == 0).sum()}")

print(f"Zero bathrooms: {(df['bathrooms'] == 0).sum()}")

print(f"Zero sqft_living: {(df['sqft_living'] == 0).sum()}")

print(f"Zero sqft_lot: {(df['sqft_lot'] == 0).sum()}")

print(f"yr_renovated == 0: {(df['yr_renovated'] == 0).sum()} (no renovation)")

print(f"yr_renovated > 0: {(df['yr_renovated'] > 0).sum()} (renovated)")



# ── Univariate analysis ───────────────────────────────────────────────────────

print("\n=== Univariate analysis ===")



fig, axes = plt.subplots(1, 2, figsize=(12, 4))

sns.histplot(df["price"], bins=50, ax=axes[0])

axes[0].set_title("Price distribution")

axes[0].set_xlabel("Price ($)")

sns.boxplot(x=df["price"], ax=axes[1])

axes[1].set_title("Price boxplot")

plt.tight_layout()

plt.savefig("regression/report/univariate_price.png", dpi=150)

print("Saved: regression/report/univariate_price.png")



price_log = np.log1p(df["price"])

Q1 = price_log.quantile(0.25)

Q3 = price_log.quantile(0.75)

IQR = Q3 - Q1

lower = price_log < Q1 - 1.5 * IQR

upper = price_log > Q3 + 1.5 * IQR

outlier_count = lower.sum() + upper.sum()

print(f"\nPrice outliers (1.5 IQR on log(price)): {outlier_count} rows")



fig, axes = plt.subplots(1, 2, figsize=(12, 4))

sns.histplot(np.log1p(df["price"]), bins=50, ax=axes[0])

axes[0].set_title("Log(price) distribution")

sns.boxplot(x=np.log1p(df["price"]), ax=axes[1])

axes[1].set_title("Log(price) boxplot")

plt.tight_layout()

plt.savefig("regression/report/univariate_price_log.png", dpi=150)

print("Saved: regression/report/univariate_price_log.png")



num_cols = df.select_dtypes(include=[np.number]).columns.tolist()

corr = df[num_cols].corr(numeric_only=True)

plt.figure(figsize=(10, 8))

sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0)

plt.title("Correlation matrix")

plt.tight_layout()

plt.savefig("regression/report/correlation_matrix.png", dpi=150)

print("Saved: regression/report/correlation_matrix.png")



print("\nTop 10 features correlated with price:")

print(corr["price"].sort_values(ascending=False).head(10))



fig, axes = plt.subplots(2, 2, figsize=(14, 10))

sns.scatterplot(data=df, x="sqft_living", y="price", ax=axes[0, 0], alpha=0.3)

axes[0, 0].set_title("Price vs Sqft Living")

sns.scatterplot(data=df, x="bedrooms", y="price", ax=axes[0, 1], alpha=0.3)

axes[0, 1].set_title("Price vs Bedrooms")

sns.scatterplot(data=df, x="bathrooms", y="price", ax=axes[1, 0], alpha=0.3)

axes[1, 0].set_title("Price vs Bathrooms")

sns.scatterplot(data=df, x="condition", y="price", ax=axes[1, 1], alpha=0.3)

axes[1, 1].set_title("Price vs Condition")

plt.tight_layout()

plt.savefig("regression/report/bivariate_price.png", dpi=150)

print("Saved: regression/report/bivariate_price.png")



# ── Feature engineering ───────────────────────────────────────────────────────

print("\n=== Feature engineering ===")



for col in ["sqft_living", "sqft_lot", "sqft_above", "sqft_basement"]:

 if col in df.columns:

 df[f"log_{col}"] = np.log1p(df[col])



if "sqft_above" in df.columns and "sqft_basement" in df.columns:

 df["total_sqft"] = df["sqft_above"] + df["sqft_basement"]



if "yr_built" in df.columns:

 df["house_age"] = 2015 - df["yr_built"]

 df["is_new"] = (df["yr_built"] >= 2010).astype(int)



if "yr_renovated" in df.columns:

 df["is_renovated"] = (df["yr_renovated"] > 0).astype(int)



if "waterfront" in df.columns and "view" in df.columns:

 df["waterfront_view"] = df["waterfront"] * df["view"]



if "bedrooms" in df.columns:

 df["has_5_plus_bedrooms"] = (df["bedrooms"] >= 5).astype(int)



if "bathrooms" in df.columns:

 df["total_bathrooms"] = df["bedrooms"] + df["bathrooms"]



# ── Modeling ──────────────────────────────────────────────────────────────────

print("\n=== Modeling ===")

price_log_clean = np.log1p(df["price"])

Q1_log = price_log_clean.quantile(0.25)

Q3_log = price_log_clean.quantile(0.75)

IQR_log = Q3_log - Q1_log

lower_log = price_log_clean < Q1_log - 1.5 * IQR_log

upper_log = price_log_clean > Q3_log + 1.5 * IQR_log

clean_mask = ~(lower_log | upper_log)



df_model = df.copy()

df_model = df_model[clean_mask]

print(f"Modeling with {len(df_model)} rows (removed {len(df) - len(df_model)} price outliers)")



num_cols_final = df_model.select_dtypes(include=[np.number]).columns.tolist()

feature_cols = [c for c in num_cols_final if c != "price"]

print(f"Numeric features: {feature_cols}")



X = df_model[feature_cols]

y = np.log1p(df_model["price"])



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Train: {len(X_train)}, Test: {len(X_test)}")



num_features = [c for c in X.columns if c != "bedrooms"]

preprocessor = ColumnTransformer(

 transformers=[

 ("num", StandardScaler(), num_features),

 ]

)



# ── Ridge Regression ──────────────────────────────────────────────────────────

print("\n--- Ridge Regression ---")

pipe_ridge = Pipeline([

 ("preprocess", preprocessor),

 ("model", Ridge(alpha=1.0))

])

pipe_ridge.fit(X_train, y_train)

y_pred_ridge = pipe_ridge.predict(X_test)

ridge_rmse = np.sqrt(mean_squared_error(y_test, y_pred_ridge))

ridge_r2 = r2_score(y_test, y_pred_ridge)

print(f"RMSE (log scale): {ridge_rmse:.4f}")

print(f"R²: {ridge_r2:.4f}")



coef = pipe_ridge.named_steps["model"].coef_

coef_df = pd.DataFrame({"feature": num_features, "coef": coef})

coef_df["abs_coef"] = coef_df["coef"].abs()

coef_df = coef_df.sort_values("abs_coef", ascending=False)

print("\nTop 10 coefficients:")

print(coef_df.head(10))



# ── Random Forest ─────────────────────────────────────────────────────────────

print("\n--- Random Forest ---")

pipe_rf = Pipeline([

 ("preprocess", preprocessor),

 ("model", RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1))

])

pipe_rf.fit(X_train, y_train)

y_pred_rf = pipe_rf.predict(X_test)

rf_rmse = np.sqrt(mean_squared_error(y_test, y_pred_rf))

rf_r2 = r2_score(y_test, y_pred_rf)

print(f"RMSE (log scale): {rf_rmse:.4f}")

print(f"R²: {rf_r2:.4f}")



rf_importance = pd.DataFrame({

 "feature": num_features,

 "importance": pipe_rf.named_steps["model"].feature_importances_

})

rf_importance = rf_importance.sort_values("importance", ascending=False)

print("\nTop 10 RF feature importances:")

print(rf_importance.head(10))



# ── Gradient Boosting ─────────────────────────────────────────────────────────

print("\n--- Gradient Boosting (with tuning) ---")

param_grid = {

 "model__n_estimators": [200, 500],

 "model__max_depth": [4, 6],

 "model__learning_rate": [0.05, 0.1],

}

pipe_gb = Pipeline([

 ("preprocess", preprocessor),

 ("model", GradientBoostingRegressor(random_state=42))

])

gs = GridSearchCV(pipe_gb, param_grid, cv=3, scoring="neg_mean_squared_error", n_jobs=-1)

gs.fit(X_train, y_train)

print(f"Best params: {gs.best_params_}")

y_pred_gb = gs.predict(X_test)

gb_rmse = np.sqrt(mean_squared_error(y_test, y_pred_gb))

gb_r2 = r2_score(y_test, y_pred_gb)

print(f"RMSE (log scale): {gb_rmse:.4f}")

print(f"R²: {gb_r2:.4f}")



# ── Ensemble ──────────────────────────────────────────────────────────────────

print("\n--- Ensemble (Ridge + RF + GB) ---")

y_pred_ensemble = (y_pred_ridge + y_pred_rf + y_pred_gb) / 3

ensemble_rmse = np.sqrt(mean_squared_error(y_test, y_pred_ensemble))

ensemble_r2 = r2_score(y_test, y_pred_ensemble)

print(f"RMSE (log scale): {ensemble_rmse:.4f}")

print(f"R²: {ensemble_r2:.4f}")



# ── Final Evaluation ──────────────────────────────────────────────────────────

print("\n=== Final Evaluation (test set, log scale) ===")

print(f"Ridge RMSE: {ridge_rmse:.4f} R²: {ridge_r2:.4f}")

print(f"RF RMSE: {rf_rmse:.4f} R²: {rf_r2:.4f}")

print(f"GB RMSE: {gb_rmse:.4f} R²: {gb_r2:.4f}")

print(f"Ensemble RMSE: {ensemble_rmse:.4f} R²: {ensemble_r2:.4f}")



print("\n=== Cross-validation (5-fold, Ridge) ===")

cv_scores = cross_val_score(pipe_ridge, X_train, y_train, cv=5, scoring="neg_mean_squared_error")

print(f"CV RMSE: {np.sqrt(-cv_scores.mean()):.4f} ± {np.sqrt(cv_scores.std()):.4f}")



# ── Save results ───────────────────────────────────────────────────────────────

import os

os.makedirs("regression/report", exist_ok=True)

pd.DataFrame({"log_price_pred": y_pred_ensemble, "actual_log_price": y_test}).to_csv(

 "regression/report/ensemble_predictions.csv", index=False

)

print("\nSaved: regression/report/ensemble_predictions.csv")

print("\nDone.")
