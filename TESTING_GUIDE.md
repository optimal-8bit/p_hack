# 🧪 Testing Guide

Complete testing guide for the Offline AI Health Assistant.

---

## Quick Test (5 minutes)

### 1. Backend Test

```bash
cd py_server
python test_diagnosis.py
```

**Expected Output:**
```
Testing Offline AI Health Diagnostic System
============================================================

[Test 1] Symptoms only (itching, redness)
------------------------------------------------------------
Disease: fungal infection
Confidence: 72%
Risk Level: Medium
...

All tests completed successfully! ✅
```

### 2. API Test

**Start server:**
```bash
uvicorn app.main:app --reload
```

**Test health endpoint:**
```bash
curl http://localhost:8000/api/v1/health
```

**Expected:**
```json
{"status":"ok","mongo":"connected"}
```

**Test diagnosis endpoint:**
```bash
curl -X POST http://localhost:8000/api/v1/health/analyze \
  -H "Content-Type: application/json" \
  -d '{"symptoms":["itching","redness"]}'
```

**Expected:**
```json
{
  "disease": "fungal infection",
  "confidence": 0.72,
  "risk_level": "Medium",
  ...
}
```

### 3. Frontend Test

**Start dev server:**
```bash
cd react_web
npm run dev
```

**Manual testing:**
1. Open http://localhost:5173
2. Navigate to diagnosis page
3. Upload test image
4. Select symptoms
5. Click "Analyze"
6. Verify results display

---

## Comprehensive Testing

### Backend Unit Tests

#### Test 1: SQLite Database

```python
from app.core.sqlite_db import init_sqlite_db, save_diagnosis, get_diagnosis_history

# Initialize
init_sqlite_db()

# Save diagnosis
record_id = save_diagnosis(
    symptoms="itching, redness",
    prediction="fungal infection",
    confidence=0.72,
    risk_level="Medium",
    explanation="Test diagnosis"
)

# Retrieve history
history = get_diagnosis_history(limit=10)
assert len(history) > 0
assert history[0]['prediction'] == "fungal infection"

print("✅ Database test passed")
```

#### Test 2: AI Engine

```python
from app.modules.health.ai_engine import analyze_image

# Test with mock image
test_image = b'\x89PNG\r\n\x1a\n...'  # Small PNG
scores = analyze_image(test_image)

assert len(scores) == 4  # 4 diseases
assert sum(scores.values()) > 0.99  # Probabilities sum to ~1
assert all(0 <= v <= 1 for v in scores.values())  # Valid range

print("✅ AI engine test passed")
```

#### Test 3: Symptom Analyzer

```python
from app.modules.health.symptom_analyzer import analyze_symptoms

# Test with symptoms
scores = analyze_symptoms(["itching", "redness"])

assert len(scores) == 4
assert scores["fungal infection"] > 0
assert sum(scores.values()) > 0.99

print("✅ Symptom analyzer test passed")
```

#### Test 4: Decision Engine

```python
from app.modules.health.decision_engine import (
    combine_scores,
    get_top_prediction,
    calculate_risk_level,
    generate_explanation
)

# Test score combination
image_scores = {"fungal infection": 0.7, "eczema": 0.2, "psoriasis": 0.05, "bacterial infection": 0.05}
symptom_scores = {"fungal infection": 0.5, "eczema": 0.3, "psoriasis": 0.1, "bacterial infection": 0.1}

combined = combine_scores(image_scores, symptom_scores)
assert len(combined) == 4

# Test top prediction
disease, confidence = get_top_prediction(combined)
assert disease == "fungal infection"
assert 0 <= confidence <= 1

# Test risk level
assert calculate_risk_level(0.8) == "High"
assert calculate_risk_level(0.5) == "Medium"
assert calculate_risk_level(0.3) == "Low"

# Test explanation
explanation = generate_explanation(disease, confidence, ["itching"], True)
assert len(explanation) > 0
assert disease in explanation

print("✅ Decision engine test passed")
```

#### Test 5: Service Layer

```python
import asyncio
from app.modules.health.service import analyze_patient

async def test_service():
    # Test with symptoms only
    result = await analyze_patient(
        symptoms=["itching", "redness"],
        image_base64=None
    )
    
    assert "disease" in result
    assert "confidence" in result
    assert "risk_level" in result
    assert "explanation" in result
    assert "all_scores" in result
    
    print("✅ Service layer test passed")

asyncio.run(test_service())
```

---

### Frontend Tests

#### Test 1: Diagnosis Service

