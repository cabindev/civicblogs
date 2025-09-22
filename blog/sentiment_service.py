"""
Sentiment Analysis Service for Thai Comments
ระบบวิเคราะห์ความรู้สึกของความคิดเห็นภาษาไทย
"""

import re
from textblob import TextBlob
from collections import Counter
import json

class ThaiSentimentAnalyzer:
    """Thai Sentiment Analysis Class"""
    
    def __init__(self):
        # Thai positive words
        self.positive_words = {
            'ดี', 'เก่ง', 'สุดยอด', 'ยอดเยี่ยม', 'เยี่ยม', 'ชอบ', 'รัก', 'สนับสนุน',
            'เห็นด้วย', 'ถูกต้อง', 'ดีมาก', 'ประทับใจ', 'น่าชื่นชม', 'เจ็บ', 'สวย',
            'เท่', 'มีประโยชน์', 'ช่วยได้', 'เข้าใจ', 'ชัดเจน', 'น่าสนใจ', 'แน่นอน',
            '👍', '❤️', '😍', '😊', '👏', '💪', '✅', '⭐', '🔥', '💯'
        }
        
        # Thai negative words  
        self.negative_words = {
            'แย่', 'ไม่ดี', 'ห่วย', 'เลว', 'ผิด', 'ไม่เห็นด้วย', 'ไม่ชอบ', 'เกลียด',
            'โกรธ', 'หงุดหงิด', 'น่ารำคาญ', 'เสียใจ', 'ผิดหวัง', 'เศร้า', 'ไร้สาระ',
            'โง่', 'ไม่เข้าใจ', 'สับสน', 'ยุ่งยาก', 'ปัญหา', 'วิกฤต', 'เสียหาย',
            'ไม่เหมาะสม', 'ไม่มีประโยชน์', 'เสียเวลา', 'ไม่ใช่', 'ไม่', 'เสีย', 'ห่วย',
            '👎', '😠', '😡', '😢', '😞', '💔', '❌', '🤦', '😤', '🙄'
        }
        
        # Thai neutral/question words
        self.neutral_words = {
            'อย่างไร', 'ทำไม', 'เมื่อไหร่', 'ที่ไหน', 'ใคร', 'อะไร', 'คิดว่า', 'ว่าไง',
            'รู้ไหม', 'เป็นยังไง', 'ช่วยได้ไหม', 'มีใครรู้บ้าง', '🤔', '❓', '❔'
        }
    
    def clean_text(self, text):
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Convert to lowercase for analysis
        return text.lower()
    
    def analyze_sentiment(self, text):
        """
        Analyze sentiment of Thai text
        Returns: dict with sentiment score and label
        """
        if not text:
            return {
                'sentiment': 'neutral',
                'score': 0.0,
                'confidence': 0.0,
                'details': {
                    'positive_count': 0,
                    'negative_count': 0,
                    'neutral_count': 0
                }
            }
        
        clean_text = self.clean_text(text)
        
        # Count sentiment words with partial matching
        positive_count = 0
        negative_count = 0 
        neutral_count = 0
        
        for word in self.positive_words:
            if word in clean_text:
                positive_count += clean_text.count(word)
                
        for word in self.negative_words:
            if word in clean_text:
                negative_count += clean_text.count(word)
                
        for word in self.neutral_words:
            if word in clean_text:
                neutral_count += clean_text.count(word)
        
        # Calculate sentiment score
        total_sentiment_words = positive_count + negative_count
        
        if total_sentiment_words == 0:
            # Use TextBlob for English/mixed content
            try:
                blob = TextBlob(text)
                polarity = blob.sentiment.polarity
                
                if polarity > 0.1:
                    sentiment = 'positive'
                    score = polarity
                elif polarity < -0.1:
                    sentiment = 'negative' 
                    score = polarity
                else:
                    sentiment = 'neutral'
                    score = 0.0
                    
                confidence = abs(polarity)
                
            except:
                sentiment = 'neutral'
                score = 0.0
                confidence = 0.0
        else:
            # Thai sentiment analysis
            score = (positive_count - negative_count) / max(total_sentiment_words, 1)
            confidence = total_sentiment_words / max(len(clean_text.split()), 1)
            
            if score > 0.2:
                sentiment = 'positive'
            elif score < -0.2:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
        
        return {
            'sentiment': sentiment,
            'score': round(score, 3),
            'confidence': round(min(confidence, 1.0), 3),
            'details': {
                'positive_count': positive_count,
                'negative_count': negative_count,
                'neutral_count': neutral_count,
                'total_words': len(clean_text.split()),
                'sentiment_words': total_sentiment_words
            }
        }
    
    def analyze_comments_batch(self, comments):
        """
        Analyze multiple comments
        Args: comments (list) - List of comment texts
        Returns: dict with overall analysis
        """
        if not comments:
            return {
                'total_comments': 0,
                'sentiment_distribution': {'positive': 0, 'negative': 0, 'neutral': 0},
                'average_score': 0.0,
                'individual_results': []
            }
        
        results = []
        sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
        total_score = 0.0
        
        for i, comment in enumerate(comments):
            if isinstance(comment, dict):
                text = comment.get('text', '')
                comment_id = comment.get('id', i)
            else:
                text = str(comment)
                comment_id = i
            
            analysis = self.analyze_sentiment(text)
            analysis['comment_id'] = comment_id
            analysis['original_text'] = text[:100] + '...' if len(text) > 100 else text
            
            results.append(analysis)
            sentiment_counts[analysis['sentiment']] += 1
            total_score += analysis['score']
        
        return {
            'total_comments': len(comments),
            'sentiment_distribution': sentiment_counts,
            'sentiment_percentages': {
                'positive': round((sentiment_counts['positive'] / len(comments)) * 100, 1),
                'negative': round((sentiment_counts['negative'] / len(comments)) * 100, 1),
                'neutral': round((sentiment_counts['neutral'] / len(comments)) * 100, 1)
            },
            'average_score': round(total_score / len(comments), 3),
            'individual_results': results
        }


