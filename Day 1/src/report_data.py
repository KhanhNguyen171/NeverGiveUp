from __future__ import annotations

import pandas as pd

from src.data_analysis import (
    data_overview,
    preview_data,
    data_schema,
    statistical_summary,
    missing_value_report,
    duplicate_report,
    numerical_features,
    categorical_features,
    categorical_summary,
    value_counts_report,
    groupby_target,
    groupby_aggregate,
    correlation_report,
    outlier_report,
    target_report,
    invalid_value_report, 
    feature_quality_report, 
    preprocessing_decision,
)

# ============================================================
# Configuration
# ============================================================

DEFAULT_TARGET = "charges"


# ============================================================
# Full EDA Report
# ============================================================

def report_data(
    df: pd.DataFrame,
    target: str = DEFAULT_TARGET,
) -> None:
    """
    Generate a structured EDA report.

    Report structure:

    1. Dataset Overview
    2. Data Quality
    3. Feature Types
    4. Distribution Analysis
    5. Relationship Analysis
    6. Feature Quality
    7. Preprocessing Decisions

    The analysis logic is implemented in data_analysis.py.
    This function only orchestrates the existing utilities.
    """

    print("\n")
    print("=" * 80)
    print("EDA REPORT")
    print("=" * 80)

    # ========================================================
    # 1. Dataset Overview
    # ========================================================

    print("\n")
    print("=" * 80)
    print("1. DATASET OVERVIEW")
    print("=" * 80)

    data_overview(df)

    print("\nTarget variable:")
    print(f"  - {target}")

    print("\nTarget exists:")
    print(f"  - {target in df.columns}")

    # Optional preview
    print("\nDataset preview:")
    preview_data(df)

    # ========================================================
    # 2. Data Quality
    # ========================================================

    print("\n")
    print("=" * 80)
    print("2. DATA QUALITY")
    print("=" * 80)

    # --------------------------------------------------------
    # 2.1 Missing Values
    # --------------------------------------------------------

    print("\n2.1 Missing Values")
    missing_value_report(df)

    # --------------------------------------------------------
    # 2.2 Duplicates
    # --------------------------------------------------------

    print("\n2.2 Duplicates")
    duplicate_report(df)

    # --------------------------------------------------------
    # 2.3 Invalid Values
    # --------------------------------------------------------

    print("\n2.3 Invalid Values")

    insurance_rules = { 
                       "age": lambda x: x > 0, 
                       "bmi": lambda x: x > 0, 
                       "children": lambda x: x >= 0, 
                       "charges": lambda x: x > 0, 
                       } 
    
    invalid_value_report( df, rules=insurance_rules)

    # --------------------------------------------------------
    # 2.4 Data Type Consistency
    # --------------------------------------------------------

    print("\n2.4 Data Type Consistency")
    data_schema(df)

    # ========================================================
    # 3. Feature Types
    # ========================================================

    print("\n")
    print("=" * 80)
    print("3. FEATURE TYPES")
    print("=" * 80)

    # --------------------------------------------------------
    # 3.1 Numerical Features
    # --------------------------------------------------------

    print("\n3.1 Numerical Features")

    numerical_columns = numerical_features(df)

    print(
        f"\nTotal numerical features: "
        f"{len(numerical_columns)}"
    )

    # --------------------------------------------------------
    # 3.2 Categorical Features
    # --------------------------------------------------------

    print("\n3.2 Categorical Features")

    categorical_columns = categorical_features(df)

    print(
        f"\nTotal categorical features: "
        f"{len(categorical_columns)}"
    )

    # --------------------------------------------------------
    # 3.3 Cardinality
    # --------------------------------------------------------

    print("\n3.3 Cardinality")

    categorical_summary(df)

    # --------------------------------------------------------
    # 3.4 Feature / Target Separation
    # --------------------------------------------------------

    print("\n3.4 Feature / Target Separation")

    if target in df.columns:

        features = [
            column
            for column in df.columns
            if column != target
        ]

        print(
            f"\nFeatures ({len(features)}):"
        )

        for column in features:
            print(f"  - {column}")

        print(
            f"\nTarget:"
            f" {target}"
        )

    else:

        print(
            f"Target '{target}' was not found."
        )

    # ========================================================
    # 4. Distribution Analysis
    # ========================================================

    print("\n")
    print("=" * 80)
    print("4. DISTRIBUTION ANALYSIS")
    print("=" * 80)

    # --------------------------------------------------------
    # 4.1 Numerical Distribution
    # --------------------------------------------------------

    print("\n4.1 Numerical Distribution")

    statistical_summary(df)

    # --------------------------------------------------------
    # 4.2 Categorical Distribution
    # --------------------------------------------------------

    print("\n4.2 Categorical Distribution")

    for column in categorical_columns:

        value_counts_report(
            df,
            column,
        )

    # --------------------------------------------------------
    # 4.3 Target Distribution
    # --------------------------------------------------------

    print("\n4.3 Target Distribution")

    if target in df.columns:

        target_report(
            df,
            target,
        )

    else:

        print(
            f"Target '{target}' was not found."
        )

    # ========================================================
    # 5. Relationship Analysis
    # ========================================================

    print("\n")
    print("=" * 80)
    print("5. RELATIONSHIP ANALYSIS")
    print("=" * 80)

    # --------------------------------------------------------
    # 5.1 Numerical → Target
    # --------------------------------------------------------

    print("\n5.1 Numerical → Target")

    correlation_report(
        df,
        target=target,
    )

    # --------------------------------------------------------
    # 5.2 Categorical → Target
    # --------------------------------------------------------

    print("\n5.2 Categorical → Target")

    if target in df.columns:

        for column in categorical_columns:

            groupby_target(
                df,
                group_columns=column,
                target=target,
            )

    else:

        print(
            f"Target '{target}' was not found."
        )

    # ========================================================
    # 6. Feature Quality
    # ========================================================

    print("\n")
    print("=" * 80)
    print("6. FEATURE QUALITY")
    print("=" * 80)
    
    feature_quality_report(df, variance_threshold=0.01, cardinality_threshold=20, correlation_threshold=0.90)

    # --------------------------------------------------------
    # 6.1 Constant Features
    # --------------------------------------------------------

    print("\n6.1 Constant Features")

    constant_features = [
        column
        for column in df.columns
        if df[column].nunique(dropna=False) <= 1
    ]

    if constant_features:

        for column in constant_features:
            print(f"  - {column}")

    else:

        print("  None detected.")

    # --------------------------------------------------------
    # 6.2 Near-zero Variance
    # --------------------------------------------------------

    print("\n6.2 Near-zero Variance")

    numerical = df.select_dtypes(
        include="number"
    )

    if numerical.empty:

        print("  No numerical features.")

    else:

        variance = numerical.var()

        print(
            variance
            .sort_values()
            .to_string()
        )

        print(
            "\n  Review features with "
            "extremely low variance."
        )

    # --------------------------------------------------------
    # 6.3 High Cardinality
    # --------------------------------------------------------

    print("\n6.3 High Cardinality")

    if categorical_columns:

        categorical_summary(df)

        print(
            "\n  Review categorical features "
            "with unusually high cardinality."
        )

    else:

        print("  No categorical features.")

    # --------------------------------------------------------
    # 6.4 Redundant / Highly Correlated Features
    # --------------------------------------------------------

    print(
        "\n6.4 Redundant / Highly Correlated Features"
    )

    correlation_report(df)

    print(
        "\n  Review pairs with high absolute "
        "correlation."
    )

    # --------------------------------------------------------
    # 6.5 Outliers
    # --------------------------------------------------------

    print("\n6.5 Outliers")

    outlier_report(df)

    # ========================================================
    # 7. Preprocessing Decisions
    # ========================================================

    print("\n")
    print("=" * 80)
    print("7. PREPROCESSING DECISIONS")
    print("=" * 80)
    
    preprocessing_decision(df, target=target, invalid_rules=insurance_rules, cardinality_threshold=20, correlation_threshold=0.90)

    # --------------------------------------------------------
    # 7.1 Missing Value Handling
    # --------------------------------------------------------

    print("\n7.1 Missing Value Handling")

    missing_report = missing_value_report(df)

    if missing_report.empty:

        print(
            "  Decision: No imputation required."
        )

    else:

        print(
            "  Decision: Define imputation strategy "
            "based on feature type and missing rate."
        )

    # --------------------------------------------------------
    # 7.2 Duplicate Handling
    # --------------------------------------------------------

    print("\n7.2 Duplicate Handling")

    duplicate_report(df)

    print(
        "  Decision: Review duplicate records "
        "before model training."
    )

    # --------------------------------------------------------
    # 7.3 Encoding
    # --------------------------------------------------------

    print("\n7.3 Encoding")

    if categorical_columns:

        print(
            "  Categorical features detected:"
        )

        for column in categorical_columns:
            print(f"    - {column}")

        print(
            "\n  Decision: Evaluate One-Hot Encoding "
            "for low-cardinality categorical features."
        )

    else:

        print(
            "  Decision: No categorical encoding required."
        )

    # --------------------------------------------------------
    # 7.4 Scaling
    # --------------------------------------------------------

    print("\n7.4 Scaling")

    if numerical_columns:

        print(
            "  Numerical features detected:"
        )

        for column in numerical_columns:
            print(f"    - {column}")

        print(
            "\n  Decision: Apply feature scaling "
            "before ANN training."
        )

        print(
            "  Candidate: StandardScaler."
        )

    else:

        print(
            "  Decision: No numerical scaling required."
        )

    # --------------------------------------------------------
    # 7.5 Outlier Handling
    # --------------------------------------------------------

    print("\n7.5 Outlier Handling")

    outlier_report(df)

    print(
        "\n  Decision: Investigate outliers before "
        "removing, clipping, or transforming them."
    )

    # --------------------------------------------------------
    # 7.6 Feature Selection
    # --------------------------------------------------------

    print("\n7.6 Feature Selection")

    if constant_features:

        print(
            "  Decision: Remove constant features:"
        )

        for column in constant_features:
            print(f"    - {column}")

    else:

        print(
            "  Decision: No constant features detected."
        )

    print(
        "\n  Review highly correlated or redundant "
        "features before final model design."
    )

    # --------------------------------------------------------
    # 7.7 Target Transformation
    # --------------------------------------------------------

    print("\n7.7 Target Transformation")

    if target in df.columns:

        target_series = df[target]

        skewness = target_series.skew()

        print(
            f"  Target skewness: {skewness:.4f}"
        )

        if abs(skewness) > 1:

            print(
                "  Decision: Target is strongly skewed."
            )

            print(
                "  Evaluate log1p transformation "
                "before ANN training."
            )

        else:

            print(
                "  Decision: No strong target skewness "
                "detected."
            )

    else:

        print(
            f"  Target '{target}' was not found."
        )

    # ========================================================
    # End
    # ========================================================

    print("\n")
    print("=" * 80)
    print("END OF EDA REPORT")
    print("=" * 80)
    print("\n")


# ============================================================
# Target-specific GroupBy Report
# ============================================================

def report_groupby(
    df: pd.DataFrame,
    target: str = DEFAULT_TARGET,
) -> None:
    """
    Run categorical → target analysis.
    """

    categorical_columns = categorical_features(df)

    if target not in df.columns:

        print(
            f"Target '{target}' was not found."
        )

        return

    print("\n")
    print("=" * 80)
    print("CATEGORICAL → TARGET ANALYSIS")
    print("=" * 80)

    for column in categorical_columns:

        groupby_target(
            df,
            group_columns=column,
            target=target,
        )

        print("\n")


# ============================================================
# Multi-metric GroupBy
# ============================================================

def report_groupby_metrics(
    df: pd.DataFrame,
    group_columns: str | list[str],
    aggregations: dict,
) -> pd.DataFrame:
    """
    Run custom multi-metric groupby analysis.
    """

    return groupby_aggregate(
        df,
        group_columns=group_columns,
        aggregations=aggregations,
    )
