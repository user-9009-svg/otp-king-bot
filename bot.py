import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

wallets = {}

def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("🇮🇳 Indian Numbers", callback_data="numbers"),
            InlineKeyboardButton("💰 Wallet", callback_data="wallet"),
        ],
        [
            InlineKeyboardButton("➕ Recharge", callback_data="recharge"),
            InlineKeyboardButton("📋 Orders", callback_data="orders"),
        ],
        [
            InlineKeyboardButton("📩 My SMS", callback_data="sms"),
            InlineKeyboardButton("👤 Profile", callback_data="profile"),
        ],
        [
            InlineKeyboardButton("🆘 Support", callback_data="support")
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in wallets:
        wallets[user_id] = 0.0

    await update.message.reply_text(
        "👑 *WELCOME TO OTP KING*\n\n"
        "🇮🇳 Indian marketplace\n"
        "💰 Secure wallet system\n"
        "⚡ Fast service\n\n"
        f"Wallet Balance: ₹{wallets[user_id]:.2f}",
        reply_markup=main_menu(),
        parse_mode="Markdown",
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    balance = wallets.get(user_id, 0.0)

    if query.data == "wallet":
        await query.edit_message_text(
            f"💰 *Your Wallet*\n\n"
            f"Balance: ₹{balance:.2f}\n\n"
            "Use Recharge to add balance after payment verification.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Recharge", callback_data="recharge")],
                [InlineKeyboardButton("⬅️ Main Menu", callback_data="home")]
            ]),
            parse_mode="Markdown"
        )

    elif query.data == "recharge":
        keyboard = [
            [
                InlineKeyboardButton("₹50", callback_data="recharge_50"),
                InlineKeyboardButton("₹100", callback_data="recharge_100"),
            ],
            [
                InlineKeyboardButton("₹250", callback_data="recharge_250"),
                InlineKeyboardButton("₹500", callback_data="recharge_500"),
            ],
            [
                InlineKeyboardButton("₹1000", callback_data="recharge_1000"),
            ],
            [InlineKeyboardButton("⬅️ Main Menu", callback_data="home")]
        ]

        await query.edit_message_text(
            "➕ *Recharge Wallet*\n\n"
            "Select an amount.\n\n"
            "Payment will remain *pending* until an admin verifies it.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif query.data.startswith("recharge_"):
        amount = query.data.replace("recharge_", "")

        await query.edit_message_text(
            f"💳 *Recharge Request: ₹{amount}*\n\n"
            "The payment/UPI details will be configured by the admin.\n\n"
            "After payment, submit the UTR/transaction ID for manual verification.\n\n"
            "⚠️ Balance is NOT added automatically.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Recharge", callback_data="recharge")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="home")]
            ]),
            parse_mode="Markdown"
        )

    elif query.data == "numbers":
        await query.edit_message_text(
            "🇮🇳 *Indian Numbers*\n\n"
            "Number inventory will be connected only after the authorized "
            "backend/device data structure is configured.\n\n"
            "No real numbers are available in this demo.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Main Menu", callback_data="home")]
            ]),
            parse_mode="Markdown"
        )

    elif query.data == "orders":
        await query.edit_message_text(
            "📋 *My Orders*\n\nNo orders yet.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Main Menu", callback_data="home")]
            ]),
            parse_mode="Markdown"
        )

    elif query.data == "sms":
        await query.edit_message_text(
            "📩 *My SMS*\n\n"
            "SMS inbox will be connected later to your authorized devices.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Main Menu", callback_data="home")]
            ]),
            parse_mode="Markdown"
        )

    elif query.data == "profile":
        await query.edit_message_text(
            f"👤 *Profile*\n\n"
            f"Telegram ID: `{user_id}`\n"
            f"Wallet: ₹{balance:.2f}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Main Menu", callback_data="home")]
            ]),
            parse_mode="Markdown"
        )

    elif query.data == "support":
        await query.edit_message_text(
            "🆘 *Support*\n\nPlease contact the OTP KING administrator.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Main Menu", callback_data="home")]
            ]),
            parse_mode="Markdown"
        )

    elif query.data == "home":
        await query.edit_message_text(
            "👑 *OTP KING*\n\nChoose an option:",
            reply_markup=main_menu(),
            parse_mode="Markdown"
        )


def run():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is missing.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    print("OTP KING bot is running...")
    app.run_polling()


if __name__ == "__main__":
    run()
