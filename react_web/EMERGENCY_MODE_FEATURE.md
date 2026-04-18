# Emergency/Crisis Mode - Enhanced Rendering

## Overview
The chat interface now features a specialized rendering system for emergency/crisis situations. When the backend detects critical keywords indicating self-harm, suicide, or severe distress, the response is displayed with enhanced visual prominence and immediate access to crisis resources.

## Features

### 1. **Crisis Detection**
The backend automatically detects crisis situations using pattern matching for keywords like:
- Suicide ideation
- Self-harm intentions
- Severe distress signals
- Emergency situations

### 2. **Enhanced Visual Design**
When a crisis is detected, the message is rendered with:
- **Red gradient header** with pulsing animation
- **Alert icon** with continuous pulse effect
- **Prominent title**: "Crisis Support Available"
- **Reassuring subtitle**: "You're not alone. Help is here."
- **High-contrast design** for maximum visibility

### 3. **Structured Crisis Response**
The emergency bubble displays:
- **Compassionate message** with heart icon
- **Helpline cards** with immediate contact options
- **Call-to-action buttons** for quick access
- **Reassurance footer** with supportive message

### 4. **Interactive Helpline Cards**
Each helpline is displayed as an interactive card with:
- **Phone icon** for voice helplines
- **Chat icon** for online chat services
- **Call buttons** that:
  - On mobile: Direct dial the number
  - On desktop: Copy number to clipboard
- **Special styling** for emergency numbers (112)
- **External links** for chat services

### 5. **Accessibility Features**
- High contrast colors for visibility
- Clear visual hierarchy
- Keyboard accessible buttons
- Screen reader friendly
- Reduced motion support for accessibility preferences

## Visual Design

