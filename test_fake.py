import sys
sys.path.insert(0, r'C:\Users\Lithesh\ClariFact')
from ai_model.inference.text_analyzer import analyze_text

# Test 'fake hoax' case
result = analyze_text('This is a fake hoax.')
print('Fake hoax result:')
print(f'  label={result["credibility_label"]}, score={result["overall_credibility_score"]}')
print(f'  claims={len(result["claims"])}')
for c in result['claims']:
    print(f'  claim: "{c["claim_text"]}" -> assessment={c["assessment"]}')