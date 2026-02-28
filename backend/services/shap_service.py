"""
SHAP Explainability service.

Computes SHAP values for a given prediction so users can understand
which features most influenced their risk assessment.
"""

import shap
import numpy as np
from config import FEATURE_NAMES


def compute_shap(model, X: np.ndarray) -> dict:
    """
    Compute SHAP values for a single prediction.

    Returns
    -------
    dict with keys:
        shap_values  – {feature_name: float}
        top_risk_factors – feature names sorted by absolute SHAP impact
        base_value – the explainer's expected (base) value
    """
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    # For binary classifiers, shap_values is often a list [class_0, class_1]
    if isinstance(shap_values, list):
        sv = shap_values[1][0]
    else:
        sv = shap_values[0]

    base_value = explainer.expected_value
    if isinstance(base_value, (list, np.ndarray)):
        base_value = base_value[1]

    shap_dict = {
        FEATURE_NAMES[i]: float(sv[i]) for i in range(len(FEATURE_NAMES))
    }
    top_risk_factors = sorted(
        shap_dict, key=lambda k: abs(shap_dict[k]), reverse=True
    )

    return {
        "shap_values": shap_dict,
        "top_risk_factors": top_risk_factors,
        "base_value": float(base_value),
    }
