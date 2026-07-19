import pytest
from app.classifier import IntentClassifier

@pytest.fixture
def classifier():
    return IntentClassifier()

def test_order_track(classifier):
    intent, conf = classifier.classify("Where is my order #10001?")
    assert intent == "EC_ORDER_TRACK"
    assert conf >= 0.8

def test_return(classifier):
    intent, conf = classifier.classify("I want a refund for my shoes")
    assert intent == "EC_RETURN_REFUND"
    assert conf >= 0.8

def test_entities(classifier):
    entities = classifier.extract_entities("Order #10001 tomorrow")
    assert entities.get("order_id") == "10001"
