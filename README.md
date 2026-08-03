# Setup Steps

1. Create GitHub repo, upload these files.
2. Repo Settings → Secrets and variables → Actions → add:
   - EXCHANGE_API_KEY
   - EXCHANGE_API_SECRET
   - TELEGRAM_BOT_TOKEN
   - TELEGRAM_CHAT_ID
3. Get Binance testnet keys: testnet.binance.vision
4. Create Telegram bot via @BotFather, get token.
5. Get chat_id: message your bot, visit
   https://api.telegram.org/bot<TOKEN>/getUpdates
6. Actions tab → enable workflows → run "crypto-bot" manually once to test.
7. Runs automatically every 4h after that.
8. To pause: edit state/positions.json, set "enabled": false, commit.
9. Monitor via Telegram messages on phone.

Switch testnet to live: config.yaml → testnet: false, use real API keys.
