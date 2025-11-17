#!/usr/bin/env python3
"""
Text Analyzer Function - Python Example
Demonstrates text processing and analysis.
"""

from endercom import AgentFunction
import re
import datetime

# Create a text analysis function
function = AgentFunction(
    name="Text Analyzer",
    description="Analyzes text for various metrics and insights",
    capabilities=["analyze", "text", "nlp", "metrics"]
)

@function.handler
def analyze_text(input_data):
    """
    Analyze text and return various metrics.
    Expects input like: {"text": "Your text here"} or just "text string"
    """
    try:
        # Extract text from input
        text = None
        if isinstance(input_data, dict):
            text = input_data.get('text') or input_data.get('content') or input_data.get('message')
        elif isinstance(input_data, str):
            text = input_data

        if not text:
            return {
                "error": "No text found. Expected format: {'text': 'your text here'}",
                "example": {"text": "Hello world! This is a sample text."}
            }

        # Basic text metrics
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        paragraphs = text.split('\n\n')
        paragraphs = [p.strip() for p in paragraphs if p.strip()]

        # Character analysis
        char_count = len(text)
        char_count_no_spaces = len(text.replace(' ', ''))

        # Word analysis
        word_lengths = [len(word.strip('.,!?;:"()[]{}')) for word in words]
        avg_word_length = sum(word_lengths) / len(word_lengths) if word_lengths else 0

        # Sentence analysis
        avg_sentence_length = len(words) / len(sentences) if sentences else 0

        # Find most common words (simple version)
        word_freq = {}
        for word in words:
            clean_word = re.sub(r'[^\w]', '', word.lower())
            if clean_word and len(clean_word) > 2:  # Skip short words
                word_freq[clean_word] = word_freq.get(clean_word, 0) + 1

        # Get top 5 most common words
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]

        return {
            "original_text": text[:200] + "..." if len(text) > 200 else text,
            "analyzed_at": datetime.datetime.now().isoformat(),
            "metrics": {
                "character_count": char_count,
                "character_count_no_spaces": char_count_no_spaces,
                "word_count": len(words),
                "sentence_count": len(sentences),
                "paragraph_count": len(paragraphs),
                "average_word_length": round(avg_word_length, 2),
                "average_sentence_length": round(avg_sentence_length, 2)
            },
            "insights": {
                "readability": "Simple" if avg_word_length < 4 and avg_sentence_length < 15 else
                             "Moderate" if avg_word_length < 6 and avg_sentence_length < 25 else "Complex",
                "most_common_words": top_words,
                "text_type": "Long form" if len(sentences) > 5 else "Short form"
            }
        }

    except Exception as e:
        return {
            "error": f"Analysis failed: {str(e)}",
            "input_received": str(input_data)[:100]
        }

if __name__ == "__main__":
    print("Starting Text Analyzer function...")
    print("Example usage:")
    print('  POST http://localhost:3003/execute')
    print('  Body: {"input": {"text": "Your text to analyze here."}}')

    function.run(port=3003)