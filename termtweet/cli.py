#!/usr/bin/env python3
"""
TermTweet CLI - Command Line Interface for tweeting from terminal
"""

import os
import sys
import argparse
from pathlib import Path

# Add parent directory to path so we can import termtweet modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from termtweet.core import tweet, setup_credentials, test_credentials

def create_parser():
    """Create argument parser for CLI."""
    parser = argparse.ArgumentParser(
        description="Tweet from your terminal - TermTweet",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  termtweet "Hello from terminal! #coding"
  termtweet "Check this out!" --image screenshot.png
  termtweet --setup
  termtweet --test
        """
    )

    parser.add_argument(
        'text',
        nargs='?',
        help='Text to tweet (280 characters max)'
    )

    parser.add_argument(
        '--image', '-i',
        type=str,
        help='Path to image file to attach'
    )

    parser.add_argument(
        '--setup', '-s',
        action='store_true',
        help='Run interactive setup to configure credentials'
    )

    parser.add_argument(
        '--test', '-t',
        action='store_true',
        help='Test if credentials are configured correctly'
    )

    parser.add_argument(
        '--version', '-v',
        action='version',
        version='TermTweet 1.0.0'
    )

    return parser

def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # Handle setup mode
    if args.setup:
        print("=== TermTweet Setup ===")
        success = setup_credentials()
        if success:
            print("✅ Setup completed successfully!")
            print("You can now use 'termtweet \"Your message\"' to post tweets.")
        else:
            print("❌ Setup failed. Please try again.")
            sys.exit(1)
        return

    # Handle test mode
    if args.test:
        print("Testing TermTweet configuration...")
        success = test_credentials()
        if success:
            print("TermTweet is properly configured!")
        else:
            print("Configuration test failed.")
            print("Run 'termtweet --setup' to configure your credentials.")
            sys.exit(1)
        return

    # Handle tweet mode
    if not args.text:
        parser.print_help()
        return

    # Validate tweet length
    if len(args.text) > 280:
        print(f"Tweet text is {len(args.text)} characters long. Maximum is 280 characters.")
        sys.exit(1)

    # Validate image if provided
    if args.image:
        if not os.path.exists(args.image):
            print(f"Image file '{args.image}' not found.")
            sys.exit(1)

    # Post the tweet
    success = tweet(args.text, args.image)
    if success:
        print("Tweet posted successfully!")
    else:
        print("Failed to post tweet.")
        print("Make sure your credentials are correct and your app has 'Read and Write' permissions.")
        sys.exit(1)

if __name__ == "__main__":
    main()