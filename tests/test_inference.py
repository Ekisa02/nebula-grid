import pytest
from app.ml.inference import InferenceEngine

def test_inference_output_shape():
    engine = InferenceEngine(model_path=None)
    inp = [0.1] * 8
    out = engine.predict(inp)
    assert 'prediction' in out
    assert 'probabilities' in out
    assert isinstance(out['probabilities'], list)
    assert len(out['probabilities']) == 2

def test_inference_padding_truncation():
    engine = InferenceEngine()
    short = [0.5, 0.2]
    long = [0.1] * 20
    out_short = engine.predict(short)
    out_long = engine.predict(long)
    assert 'prediction' in out_short
    assert 'prediction' in out_long
