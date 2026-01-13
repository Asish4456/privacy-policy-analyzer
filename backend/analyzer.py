import re
from typing import Dict, List, Any
from rules import PRIVACY_RULES
from risk_scoring import calculate_risk_score

async def analyze_policy(text: str) -> Dict[str, Any]:
    """
    Analyze privacy policy text against defined rules.
    
    Args:
        text: The privacy policy text to analyze
        
    Returns:
        Dictionary containing analysis results and risk score
    """
    if not text or not text.strip():
        return {
            "results": [],
            "risk_score": 0,
            "message": "No text provided for analysis"
        }
    
    results = []
    
    # Analyze text against each privacy rule
    for rule in PRIVACY_RULES:
        matches = []
        
        # Check if rule has patterns to match
        if "patterns" in rule:
            for pattern in rule["patterns"]:
                # Find all matches in the text
                found = re.finditer(pattern, text, re.IGNORECASE)
                for match in found:
                    matches.append({
                        "text": match.group(),
                        "position": match.start()
                    })
        
        # If matches found, add to results
        if matches:
            results.append({
                "rule_id": rule.get("id"),
                "rule_name": rule.get("name"),
                "category": rule.get("category"),
                "severity": rule.get("severity"),
                "description": rule.get("description"),
                "matches": matches,
                "match_count": len(matches)
            })
    
    # Calculate overall risk score
    risk_score = calculate_risk_score(results)
    
    return {
        "results": results,
        "risk_score": risk_score,
        "total_issues": len(results),
        "analyzed": True
    }