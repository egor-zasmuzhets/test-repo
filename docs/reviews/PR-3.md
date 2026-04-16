# Code Review Report - PR #3

> **PR:** testing github models requests
> **Author:** @egor-zasmuzhets
> **Generated:** 2026-04-16 15:12:36 UTC

## Summary

| Severity | Count |
|----------|-------|
| 🔴 High | 2 |
| 🟡 Medium | 4 |
| 🟢 Low | 2 |
| **Total** | 8 |

## Detailed Issues


### 🟡 SECURITY (line 18)

| Property | Value |
|----------|-------|
| **File** | `.github/workflows/ai-review.yml` |
| **Code** | `api-key: ${{ secrets.GROQ_API_KEY }}` |
| **Description** | The API key is stored as a secret, but it's still being used directly in the workflow. Consider using a more secure method to handle sensitive information. |
| **Suggestion** | Use an environment variable or a secure token instead of directly referencing the secret. |


### 🟢 STYLE (line 2)

| Property | Value |
|----------|-------|
| **File** | `.github/workflows/ai-review.yml` |
| **Description** | There is an empty line in the YAML file, which can make the code harder to read. |
| **Suggestion** | Remove empty lines to improve code readability. |


### 🔴 BUG (line 31)

| Property | Value |
|----------|-------|
| **File** | `titanic.py` |
| **Code** | `cabin_column = df_X["Cabin"].fillna("Unknown").apply(lambda row: row[0])` |
| **Description** | The variable df_X is not defined anywhere in the code. It should be X instead of df_X. |
| **Suggestion** | Replace df_X with X |


### 🟡 PERFORMANCE (line 83)

| Property | Value |
|----------|-------|
| **File** | `titanic.py` |
| **Code** | `rfr_imputation_age = RandomForestRegressor(n_estimators=100, max_depth=3, random_state=42)` |
| **Description** | The number of estimators in the RandomForestRegressor is set to 100. This could be computationally expensive for large datasets. Consider reducing the number of estimators or using a more efficient algorithm. |
| **Suggestion** | Consider using a more efficient algorithm or reducing the number of estimators |


### 🟢 STYLE (line 5)

| Property | Value |
|----------|-------|
| **File** | `titanic.py` |
| **Code** | `from sklearn.ensemble import RandomForestRegressor` |
| **Description** | The import statement for RandomForestRegressor is repeated. Remove the duplicate import statement. |
| **Suggestion** | Remove the duplicate import statement |


### 🟡 BUG (line 93)

| Property | Value |
|----------|-------|
| **File** | `titanic.py` |
| **Code** | `return None` |
| **Description** | The return statement is unreachable because it is after a raise statement. Remove the return statement. |
| **Suggestion** | Remove the return statement |


### 🟡 PERFORMANCE (line 120)

| Property | Value |
|----------|-------|
| **File** | `titanic.py` |
| **Code** | `X_transform["Fare"] = X_transform["Fare"].fillna(X_transform["Fare"].mean())` |
| **Description** | The mean of the Fare column is calculated every time the transform method is called. Consider calculating the mean in the fit method and storing it in an instance variable. |
| **Suggestion** | Calculate the mean in the fit method and store it in an instance variable |


### 🔴 BUG (line 141)

| Property | Value |
|----------|-------|
| **File** | `titanic.py` |
| **Code** | `X_transform.loc[X_transform["Age"].isna(), "AgeBins"] = self.imputations["AgeBins"].predict(X_transf` |
| **Description** | The predict method is called on self.imputations["AgeBins"], but self.imputations["AgeBins"] is not a trained model. It should be the trained RandomForestRegressor model. |
| **Suggestion** | Replace self.imputations["AgeBins"] with the trained RandomForestRegressor model |