class FacebookPostAnalyzer:
    """Analyze Facebook Post Comments with Sentiment"""
    
    def __init__(self):
        self.sentiment_analyzer = ThaiSentimentAnalyzer()
    
    def analyze_post_url(self, post_url, comments_data):
        """
        Analyze a Facebook post with comments
        Args:
            post_url (str): Facebook post URL
            comments_data (list): List of comments (manually collected)
        """
        
        # Extract post ID from URL if possible
        post_id = self.extract_post_id(post_url)
        
        # Analyze comments sentiment
        sentiment_analysis = self.sentiment_analyzer.analyze_comments_batch(comments_data)
        
        return {
            'post_url': post_url,
            'post_id': post_id,
            'analysis_timestamp': self.get_timestamp(),
            'comments_analysis': sentiment_analysis,
            'recommendations': self.generate_recommendations(sentiment_analysis)
        }
    
    def extract_post_id(self, url):
        """Extract post ID from Facebook URL"""
        patterns = [
            r'/p/([^/]+)/',
            r'posts/([^/]+)',
            r'story_fbid=(\d+)',
            r'fbid=(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def generate_recommendations(self, analysis):
        """Generate recommendations based on sentiment analysis"""
        positive_pct = analysis['sentiment_percentages']['positive']
        negative_pct = analysis['sentiment_percentages']['negative']
        total_comments = analysis['total_comments']
        
        recommendations = []
        
        if positive_pct > 70:
            recommendations.append("📈 ความคิดเห็นเป็นบวกสูง - เหมาะสำหรับการขยายผลหรือใช้เป็น case study")
        
        if negative_pct > 50:
            recommendations.append("⚠️ ความคิดเห็นเป็นลบสูง - ควรทบทวนเนื้อหาหรือชี้แจงเพิ่มเติม")
        
        if total_comments < 5:
            recommendations.append("💬 ความคิดเห็นน้อย - ควรเพิ่ม engagement หรือ promote เพิ่มเติม")
        elif total_comments > 50:
            recommendations.append("🔥 ความคิดเห็นมาก - เนื้อหาได้รับความสนใจสูง")
        
        if analysis['average_score'] > 0.5:
            recommendations.append("✅ คะแนนความรู้สึกเป็นบวกโดยรวม")
        elif analysis['average_score'] < -0.5:
            recommendations.append("❌ คะแนนความรู้สึกเป็นลบโดยรวม - ต้องการการปรับปรุง")
        
        return recommendations


# Example usage and testing
if __name__ == "__main__":
    # Test the sentiment analyzer
    analyzer = ThaiSentimentAnalyzer()
    
    test_comments = [
        "เนื้อหาดีมาก ให้ความรู้เยอะ 👍",
        "ไม่เห็นด้วยกับเรื่องนี้เลย แย่มาก",
        "อยากทราบรายละเอียดเพิ่มเติมครับ",
        "สุดยอดเลย ชอบมาก ❤️",
        "ไร้สาระ ไม่มีประโยชน์ 👎"
    ]
    
    # Test individual sentiment
    for comment in test_comments:
        result = analyzer.analyze_sentiment(comment)
        print(f"Comment: {comment}")
        print(f"Sentiment: {result['sentiment']} (Score: {result['score']}, Confidence: {result['confidence']})")
        print("---")
    
    # Test batch analysis
    batch_result = analyzer.analyze_comments_batch(test_comments)
    print("\nBatch Analysis:")
    print(f"Total Comments: {batch_result['total_comments']}")
    print(f"Sentiment Distribution: {batch_result['sentiment_percentages']}")
    print(f"Average Score: {batch_result['average_score']}")