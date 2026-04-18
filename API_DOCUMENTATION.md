# 📡 API Documentation

Complete API reference for the Offline AI Health Assistant.

## Base URL

```
Local Development: http://localhost:8000/api/v1
Production: https://your-domain.com/api/v1
```

## Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

**Note:** The diagnosis endpoint can be configured to work without authentication for offline clinic use.

---

## Endpoints

### 1. Health Check

Check system health and database connectivity.

**Endpoint:** `GET /health`

**Authentication:** Not required

**Response:**
```json
{
  "status": "ok",
  "mongo": "connected"
}
```

**Status Codes:**
- `200 OK`: System is healthy
- `500 Internal Server Error`: System error

---

### 2. Analyze Diagnosis

Analyze patient symptoms and image to provide AI-powered diagnosis.

**Endpoint:** `POST /health/analyze`

**Authentication:** Optional (configurable)

**Request Body:**
```json
{
  "symptoms": ["itching", "redness", "fever"],
  "image_base64": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
```

**Request Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `symptoms` | array[string] | No | List of symptom names. Valid values: "itching", "redness", "fever", "cough", "fatigue" |
| `image_base64` | string | No | Base64-encoded image data. Can include data URL prefix or just the base64 string |

**Response:**
```json
{
  "disease": "fungal infection",
  "confidence": 0.72,
  "risk_level": "Medium",
  "explanation": "Based on image analysis and reported symptoms, the system detected patterns consistent with fungal infection. Key symptoms considered: itching, redness. The confidence level is moderate (72.0%), suggesting further clinical evaluation may be beneficial. This is an AI-assisted preliminary assessment and should not replace professional medical diagnosis.",
  "all_scores": {
    "fungal infection": 0.72,
    "eczema": 0.15,
    "psoriasis": 0.08,
    "bacterial infection": 0.05
  }
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `disease` | string | Predicted disease name |
| `confidence` | float | Confidence score (0.0 to 1.0) |
| `risk_level` | string | Risk assessment: "High" (≥0.75), "Medium" (0.4-0.75), or "Low" (<0.4) |
| `explanation` | string | Human-readable explanation of the diagnosis |
| `all_scores` | object | Probability scores for all diseases |

**Status Codes:**
- `200 OK`: Analysis completed successfully
- `400 Bad Request`: Invalid request data
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Analysis failed

**Example cURL:**
```bash
curl -X POST http://localhost:8000/api/v1/health/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": ["itching", "redness"],
    "image_base64": "data:image/jpeg;base64,/9j/4AAQ..."
  }'
```

**Example JavaScript:**
```javascript
const response = await fetch('http://localhost:8000/api/v1/health/analyze', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    symptoms: ['itching', 'redness'],
    image_base64: 'data:image/jpeg;base64,...'
  })
});

const result = await response.json();
console.log(result.disease, result.confidence);
```

**Example Python:**
```python
import requests
import base64

