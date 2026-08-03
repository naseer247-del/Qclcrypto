name: crypto-bot

on:
  schedule:
    - cron: "5 */4 * * *"
  workflow_dispatch:

permissions:
  contents: write

jobs:
  run-bot:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - run: pip install -r requirements.txt

      - name: Run bot
        env:
          EXCHANGE_API_KEY: ${{ secrets.EXCHANGE_API_KEY }}
          EXCHANGE_API_SECRET: ${{ secrets.EXCHANGE_API_SECRET }}
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        working-directory: bot
        run: python main.py

      - name: Commit state
        run: |
          git config user.name "trading-bot"
          git config user.email "bot@users.noreply.github.com"
          git add state/
          git diff --cached --quiet || git commit -m "update state [skip ci]"
          git push
