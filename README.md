1. Repo Settings → Secrets and variables → Actions → add:
   EXCHANGE_API_KEY, EXCHANGE_API_SECRET, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
2. Get Binance testnet keys: testnet.binance.vision
3. Create Telegram bot via @BotFather, get token.
4. Get chat_id: message bot, visit https://api.telegram.org/bot<TOKEN>/getUpdates
5. Actions tab → enable workflows → run "crypto-bot" manually to test.
6. Runs every 4h automatically after.
7. To pause: edit state/positions.json, set "enabled": false, commit.