# Read image
with open('patient_image.jpg', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode('utf-8')

# Make request
response = requests.post(
    'http://localhost:8000/api/v1/health/analyze',
    json={
        'symptoms': ['itching', 'redness'],
        'image_base64': f'data:image/jpeg;base64,{image_data}'
    }
)

result = response.json()
print(f"Disease: {result['disease']}")
print(f"Confidence: {result['confidence']:.2%}")
```

---

### 3. Get Diagnosis History

Retrieve recent diagnosis records from local database.

**Endpoint:** `GET /health/history`

**Authentication:** Optional (configurable)

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `limit` | integer | No | 10 | Maximum number of records to return (1-100) |

**Response:**
```json
{
  "history": [
    {
      "id": 1,
      "symptoms": "itching, redness",
      "prediction": "fungal infection",
      "confidence": 0.72,
      "risk_level": "Medium",
      "explanation": "Based on image analysis and reported symptoms...",
      "image_path": "base64_image",
      "timestamp": "2026-04-18 10:30:00"
    },
    {
      "id": 2,
      "symptoms": "fever, cough",
      "prediction": "bacterial infection",
      "confidence": 0.65,
      "risk_level": "Medium",
      "explanation": "Based on reported symptoms...",
      "image_path": null,
      "timestamp": "2026-04-18 09:15:00"
    }
  ],
  "count": 2
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `history` | array | List of diagnosis records |
| `history[].id` | integer | Unique record ID |
| `history[].symptoms` | string | Comma-separated symptoms |
| `history[].prediction` | string | Predicted disease |
| `history[].confidence` | float | Confidence score |
| `history[].risk_level` | string | Risk level |
| `history[].explanation` | string | Diagnosis explanation |
| `history[].image_path` | string\|null | Image path or null |
| `history[].timestamp` | string | Diagnosis timestamp |
| `count` | integer | Total number of records returned |

**Status Codes:**
- `200 OK`: History retrieved successfully
- `400 Bad Request`: Invalid query parameters
- `500 Internal Server Error`: Database error

**Example cURL:**
```bash
curl http://localhost:8000/api/v1/health/history?limit=5
```

**Example JavaScript:**
```javascript
const response = await fetch('http://localhost:8000/api/v1/health/history?limit=20');
const data = await response.json();

console.log(`Found ${data.count} records`);
data.history.forEach(record => {
  console.log(`${record.timestamp}: ${record.prediction} (${record.confidence})`);
});
```

---

## Data Models

### DiagnosisRequest

```typescript
interface DiagnosisRequest {
  symptoms: string[];        // Array of symptom names
  image_base64?: string;     // Optional base64-encoded image
}
```

### DiagnosisResponse

```typescript
interface DiagnosisResponse {
  disease: string;           // Predicted disease name
  confidence: number;        // Confidence score (0-1)
  risk_level: string;        // "High" | "Medium" | "Low"
  explanation: string;       // Human-readable explanation
  all_scores: {              // All disease probabilities
    [disease: string]: number;
  };
}
```

### DiagnosisHistoryItem

```typescript
interface DiagnosisHistoryItem {
  id: number;                // Unique record ID
  symptoms: string;          // Comma-separated symptoms
  prediction: string;        // Predicted disease
  confidence: number;        // Confidence score
  risk_level: string;        // Risk level
  explanation: string;       // Explanation text
  image_path: string | null; // Image path or null
  timestamp: string;         // ISO timestamp
}
```

---

## Valid Values

### Symptoms
- `itching`
- `redness`
- `fever`
- `cough`
- `fatigue`

### Diseases
- `fungal infection`
- `eczema`
- `psoriasis`
- `bacterial infection`

### Risk Levels
- `High`: Confidence ≥ 75%
- `Medium`: 40% ≤ Confidence < 75%
- `Low`: Confidence < 40%

---

## Error Responses

All endpoints return errors in this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid input data |
| 401 | Unauthorized - Missing or invalid authentication |
| 404 | Not Found - Endpoint doesn't exist |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error - Server-side error |

---

## Rate Limiting

Currently no rate limiting is implemented. For production use, consider adding rate limiting based on your requirements.

---

## CORS

CORS is enabled for all origins in development. For production, configure allowed origins in `app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Performance

- **Average Response Time**: < 3 seconds
- **Image Processing**: ~1-2 seconds
- **Symptom Analysis**: < 100ms
- **Database Operations**: < 50ms

---

## Offline Capability

All endpoints work completely offline:
- No external API calls
- No internet required
- Local model inference
- Local database storage

---

## Testing

### Interactive API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Test with Postman

Import this collection:

```json
{
  "info": {
    "name": "Health Assistant API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/health"
      }
    },
    {
      "name": "Analyze Diagnosis",
      "request": {
        "method": "POST",
        "url": "{{base_url}}/health/analyze",
        "body": {
          "mode": "raw",
          "raw": "{\n  \"symptoms\": [\"itching\", \"redness\"],\n  \"image_base64\": null\n}"
        }
      }
    },
    {
      "name": "Get History",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/health/history?limit=10"
      }
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8000/api/v1"
    }
  ]
}
```

---

## Support

For issues or questions:
1. Check the [README.md](README.md)
2. Review the [QUICKSTART.md](QUICKSTART.md)
3. Test with interactive docs at `/docs`
4. Check server logs for errors

---

**Last Updated**: April 18, 2026
