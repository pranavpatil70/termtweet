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
    # Priority order: environment variables > ~/.termtweet/.env > current directory .env
    # This allows overriding with env vars for CI/CD or different profiles

    # First, try loading from user's home directory
    env_file = Path.home() / '.termtweet' / '.env'
    if env_file.exists():
        load_dotenv(env_file)
    else:
        # Fallback to current directory
        load_dotenv()

    # Allow environment variables to override file values
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
        print("❌ No credentials found. Run 'termtweet --setup' to configure.")
        return False

    api_key, api_secret, access_token, access_token_secret, bearer_token = creds

    # Authenticate
    client = authenticate_twitter(api_key, api_secret, access_token, access_token_secret, bearer_token)
    if not client:
        print("❌ Authentication failed. Check your credentials.")
        return False

    # Handle image upload if provided
    media_id = None
    if image_path:
        print(f"📤 Uploading image: {image_path}")
        media_id = upload_media(api_key, api_secret, access_token, access_token_secret, image_path)
        if not media_id:
            print("❌ Failed to upload image.")
            return False
        print("✅ Image uploaded successfully!")

    # Post the tweet
    print("Posting tweet...")
    tweet_id = post_tweet(client, text, media_id)
    if tweet_id:
        print("Tweet posted successfully!")
        return True
    else:
        print("Failed to post tweet.")
        return False

def setup_credentials():
    """Interactive setup for credentials."""
    print("🔧 Let's set up your Twitter API credentials.")
    print("📋 Get these from: https://developer.twitter.com/en/portal/dashboard")
    print("⚠️  Make sure your app has 'Read and Write' permissions!")
    print()

    # Get credentials from user
    api_key = input("🔑 Enter your Twitter API Key: ").strip()
    api_secret = input("🔐 Enter your Twitter API Secret: ").strip()
    access_token = input("🎫 Enter your Access Token: ").strip()
    access_token_secret = input("🔑 Enter your Access Token Secret: ").strip()
    bearer_token = input("🪙 Enter your Bearer Token: ").strip()

    # Validate inputs
    if not all([api_key, api_secret, access_token, access_token_secret, bearer_token]):
        print("❌ All fields are required!")
        return False

    # Basic format validation
    if not api_key.startswith(('AA', 'BB', 'CC', 'DD')):
        print("⚠️  Warning: API Key should typically start with AA, BB, CC, or DD")
    if len(api_key) != 25 or len(api_secret) != 50:
        print("⚠️  Warning: API Key should be 25 chars, API Secret should be 50 chars")
    if not access_token.startswith(('1', '2')):
        print("⚠️  Warning: Access Token should typically start with 1 or 2")

    # Create .env content
    env_content = f"""# Twitter API Credentials
# Get these from https://developer.twitter.com/en/portal/dashboard
# IMPORTANT: Keep this file secure and never commit to version control
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
        print("🧪 Run 'termtweet --test' to verify your setup!")
        return True
    except Exception as e:
        print(f"❌ Error saving credentials: {e}")
        return False

def test_credentials():
    """Test if credentials are configured correctly."""
    print("Testing TermTweet configuration...")

    creds = load_credentials()
    if not creds:
        print("No credentials found. Run 'termtweet --setup' to configure.")
        return False

    api_key, api_secret, access_token, access_token_secret, bearer_token = creds

    # Check credential format
    issues = []
    if not api_key.startswith(('AA', 'BB', 'CC', 'DD')):
        issues.append("API Key format looks unusual")
    if len(api_key) != 25:
        issues.append("API Key length is {}, should be 25".format(len(api_key)))
    if len(api_secret) != 50:
        issues.append("API Secret length is {}, should be 50".format(len(api_secret)))

    if issues:
        print("Credential format warnings:")
        for issue in issues:
            print("   - {}".format(issue))

    print("Testing Twitter API connection...")
    client = authenticate_twitter(api_key, api_secret, access_token, access_token_secret, bearer_token)

    if client is None:
        print("Authentication failed. Check your credentials and app permissions.")
        print("Make sure your Twitter app has 'Read and Write' permissions.")
        return False

    print("Authentication successful!")
    print("TermTweet is ready to use!")
    return True