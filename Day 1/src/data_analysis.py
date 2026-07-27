import pandas as pd

# ============================================================
# 1. Overview
# ============================================================

def data_overview(df: pd.DataFrame) -> None:
    """
    Display basic information about the dataset.
    """

    print("=" * 60)
    print("DATASET OVERVIEW")
    print("=" * 60)

    print(f"Shape      : {df.shape}")
    print(f"Samples    : {df.shape[0]:,}")
    print(f"Features   : {df.shape[1]:,}")

    print("\nColumns:")
    print(df.columns.tolist())

# ============================================================
# 2. Preview
# ============================================================

def preview_data(
    df: pd.DataFrame,
    n: int = 5,
) -> None:
    """
    Display sample records.
    """

    print("=" * 60)
    print("DATA PREVIEW")
    print("=" * 60)

    print("\nFirst rows:")
    print(df.head(n))

    print("\nRandom samples:")
    print(df.sample(n=min(n, len(df)), random_state=42))

    print("\nLast rows:")
    print(df.tail(n))


# ============================================================
# 3. Schema / Info
# ============================================================

def data_schema(df: pd.DataFrame) -> None:
    """
    Display dataframe schema.
    """

    print("=" * 60)
    print("DATA SCHEMA")
    print("=" * 60)

    df.info()


# ============================================================
# 4. Statistical Summary
# ============================================================

def statistical_summary(
    df: pd.DataFrame,
) -> None:
    """
    Display statistical summaries for numerical
    and categorical columns.
    """

    print("=" * 60)
    print("STATISTICAL SUMMARY")
    print("=" * 60)

    print("\nNumerical:")
    print(df.describe())

    print("\nCategorical:")
    print(df.describe(include="object"))


# ============================================================
# 5. Missing Values
# ============================================================

