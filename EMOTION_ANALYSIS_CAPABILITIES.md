# Emotion Analysis Capabilities

## 📊 Text-Based Emotions (7 emotions)

Your emotion classifier (j-hartmann/emotion-english-distilroberta-base) can detect:

1. **anger** - Frustration, rage, irritation
2. **disgust** - Revulsion, aversion
3. **fear** - Anxiety, worry, panic, dread
4. **joy** - Happiness, excitement, contentment
5. **neutral** - No strong emotion
6. **sadness** - Depression, grief, sorrow
7. **surprise** - Shock, amazement

### Model Details
- **Model**: j-hartmann/emotion-english-distilroberta-base (ONNX optimized)
- **Training**: Fine-tuned on emotion datasets
- **Output**: Confidence scores for all 7 emotions
- **Language**: English (other languages are translated first)

---

## 🎤 Audio-Based Emotion Hints (5 hints)

The voice pipeline analyzes audio features (pitch, amplitude, stress) to provide emotion hints:

1. **anger** - High pitch (>0.7) + High amplitude (>0.65)
   - Loud, high-pitched speech
   - Shouting, yelling patterns

2. **anxiety** - High pitch (>0.65) + High pitch deviation (>0.6)
   - Voice trembling, shaking
   - Rapid pitch changes
   - Nervous speech patterns

3. **sadness** - Low pitch (<0.35) + Low amplitude (<0.4)
   - Quiet, low voice
   - Monotone, flat delivery
   - Lack of energy

4. **dissociation** - Very low amplitude (<0.3) + Low pitch deviation (<0.2)
   - Flat affect (emotionless voice)
   - Robotic, monotone speech
   - Clinically significant indicator

5. **neutral** - Everything else
   - Normal speech patterns
   - Balanced pitch and volume

### Audio Features Analyzed
- **Pitch**: 50-400 Hz range using YIN algorithm
- **Amplitude**: RMS energy levels
- **Stress**: Volume spikes above baseline
- **Baseline**: Speaker's normal pitch/volume computed from full clip

---

## ⚡ Fused Emotions (Best of Both Worlds)

The voice pipeline combines text + audio for enhanced accuracy:

### Two-Stage Process

**Stage 1: Text-Only Emotion**
- Analyzes full transcript text
- Uses emotion classifier
- Example: "I'm anxious" → fear (82%)

**Stage 2: Audio-Focused Emotion**
- Extracts high-weight words (final_weight > 0.55)
- Re-analyzes just those words
- Example: "really anxious" → fear (91%)

**Stage 3: Fusion**
- If both agree: Weighted average (40% text, 60% audio-focused)
- If disagree: Pick higher confidence, apply 15% penalty
- Example: Both say fear → fused fear (88%)

### Fusion Formula
```python
if audio_emotion == text_emotion:
    fused_confidence = (text_conf * 0.40) + (audio_conf * 0.60)
else:
    fused_emotion = higher_confidence_emotion
    fused_confidence = higher_confidence * 0.85  # penalty
```

---

## 🎯 Intent Classification (6 intents)

Your system also classifies user intent:

1. **anxiety and panic** - Worry, fear, panic attacks
2. **sadness and depression** - Low mood, hopelessness
3. **stress and overwhelm** - Too much to handle, burnout
4. **loneliness and isolation** - Feeling alone, disconnected
5. **anger and frustration** - Irritation, rage
6. **general emotional support** - Default/unclear intent

### Model Details
- **Model**: MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7 (ONNX)
- **Method**: Zero-shot classification using NLI
- **Output**: Confidence scores for all 6 intents

---

## 🔍 Special Detection Features

### 1. Emotional Incongruence
Detects when words contradict voice:

**Example:**
- **Words**: "I'm fine" → neutral/joy
- **Voice**: Low pitch, quiet → sadness
- **Result**: ⚠️ Incongruence detected!

**Clinical Significance:**
- Emotional suppression
- Alexithymia (difficulty identifying emotions)
- Social masking
- Dissociation

**Detection Method:**
```python
text_valence = EMOTION_VALENCE[text_emotion]  # -1, 0, or 1
audio_valence = EMOTION_VALENCE[audio_emotion]
incongruence_score = abs(text_valence - audio_valence) / 2.0
is_incongruent = incongruence_score > 0.4
```

### 2. Stressed Words Detection
Identifies emotionally important words:

**Criteria:**
- High text weight (important vocabulary)
- High audio weight (pitch/amplitude spikes)
- Combined final_weight > 0.6

**Example:**
- Input: "I'm feeling REALLY anxious"
- Stressed words: ["really", "anxious"]

### 3. Crisis Detection
Immediate pattern matching for safety:

**Triggers:**
- Suicide mentions
- Self-harm indicators
- "want to die", "kill myself"
- "no reason to live"
- Overdose mentions

**Response:** Immediate crisis resources, skip all analysis

---

## 📈 Confidence Scores

All emotions and intents include confidence scores (0.0 - 1.0):

- **0.0 - 0.3**: Very uncertain
- **0.3 - 0.5**: Low confidence
- **0.5 - 0.7**: Moderate confidence
- **0.7 - 0.9**: High confidence
- **0.9 - 1.0**: Very high confidence

---

## 🌍 Multilingual Support

**Supported Languages:**
1. **English** (en) - Native
2. **Hindi** (hi) - Translated
3. **French** (fr) - Translated
4. **Spanish** (es) - Translated

**Process:**
1. Detect language
2. Translate to English (if needed)
3. Analyze emotion/intent in English
4. Translate response back

---

## 🎭 Emotion Mapping

### Audio Hint → Standard Emotion
```python
"anxiety" → "fear"
"sadness" → "sadness"
"anger" → "anger"
"dissociation" → "neutral"
"neutral" → "neutral"
```

### Valence Mapping (for incongruence)
```python
"sadness": -1 (negative)
"fear": -1 (negative)
"anger": -1 (negative)
"disgust": -1 (negative)
"joy": +1 (positive)
"surprise": 0 (neutral)
"neutral": 0 (neutral)
```

---

## 💡 Summary

**Your system can analyze:**

✅ **7 text-based emotions** (anger, disgust, fear, joy, neutral, sadness, surprise)  
✅ **5 audio-based emotion hints** (anger, anxiety, sadness, dissociation, neutral)  
✅ **6 user intents** (anxiety, sadness, stress, loneliness, anger, general support)  
✅ **Emotional incongruence** (words vs voice mismatch)  
✅ **Stressed words** (emotionally important words)  
✅ **Crisis patterns** (immediate safety detection)  
✅ **4 languages** (English, Hindi, French, Spanish)  

**Unique Features:**
- Audio-fused emotion detection (text + audio combined)
- Per-word audio analysis (pitch, amplitude, stress)
- Clinically meaningful signals (dissociation, incongruence)
- Two-stage emotion fusion for higher accuracy

---

## 🔬 Technical Accuracy

**Text Emotion Classifier:**
- Trained on emotion datasets
- State-of-the-art transformer model
- High accuracy on English text

**Audio Analysis:**
- Pitch: YIN algorithm (50-400 Hz)
- Amplitude: RMS energy
- Baseline normalization per speaker
- Heuristic-based emotion hints

**Fusion:**
- Combines strengths of both modalities
- Higher accuracy than text-only
- Detects masked emotions

**Best Use Cases:**
- Mental health support conversations
- Emotion-aware chatbots
- Crisis detection
- Therapeutic applications
- Research on emotional expression
