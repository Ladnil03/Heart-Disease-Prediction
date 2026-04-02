"""
SHAP Explainability service.

Computes SHAP values for a given prediction so users can understand
which features most influenced their risk assessment.
"""
# Fixes: FIX-5 (SHAP format robustness), FIX-6 (cache TreeExplainer)

import shap
import numpy as np
from config import FEATURE_NAMES

# ---------------------------------------------------------------------------
# Module-level explainer cache (FIX-6)
# ---------------------------------------------------------------------------
_explainer_cache: dict = {}


def get_explainer(model):
    """Return a cached shap.TreeExplainer for *model*, creating one if needed."""
    model_id = id(model)
    if model_id not in _explainer_cache:
        _explainer_cache[model_id] = shap.TreeExplainer(model)
    return _explainer_cache[model_id]


# ---------------------------------------------------------------------------
# Robust SHAP value extractors (FIX-5)
# ---------------------------------------------------------------------------

def _extract_shap_vector(shap_values, class_index: int = 1) -> np.ndarray:
    """
    Handle all known SHAP output formats:
    - list of arrays  (old TreeExplainer binary)
    - 3-D ndarray     (new Explanation object .values)
    - 2-D ndarray     (single output)
    """
    if isinstance(shap_values, list):
        sv = shap_values[class_index][0]
    elif isinstance(shap_values, np.ndarray):
        if shap_values.ndim == 3:          # (n_samples, n_features, n_classes)
            sv = shap_values[0, :, class_index]
        elif shap_values.ndim == 2:
            sv = shap_values[0]
        else:
            sv = shap_values
    else:
        # shap.Explanation object (shap >= 0.41)
        vals = shap_values.values
        if vals.ndim == 3:
            sv = vals[0, :, class_index]
        elif vals.ndim == 2:
            sv = vals[0]
        else:
            sv = vals
    return sv


def _extract_base_value(base_value, class_index: int = 1) -> float:
    """Safely extract a scalar base value from any SHAP expected_value format."""
    if isinstance(base_value, (list, np.ndarray)):
        return float(base_value[class_index])
    try:                          # shap.Explanation expected_value
        return float(base_value[class_index])
    except (TypeError, IndexError):
        return float(base_value)


# ---------------------------------------------------------------------------
# Main compute function
# ---------------------------------------------------------------------------

def compute_shap(model, X: np.ndarray) -> dict:
    """
    Compute SHAP values for a single prediction.

    Returns
    -------
    dict with keys:
        shap_values      – {feature_name: float}
        top_risk_factors – feature names sorted by absolute SHAP impact
        base_value       – the explainer's expected (base) value
    """
    explainer = get_explainer(model)
    shap_values = explainer.shap_values(X)

    sv = _extract_shap_vector(shap_values, class_index=1)
    base_value = _extract_base_value(explainer.expected_value, class_index=1)

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
