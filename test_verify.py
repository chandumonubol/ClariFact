import sys
sys.path.insert(0, r'C:\Users\Lithesh\ClariFact')
from ai_model.inference.text_analyzer import analyze_text

# Test all required input types from specification

print('=== Testing Required Input Types ===')
print()

# 1. Normal text
result = analyze_text('The company launched a product in 2025.')
print('1. Normal text:')
print(f'   score={result["overall_credibility_score"]}, label={result["credibility_label"]}, claims={len(result["claims"])}')
print()

# 2. Empty text
result = analyze_text('')
print('2. Empty text:')
print(f'   score={result["overall_credibility_score"]}, label={result["credibility_label"]}, claims={len(result["claims"])}')
print()

# 3. Whitespace
result = analyze_text('     ')
print('3. Whitespace:')
print(f'   score={result["overall_credibility_score"]}, label={result["credibility_label"]}, claims={len(result["claims"])}')
print()

# 4. Multiple claims
result = analyze_text('The company launched the product in 2025. It sold 2 million units. The product is high quality.')
print('4. Multiple claims:')
print(f'   score={result["overall_credibility_score"]}, label={result["credibility_label"]}, claims={len(result["claims"])}')
print()

# 5. Opinion
result = analyze_text('I think this product is excellent.')
print('5. Opinion:')
print(f'   score={result["overall_credibility_score"]}, label={result["credibility_label"]}, claims={len(result["claims"])}')
for c in result['claims']:
    print(f'   claim: "{c["claim_text"]}" -> assessment={c["assessment"]}')
print()

# 6. Question
result = analyze_text('Did the company launch the product in 2025?')
print('6. Question:')
print(f'   score={result["overall_credibility_score"]}, label={result["credibility_label"]}, claims={len(result["claims"])}')
for c in result['claims']:
    print(f'   claim: "{c["claim_text"]}" -> assessment={c["assessment"]}')
print()

# 7. Instruction
result = analyze_text('Check this information.')
print('7. Instruction:')
print(f'   score={result["overall_credibility_score"]}, label={result["credibility_label"]}, claims={len(result["claims"])}')
for c in result['claims']:
    print(f'   claim: "{c["claim_text"]}" -> assessment={c["assessment"]}')
print()

# 8. Long text
long_text = ' '.join(['The claim is verified and true ' * 10])
result = analyze_text(long_text)
print('8. Long text:')
print(f'   score={result["overall_credibility_score"]}, label={result["credibility_label"]}')
print()

# 9. Special characters
result = analyze_text('Price: $19.99, 50% off! (Q4 2025).')
print('9. Special characters:')
print(f'   score={result["overall_credibility_score"]}, label={result["credibility_label"]}, claims={len(result["claims"])}')
for c in result['claims']:
    print(f'   claim: "{c["claim_text"]}" -> assessment={c["assessment"]}')
print()

# 10. Numbers/dates
result = analyze_text('The product launched in 2025 and has a 2-year warranty.')
print('10. Numbers/dates:')
print(f'   score={result["overall_credibility_score"]}, label={result["credibility_label"]}, claims={len(result["claims"])}')
for c in result['claims']:
    print(f'   claim: "{c["claim_text"]}" -> assessment={c["assessment"]}')
print()

# 11. Uncertain claim (no evidence)
result = analyze_text('The company launched a product in an unknown city in 2025.')
print('11. Uncertain claim:')
print(f'   score={result["overall_credibility_score"]}, label={result["credibility_label"]}, claims={len(result["claims"])}')
for c in result['claims']:
    print(f'   claim: "{c["claim_text"]}" -> assessment={c["assessment"]}')
print()

# 12. Malformed input (None)
try:
    result = analyze_text(None)
    print('12. None: No error raised (unexpected)')
except ValueError as e:
    print('12. None: ValueError raised correctly')
print()

# 13. Verify output structure matches API contract
result = analyze_text('The company launched the product in 2025.')
required_fields = ['overall_credibility_score', 'credibility_label', 'confidence', 'quality_score', 'claims', 'evidence', 'explanation']
print('13. Output structure validation:')
for field in required_fields:
    has_field = field in result
    print(f'   {field}: {"OK" if has_field else "MISSING"}')
print()

print('=== All input type tests completed ===')