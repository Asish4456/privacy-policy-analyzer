from rules import (
    DATA_COLLECTION,
    THIRD_PARTY,
    TRACKING,
    VAGUE_CONSENT,
    RETENTION
)

def calculate_risk(sentences):
    score = 0
    detected = {
        "data_collection": [],
        "third_party": [],
        "tracking": [],
        "vague_consent": [],
        "retention": []
    }

    for s in sentences:
        if any(k in s for k in DATA_COLLECTION):
            detected["data_collection"].append(s)
            score += 1

        if any(k in s for k in THIRD_PARTY):
            detected["third_party"].append(s)
            score += 2

        if any(k in s for k in TRACKING):
            detected["tracking"].append(s)
            score += 1

        if any(k in s for k in VAGUE_CONSENT):
            detected["vague_consent"].append(s)
            score += 2

        if any(k in s for k in RETENTION):
            detected["retention"].append(s)
            score += 2

    return score, detected