### Color Scheme
- **Primary**: Red gradient (#dc2626 to #991b1b)
- **Accent**: Light red (#fca5a5)
- **Background**: Dark with red tint
- **Text**: White and light gray for readability

### Animations
- **Pulse effect** on header (3 seconds)
- **Icon pulse** continuous
- **Hover effects** on interactive elements
- **Smooth transitions** throughout

### Layout Structure
```
┌─────────────────────────────────────┐
│ 🚨 Crisis Support Available        │ ← Pulsing header
│    You're not alone. Help is here. │
├─────────────────────────────────────┤
│ 💙 Compassionate message...         │ ← Main message
├─────────────────────────────────────┤
│ IMMEDIATE SUPPORT                   │
│ ┌─────────────────────────────────┐ │
│ │ 📞 iCall India: 9152987821      │ │ ← Helpline cards
│ │    [Call]                       │ │
│ └─────────────────────────────────┘ │
│ ┌─────────────────────────────────┐ │
│ │ 🚨 112 (Emergency)              │ │ ← Emergency card
│ │    [Call Now]                   │ │   (highlighted)
│ └─────────────────────────────────┘ │
├─────────────────────────────────────┤
│ 💙 I'm here with you...             │ ← Reassurance
└─────────────────────────────────────┘
```

## Technical Implementation

### Components
- **EmergencyBubble.jsx** - Specialized component for crisis messages
- **EmergencyBubble.css** - Styling with animations and responsive design
- **MessageBubble.jsx** - Updated to conditionally render EmergencyBubble

### Data Flow
1. User sends message with crisis keywords
2. Backend `SafetyChecker` detects crisis
3. Backend returns `is_crisis: true` in response
4. Frontend receives `isCrisis` flag in metadata
5. `MessageBubble` conditionally renders `EmergencyBubble`
6. Emergency UI is displayed with all features

### Props
```jsx
<EmergencyBubble 
  content={string}    // Crisis response text
  streaming={boolean} // Whether message is still streaming
/>
```

### Backend Integration
The backend returns crisis information in the API response:
```json
{
  "response_text": "Crisis response with helplines...",
  "is_crisis": true,
  "emotion": { "emotion": "fear", "confidence": 1.0 },
  "intent": { "intent": "anxiety and panic", "confidence": 1.0 }
}
```

## Crisis Resources Displayed

### India-Specific Helplines
1. **iCall India**: 9152987821
   - Available: Mon-Sat, 8am-10pm
   - Professional counseling service

2. **iCall Chat**: icallhelpline.org
   - Online chat support
   - Opens in new tab

3. **Emergency Services**: 112
   - 24/7 emergency response
   - Highlighted with special styling

## User Experience Flow

### Crisis Scenario
1. User types: "I want to hurt myself"
2. Message is sent to backend
3. Backend detects crisis pattern
4. Crisis response is generated
5. Frontend receives `isCrisis: true`
6. EmergencyBubble renders with:
   - Pulsing red header
   - Compassionate message
   - Helpline cards with call buttons
   - Reassuring footer
7. User can immediately:
   - Call helpline (mobile)
   - Copy number (desktop)
   - Open chat service
   - Continue conversation

### Visual Feedback
- **Immediate attention**: Pulsing animation draws eye
- **Clear hierarchy**: Most urgent info (emergency number) highlighted
- **Easy action**: Large, clear buttons
- **Reassurance**: Supportive messaging throughout

## Responsive Design

### Mobile (< 768px)
- Stacked layout
- Full-width cards
- Touch-friendly buttons
- Optimized font sizes
- Direct dial on tap

### Desktop (≥ 768px)
- Wider layout (max 700px)
- Hover effects
- Copy-to-clipboard on click
- Larger interactive areas

## Customization

### Adding New Helplines
Edit the backend crisis response in `backend/pipeline/safety.py`:
```python
CRISIS_RESPONSE = """
🆘 New Helpline: 1234567890 (24/7)
🆘 Another Service: website.com
"""
```

The frontend will automatically parse and display them.

### Changing Colors
Edit `EmergencyBubble.css`:
```css
.emergency-header {
  background: linear-gradient(135deg, #your-color 0%, #your-color-dark 100%);
}
```

### Adjusting Animation Duration
```css
.emergency-header.pulse-animation {
  animation: emergencyPulse 2s ease-in-out infinite; /* Change 2s */
}
```

## Testing

### Test Crisis Detection
Send these messages to trigger emergency mode:
- "I want to kill myself"
- "I want to hurt myself"
- "I'm going to end it all"
- "I can't go on anymore"

### Expected Behavior
1. Message should render with EmergencyBubble
2. Red pulsing header should appear
3. Helpline cards should be interactive
4. Call buttons should work (mobile) or copy (desktop)
5. Chat links should open in new tab

## Accessibility Compliance

### WCAG 2.1 Level AA
- ✅ Color contrast ratio > 4.5:1
- ✅ Keyboard navigation support
- ✅ Focus indicators on interactive elements
- ✅ ARIA labels on buttons
- ✅ Semantic HTML structure
- ✅ Reduced motion support

### Screen Reader Support
- Descriptive button labels
- Proper heading hierarchy
- Alt text for icons (via aria-label)
- Meaningful link text

## Future Enhancements

### Potential Improvements
1. **Geolocation-based helplines**: Show local resources
2. **Language-specific helplines**: Match user's language
3. **Time-aware display**: Show only available helplines
4. **Follow-up prompts**: Check-in after crisis message
5. **Resource library**: Link to additional support materials
6. **Anonymous reporting**: Option to alert emergency contacts
7. **Crisis history**: Track and monitor crisis events
8. **Integration with emergency services**: Direct connection to 112

### Advanced Features
- Voice call integration (WebRTC)
- Video chat support
- Real-time counselor availability
- Crisis severity levels
- Automated follow-up messages
- Safety planning tools

## Safety Considerations

### Important Notes
1. **Not a replacement**: This is NOT a replacement for professional help
2. **Immediate danger**: Always encourage calling emergency services
3. **Privacy**: Crisis events are logged for monitoring
4. **Limitations**: AI cannot provide emergency intervention
5. **Liability**: Clear disclaimers about service limitations

### Best Practices
- Always display multiple helpline options
- Prioritize emergency services (112)
- Use compassionate, non-judgmental language
- Provide immediate, actionable steps
- Maintain conversation after crisis response
- Log crisis events for follow-up

## Troubleshooting

### Crisis Mode Not Triggering
- Check backend logs for crisis detection
- Verify `is_crisis` flag in API response
- Ensure `isCrisis` prop is passed to MessageBubble
- Check browser console for errors

### Styling Issues
- Clear browser cache
- Check CSS import in MessageBubble.jsx
- Verify EmergencyBubble.css is loaded
- Inspect element for conflicting styles

### Button Not Working
- Check phone number format
- Verify `tel:` protocol support
- Test clipboard API permissions
- Check external link URLs

## Support

For issues or questions about the emergency mode feature:
1. Check backend logs: `backend/logs/`
2. Review crisis patterns: `backend/pipeline/safety.py`
3. Test with known crisis keywords
4. Verify API response structure
5. Check browser console for frontend errors
