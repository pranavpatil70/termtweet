#!/usr/bin/env python3
"""
Terminal Tweet Tool
A simple script to tweet from the terminal with optional image support.
"""

import os
import sys
try:
    import tweepy
except ImportError:
    print("Error: missing required Python package 'tweepy'. Install it with: pip install tweepy")
    sys.exit(1)
from dotenv import load_dotenv

def load_credentials():
    """Load Twitter API credentials from environment variables."""
    load_dotenv()

    api_key = os.getenv('TWITTER_API_KEY')
    api_secret = os.getenv('TWITTER_API_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

    if not all([api_key, api_secret, access_token, access_token_secret, bearer_token]):
        print("Error: Missing Twitter API credentials in environment variables.")
        print("Please set the following environment variables:")
        print("  TWITTER_API_KEY")
        print("  TWITTER_API_SECRET")
        print("  TWITTER_ACCESS_TOKEN")
        print("  TWITTER_ACCESS_TOKEN_SECRET")
        print("  TWITTER_BEARER_TOKEN")
        sys.exit(1)

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
    except Exception as e:
        print(f"Authentication failed: {e}")
        sys.exit(1)

def upload_media(api_key, api_secret, access_token, access_token_secret, image_path):
    """Upload image to Twitter and return media ID."""
    try:
        auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
        api = tweepy.API(auth)
        media = api.media_upload(image_path)
        return media.media_id_string
    except Exception as e:
        print(f"Failed to upload image: {e}")
        sys.exit(1)

def post_tweet(client, text, media_id=None):
    """Post a tweet with optional media."""
    try:
        if media_id:
            response = client.create_tweet(text=text, media_ids=[media_id])
        else:
            response = client.create_tweet(text=text)

        print(f"Tweet posted successfully! Tweet ID: {response.data['id']}")
        return True
    except Exception as e:
        print(f"Failed to post tweet: {e}")
        return False

def main():
    # Check for setup/test mode
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        print("Testing TermTweet setup...")
        # Load credentials to test
        try:
            api_key, api_secret, access_token, access_token_secret, bearer_token = load_credentials()
            print("✅ Credentials loaded successfully!")
            print("✅ TermTweet is properly configured.")
        except SystemExit:
            print("❌ Credentials not configured. Run 'python setup.py' to set up.")
            sys.exit(1)
        return

    if len(sys.argv) < 2:
        print("Usage: python tweet.py 'Your tweet text' [image_path]")
        print("Setup: python setup.py")
        sys.exit(1)

    tweet_text = sys.argv[1]
    image_path = sys.argv[2] if len(sys.argv) > 2 else None

    # Validate tweet length
    if len(tweet_text) > 280:
        print("Error: Tweet text exceeds 280 characters.")
        sys.exit(1)

    # Load credentials
    api_key, api_secret, access_token, access_token_secret, bearer_token = load_credentials()

    # Authenticate
    client = authenticate_twitter(api_key, api_secret, access_token, access_token_secret, bearer_token)

    # Handle image upload if provided
    media_id = None
    if image_path:
        if not os.path.exists(image_path):
            print(f"Error: Image file '{image_path}' not found.")
            sys.exit(1)
        media_id = upload_media(api_key, api_secret, access_token, access_token_secret, image_path)

    # Post the tweet
    success = post_tweet(client, tweet_text, media_id)
    if not success:
        print("Tweet posting failed. Please check your app permissions in the Twitter Developer Portal.")
        print("Make sure your app has 'Read and Write' permissions enabled.")
        sys.exit(1)

if __name__ == "__main__":
    main()