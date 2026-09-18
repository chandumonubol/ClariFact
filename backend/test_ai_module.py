"""Test script for the ClariFact AI module."""

from ai_model.inference.text_analyzer import analyze_text
from ai_model.nlp.claim_extractor import extract_claims
from ai_model.preprocessing.text_preprocessor import preprocess
from ai_model.credibility.credibility_scorer import ClaimClassifier, assess_claim
from ai_model.credibility.content_quality import assess_quality


def test_preprocessing():
    """Test text preprocessing pipeline."""
    print("=== Text Preprocessing Tests ===")
    
    # Normal text
    result = preprocess("The company launched the product in 2025.")
    print(f"Normal text - cleaned: '{result['cleaned']}'")
    print(f"  sentences: {result['sentences']}")
    
    # Empty text
    result = preprocess("")
    print(f"Empty text - cleaned: '{result['cleaned']}'")
    
    # Whitespace only
    result = preprocess("   ")
    print(f"Whitespace text - cleaned: '{result['cleaned']}'")
    
    # Multiple spaces
    result = preprocess("Hello    world    test")
    print(f"Multiple spaces - cleaned: '{result['cleaned']}'")
    
    # Numbers preserved
    result = preprocess("The price is 100 dollars.")
    print(f"Numbers preserved - cleaned: '{result['cleaned']}'")
    
    print()


def test_claim_extraction():
    """Test claim extraction pipeline."""
    print("=== Claim Extraction Tests ===")
    
    # Normal text with checkable claim
    claims = extract_claims("The company launched the product in 2025.")
    print(f"Checkable claim: {len(claims)} claims found")
    for c in claims:
        print(f'  - "{c["claim_text"]}" -> type={c["claim_type"]}, checkable={c["checkable"]}, conf={c["confidence"]}')
    
    # Opinion
    claims = extract_claims("I think this product is excellent.")
    print(f"Opinion: {len(claims)} claims found")
    for c in claims:
        print(f'  - "{c["claim_text"]}" -> type={c["claim_type"]}, checkable={c["checkable"]}, conf={c["confidence"]}')
    
    # Question
    claims = extract_claims("Did the company launch the product in 2025?")
    print(f"Question: {len(claims)} claims found")
    for c in claims:
        print(f'  - "{c["claim_text"]}" -> type={c["claim_type"]}, checkable={c["checkable"]}, conf={c["confidence"]}')
    
    # Instruction
    claims = extract_claims("Check this information.")
    print(f"Instruction: {len(claims)} claims found")
    for c in claims:
        print(f'  - "{c["claim_text"]}" -> type={c["claim_type"]}, checkable={c["checkable"]}, conf={c["confidence"]}')
    
    # Empty
    claims = extract_claims("")
    print(f"Empty: {len(claims)} claims found")
    
    # Multiple claims
    claims = extract_claims("The company launched the product in 2025. It sold 2 million units. I think it is excellent.")
    print(f"Multiple claims: {len(claims)} claims found")
    for c in claims:
        print(f'  - "{c["claim_text"][:40]}..." -> type={c["claim_type"]}, checkable={c["checkable"]}, conf={c["confidence"]}')
    
    print()


def test_credibility():
    """Test credibility assessment."""
    print("=== Credibility Assessment Tests ===")
    
    classifier = ClaimClassifier()
    
    # Supported claim
    result = assess_claim("The company launched the product in 2025.", classifier=classifier)
    print(f"Supported claim: score={result['credibility_score']}, label={result['credibility_label']}, conf={result['confidence']}")
    
    # Opinion claim
    result = assess_claim("I think this product is excellent.", classifier=classifier)
    print(f"Opinion claim: score={result['credibility_score']}, label={result['credibility_label']}, conf={result['confidence']}")
    
    # Question claim
    result = assess_claim("Did the company launch the product in 2025?", classifier=classifier)
    print(f"Question claim: score={result['credibility_score']}, label={result['credibility_label']}, conf={result['confidence']}")
    
    # Uncertain claim (hedged)
    result = assess_claim("The product might be good.", classifier=classifier)
    print(f"Hedged claim: score={result['credibility_score']}, label={result['credibility_label']}, conf={result['confidence']}")
    
    # Potentially misleading
    result = assess_claim("This is a fake hoax.", classifier=classifier)
    print(f"Potentially misleading: score={result['credibility_score']}, label={result['credibility_label']}, conf={result['confidence']}")
    
    print()


