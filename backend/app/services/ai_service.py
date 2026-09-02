import time

def analyze_text(text: str) -> dict:
    """
    Mock AI adapter for text analysis.
    Returns deterministic structured result based on input text length.
    """
    # Simulate processing delay
    time.sleep(1)

    # Deterministic mock based on text content
    if "fake" in text.lower() or "hoax" in text.lower():
        return {
            "overall_credibility_score": 30,
            "credibility_label": "Potentially Misleading",
            "confidence": 85,
            "quality_score": 60,
            "claims": [
                {
                    "claim_text": "The provided text contains claims that are unverified or false.",
                    "assessment": "Potentially Misleading",
                    "confidence": 0.8,
                    "explanation": "This claim could not be verified by reliable sources and matches known patterns of misinformation."
                }
            ],
            "evidence": [
                {
                    "source_name": "FactCheck.org Fake News Archive",
                    "snippet": "This specific hoax has been circulating since 2015."
                }
            ],
            "explanation": "The text contains keywords often associated with fake news or hoaxes. Analysis strongly suggests it is misleading."
        }

    return {
        "overall_credibility_score": 85,
        "credibility_label": "Supported",
        "confidence": 90,
        "quality_score": 80,
        "claims": [
            {
                "claim_text": "This is a factual claim extracted from the text.",
                "assessment": "Supported",
                "confidence": 0.9,
                "explanation": "This claim aligns with established knowledge and reliable sources."
            }
        ],
        "evidence": [
            {
                "source_name": "Verified Reliable Source API",
                "snippet": "The information presented aligns perfectly with our factual database."
            }
        ],
        "explanation": "The text appears to be credible and is well-supported by available evidence."
    }

def analyze_image(file_path: str) -> dict:
    raise NotImplementedError("Image analysis is not implemented yet.")

def analyze_video(file_path: str) -> dict:
    raise NotImplementedError("Video analysis is not implemented yet.")
