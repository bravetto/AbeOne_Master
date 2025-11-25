from typing import List
from .core import AnalysisResult, MitigationAction, Report


class Reporter:
    """
    Generates reports based on analysis and mitigation actions.
    """
    def generate_report(self, analysis_results: List[AnalysisResult], mitigation_actions: List[MitigationAction]) -> Report:
        """
        Generates a summary report.
        """
        total_samples = len(analysis_results)
        poisoned_samples = sum(1 for r in analysis_results if r.is_poisoned)
        mitigated_samples = sum(1 for a in mitigation_actions if a.action_taken != "none")

        return Report(
            total_samples=total_samples,
            poisoned_samples=poisoned_samples,
            mitigated_samples=mitigated_samples,
            analysis_results=analysis_results,
            mitigation_actions=mitigation_actions,
        )

    def format_report(self, report: Report) -> str:
        """
        Formats the report into a human-readable string.
        """
        output = []
        output.append("--- PoisonGuard Analysis Report ---")
        output.append(f"Total Samples Analyzed: {report.total_samples}")
        output.append(f"Potentially Poisoned Samples Detected: {report.poisoned_samples}")
        output.append(f"Samples Mitigated: {report.mitigated_samples}")
        output.append("\n--- Detailed Analysis Results ---")

        for result in report.analysis_results:
            status = "Poisoned" if result.is_poisoned else "Clean"
            output.append(f"  - Sample ID: {result.sample_id} | Status: {status} | Confidence: {result.confidence:.2f}")
            reasons = "; ".join(result.details.get('reasons', ['N/A']))
            output.append(f"    Details: {reasons}")

        if any(action.action_taken != "none" for action in report.mitigation_actions):
            output.append("\n--- Mitigation Actions ---")
            for action in report.mitigation_actions:
                if action.action_taken != "none":
                    output.append(f"  - Sample ID: {action.sample_id} | Action: {action.action_taken}")
                    reasons = "; ".join(action.details.get('reasons', ['N/A']))
                    output.append(f"    Reason: {reasons}")

        output.append("\n--- End of Report ---")
        return "\n".join(output)
