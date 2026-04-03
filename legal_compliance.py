from typing import Dict, Any

class LegalComplianceModule:
    """Assesses legal risk based on similarity results and context."""
    
    def assess_compliance(self, detection_result, use_purpose: str = "general") -> Dict[str, str]:
        if detection_result.risk_level == "HIGH":
            status = "Non-Compliant"
        elif detection_result.risk_level == "MEDIUM":
            if use_purpose in ["educational", "research", "non-profit"]:
                status = "Fair Use Possible"
            else:
                status = "At Risk"
        elif detection_result.risk_level == "LOW":
            status = "Likely Safe (Attribution Advised)"
        else:
            status = "Compliant"
            
        return {
            "status": status,
            "notes": f"Assessed based on {use_purpose} use context.",
            "requires_license": detection_result.risk_level in ["HIGH", "MEDIUM"],
            "recommendations": [
                {
                    "priority": "HIGH" if detection_result.risk_level == "HIGH" else ("MEDIUM" if detection_result.risk_level == "MEDIUM" else "LOW"),
                    "category": "Usage",
                    "action": "Ensure appropriate fair-use doctrine or formal licensing."
                }
            ] if detection_result.risk_level != "NONE" else [],
            "suggested_modifications": ["Consider fully rewriting this section"] if detection_result.risk_level in ["HIGH", "MEDIUM"] else []
        }