def missing_value_report(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Report missing values and percentages.
    """

    missing_count = df.isna().sum()

    missing_percentage = (
        df.isna().mean() * 100
    )

    report = pd.DataFrame({
        "missing_count": missing_count,
        "missing_percentage": missing_percentage,
    })

    report = report[
        report["missing_count"] > 0
    ].sort_values(
        "missing_count",
        ascending=False,
    )

    print("=" * 60)
    print("MISSING VALUES")
    print("=" * 60)

    if report.empty:
        print("No missing values.")
    else:
        print(report)

    return report


# ============================================================
# 6. Duplicate
# ============================================================

def duplicate_report(
    df: pd.DataFrame,
) -> None:
    """
    Report duplicate records.
    """

    duplicates = df.duplicated()

    n_duplicates = duplicates.sum()

    percentage = (
        n_duplicates / len(df) * 100
    )

    print("=" * 60)
    print("DUPLICATE DATA")
    print("=" * 60)

    print(f"Duplicates: {n_duplicates:,}")
    print(f"Percentage: {percentage:.2f}%")

    if n_duplicates > 0:
        print("\nDuplicate rows:")
        print(df[duplicates])


# ============================================================
# 7. Numerical Features
# ============================================================

def numerical_features(
    df: pd.DataFrame,
) -> list[str]:
    """
    Return numerical feature names.
    """

    columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    print("=" * 60)
    print("NUMERICAL FEATURES")
    print("=" * 60)

    for column in columns:
        print(f"- {column}")

    return columns


# ============================================================
# 8. Categorical Features
# ============================================================

def categorical_features(
    df: pd.DataFrame,
) -> list[str]:
    """
    Return categorical feature names.
    """

    columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    print("=" * 60)
    print("CATEGORICAL FEATURES")
    print("=" * 60)

    for column in columns:
        print(f"- {column}")

    return columns


# ============================================================
# 9. Unique Values
# ============================================================

def categorical_summary(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Summarize categorical columns.
    """

    categorical = df.select_dtypes(
        include=["object", "category"]
    )

    report = pd.DataFrame({
        "unique": categorical.nunique(),
        "missing": categorical.isna().sum(),
    })

    print("=" * 60)
    print("CATEGORICAL SUMMARY")
    print("=" * 60)

    print(report)

    return report


# ============================================================
# 10. Value Counts
# ============================================================

def value_counts_report(
    df: pd.DataFrame,
    column: str,
) -> pd.DataFrame:
    """
    Show frequency and percentage of categories.
    """

    counts = df[column].value_counts(
        dropna=False
    )

    percentage = (
        df[column]
        .value_counts(
            normalize=True,
            dropna=False,
        )
        .mul(100)
    )

    report = pd.DataFrame({
        "count": counts,
        "percentage": percentage,
    })

    print("=" * 60)
    print(f"VALUE COUNTS: {column}")
    print("=" * 60)

    print(report)

    return report

# Tái sử dụng cho groupby

def groupby_target(
    df: pd.DataFrame,
    group_columns: str | list[str],
    target: str,
) -> pd.DataFrame:
    """
    Analyze target statistics across groups.
    """

    if isinstance(group_columns, str):
        group_columns = [group_columns]

    report = (
        df.groupby(group_columns)[target]
        .agg(
            count="count",
            mean="mean",
            median="median",
            std="std",
            min="min",
            max="max",
        )
        .sort_values(
            "mean",
            ascending=False,
        )
    )

    print("=" * 60)
    print(
        f"GROUPBY: {group_columns} → {target}"
    )
    print("=" * 60)

    print(report)

    return report

# Groupby nhiều metric
def groupby_aggregate(
    df: pd.DataFrame,
    group_columns: str | list[str],
    aggregations: dict,
) -> pd.DataFrame:
    """
    Flexible groupby aggregation.
    """

    result = (
        df.groupby(group_columns)
        .agg(aggregations)
        .sort_values(
            by=list(aggregations.keys())[0],
            ascending=False,
        )
    )

    return result

def correlation_report(
    df: pd.DataFrame,
    target: str | None = None,
) -> pd.DataFrame:
    """
    Calculate correlation matrix for numerical features.
    """

    numerical = df.select_dtypes(
        include="number"
    )

    correlation = numerical.corr()

    print("=" * 60)
    print("CORRELATION MATRIX")
    print("=" * 60)

    if target is not None and target in correlation.columns:
        print(
            correlation[target]
            .sort_values(ascending=False)
        )
    else:
        print(correlation)

    return correlation

# Outlier bằng pandas
def outlier_report(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Detect numerical outliers using IQR.
    """

    numerical = df.select_dtypes(
        include="number"
    )

    q1 = numerical.quantile(0.25)
    q3 = numerical.quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outlier_mask = (
        (numerical < lower)
        | (numerical > upper)
    )

    report = pd.DataFrame({
        "Q1": q1,
        "Q3": q3,
        "IQR": iqr,
        "lower_bound": lower,
        "upper_bound": upper,
        "outlier_count": outlier_mask.sum(),
    })

    report["outlier_percentage"] = (
        report["outlier_count"]
        / len(df)
        * 100
    )

    print("=" * 60)
    print("OUTLIER REPORT")
    print("=" * 60)

    print(report)

    return report

# Target Analysis
def target_report(
    df: pd.DataFrame,
    target: str,
) -> pd.Series:
    """
    Analyze target distribution.
    """

    series = df[target]

    report = series.describe()

    print("=" * 60)
    print(f"TARGET REPORT: {target}")
    print("=" * 60)

    print(report)

    print(f"\nSkewness: {series.skew():.4f}")
    print(f"Kurtosis: {series.kurt():.4f}")

    return report

# ============================================================
# Invalid Values
# ============================================================

def invalid_value_report(
    df: pd.DataFrame,
    rules: dict[str, callable] | None = None,
) -> pd.DataFrame:
    """
    Detect invalid values based on domain-specific rules.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataset.

    rules : dict[str, callable], optional
        Dictionary mapping column names to validation functions.

        Example:
            {
                "age": lambda x: x > 0,
                "bmi": lambda x: x > 0,
                "children": lambda x: x >= 0,
                "charges": lambda x: x > 0,
            }

    Returns
    -------
    pd.DataFrame
        Invalid value statistics.
    """

    if rules is None:
        rules = {}

    records = []

    for column, rule in rules.items():

        if column not in df.columns:
            continue

        series = df[column]

        valid_mask = series.isna() | series.map(rule)

        invalid_mask = ~valid_mask

        invalid_count = int(
            invalid_mask.sum()
        )

        records.append({
            "column": column,
            "invalid_count": invalid_count,
            "invalid_percentage": (
                invalid_count / len(df) * 100
                if len(df) > 0
                else 0.0
            ),
        })

    report = pd.DataFrame(records)

    if not report.empty:
        report = report.sort_values(
            "invalid_count",
            ascending=False,
        )

    print("=" * 60)
    print("INVALID VALUE REPORT")
    print("=" * 60)

    if report.empty:
        print("No validation rules provided.")
    else:
        print(report.to_string(index=False))

    return report

# ============================================================
# Feature Quality
# ============================================================

def feature_quality_report(
    df: pd.DataFrame,
    variance_threshold: float = 0.01,
    cardinality_threshold: int = 20,
    correlation_threshold: float = 0.90,
) -> dict:
    """
    Analyze feature quality.

    Checks:
        1. Constant features
        2. Near-zero variance
        3. High-cardinality categorical features
        4. Highly correlated numerical features

    Parameters
    ----------
    df : pd.DataFrame
        Input dataset.

    variance_threshold : float
        Variance threshold for near-zero variance detection.

    cardinality_threshold : int
        Number of unique categories considered high cardinality.

    correlation_threshold : float
        Absolute correlation threshold for redundant features.

    Returns
    -------
    dict
        Feature quality report.
    """

    # ========================================================
    # 1. Constant Features
    # ========================================================

    constant_features = [
        column
        for column in df.columns
        if df[column].nunique(
            dropna=False
        ) <= 1
    ]

    # ========================================================
    # 2. Numerical Features
    # ========================================================

    numerical = df.select_dtypes(
        include="number"
    )

    variance = numerical.var()

    near_zero_variance = (
        variance[
            variance <= variance_threshold
        ]
        .sort_values()
    )

    # ========================================================
    # 3. High Cardinality
    # ========================================================

    categorical = df.select_dtypes(
        include=["object", "category"]
    )

    cardinality = categorical.nunique(
        dropna=True
    )

    high_cardinality = (
        cardinality[
            cardinality >= cardinality_threshold
        ]
        .sort_values(
            ascending=False
        )
    )

    # ========================================================
    # 4. Highly Correlated Features
    # ========================================================

    correlation = numerical.corr()

    highly_correlated_pairs = []

    if not correlation.empty:

        columns = correlation.columns

        for i in range(len(columns)):

            for j in range(i + 1, len(columns)):

                column_a = columns[i]
                column_b = columns[j]

                value = correlation.loc[
                    column_a,
                    column_b,
                ]

                if abs(value) >= correlation_threshold:

                    highly_correlated_pairs.append({
                        "feature_1": column_a,
                        "feature_2": column_b,
                        "correlation": value,
                        "abs_correlation": abs(value),
                    })

    highly_correlated = pd.DataFrame(
        highly_correlated_pairs
    )

    if not highly_correlated.empty:

        highly_correlated = (
            highly_correlated
            .sort_values(
                "abs_correlation",
                ascending=False,
            )
            .reset_index(drop=True)
        )

    # ========================================================
    # Report
    # ========================================================

    report = {
        "constant_features": constant_features,

        "variance": variance.sort_values(),

        "near_zero_variance": near_zero_variance,

        "cardinality": cardinality.sort_values(
            ascending=False
        ),

        "high_cardinality": high_cardinality,

        "highly_correlated": highly_correlated,
    }

    # ========================================================
    # Print
    # ========================================================

    print("=" * 60)
    print("FEATURE QUALITY REPORT")
    print("=" * 60)

    # Constant
    print("\n[1] Constant Features")

    if constant_features:
        for column in constant_features:
            print(f"- {column}")
    else:
        print("None detected.")

    # Near-zero variance
    print("\n[2] Near-zero Variance")

    if near_zero_variance.empty:
        print("None detected.")
    else:
        print(
            near_zero_variance
            .to_string()
        )

    # High cardinality
    print("\n[3] High Cardinality")

    if high_cardinality.empty:
        print("None detected.")
    else:
        print(
            high_cardinality
            .to_string()
        )

    # Correlation
    print(
        "\n[4] Highly Correlated Features"
    )

    if highly_correlated.empty:
        print("None detected.")
    else:
        print(
            highly_correlated
            .round(4)
            .to_string(index=False)
        )

    return report


# ============================================================
# Preprocessing Decisions
# ============================================================

def preprocessing_decision(
    df: pd.DataFrame,
    target: str,
    invalid_rules: dict[str, callable] | None = None,
    cardinality_threshold: int = 20,
    correlation_threshold: float = 0.90,
) -> pd.DataFrame:
    """
    Generate preprocessing decisions based on EDA findings.

    This function does NOT modify the dataset.

    It only produces recommendations for:
        - Missing values
        - Duplicates
        - Invalid values
        - Encoding
        - Scaling
        - Outlier handling
        - Feature selection
        - Target transformation

    Returns
    -------
    pd.DataFrame
        Preprocessing decision table.
    """

    decisions = []

    # ========================================================
    # 1. Missing Values
    # ========================================================

    missing = df.isna().sum()

    for column in df.columns:

        count = int(missing[column])

        if count > 0:

            percentage = (
                count / len(df) * 100
            )

            decisions.append({
                "category": "Missing Values",
                "feature": column,
                "evidence": (
                    f"{count} missing "
                    f"({percentage:.2f}%)"
                ),
                "decision": (
                    "Investigate and apply "
                    "imputation strategy."
                ),
            })

    if not decisions:

        decisions.append({
            "category": "Missing Values",
            "feature": "Dataset",
            "evidence": "No missing values.",
            "decision": "No imputation required.",
        })

    # ========================================================
    # 2. Duplicates
    # ========================================================

    duplicate_count = int(
        df.duplicated().sum()
    )

    if duplicate_count > 0:

        decisions.append({
            "category": "Duplicates",
            "feature": "Dataset",
            "evidence": (
                f"{duplicate_count} duplicate rows."
            ),
            "decision": (
                "Review and remove duplicates "
                "if they are accidental."
            ),
        })

    else:

        decisions.append({
            "category": "Duplicates",
            "feature": "Dataset",
            "evidence": "No duplicates.",
            "decision": "No duplicate handling required.",
        })

    # ========================================================
    # 3. Invalid Values
    # ========================================================

    invalid_report = invalid_value_report(
        df,
        rules=invalid_rules,
    )

    if not invalid_report.empty:

        invalid_rows = invalid_report[
            invalid_report["invalid_count"] > 0
        ]

        if not invalid_rows.empty:

            for _, row in invalid_rows.iterrows():

                decisions.append({
                    "category": "Invalid Values",
                    "feature": row["column"],
                    "evidence": (
                        f"{int(row['invalid_count'])} "
                        f"invalid values "
                        f"({row['invalid_percentage']:.2f}%)."
                    ),
                    "decision": (
                        "Investigate and correct, "
                        "remove, or transform."
                    ),
                })

        else:

            decisions.append({
                "category": "Invalid Values",
                "feature": "Dataset",
                "evidence": "No invalid values detected.",
                "decision": "No invalid-value handling required.",
            })

    # ========================================================
    # 4. Encoding
    # ========================================================

    categorical = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    if categorical:

        for column in categorical:

            cardinality = df[column].nunique(
                dropna=True
            )

            if cardinality <= cardinality_threshold:

                decisions.append({
                    "category": "Encoding",
                    "feature": column,
                    "evidence": (
                        f"{cardinality} unique categories."
                    ),
                    "decision": (
                        "Use One-Hot Encoding "
                        "for low-cardinality feature."
                    ),
                })

            else:

                decisions.append({
                    "category": "Encoding",
                    "feature": column,
                    "evidence": (
                        f"{cardinality} unique categories."
                    ),
                    "decision": (
                        "Use a suitable high-cardinality "
                        "encoding strategy."
                    ),
                })

    # ========================================================
    # 5. Scaling
    # ========================================================

    numerical = df.select_dtypes(
        include="number"
    ).columns.tolist()

    numerical_features_without_target = [
        column
        for column in numerical
        if column != target
    ]

    for column in numerical_features_without_target:

        decisions.append({
            "category": "Scaling",
            "feature": column,
            "evidence": (
                "Numerical feature used by ANN."
            ),
            "decision": (
                "Apply StandardScaler "
                "before ANN training."
            ),
        })

    # ========================================================
    # 6. Outlier Handling
    # ========================================================

    outliers = outlier_report(df)

    if not outliers.empty:

        for column, row in outliers.iterrows():

            count = int(
                row["outlier_count"]
            )

            percentage = (
                row["outlier_percentage"]
            )

            if count > 0:

                decisions.append({
                    "category": "Outlier Handling",
                    "feature": column,
                    "evidence": (
                        f"{count} outliers "
                        f"({percentage:.2f}%)."
                    ),
                    "decision": (
                        "Investigate whether values "
                        "are valid before removing, "
                        "clipping, or transforming."
                    ),
                })

    # ========================================================
    # 7. Feature Selection
    # ========================================================

    constant_features = [
        column
        for column in df.columns
        if column != target
        and df[column].nunique(
            dropna=False
        ) <= 1
    ]

    for column in constant_features:

        decisions.append({
            "category": "Feature Selection",
            "feature": column,
            "evidence": (
                "Constant feature."
            ),
            "decision": (
                "Remove from model input."
            ),
        })

    # Highly correlated features

    if len(numerical_features_without_target) > 1:

        correlation = (
            df[
                numerical_features_without_target
            ]
            .corr()
            .abs()
        )

        for i, column_a in enumerate(
            correlation.columns
        ):

            for column_b in correlation.columns[
                i + 1:
            ]:

                value = correlation.loc[
                    column_a,
                    column_b,
                ]

                if value >= correlation_threshold:

                    decisions.append({
                        "category": "Feature Selection",
                        "feature": (
                            f"{column_a} ↔ {column_b}"
                        ),
                        "evidence": (
                            f"|correlation| = "
                            f"{value:.4f}"
                        ),
                        "decision": (
                            "Investigate redundancy "
                            "before removing either feature."
                        ),
                    })

    # ========================================================
    # 8. Target Transformation
    # ========================================================

    if target in df.columns:

        target_series = df[target]

        if pd.api.types.is_numeric_dtype(
            target_series
        ):

            skewness = target_series.skew()

            if abs(skewness) > 1:

                decisions.append({
                    "category": "Target Transformation",
                    "feature": target,
                    "evidence": (
                        f"Skewness = {skewness:.4f}"
                    ),
                    "decision": (
                        "Evaluate log1p transformation "
                        "and compare model performance."
                    ),
                })

            else:

                decisions.append({
                    "category": "Target Transformation",
                    "feature": target,
                    "evidence": (
                        f"Skewness = {skewness:.4f}"
                    ),
                    "decision": (
                        "No target transformation "
                        "required based on skewness."
                    ),
                })

    # ========================================================
    # Final Report
    # ========================================================

    report = pd.DataFrame(
        decisions,
        columns=[
            "category",
            "feature",
            "evidence",
            "decision",
        ],
    )

    print("=" * 80)
    print("PREPROCESSING DECISION REPORT")
    print("=" * 80)

    print(
        report.to_string(
            index=False
        )
    )

    return report