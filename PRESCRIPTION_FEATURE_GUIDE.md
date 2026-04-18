# Prescription Analyzer & Reminder System - User Guide

## 🎯 Overview

This feature allows you to:
1. Upload prescription images
2. Extract medicine information automatically
3. Create customized reminder schedules
4. Track daily medicine doses

## 📱 How to Use

### Step 1: Access the Feature

**From Chat Interface:**
- Look for the **pill icon (💊)** in the chat input area
- It's located next to the attachment button
- Click it to open the prescription analyzer

**Location:**
```
Chat Input Bar:
[+] [💊] [Text Input...] [🎤] [Send]
     ↑
  Click here!
```

### Step 2: Upload Prescription

**Upload Screen:**
1. Click the upload area or drag & drop an image
2. Supported formats: JPG, PNG
3. Maximum size: 10MB
4. Preview appears after selection
5. Click "Analyze Prescription" to process

**What Happens:**
- Image is uploaded to backend
- OCR extracts text from prescription
- AI identifies medicines, dosages, and instructions
- Results appear in next step

### Step 3: Review & Customize

**Review Screen Shows:**
- Medicine name (e.g., "Aspirin")
- Dosage (e.g., "100mg")
- Instructions (e.g., "Take after meals")
- Suggested reminder times

**Customize Reminder Times:**
1. Each medicine has time inputs
2. Click time input to change (24-hour format)
3. Click "+ Add Time" to add more reminders
4. Click "×" to remove a time
5. Set times when you want to be reminded

**Example:**
```
Medicine: Aspirin 100mg
Instructions: Take twice daily after meals

Reminder Times:
[09:00] [×]  ← Morning dose
[21:00] [×]  ← Evening dose
[+ Add Time]
```

### Step 4: Create Schedule

1. Review all medicines and times
2. Click "Create Reminder Schedule"
3. Wait for confirmation
4. Success message appears
5. Click "Done" to close modal

### Step 5: View Reminders

**Navigate to Reminder Page:**
- Click "Medicine Reminder" button in top-right of chat
- Or use navigation menu

**Reminder Dashboard Shows:**
- All active medicine reminders
- Medicine name and dosage
- Scheduled time
- Dose counter (taken / total per day)
- Progress bar

**Track Your Doses:**
1. Find the medicine card
2. Use [−] and [+] buttons to adjust doses taken
3. Progress bar updates automatically
4. Changes save to backend immediately

**Example Card:**
```
┌─────────────────────────────────┐
│ Aspirin                         │
│ 100mg                           │
│                                 │
│ 🕐 09:00 AM                     │
│                                 │
│ Doses Today                     │
│ [−]  2 / 3  [+]                │
│                                 │
│ Progress: ████████░░ 67%        │
└─────────────────────────────────┘
```

## 🎨 Visual Flow

