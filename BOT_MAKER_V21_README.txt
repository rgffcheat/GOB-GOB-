BOT MAKER INTEGRATION — RGG BOT v21

WHAT CHANGED
- The existing reseller website features and main wallet remain in place.
- Bot Maker now deploys the complete multi-file RGG Bot v21 package (not only a single main.py).
- Each reseller bot runs in its own process and has its own SQLite database under DATA_DIR/bot_instances/<id>/.
- Resellers pay for a plan from their existing website wallet. If bot creation fails after wallet deduction, the wallet amount is refunded.
- Website Admin > Bots > Bot Plans lets the admin create, edit, activate/deactivate, and delete plans (custom name, duration in days, and price).
- Starter examples (1 Day, 3 Days, 1 Month) are intentionally OFF and have zero price until the admin configures them.
- Subscription expiry stops the bot automatically. Its database is retained.
- Resellers get a separate Bot Admin Panel link and generated login credentials. The website proxy restricts the panel to that reseller and the website administrator.
- Website Admin > Bots > Bot Plans stores the Telegram backup Chat ID and interval. All bot databases are packaged into a ZIP and sent using the website Telegram bot token at the selected interval. Manual single-bot and all-bot backups also download a ZIP and send it to that Chat ID.
- Restore is available from Website Admin > Bots. A single-bot ZIP can be restored through that bot's database restore upload; the all-bot ZIP uses Restore.
- The existing Bot Maker global ON/OFF and per-reseller access controls remain active.

DEPLOYMENT NOTES
- Deploy with the project's requirements.txt. RGG Bot v21 requires Waitress and Segno; both are included.
- Keep the website's Telegram bot token configured. The central backup feature uses that token to send backup ZIPs to the configured Chat ID.
- Keep DATA_DIR on persistent storage where the hosting provider supports it. If the provider wipes local disk on redeploy, restore the latest all-bot ZIP from the configured Telegram chat using Website Admin > Bots > Restore.
- Backup ZIPs contain bot API tokens, panel passwords, and customer databases. Keep the configured Telegram chat private.
- Subscription purchase currently uses the existing reseller wallet balance.

TEST STATUS
- All Python source files passed Python bytecode compilation. Runtime integration could not be executed in this build environment because its Python dependencies were not preinstalled and outbound package installation was unavailable.
