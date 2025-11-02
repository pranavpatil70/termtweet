"""
TermTweet Core - Core functionality for tweeting
"""

import os
import sys
from pathlib import Path
import tweepy
from dotenv import load_dotenv

def load_credentials():
    """Load Twitter API credentials from environment variables."""
    # Try loading from user's home directory first
    env_file = Path.home() / '.termtweet' / '.env'
    if env_file.exists():
        load_dotenv(env_file)
    else:
        # Fallback to current directory
        load_dotenv()

    api_key = os.getenv('TWITTER_API_KEY')
    api_secret = os.getenv('TWITTER_API_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

    if not all([api_key, api_secret, access_token, access_token_secret, bearer_token]):
        return None

    return api_key, api_secret, access_token, access_token_secret, bearer_token

def authenticate_twitter(api_key, api_secret, access_token, access_token_secret, bearer_token):
    """Authenticate with Twitter API."""
    try:
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            bearer_token=bearer_token
        )
        return client
    except Exception:
        return None

def upload_media(api_key, api_secret, access_token, access_token_secret, image_path):
    """Upload image to Twitter and return media ID."""
    try:
        auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
        api = tweepy.API(auth)
        media = api.media_upload(image_path)
        return media.media_id_string
    except Exception:
        return None

def post_tweet(client, text, media_id=None):
    """Post a tweet with optional media."""
    try:
        if media_id:
            response = client.create_tweet(text=text, media_ids=[media_id])
        else:
            response = client.create_tweet(text=text)
        return response.data['id']
    except Exception:
        return None

def tweet(text, image_path=None):
    """Main tweet function."""
    # Load credentials
    creds = load_credentials()
    if not creds:
        return False

    api_key, api_secret, access_token, access_token_secret, bearer_token = creds

    # Authenticate
    client = authenticate_twitter(api_key, api_secret, access_token, access_token_secret, bearer_token)
    if not client:
        return False

    # Handle image upload if provided
    media_id = None
    if image_path:
        media_id = upload_media(api_key, api_secret, access_token, access_token_secret, image_path)
        if not media_id:
            return False

    # Post the tweet
    tweet_id = post_tweet(client, text, media_id)
    return tweet_id is not None

def setup_credentials():
    """Interactive setup for credentials."""
    print("Let's set up your Twitter API credentials.")
    print("Get these from: https://developer.twitter.com/en/portal/dashboard")
    print()

    # Get credentials from user
    api_key = input("Enter your Twitter API Key: ").strip()
    api_secret = input("Enter your Twitter API Secret: ").strip()
    access_token = input("Enter your Access Token: ").strip()
    access_token_secret = input("Enter your Access Token Secret: ").strip()
    bearer_token = input("Enter your Bearer Token: ").strip()

    # Validate inputs
    if not all([api_key, api_secret, access_token, access_token_secret, bearer_token]):
        print("All fields are required!")
        return False

    # Create .env content
    env_content = f"""# Twitter API Credentials
# Get these from https://developer.twitter.com/en/portal/dashboard
TWITTER_API_KEY={api_key}
TWITTER_API_SECRET={api_secret}
TWITTER_ACCESS_TOKEN={access_token}
TWITTER_ACCESS_TOKEN_SECRET={access_token_secret}
TWITTER_BEARER_TOKEN={bearer_token}
"""

    # Ensure .env directory exists
    env_dir = Path.home() / '.termtweet'
    env_dir.mkdir(exist_ok=True)
    env_file = env_dir / '.env'

    # Write to .env file
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print(f"✅ Credentials saved to {env_file}")
        return True
    except Exception as e:
        print(f"❌ Error saving credentials: {e}")
        return False

def test_credentials():
    """Test if credentials are configured correctly."""
    creds = load_credentials()
    if not creds:
        return False

    api_key, api_secret, access_token, access_token_secret, bearer_token = creds
    client = authenticate_twitter(api_key, api_secret, access_token, access_token_secret, bearer_token)

    return client is not None