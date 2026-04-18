# Response templates organized by emotion × intent × turn_stage
# Structure: RESPONSE_TEMPLATES[emotion][intent][turn_stage]
# turn_stage: "opening" (turns 1-2), "middle" (turns 3-4), "deeper" (turn 5+)

RESPONSE_TEMPLATES = {
    "sadness": {
        "sadness and depression": {
            "opening": [
                "That sounds incredibly hard. I can hear the pain in your words. What's been weighing on you most?",
                "I'm really sorry you're going through this. It takes courage to share these feelings. Can you tell me more about what's happening?",
                "That sounds really painful. You don't have to go through this alone. What's been making you feel this way?"
            ],
            "middle": [
                "I hear you. When sadness feels this heavy, sometimes it helps to focus on just this moment. Can you try putting one hand on your chest and feeling it rise and fall? You are here, you are okay.",
                "Thank you for trusting me with this. Sometimes when everything feels dark, it can help to notice small things around you. Can you name one thing you can see right now?",
                "It makes sense that you'd feel this way given what you're going through. Have you been able to talk to anyone else about this, or would you like to explore some gentle coping strategies together?"
            ],
            "deeper": [
                "I've been here with you through this conversation, and I can see you're carrying a lot. Have you considered reaching out to a counselor or therapist who can provide ongoing support?",
                "You've shared so much with me, and I want you to know that what you're feeling is valid. Professional support can make a real difference. Would you be open to exploring that?",
                "I'm glad you've been talking with me. For ongoing support with these deep feelings, connecting with a mental health professional could be really helpful. What do you think about that?"
            ]
        },
        "loneliness and isolation": {
            "opening": [
                "Feeling alone can be one of the hardest things. I'm here with you right now. Can you tell me more about what's been making you feel isolated?",
                "That sounds really lonely. I hear you, and I'm listening. What's been going on that's made you feel this way?",
                "I can sense how isolated you're feeling. You're not alone in this moment—I'm here. What would help you feel a little more connected?"
            ],
            "middle": [
                "Loneliness can feel overwhelming. Sometimes reaching out, even in small ways, can help. Is there anyone you've thought about connecting with, even just to say hello?",
                "I hear how alone you've been feeling. Even small connections can matter. Have you tried any activities where you might meet others, or would you like to talk about ways to feel less isolated?",
                "It's hard when it feels like no one understands. I'm here listening to you. What's one small thing that's brought you even a tiny bit of comfort recently?"
            ],
            "deeper": [
                "You've been carrying this loneliness for a while. Talking to a counselor could give you a space to explore these feelings more deeply. Would that be something you'd consider?",
                "I've been here with you, and I can see how much you're struggling with feeling alone. Professional support can help you work through this. What are your thoughts on that?",
                "Loneliness can be really painful, and you don't have to face it alone. A therapist could help you build connections and work through these feelings. Would you be open to that?"
            ]
        },
        "general emotional support": {
            "opening": [
                "I can hear that you're feeling sad. I'm here to listen. What's been on your mind?",
                "That sounds tough. I'm here with you. Can you share more about what's been happening?",
                "I hear the sadness in what you're sharing. You're not alone right now. What would help you feel supported?"
            ],
            "middle": [
                "Thank you for sharing that with me. When sadness comes up, sometimes it helps to be gentle with yourself. What's one kind thing you could do for yourself today?",
                "I'm listening. It's okay to feel sad—emotions are information. What do you think your sadness is trying to tell you?",
                "I hear you. Sometimes just acknowledging the sadness can help. Have you been able to rest or do anything that brings you a little peace?"
            ],
            "deeper": [
                "You've been working through a lot in our conversation. If these feelings continue, talking to a professional could give you more tools to cope. What do you think?",
                "I'm glad you've been sharing with me. For deeper support, a counselor could really help. Would you be interested in exploring that option?",
                "You've been very open about your feelings, which is important. Ongoing support from a therapist might be beneficial. How do you feel about that?"
            ]
        }
    },
    "fear": {
        "anxiety and panic": {
            "opening": [
                "It sounds like you're feeling really scared right now. I'm here with you. Can you tell me what's making you feel this way?",
                "I can sense a lot of anxiety in what you're sharing. You're safe in this moment. What's been triggering these feelings?",
                "That sounds terrifying. I'm here, and I'm listening. What's been going on that's made you feel so anxious?"
            ],
            "middle": [
                "When panic feels overwhelming, grounding can help. Can you try this with me? Notice 5 things you can see, 4 things you can touch, 3 things you can hear, 2 things you can smell, and 1 thing you can taste.",
                "I hear how anxious you're feeling. Let's try slowing down together. Can you breathe in for 4 counts, hold for 4, breathe out for 4, and hold for 4? This is called box breathing.",
                "Anxiety can feel like it's taking over. You're doing the right thing by talking about it. Have you noticed what tends to trigger these feelings, or when they're strongest?"
            ],
            "deeper": [
                "You've been dealing with a lot of anxiety. A therapist who specializes in anxiety can teach you more techniques to manage these feelings. Would you consider that?",
                "I've been here with you through this, and I can see how much anxiety you're carrying. Professional support could make a real difference. What are your thoughts?",
                "Anxiety can be really debilitating, and you don't have to manage it alone. A mental health professional could help you develop stronger coping strategies. Would that interest you?"
            ]
        },
        "stress and overwhelm": {
            "opening": [
                "It sounds like you're feeling really overwhelmed. I'm here to listen. What's been piling up on you?",
                "That sounds like a lot to handle. I hear you. Can you tell me more about what's been stressing you out?",
                "I can hear how stressed you are. You're not alone in this. What's been the biggest source of pressure for you?"
            ],
            "middle": [
                "When everything feels like too much, sometimes breaking things down helps. What's one small thing you could focus on right now, just for today?",
                "I hear how overwhelmed you are. It's okay to not have it all figured out. Have you been able to take any breaks, even small ones, to breathe?",
                "Stress can build up so quickly. What would it look like to let go of just one thing on your plate, even temporarily?"
            ],
            "deeper": [
                "You've been carrying a lot of stress. Talking to a counselor could help you develop better strategies for managing overwhelm. Would you be open to that?",
                "I can see how much you're juggling. Professional support could give you tools to handle stress more effectively. What do you think about exploring that?",
                "Chronic stress can take a real toll. A therapist could help you work through what's overwhelming you and build resilience. Would that be helpful?"
            ]
        },
        "general emotional support": {
            "opening": [
                "I can hear that you're feeling afraid. I'm here with you. What's been scaring you?",
                "That sounds really frightening. You're safe right now. Can you share more about what's going on?",
                "I hear the fear in what you're sharing. I'm listening. What's been making you feel this way?"
            ],
            "middle": [
                "Fear is a natural response, but it doesn't have to control you. What helps you feel safer when fear comes up?",
                "I'm here with you. Sometimes fear is trying to protect us. What do you think your fear is trying to tell you?",
                "It's okay to feel scared. You're taking a brave step by talking about it. What would help you feel a little more grounded right now?"
            ],
            "deeper": [
                "You've been working through these fears with me. A therapist could help you explore them more deeply and find lasting relief. Would you consider that?",
                "I'm glad you've been sharing your fears. Professional support could give you more tools to work through them. How do you feel about that?",
                "Fear can be really limiting. A counselor could help you understand and manage it better. Would that be something you'd be interested in?"
            ]
        }
    },
    "anger": {
        "anger and frustration": {
            "opening": [
                "I can hear how frustrated you are. That sounds really infuriating. What's been making you feel this way?",
                "It sounds like you're really angry right now. I'm listening. Can you tell me more about what happened?",
                "I hear the anger in your words. It makes sense that you'd feel this way. What's been going on?"
            ],
            "middle": [
                "Anger is a valid emotion—it's telling you something matters to you. What do you think is underneath the anger? What's been hurt or threatened?",
                "I hear you. When anger feels this strong, it can help to step back. What would you tell a good friend who was in this exact situation?",
                "It's okay to be angry. Sometimes anger is protecting us from other feelings. Have you been able to express this anger in a way that feels safe?"
            ],
            "deeper": [
                "You've been dealing with a lot of anger. A therapist could help you understand what's driving it and find healthier ways to express it. Would you be open to that?",
                "I can see how much frustration you're carrying. Professional support could help you work through this anger constructively. What do you think?",
                "Anger can be exhausting to carry. A counselor could help you process it and find resolution. Would that be helpful for you?"
            ]
        },
        "stress and overwhelm": {
            "opening": [
                "It sounds like you're feeling really frustrated with everything on your plate. I hear you. What's been the most overwhelming part?",
                "I can hear the anger and stress in what you're sharing. That's a lot to deal with. Can you tell me more?",
                "That sounds incredibly frustrating. I'm listening. What's been pushing you to this point?"
            ],
            "middle": [
                "When stress turns into anger, it's often a sign that boundaries have been crossed. What's one boundary you could set to protect your energy?",
                "I hear how overwhelmed and angry you are. It's okay to feel this way. What would it look like to give yourself permission to step back from something?",
                "Frustration can build when we're stretched too thin. What's one thing you could say no to, or ask for help with?"
            ],
            "deeper": [
                "You've been dealing with a lot of stress and anger. A therapist could help you develop better coping strategies. Would you consider that?",
                "I can see how much you're carrying. Professional support could help you manage stress before it turns into anger. What are your thoughts?",
                "Chronic stress and frustration can be really draining. A counselor could help you find healthier ways to cope. Would that interest you?"
            ]
        },
        "general emotional support": {
            "opening": [
                "I can hear that you're feeling angry. I'm here to listen. What's been making you feel this way?",
                "That sounds really frustrating. I hear you. Can you share more about what's going on?",
                "I hear the anger in what you're sharing. It's okay to feel this way. What happened?"
            ],
            "middle": [
                "Anger is a natural emotion. It's okay to feel it. What do you think would help you feel a little calmer right now?",
                "I'm listening. Sometimes anger is a signal that something needs to change. What do you think that might be?",
                "It's okay to be angry. You're allowed to have these feelings. What would help you process this anger in a healthy way?"
            ],
            "deeper": [
                "You've been working through a lot of anger. A therapist could help you understand it better and find constructive outlets. Would you be open to that?",
                "I'm glad you've been sharing your feelings. Professional support could give you more tools to manage anger. How do you feel about that?",
                "Anger can be really consuming. A counselor could help you work through it. Would that be something you'd consider?"
            ]
        }
    },
    "neutral": {
        "general emotional support": {
            "opening": [
                "Thank you for sharing that. I'm here to listen. What's been on your mind?",
                "I hear you. I'm here with you. Can you tell me more about what you're experiencing?",
                "I'm listening. What would be most helpful for you to talk about right now?"
            ],
            "middle": [
                "Thank you for continuing to share with me. How are you feeling about everything we've talked about?",
                "I'm here with you. What else would you like to explore or talk through?",
                "I appreciate you opening up. What's been the most important thing for you in our conversation so far?"
            ],
            "deeper": [
                "We've covered a lot together. If you ever need more support, talking to a counselor could be really beneficial. What do you think?",
                "I'm glad we've been able to talk. For ongoing support, a therapist could provide a consistent space for you. Would you be interested in that?",
                "You've been very thoughtful in our conversation. Professional support could help you continue this work. How do you feel about exploring that?"
            ]
        }
    },
    "joy": {
        "general emotional support": {
            "opening": [
                "It's wonderful that you're feeling this way! I'm so glad to hear some positivity. What's been bringing you joy?",
                "That's really lovely to hear. I'm happy you're doing well today. What's been going well for you?",
                "It's so good to hear you're feeling happy! What's been the highlight for you recently?"
            ],
            "middle": [
                "I love hearing about what's bringing you joy. Moments like these are so important. What else has been positive for you?",
                "That's wonderful! It's great to celebrate the good moments. How can you hold onto this feeling?",
                "I'm really glad you're experiencing this happiness. What do you think has contributed to feeling this way?"
            ],
            "deeper": [
                "It's been great to hear about the positive things in your life. Keep nurturing what brings you joy. Is there anything else you'd like to talk about?",
                "I'm so happy you're in a good place. Remember to celebrate these moments. What are you looking forward to?",
                "It's wonderful to see you feeling positive. Keep taking care of yourself. What helps you maintain this sense of well-being?"
            ]
        }
    },
    "surprise": {
        "general emotional support": {
            "opening": [
                "That sounds like it came out of nowhere. I'm here to listen. What happened?",
                "Wow, that must have been unexpected. Can you tell me more about what surprised you?",
                "That sounds really surprising. I'm listening. How are you feeling about it?"
            ],
            "middle": [
                "Unexpected things can be disorienting. How are you processing what happened?",
                "I hear you. Surprises can be hard to make sense of. What's been your reaction to all of this?",
                "It sounds like you're still taking it all in. What would help you feel more grounded right now?"
            ],
            "deeper": [
                "You've been working through this unexpected situation. If you need ongoing support to process it, a counselor could help. What do you think?",
                "I'm glad you've been talking through this surprise with me. Professional support could help you navigate it further. Would you be interested?",
                "Unexpected events can have lasting effects. A therapist could help you process and adapt. Would that be helpful?"
            ]
        }
    },
    "disgust": {
        "general emotional support": {
            "opening": [
                "It sounds like something really bothered you. I'm here to listen. What happened?",
                "That sounds deeply uncomfortable. I hear you. Can you tell me more?",
                "I can sense that something really upset you. I'm listening. What's been going on?"
            ],
            "middle": [
                "It's okay to feel disgusted or bothered by things. What do you think would help you feel better about this?",
                "I hear you. Sometimes we encounter things that just don't sit right with us. How are you coping with this feeling?",
                "That sounds really unpleasant. What would help you move past this feeling?"
            ],
            "deeper": [
                "You've been dealing with some difficult feelings. If they persist, talking to a counselor could help. Would you consider that?",
                "I'm glad you've been sharing these uncomfortable feelings. Professional support could help you process them. What do you think?",
                "Strong negative reactions can be hard to shake. A therapist could help you work through them. Would that be helpful?"
            ]
        }
    },
    # Special templates
    "UNKNOWN": [
        "Thank you for sharing that with me. I'm listening—can you tell me a little more about what you're going through?",
        "I hear you. I'm here to support you. Can you help me understand what you're feeling right now?",
        "I'm here with you. What's the most important thing you'd like to talk about?"
    ],
    "POSITIVE_AFFIRMATION": [
        "It's wonderful that you're feeling this way. What's been bringing you joy?",
        "That's really lovely to hear. I'm glad you're doing well today.",
        "Moments like these matter. What's been going well for you?"
    ]
}
