import pytest
from unittest.mock import patch, MagicMock
import os
from src.core.llm import get_gemini_response


class TestGeminiLLM:
    """Test cases for Gemini LLM integration."""

    @patch('src.core.llm.genai.GenerativeModel')
    def test_get_gemini_response_success_primary_model(self, mock_model_class):
        """Test successful response from primary Gemini model."""
        # Setup mock
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "This is a test response about AI"
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        # Test
        query = "What is artificial intelligence?"
        result = get_gemini_response(query)

        # Assertions
        assert result == "This is a test response about AI"
        mock_model_class.assert_called_with("models/gemini-2.5-flash")
        mock_model.generate_content.assert_called_once_with(query)

    @patch('src.core.llm.genai.GenerativeModel')
    def test_get_gemini_response_fallback_model(self, mock_model_class):
        """Test fallback to secondary model when primary fails."""
        # Setup mocks
        mock_model_primary = MagicMock()
        mock_model_fallback = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Fallback response"
        
        # Primary model fails, fallback succeeds
        mock_model_primary.generate_content.side_effect = Exception("Primary model error")
        mock_model_fallback.generate_content.return_value = mock_response
        
        mock_model_class.side_effect = [mock_model_primary, mock_model_fallback]

        # Test
        result = get_gemini_response("Test query")

        # Assertions
        assert result == "Fallback response"
        assert mock_model_class.call_count == 2
        mock_model_class.assert_any_call("models/gemini-2.5-flash")
        mock_model_class.assert_any_call("models/gemini-flash-latest")

    @patch('src.core.llm.genai.GenerativeModel')
    def test_get_gemini_response_both_models_fail(self, mock_model_class):
        """Test error handling when both models fail."""
        # Setup mocks to fail
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = Exception("API Error")
        mock_model_class.return_value = mock_model

        # Test
        result = get_gemini_response("Test query")

        # Assertions
        assert result.startswith("Error:")
        assert "API Error" in result

    def test_prompt_formatting(self):
        """Test that the prompt is formatted correctly."""
        with patch('src.core.llm.genai.GenerativeModel') as mock_model_class:
            mock_model = MagicMock()
            mock_response = MagicMock()
            mock_response.text = "Response"
            mock_model.generate_content.return_value = mock_response
            mock_model_class.return_value = mock_model

            query = "Explain quantum physics"
            get_gemini_response(query)

            # Check that the prompt is passed as-is (no formatting in current implementation)
            call_args = mock_model.generate_content.call_args[0][0]
            assert call_args == query

    @pytest.mark.parametrize("query,expected_in_prompt", [
        ("What is DNA?", "What is DNA?"),
        ("How does photosynthesis work?", "How does photosynthesis work?"),
        ("Explain machine learning algorithms", "Explain machine learning algorithms"),
    ])
    def test_different_queries(self, query, expected_in_prompt):
        """Test various types of scientific queries."""
        with patch('src.core.llm.genai.GenerativeModel') as mock_model_class:
            mock_model = MagicMock()
            mock_response = MagicMock()
            mock_response.text = f"Response to: {query}"
            mock_model.generate_content.return_value = mock_response
            mock_model_class.return_value = mock_model

            result = get_gemini_response(query)

            assert f"Response to: {query}" == result
            call_args = mock_model.generate_content.call_args[0][0]
            assert expected_in_prompt in call_args

    def test_empty_response_handling(self):
        """Test handling of empty response from Gemini."""
        with patch('src.core.llm.genai.GenerativeModel') as mock_model_class:
            mock_model = MagicMock()
            mock_response = MagicMock()
            mock_response.text = ""
            mock_model.generate_content.return_value = mock_response
            mock_model_class.return_value = mock_model

            result = get_gemini_response("Test query")

            assert result == ""

    def test_large_query_handling(self):
        """Test handling of very large queries."""
        with patch('src.core.llm.genai.GenerativeModel') as mock_model_class:
            mock_model = MagicMock()
            mock_response = MagicMock()
            mock_response.text = "Response to large query"
            mock_model.generate_content.return_value = mock_response
            mock_model_class.return_value = mock_model

            # Create a very long query
            large_query = "What is " + "very " * 1000 + "complex question?"
            result = get_gemini_response(large_query)

            assert result == "Response to large query"
            # Verify the full query was passed
            call_args = mock_model.generate_content.call_args[0][0]
            assert large_query in call_args