def test_quality():
    """Test content quality analysis."""
    print("=== Content Quality Tests ===")
    
    # Normal text
    result = assess_quality("The company launched the product in 2025. It sold 2 million units.")
    print(f"Normal text: clarity={result['clarity']}, relevance={result['relevance']}, completeness={result['completeness']}, language_quality={result['language_quality']}")
    
    # Empty text
    result = assess_quality("")
    print(f"Empty text: clarity={result['clarity']}, relevance={result['relevance']}, completeness={result['completeness']}, language_quality={result['language_quality']}")
    
    # Short text
    result = assess_quality("Hi.")
    print(f"Short text: clarity={result['clarity']}, relevance={result['relevance']}, completeness={result['completeness']}, language_quality={result['language_quality']}")
    
    # Text with numbers
    result = assess_quality("The price is 100 dollars.")
    print(f"With numbers: clarity={result['clarity']}, relevance={result['relevance']}, completeness={result['completeness']}, language_quality={result['language_quality']}")
    
    print()


def test_full_pipeline():
    """Test the complete analysis pipeline."""
    print("=== Full Pipeline Tests ===")
    
    # Test 1: Normal credible text
    print("Test 1: Normal credible text")
    result = analyze_text("The company launched the product in 2025. It sold 2 million units.")
    print(f"  credibility_score: {result['overall_credibility_score']}")
    print(f"  credibility_label: {result['credibility_label']}")
    print(f"  confidence: {result['confidence']}")
    print(f"  quality_score: {result['quality_score']}")
    print(f"  num_claims: {len(result['claims'])}")
    for c in result['claims']:
        print(f'    claim: "{c["claim_text"][:30]}..." -> assessment="{c["assessment"]}" conf={c["confidence"]}')
    print(f"  explanation: {result['explanation'][:80]}...")
    print()
    
    # Test 2: Opinion text
    print("Test 2: Opinion text")
    result = analyze_text("I think this product is excellent.")
    print(f"  credibility_label: {result['credibility_label']}")
    print(f"  num_claims: {len(result['claims'])}")
    for c in result['claims']:
        print(f'    claim: "{c["claim_text"]}" -> assessment="{c["assessment"]}"')
    print()
    
    # Test 3: Question text
    print("Test 3: Question text")
    result = analyze_text("Did the company launch the product in 2025?")
    print(f"  credibility_label: {result['credibility_label']}")
    print(f"  num_claims: {len(result['claims'])}")
    for c in result['claims']:
        print(f'    claim: "{c["claim_text"]}" -> assessment="{c["assessment"]}"')
    print()
    
    # Test 4: Empty text
    print("Test 4: Empty text")
    result = analyze_text("")
    print(f"  credibility_label: {result['credibility_label']}")
    print(f"  num_claims: {len(result['claims'])}")
    print()
    
    # Test 5: Whitespace only
    print("Test 5: Whitespace only")
    result = analyze_text("   ")
    print(f"  credibility_label: {result['credibility_label']}")
    print(f"  num_claims: {len(result['claims'])}")
    print()
    
    # Test 6: Long text
    print("Test 6: Long text with multiple claims")
    long_text = (
        "The company launched the product in 2025. "
        "It sold 2 million units in the first quarter. "
        "The product received mixed reviews from customers. "
        "Many users reported issues with the battery life. "
        "Despite the issues, the company issued a recall."
    )
    result = analyze_text(long_text)
    print(f"  credibility_score: {result['overall_credibility_score']}")
    print(f"  credibility_label: {result['credibility_label']}")
    print(f"  confidence: {result['confidence']}")
    print(f"  quality_score: {result['quality_score']}")
    print(f"  num_claims: {len(result['claims'])}")
    for c in result['claims']:
        print(f'    claim: "{c["claim_text"][:40]}..." -> assessment="{c["assessment"]}" conf={c["confidence"]}')
    print()
    
    # Test 7: Special characters
    print("Test 7: Text with special characters")
    result = analyze_text("The company's stock price increased by 15%! (Q4 2025).")
    print(f"  credibility_label: {result['credibility_label']}")
    print(f"  num_claims: {len(result['claims'])}")
    for c in result['claims']:
        print(f'    claim: "{c["claim_text"]}" -> assessment="{c["assessment"]}"')
    print()
    
    # Test 8: Repeated whitespace
    print("Test 8: Repeated whitespace")
    result = analyze_text("The   company  launched  the  product")
    print(f"  credibility_label: {result['credibility_label']}")
    print(f"  num_claims: {len(result['claims'])}")
    for c in result['claims']:
        print(f'    claim: "{c["claim_text"]}" -> assessment="{c["assessment"]}"')
    print()


if __name__ == "__main__":
    test_preprocessing()
    test_claim_extraction()
    test_credibility()
    test_quality()
    test_full_pipeline()
    print("=== All tests completed ===")