```javascript
// test_diagnosis_service.js
import { analyzeDiagnosis } from './services/diagnosisService'

async function testDiagnosisService() {
  try {
    const result = await analyzeDiagnosis({
      symptoms: ['itching', 'redness'],
      image_base64: null
    })
    
    console.assert(result.disease, 'Disease should be present')
    console.assert(result.confidence >= 0 && result.confidence <= 1, 'Valid confidence')
    console.assert(['High', 'Medium', 'Low'].includes(result.risk_level), 'Valid risk level')
    
    console.log('✅ Diagnosis service test passed')
  } catch (error) {
    console.error('❌ Test failed:', error)
  }
}

testDiagnosisService()
```

#### Test 2: Image Upload

**Manual test:**
1. Open diagnosis page
2. Click image upload area
3. Select image file
4. Verify preview displays
5. Click "Remove" button
6. Verify preview clears

**Expected:** Image upload and preview work correctly

#### Test 3: Symptom Selection

**Manual test:**
1. Click each symptom button
2. Verify button highlights
3. Click again to deselect
4. Verify button unhighlights

**Expected:** Symptom selection toggles correctly

#### Test 4: Analysis Flow

**Manual test:**
1. Select symptoms: itching, redness
2. Click "Analyze"
3. Verify loading state
4. Verify results display
5. Check all fields present:
   - Disease name
   - Confidence percentage
   - Risk level badge
   - Explanation text
   - All disease scores

**Expected:** Complete analysis flow works

---

### Integration Tests

#### Test 1: End-to-End Flow

```bash
# Start backend
cd py_server
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Start frontend
cd react_web
npm run dev &

# Wait for servers to start
sleep 5

# Test with curl
curl -X POST http://localhost:8000/api/v1/health/analyze \
  -H "Content-Type: application/json" \
  -d '{"symptoms":["itching","redness"]}' \
  | jq .

# Expected: Valid JSON response with diagnosis
```

#### Test 2: Offline Mode

**Steps:**
1. Start both servers
2. Disconnect internet
3. Test diagnosis functionality
4. Verify it still works

**Expected:** System works without internet

#### Test 3: Performance

```python
import time
import asyncio
from app.modules.health.service import analyze_patient

async def test_performance():
    start = time.time()
    
    result = await analyze_patient(
        symptoms=["itching", "redness"],
        image_base64=None
    )
    
    elapsed = time.time() - start
    
    assert elapsed < 3.0, f"Too slow: {elapsed}s"
    print(f"✅ Performance test passed: {elapsed:.2f}s")

asyncio.run(test_performance())
```

---

### Load Testing

#### Test 1: Concurrent Requests

```python
import asyncio
import aiohttp

async def make_request(session, i):
    async with session.post(
        'http://localhost:8000/api/v1/health/analyze',
        json={'symptoms': ['itching', 'redness']}
    ) as response:
        return await response.json()

async def load_test():
    async with aiohttp.ClientSession() as session:
        tasks = [make_request(session, i) for i in range(10)]
        results = await asyncio.gather(*tasks)
        
        assert len(results) == 10
        assert all('disease' in r for r in results)
        
        print("✅ Load test passed: 10 concurrent requests")

asyncio.run(load_test())
```

---

### Error Handling Tests

#### Test 1: Invalid Symptoms

```bash
curl -X POST http://localhost:8000/api/v1/health/analyze \
  -H "Content-Type: application/json" \
  -d '{"symptoms":["invalid_symptom"]}'
```

**Expected:** System handles gracefully (treats as unknown)

#### Test 2: Invalid Image

```bash
curl -X POST http://localhost:8000/api/v1/health/analyze \
  -H "Content-Type: application/json" \
  -d '{"symptoms":["itching"],"image_base64":"invalid_base64"}'
```

**Expected:** Falls back to symptom-only analysis

#### Test 3: Empty Request

```bash
curl -X POST http://localhost:8000/api/v1/health/analyze \
  -H "Content-Type: application/json" \
  -d '{"symptoms":[]}'
```

**Expected:** Returns uniform distribution

---

### Browser Compatibility

Test in multiple browsers:
- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari
- [ ] Mobile browsers

**Test checklist per browser:**
- [ ] Page loads
- [ ] Image upload works
- [ ] Symptom selection works
- [ ] Analysis completes
- [ ] Results display correctly
- [ ] Styling looks good

---

### Accessibility Testing

#### Test 1: Keyboard Navigation

**Steps:**
1. Use Tab key to navigate
2. Use Enter/Space to activate buttons
3. Verify focus indicators visible

**Expected:** Full keyboard accessibility

#### Test 2: Screen Reader

**Steps:**
1. Enable screen reader (NVDA/JAWS/VoiceOver)
2. Navigate through page
3. Verify all content is announced

**Expected:** All content accessible

#### Test 3: Color Contrast

**Steps:**
1. Use browser dev tools
2. Check contrast ratios
3. Verify WCAG AA compliance

**Expected:** Sufficient contrast

---

### Security Testing

#### Test 1: SQL Injection

