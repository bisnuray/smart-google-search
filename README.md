<h1 align="center">🔍 Smart Google Search Telegram Bot 🤖</h1>

<p align="center">
  <em>Smart Google Search is a cutting-edge Telegram bot that leverages the power of Google's Custom Search API to deliver swift and precise search results directly within Telegram. Dive into textual content or explore images, all in one place. </em>
</p>

<hr>

## 🌟 Features

- 🌐 Instant access to Google's vast world of information.
- 🖼️ Explore visual content with the Image Search feature.
- 🕐 Efficient cooldown mechanism to ensure fair usage.
- 🎛️ Intuitive navigation through the search results.
- 👑 Admin privileges for overriding limitations.

## 🚀 Getting Started

### Prerequisites

- Python 3.6 or higher.
- Libraries: aiogram, requests.
- A Telegram bot token.
- Google API Key and Custom Search Engine ID.

### How to obtain the Google API Key and Custom Search Engine ID:

1. **Google API Key**:
   - Visit the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project.
   - Navigate to `Credentials` and click on `Create Credentials`. Select `API Key` from the dropdown. Your new API key will appear. Copy and save it securely.

2. **Google Custom Search Engine ID**:
   - Go to [Google Custom Search](https://cse.google.com/cse/).
   - Click on `New Search Engine` and fill out the form to create a custom search engine. Under 'Sites to Search', you can use `www.google.com` to search the entire web.
   - After creating, the Custom Search Engine ID (`cx` value) will be visible in the 'Basics' tab. Copy this ID.

### Installation

1. Clone the repository:
git clone https://github.com/yourusername/Smart-Google-Search.git

2. Change the working directory:
cd Smart-Google-Search

3. Update the `main.py` file with your [Telegram bot token], [Google API Key], and [Custom Search Engine ID].

4. Run the bot:
python main.py


## 📚 Usage

1. Start a chat with your bot on Telegram.
2. To search for text: `/search <query>`.
3. To search for images: `/image <query>`.
4. The bot will promptly display the results.

## Author

- Name: Bisnu Ray
- Telegram: [@SmartBisnuBio](https://t.me/SmartBisnuBio)

Feel free to reach out if you have any questions or feedback.

Please note that the README assumes you have created a Telegram bot and obtained the API token from the BotFather. Additionally, it provides instructions on how to install and run the bot. You may need to update the installation and execution steps if necessary.


