from test_env.core import example_function

def test_example_function():
    """Test the example function."""
    result = example_function()
    assert isinstance(result, str)
    assert len(result) > 0 