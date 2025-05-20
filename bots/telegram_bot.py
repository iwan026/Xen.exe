from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from core.analisis import AnalisisSymbol
from config import BOT_TOKEN, SYMBOLS
from logs.logger import setup_logging

logger = setup_logging()


class TelegramBot:
    def __init__(self):
        self.analisis_symbol = AnalisisSymbol()
        self.app = ApplicationBuilder().token(BOT_TOKEN).build()
        self.setup_handler()

    def setup_handler(self):
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("analisa", self.analisa_command))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        start_message = (
            "✨Halo, aku adalah *XenBot* 🤖, asistenmu untuk analisis forex berbasis *rule-based* yang bakal bantu kamu mencari setup entry terbaik: \n\n"
            "🛠 *Fitur yang tersedia:*\n"
            "✅ `/analisa` - Cek sinyal terbaru\n"
            "✅ `/settings` - Atur preferensi\n"
            "✅ `/help` - Panduan penggunaan\n\n"
            "🔥 *Jangan trading pakai feeling, pakai XenBot aja!*"
        )
        await update.message.reply_text(start_message, parse_mode="Markdown")

    async def analisa_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            args = context.args
            if len(args) != 2:
                await update.message.reply_text(
                    "Gunakan: /analisa [PAIR]\nContoh: /analisa EURUSD"
                )
                return None

            symbol = args[0].upper()
            timeframe = args[1].upper()
            if symbol not in SYMBOLS:
                await update.message.reply_text(
                    f"Yaah maaf, saya belum dilatih untuk menganalisa {symbol}"
                )
                return None

            processing_msg = await update.message.reply_text("⏳ Menganalisa...")
            try:
                result = self.analisis_symbol.get_analisis(symbol, timeframe)

                analisis_msg = f"🔄 **Hasil Analisa XenBot** 🔄\n{result['analisis']}"
                with open[result["chart_path"], "rb"] as chart_file:
                    await update.message.reply_photo(
                        photo=chart_file, caption=analisis_msg, parse_mode="Markdown"
                    )
                await processing_msg.delete()
            except Exception as e:
                await processing_msg.edit_text(f"❌ Analisa error: {e}")
                logger.error(f"❌ Analisa error: {e}")

        except Exception as e:
            logger.error(f"Gagal menganalisa simbol: {e}")
            await update.message.reply_text(f"❌ Analisa gagal: {e}")

    def run(self):
        self.app.run_polling()