```
┌─────────────────────────────────────────────────────────────┐
│                        CHAT PAGE                            │
│                                                             │
│  [+] [💊] [Type message...] [🎤] [Send]                    │
│       ↓                                                     │
│   Click Pill Icon                                          │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│              PRESCRIPTION UPLOAD MODAL                      │
│                                                             │
│  ┌─────────────────────────────────────────┐              │
│  │                                         │              │
│  │         📤 Upload Icon                  │              │
│  │                                         │              │
│  │   Click to upload prescription image   │              │
│  │   Supports JPG, PNG (Max 10MB)         │              │
│  │                                         │              │
│  └─────────────────────────────────────────┘              │
│                                                             │
│           [Analyze Prescription]                           │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│              REVIEW & CUSTOMIZE MODAL                       │
│                                                             │
│  📄 Extracted Medicines                                    │
│                                                             │
│  ┌─────────────────────────────────────────┐              │
│  │ Aspirin                        100mg    │              │
│  │ Take 1 tablet after meals               │              │
│  │                                         │              │
│  │ 🕐 Reminder Times                       │              │
│  │ [09:00] [×]                             │              │
│  │ [21:00] [×]                             │              │
│  │ [+ Add Time]                            │              │
│  └─────────────────────────────────────────┘              │
│                                                             │
│  [Back]  [Create Reminder Schedule]                       │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                  SUCCESS MODAL                              │
│                                                             │
│                    ✓                                        │
│                                                             │
│         Schedule Created Successfully!                      │
│                                                             │
│  Your medicine reminders have been added                   │
│  to the reminder page.                                     │
│                                                             │
│                  [Done]                                     │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│              MEDICINE REMINDER PAGE                         │
│                                                             │
│  Medicine Reminder                    [Back to Chat]       │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │ Aspirin      │  │ Vitamin D    │  │ Metformin    │    │
│  │ 100mg        │  │ 1000 IU      │  │ 500mg        │    │
│  │              │  │              │  │              │    │
│  │ 🕐 09:00     │  │ 🕐 12:00     │  │ 🕐 14:00     │    │
│  │              │  │              │  │              │    │
│  │ Doses Today  │  │ Doses Today  │  │ Doses Today  │    │
│  │ [−] 2/3 [+] │  │ [−] 2/2 [+] │  │ [−] 1/4 [+] │    │
│  │              │  │              │  │              │    │
│  │ ████████░░   │  │ ██████████   │  │ ███░░░░░░░   │    │
│  │ 67%          │  │ 100%         │  │ 25%          │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## 💡 Tips & Best Practices

### For Best Results:
1. **Clear Images**: Take photos in good lighting
2. **Readable Text**: Ensure prescription text is legible
3. **Correct Format**: Use JPG or PNG images
4. **Appropriate Size**: Keep under 10MB

### Setting Reminder Times:
1. **Match Your Routine**: Set times you'll remember
2. **Meal Times**: Align with breakfast, lunch, dinner
3. **Multiple Doses**: Space evenly throughout day
4. **Consistency**: Use same times daily

### Tracking Doses:
1. **Update Immediately**: Mark doses right after taking
2. **Daily Reset**: Counters reset each day
3. **Honest Tracking**: Accurate tracking helps adherence
4. **Review Progress**: Check progress bars regularly

## 🔧 Troubleshooting

### Upload Issues

**"File too large" error:**
- Reduce image size
- Use image compression tool
- Maximum: 10MB

**"Only image files allowed" error:**
- Use JPG or PNG format
- Don't upload PDFs or documents

**Upload fails:**
- Check internet connection
- Verify backend is running
- Try smaller image

### Extraction Issues

**No medicines found:**
- Currently using mock data
- Real OCR coming soon
- Try different image

**Wrong medicines extracted:**
- Review and edit times manually
- Real AI extraction coming soon

### Reminder Issues

**Reminders not showing:**
- Check you're on correct session
- Refresh the page
- Verify backend connection

**Dose counter not updating:**
- Check internet connection
- Verify backend is running
- Try refreshing page

## 🎯 Common Use Cases

### Daily Medication Management
```
Morning Routine:
1. Check reminder page
2. Take morning medicines
3. Mark doses as taken
4. Check progress

Evening Routine:
1. Check reminder page
2. Take evening medicines
3. Mark doses as taken
4. Review daily progress
```

### Multiple Prescriptions
```
1. Upload first prescription
2. Create schedule
3. Upload second prescription
4. Create schedule
5. All reminders appear together
```

### Changing Schedule
```
1. Delete old reminder (coming soon)
2. Upload new prescription
3. Create new schedule
4. Or manually adjust times
```

## 📊 Understanding Progress

### Progress Bar Colors:
- **Green**: Good adherence (>75%)
- **Yellow**: Moderate adherence (50-75%)
- **Red**: Low adherence (<50%)

### Dose Counter:
- **Left Number**: Doses taken today
- **Right Number**: Total doses per day
- **Percentage**: Completion rate

### Example:
```
2 / 3 = 67%
↑   ↑    ↑
│   │    └─ Completion percentage
│   └────── Total doses per day
└────────── Doses taken today
```

## 🚀 Quick Start Checklist

- [ ] Backend running (port 8000)
- [ ] Frontend running (port 5173)
- [ ] Open chat page
- [ ] Click pill icon (💊)
- [ ] Upload prescription image
- [ ] Review extracted medicines
- [ ] Set reminder times
- [ ] Create schedule
- [ ] Navigate to reminder page
- [ ] Track your doses!

## 📞 Need Help?

### Check These First:
1. Is backend running? → http://localhost:8000/api/health
2. Is frontend running? → http://localhost:5173
3. Browser console errors?
4. Network tab shows API calls?

### Common Solutions:
- Refresh the page
- Clear browser cache
- Restart backend
- Check console logs
- Verify file format

## 🎉 Success Indicators

You'll know it's working when:
- ✅ Pill icon appears in chat input
- ✅ Modal opens on click
- ✅ Image uploads successfully
- ✅ Medicines appear in review
- ✅ Schedule creates without errors
- ✅ Reminders show on reminder page
- ✅ Dose counters update on click
- ✅ Progress bars animate

Enjoy your new prescription management system! 💊✨
