# Amazon Affiliate Post Generator

Automated tool that searches Amazon products using the Product Advertising API (PA-API), finds deals with significant discounts, and generates engaging Facebook posts using Google's Gemini LLM.

## Features

- Search Amazon products by keyword categories (Mobile, Computer, Audio, Smart Home, etc.)
- Filter products with minimum 20% discount
- Get product details including price, ratings, reviews, and deals
- Generate Facebook posts automatically using AI
- Fallback to browser scraping when PA-API is unavailable

## Prerequisites

- Python 3.12 or higher
- Amazon Associates account with PA-API access (requires 10 qualifying sales in 30 days)
- Google Gemini API key

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd ai-tasks
```

### 2. Install uv

```bash
# Install uv if you don't have it

# Linux/macOS:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows:
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 3. Install Amazon PA-API SDK

The official Amazon PA-API SDK is not available on PyPI and must be installed from GitHub:

```bash
# Download the SDK
git clone https://github.com/amzn/paapi5-python-sdk.git paapi5-python-sdk-temp
cd paapi5-python-sdk-temp/paapi5-python-sdk-example

# Install the SDK with uv
uv pip install .

cd ../..
rm -rf paapi5-python-sdk-temp
```

**Note:** The SDK folder structure is `paapi5-python-sdk/paapi5-python-sdk-example/` where the actual package is in the nested directory.

### 4. Install project dependencies

```bash
# Sync all dependencies from pyproject.toml
uv sync

# Or install in editable mode
uv pip install -e .
```

### 5. Configure environment variables

Copy the example environment file and add your credentials:

```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:

```env
# Google Gemini API Key
GOOGLE_API_KEY=your_google_api_key_here

# Amazon PA-API Credentials
PAAPI_ACCESS_KEY=your_access_key_here
PAAPI_SECRET_KEY=your_secret_key_here
PAAPI_PARTNER_TAG=your_partner_tag_here
```

#### Getting Amazon PA-API Credentials:

1. Sign in to [Amazon Associates Central](https://affiliate-program.amazon.com/)
2. Go to Tools → Product Advertising API
3. Click "Request API Access"
4. Download your credentials (Access Key and Secret Key)
5. Your Partner Tag is your Store ID (e.g., `yourstore-20`)

**Important:** PA-API requires 10 qualifying sales in the trailing 30 days to maintain API access. If you haven't met this threshold yet, the tool will automatically fall back to browser scraping.

#### Getting Google Gemini API Key:

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Create an API key
3. Copy the key to your `.env` file

## Usage

### Local Usage

Run the post generator locally:

```bash
uv run post
```

### GitHub Actions (Automated Daily Runs)

The project includes a GitHub Actions workflow that automatically generates posts once a day.

#### Setup GitHub Secrets

Add the following secrets to your GitHub repository (Settings → Secrets and variables → Actions → New repository secret):

- `GOOGLE_API_KEY` - Your Google Gemini API key
- `PAAPI_ACCESS_KEY` - Your Amazon PA-API access key
- `PAAPI_SECRET_KEY` - Your Amazon PA-API secret key
- `PAAPI_PARTNER_TAG` - Your Amazon Partner Tag (e.g., `yourstore-20`)

#### Workflow Features

- Runs automatically at 9:00 AM UTC daily (customize the cron schedule in `.github/workflows/run.yaml`)
- Can be triggered manually from GitHub Actions tab
- Caches PA-API SDK for faster runs
- Saves generated posts as artifacts (kept for 30 days)
- Posts output to workflow logs

#### Manual Trigger

1. Go to your repository on GitHub
2. Click "Actions" tab
3. Select "Daily Amazon Post Generator"
4. Click "Run workflow"

#### Customize Schedule

Edit `.github/workflows/run.yaml` to change the schedule:

```yaml
on:
  schedule:
    - cron: '0 9 * * *'  # 9 AM UTC daily
    # Examples:
    # - cron: '0 */6 * * *'  # Every 6 hours
    # - cron: '0 12 * * 1-5'  # Weekdays at noon
```

### How the Tool Works

The tool will:
1. Select a random product keyword from configured categories
2. Search Amazon for products with 20%+ discounts
3. Select the best deal
4. Generate an engaging Facebook post
5. Output the post to console

### Example Output

```
🔥 DEAL ALERT! 🔥

Save 35% on the Sony WH-1000XM5 Wireless Headphones!

✨ Industry-leading noise cancellation
🎵 30-hour battery life
💎 Premium sound quality
⭐ 4.7 stars (12,450 reviews)

Was: $399.99
Now: $259.99
YOU SAVE: $140.00!

Grab yours here: https://amazon.com/dp/B09XYZ...

#AmazonDeals #TechDeals #Headphones
```

## Project Structure

```
ai-tasks/
├── src/
│   ├── __init__.py
│   ├── main.py              # Main entry point
│   ├── keywords.py          # Product search keywords
│   ├── data/
│   │   └── amazon.py        # Amazon item data model
│   └── utils/
│       ├── browser.py       # Browser scraping fallback
│       ├── llm.py           # Gemini LLM integration
│       └── paapi.py         # PA-API integration
├── pyproject.toml           # Project configuration
├── .env                     # Environment variables (not in git)
├── .env.example             # Environment template
└── README.md                # This file
```

## Development

### Adding new product categories

Edit `src/keywords.py` and add your keywords to the appropriate list:

```python
mobile_keywords = [
    "smartphone",
    "phone case",
    # Add more...
]
```

### Customizing the discount threshold

In `src/main.py`, change the `min_discount_percentage` parameter:

```python
items = search_items_with_deals(
    keyword=random_keyword,
    min_discount_percentage=30,  # Change from 20 to 30
    item_count=10
)
```

### Modifying the LLM prompt

Edit the prompt in `src/utils/llm.py` in the `generate_facebook_post()` function.

## Troubleshooting

### PA-API returns "AssociateNotEligible" error

This means you haven't met the 10 qualifying sales requirement yet. The tool will automatically fall back to browser scraping until you reach this threshold.

### Module not found errors

Make sure you synced dependencies or installed in editable mode:
```bash
uv sync
# or
uv pip install -e .
```

### Browser scraping fails

Browser scraping requires Chrome/Chromium. The `browser-use` package will download it automatically on first run.

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]
