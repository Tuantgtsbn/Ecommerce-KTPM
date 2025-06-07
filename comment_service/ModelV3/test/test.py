from transformers import DistilBertForSequenceClassification, DistilBertTokenizer
import torch

# Load model and tokenizer
model = DistilBertForSequenceClassification.from_pretrained("D:\Ecommerce\comment_service\ModelV3\models\distilbert_sentiment_model")
tokenizer = DistilBertTokenizer.from_pretrained("D:\Ecommerce\comment_service\ModelV3\models\distilbert_sentiment_model")

# Ensure model is in evaluation mode
model.eval()

# Map sentiment labels
sentiment_map = {2: "positive", 1: "neutral", 0: "negative"}

def classify_sentiment(text):
    """
    Classify the sentiment of the given text.
    
    Args:
        text (str): The input text to classify.
    
    Returns:
        str: The sentiment label ('positive', 'neutral', 'negative').
    """
    # Tokenize input text
    inputs = tokenizer(
        text,
        max_length=128,
        padding=True,
        truncation=True,
        return_tensors="pt"
    )
    
    # Perform inference
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()
    
    # Map predicted class to sentiment
    return sentiment_map[predicted_class]

# Example usage
if __name__ == "__main__":
    text = "Product is bad"
    sentiment = classify_sentiment(text)
    print(f"Sentiment: {sentiment}")