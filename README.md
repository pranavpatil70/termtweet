# TermTweet

A simple, powerful Python script to tweet directly from your terminal or IDE. Perfect for developers who want to share code updates, project milestones, or quick thoughts while working on their projects.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

## ✨ Features

- 🚀 **Tweet from terminal** - Post text tweets directly from command line
- 📸 **Image support** - Attach images by providing file path (PNG/JPG/GIF, max 5MB)
- 🔐 **Secure authentication** - Environment variables keep credentials safe
- ⚡ **Easy setup** - Interactive setup script guides you through configuration
- 🛠️ **Developer-friendly** - Works from any directory, perfect for coding sessions
- 📝 **Input validation** - Automatic tweet length checking (280 chars max)
- 🧪 **Dry run mode** - Test tweets without actually posting
- 🔧 **Flexible credentials** - Support for .env files or environment variables
- 📊 **Detailed feedback** - Clear success/error messages with emojis
- 🐛 **Comprehensive testing** - Built-in credential validation

## 📋 Prerequisites

- Python 3.8 or higher
- Twitter Developer Account with API v2 access
- pip package manager
- Terminal/Command Prompt access

## 🚀 Installation

### Option 1: Install from PyPI (Recommended)

```bash
# Install globally (like npm install -g)
pip install termtweet

# Run setup
termtweet --setup
```

### Option 2: Install from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/termtweet.git
cd termtweet

# Install in development mode
pip install -e .

# Run setup
termtweet --setup
```

### Option 3: Manual Setup (Advanced)

```bash
# Clone and install dependencies
git clone https://github.com/yourusername/termtweet.git
cd termtweet
pip install -r requirements.txt

# Configure credentials manually
cp .env.example .env
# Edit .env with your Twitter API credentials
```

## 📖 Usage

### Basic tweet:
```bash
termtweet "Hello from the terminal! #coding"
```

### Tweet with image:
```bash
termtweet "Check out this cool screenshot!" --image ./screenshot.png
```

### Short options:
```bash
termtweet "Quick tweet!" -i image.png
```

### Test your setup (dry run - no actual tweet):
```bash
termtweet "Test message" --dry-run
```

### Test your setup:
```bash
termtweet --test
```

### Run setup:
```bash
termtweet --setup
```

### Get help:
```bash
termtweet --help
```

## 💡 Examples

```bash
# Share coding progress
termtweet "Just implemented a new feature! 🚀 #programming"

# Post with screenshot
termtweet "Here's my app's new UI:" --image ./screenshots/new_ui.png

# Quick updates
termtweet "Pushed to GitHub. Time for coffee! ☕ #devlife"

# During development
termtweet "Fixed that pesky bug! Now onto the next challenge 🎯"

# From any project directory
termtweet "Working on something awesome!" -i screenshot.png

# Test without posting (dry run)
termtweet "This won't actually post" --dry-run

# Multi-line tweets (use quotes)
termtweet "Working on an exciting project!
Can't wait to share more details soon! 🚀"
```

## 🔧 Twitter API Setup

### Step 1: Create Twitter Developer Account
1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Sign up for a developer account if you don't have one
3. Create a new project/app or use an existing one

### Step 2: Configure App Permissions (CRITICAL)
**This is the most important step - without it, tweets will fail!**

1. In your app settings, go to **"App permissions"**
2. Change permissions from **"Read"** to **"Read and write"**
3. Change **"Type of App"** to **"Web App, Automated App or Bot"**
4. Fill in the required **"App info"**:
   - **Callback URI / Redirect URL**: `http://localhost`
   - **Website URL**: Your website or `https://github.com/yourusername`
   - **Organization name**: Your name or project name (optional)

### Step 3: Generate API Tokens
1. Go to **"Keys and tokens"** section
2. Generate/copy these credentials:
   - **API Key** (Consumer Key)
   - **API Secret** (Consumer Secret)
   - **Access Token**
   - **Access Token Secret**
   - **Bearer Token**

### Step 4: Configure TermTweet
Use the interactive setup:
```bash
termtweet --setup
```

Or manually create `~/.termtweet/.env` with:
```bash
# Create directory and file
mkdir -p ~/.termtweet
nano ~/.termtweet/.env  # or use your preferred editor
```

File contents:
```
# Twitter API Credentials
# Get these from https://developer.twitter.com/en/portal/dashboard
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here
```

**Alternative: Environment Variables**
You can also set credentials using environment variables (overrides .env file):
```bash
export TWITTER_API_KEY="your_key"
export TWITTER_API_SECRET="your_secret"
export TWITTER_ACCESS_TOKEN="your_token"
export TWITTER_ACCESS_TOKEN_SECRET="your_token_secret"
export TWITTER_BEARER_TOKEN="your_bearer"
```

### Step 5: Test Your Setup
```bash
termtweet --test
termtweet "Hello World! #TermTweet"
```

### ⚠️ Common Issues & Solutions

| Problem | Solution |
|---------|----------|
| "403 Forbidden" | Change app permissions to "Read and write" |
| "Authentication failed" | Regenerate tokens after permission change |
| "Missing credentials" | Run `termtweet --setup` |
| "Tweet too long" | Keep under 280 characters |
| "Command not found" | Use `python -m termtweet` or ensure PATH includes pip install location |
| "Module not found" | Install with `pip install termtweet` |
| "Image upload failed" | Check file exists and is valid image format (PNG/JPG) |
| "Rate limited" | Twitter API has rate limits; wait before retrying |

## 🔒 Security & Best Practices

- **Never commit** `.env` files to version control
- Keep API credentials secure and private
- Regenerate tokens if compromised
- Use environment variables for sensitive data
- Test with `--dry-run` before posting important tweets
- Use strong, unique passwords for your Twitter account
- Enable 2FA on your Twitter developer account
- Regularly rotate API tokens (recommended every 6 months)

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Missing Twitter API credentials" | Run `termtweet --setup` or check `~/.termtweet/.env` file |
| "403 Forbidden" | Ensure app has "Read and Write" permissions |
| "Authentication failed" | Verify all credentials in `.env` are correct |
| "Image file not found" | Check image path and ensure file exists |
| "Tweet too long" | Keep tweets under 280 characters |
| "Command not found" | Use `python -m termtweet` or add pip install location to PATH |
| "Module not found" | Install with `pip install termtweet` |
| "Rate limited" | Twitter API has rate limits; wait 15 minutes before retrying |
| "Invalid image format" | Use PNG, JPG, or GIF files under 5MB |
| "Setup failed" | Check file permissions for `~/.termtweet/` directory |

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly (`python -m pytest tests/`)
5. Update documentation if needed
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Submit a pull request

### Development Setup

```bash
# Clone and setup for development
git clone https://github.com/yourusername/termtweet.git
cd termtweet
pip install -e .[dev]  # Install with development dependencies
pip install pytest     # For running tests

# Run tests
python -m pytest tests/

# Test CLI
python -c "from termtweet.cli import main; import sys; sys.argv = ['termtweet', '--help']; main()"
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Tweepy](https://www.tweepy.org/) - Python Twitter API library
- Inspired by developers who tweet from the terminal
- Thanks to the open-source community for making development tools accessible

## 📈 Roadmap

- [ ] Thread support (multi-tweet threads)
- [ ] Scheduled tweets
- [ ] Tweet drafts
- [ ] Integration with Git hooks
- [ ] Support for polls
- [ ] Tweet analytics
- [ ] Multiple account profiles

---

**Happy tweeting from your terminal! 🐦✨**

---

**Happy tweeting from your terminal! 🐦**