```bash
curl -X POST http://localhost:8000/api/v1/health/analyze \
  -H "Content-Type: application/json" \
  -d '{"symptoms":["itching; DROP TABLE diagnosis_history;"]}'
```

**Expected:** No SQL injection (using parameterized queries)

#### Test 2: XSS

```bash
curl -X POST http://localhost:8000/api/v1/health/analyze \
  -H "Content-Type: application/json" \
  -d '{"symptoms":["<script>alert(1)</script>"]}'
```

**Expected:** Input sanitized, no script execution

#### Test 3: Large File Upload

**Steps:**
1. Try uploading very large image (>10MB)
2. Verify appropriate error handling

**Expected:** File size validation

---

### Database Testing

#### Test 1: Database Creation

```bash
# Remove database if exists
rm py_server/diagnosis.db

# Start server
cd py_server
uvicorn app.main:app

# Check database created
ls -la diagnosis.db
```

**Expected:** Database file created automatically

#### Test 2: Data Persistence

```python
from app.core.sqlite_db import save_diagnosis, get_diagnosis_history

# Save multiple records
for i in range(5):
    save_diagnosis(
        symptoms=f"test_{i}",
        prediction="fungal infection",
        confidence=0.7,
        risk_level="Medium",
        explanation="Test"
    )

# Retrieve
history = get_diagnosis_history(limit=10)
assert len(history) == 5

print("✅ Data persistence test passed")
```

---

## Automated Test Suite

Create `py_server/run_tests.py`:

```python
"""
Automated test suite for health diagnostic system.
"""
import asyncio
import sys

async def run_all_tests():
    """Run all tests and report results."""
    tests_passed = 0
    tests_failed = 0
    
    print("=" * 60)
    print("Running Automated Test Suite")
    print("=" * 60)
    
    # Test 1: Database
    try:
        from app.core.sqlite_db import init_sqlite_db, save_diagnosis
        init_sqlite_db()
        save_diagnosis("test", "test", 0.5, "Low", "test")
        print("✅ Test 1: Database - PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Test 1: Database - FAILED: {e}")
        tests_failed += 1
    
    # Test 2: AI Engine
    try:
        from app.modules.health.ai_engine import analyze_image
        scores = analyze_image(b'test')
        assert len(scores) == 4
        print("✅ Test 2: AI Engine - PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Test 2: AI Engine - FAILED: {e}")
        tests_failed += 1
    
    # Test 3: Symptom Analyzer
    try:
        from app.modules.health.symptom_analyzer import analyze_symptoms
        scores = analyze_symptoms(["itching"])
        assert len(scores) == 4
        print("✅ Test 3: Symptom Analyzer - PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Test 3: Symptom Analyzer - FAILED: {e}")
        tests_failed += 1
    
    # Test 4: Service Layer
    try:
        from app.modules.health.service import analyze_patient
        result = await analyze_patient(["itching"], None)
        assert "disease" in result
        print("✅ Test 4: Service Layer - PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Test 4: Service Layer - FAILED: {e}")
        tests_failed += 1
    
    # Summary
    print("=" * 60)
    print(f"Tests Passed: {tests_passed}")
    print(f"Tests Failed: {tests_failed}")
    print("=" * 60)
    
    return tests_failed == 0

if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
```

**Run:**
```bash
cd py_server
python run_tests.py
```

---

## Pre-Deployment Checklist

Before deploying to production:

### Backend
- [ ] All tests pass
- [ ] Environment variables set
- [ ] Database initialized
- [ ] CORS configured
- [ ] Error handling tested
- [ ] Performance acceptable (< 3s)

### Frontend
- [ ] Build succeeds (`npm run build`)
- [ ] API URL configured
- [ ] All pages load
- [ ] Image upload works
- [ ] Results display correctly
- [ ] Mobile responsive

### Integration
- [ ] End-to-end flow works
- [ ] Offline mode works
- [ ] Error handling graceful
- [ ] Performance acceptable

### Documentation
- [ ] README complete
- [ ] API docs accurate
- [ ] Deployment guide clear
- [ ] Quick start works

---

## Continuous Testing

### During Development

```bash
# Backend - watch mode
cd py_server
pytest --watch

# Frontend - watch mode
cd react_web
npm run test -- --watch
```

### Pre-Commit

```bash
# Run all tests before committing
./run_all_tests.sh
```

---

## Troubleshooting Tests

### Test Failures

**Database tests fail:**
- Check SQLite installed
- Verify write permissions
- Check database path

**API tests fail:**
- Ensure server running
- Check port availability
- Verify CORS settings

**Frontend tests fail:**
- Check API URL in .env
- Verify backend running
- Check browser console

---

## Test Coverage

Target coverage:
- Backend: 80%+
- Frontend: 70%+
- Integration: 100% of critical paths

---

**Testing complete! 🧪**

All tests passing = Ready for production deployment.
