"""
Basic tests for TermTweet
"""

import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from termtweet.core import load_credentials, authenticate_twitter, tweet


class TestCredentials:
    """Test credential loading functionality."""

    @patch('termtweet.core.Path')
    @patch('termtweet.core.load_dotenv')
    def test_load_credentials_missing(self, mock_load_dotenv, mock_path):
        """Test loading credentials when none are available."""
        # Mock the path to not exist
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = False
        mock_path.return_value = mock_path_instance

        result = load_credentials()
        assert result is None

    def test_load_credentials_with_env_vars(self):
        """Test loading credentials from environment variables."""
        with patch.dict(os.environ, {
            'TWITTER_API_KEY': 'test_key',
            'TWITTER_API_SECRET': 'test_secret',
            'TWITTER_ACCESS_TOKEN': 'test_token',
            'TWITTER_ACCESS_TOKEN_SECRET': 'test_token_secret',
            'TWITTER_BEARER_TOKEN': 'test_bearer'
        }):
            result = load_credentials()
            assert result is not None
            assert len(result) == 5
            assert result[0] == 'test_key'


class TestAuthentication:
    """Test Twitter authentication."""

    @patch('termtweet.core.tweepy.Client')
    def test_authenticate_twitter_success(self, mock_client):
        """Test successful Twitter authentication."""
        mock_client.return_value = MagicMock()
        result = authenticate_twitter('key', 'secret', 'token', 'token_secret', 'bearer')
        assert result is not None

    @patch('termtweet.core.tweepy.Client')
    def test_authenticate_twitter_failure(self, mock_client):
        """Test failed Twitter authentication."""
        mock_client.side_effect = Exception("Auth failed")
        result = authenticate_twitter('key', 'secret', 'token', 'token_secret', 'bearer')
        assert result is None


class TestTweet:
    """Test tweet functionality."""

    def test_tweet_text_length_validation(self):
        """Test that tweets over 280 characters are rejected."""
        long_text = "x" * 281
        with patch('termtweet.core.load_credentials', return_value=None):
            result = tweet(long_text)
            assert result is False

    @patch('termtweet.core.load_credentials')
    def test_tweet_no_credentials(self, mock_load_credentials):
        """Test tweeting when no credentials are available."""
        mock_load_credentials.return_value = None
        result = tweet("Test tweet")
        assert result is False

    @patch('termtweet.core.load_credentials')
    @patch('termtweet.core.authenticate_twitter')
    def test_tweet_auth_failure(self, mock_auth, mock_load_credentials):
        """Test tweeting when authentication fails."""
        mock_load_credentials.return_value = ('key', 'secret', 'token', 'token_secret', 'bearer')
        mock_auth.return_value = None

        result = tweet("Test tweet")
        assert result is False


class TestCLI:
    """Test CLI functionality."""

    @patch('termtweet.core.tweet')
    @patch('termtweet.core.load_credentials')
    def test_cli_tweet_success(self, mock_load_credentials, mock_tweet):
        """Test successful CLI tweet."""
        mock_load_credentials.return_value = ('key', 'secret', 'token', 'token_secret', 'bearer')
        mock_tweet.return_value = True

        with patch('sys.argv', ['termtweet', 'Test message']):
            from termtweet.cli import main
            # This should not raise an exception
            main()

    def test_cli_no_text(self):
        """Test CLI with no text argument."""
        with patch('sys.argv', ['termtweet']):
            with patch('termtweet.cli.create_parser') as mock_parser:
                mock_parser_instance = MagicMock()
                mock_parser.return_value = mock_parser_instance
                mock_parser_instance.parse_args.return_value = MagicMock(text=None, setup=False, test=False)

                from termtweet.cli import main
                main()
                mock_parser_instance.print_help.assert_called_once()


if __name__ == '__main__':
    pytest.main([__file__])