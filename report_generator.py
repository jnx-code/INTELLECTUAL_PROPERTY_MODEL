import json
import uuid
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, Any, List
from attribution_engine import AttributionEngine
from legal_compliance import LegalComplianceModule

@dataclass
class CopyrightReport:
    detection_summary: Dict[str, Any]
    compliance_assessment: Dict[str, Any]
    overall_recommendation: str
    attributions: List[Dict[str, Any]]
    report_id: str = field(default_factory=lambda: datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:15])

class ReportGenerator:
    """Consolidates findings into a standardized report format."""
    
    def __init__(self):
        self.attribution_engine = AttributionEngine()
        self.compliance_module = LegalComplianceModule()
        
    def generate(self, detection_result, use_purpose: str = "general", citation_style: str = "APA") -> CopyrightReport:
        summary = {
            'risk_level': detection_result.risk_level,
            'highest_similarity': detection_result.highest_similarity,
            'matches_found': len(detection_result.matches)
        }
        
        compliance = self.compliance_module.assess_compliance(detection_result, use_purpose)
        attributions = self.attribution_engine.generate_attributions(detection_result.matches, citation_style)
        
        if detection_result.risk_level == "HIGH":
            recommendation = "Do not use. Content is heavily copyrighted."
        elif detection_result.risk_level == "MEDIUM":
            recommendation = "Use with caution. Requires proper attribution and checks for fair use."
        elif detection_result.risk_level == "LOW":
            recommendation = "Likely safe to use, but attribution is recommended for caution."
        else:
            recommendation = "Safe to use. No significant matches found."
            
        return CopyrightReport(
            detection_summary=summary,
            compliance_assessment=compliance,
            overall_recommendation=recommendation,
            attributions=attributions
        )
        
    def format_report_text(self, report: CopyrightReport) -> str:
        lines = []
        lines.append("COPYRIGHT REPORT")
        lines.append("-" * 20)
        lines.append(f"Risk Level: {report.detection_summary['risk_level']}")
        lines.append(f"Highest Similarity: {report.detection_summary['highest_similarity']:.2%}")
        lines.append(f"Matches Found: {report.detection_summary['matches_found']}")
        lines.append(f"Compliance Status: {report.compliance_assessment['status']}")
        lines.append(f"Recommendation: {report.overall_recommendation}")
        
        if report.attributions:
            lines.append("-" * 20)
            lines.append("Top Matches:")
            for attr in report.attributions:
                lines.append(f"- {attr['title']} by {attr['author']} => {attr['citation']}")
                
        return "\\n".join(lines)
        
    def format_report_json(self, report: CopyrightReport) -> str:
        return json.dumps({
            "detection_summary": report.detection_summary,
            "compliance_assessment": report.compliance_assessment,
            "overall_recommendation": report.overall_recommendation,
            "attributions": report.attributions
        }, indent=2)
