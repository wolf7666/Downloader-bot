import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import yt_dlp
import logging
from flask import Flask # Yeh UptimeRobot ke liye zaroori hai

# --- Flask Web Server (Bot ko zinda rakhne ke liye) ---
app = Flask(__name__)
@app.route('/')
def home():
    return "I'm alive!"
    # --------------------------------------------------------

    # Logging setup
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Bot token ko Environment Variable se lena hai
    BOT_TOKEN = os.environ.get('BOT_TOKEN')

    def start(update, context):
        user = update.effective_user
            update.message.reply_html(f"Hi {user.mention_html()}! Bas video ka link bhejein.")

            def handle_link(update, context):
                chat_id = update.message.chat_id
                    link = update.message.text
                        message = context.bot.send_message(chat_id=chat_id, text="🔗 Download shuru kar raha hu...")
                            
                                # Baaki ka download logic bilkul same rahega...
                                    ydl_opts = {
                                            'outtmpl': f'{chat_id}_%(id)s.%(ext)s',
                                                    'format': 'best[ext=mp4][height<=720]/best[ext=mp4]/best',
                                                            'max_filesize': 50 * 1024 * 1024,
                                                                    'noplaylist': True,
                                                                        }
                                                                            try:
                                                                                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                                                                                                info = ydl.extract_info(link, download=True)
                                                                                                            filename = ydl.prepare_filename(info)
                                                                                                                        context.bot.send_message(chat_id=chat_id, text="✅ Download poora! Ab bhej raha hu...")
                                                                                                                                    with open(filename, 'rb') as video_file:
                                                                                                                                                    context.bot.send_video(chat_id=chat_id, video=video_file, caption=info.get('title', 'Downloaded Video'))
                                                                                                                                                                os.remove(filename)
                                                                                                                                                                            context.bot.delete_message(chat_id=chat_id, message_id=message.message_id)
                                                                                                                                                                                except Exception as e:
                                                                                                                                                                                        error_message = str(e)
                                                                                                                                                                                                if "File is larger than the configured maximum" in error_message:
                                                                                                                                                                                                            reply_text = "❌ Error: Video 50 MB se bada hai."
                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                reply_text = "❌ Error: Download nahi kar paaya."
                                                                                                                                                                                                                                        logging.error(f"Error for link {link}: {e}")
                                                                                                                                                                                                                                                context.bot.edit_message_text(text=reply_text, chat_id=chat_id, message_id=message.message_id)
                                                                                                                                                                                                                                                        if 'filename' in locals() and os.path.exists(filename):
                                                                                                                                                                                                                                                                    os.remove(filename)

                                                                                                                                                                                                                                                                    def run_web_server():
                                                                                                                                                                                                                                                                        # Web server alag se chalaana
                                                                                                                                                                                                                                                                            app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

                                                                                                                                                                                                                                                                            if __name__ == "__main__":
                                                                                                                                                                                                                                                                                if BOT_TOKEN:
                                                                                                                                                                                                                                                                                        # Start the Flask web server in a background thread if needed by the hosting
                                                                                                                                                                                                                                                                                                # For Render, the start command will run this script, so we don't need a separate thread
                                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                                updater = Updater(BOT_TOKEN, use_context=True)
                                                                                                                                                                                                                                                                                                                        dp = updater.dispatcher
                                                                                                                                                                                                                                                                                                                                dp.add_handler(CommandHandler("start", start))
                                                                                                                                                                                                                                                                                                                                        dp.add_handler(MessageHandler(Filters.regex(r'^(http|https)'), handle_link))
                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                        logging.info("🤖 Bot polling shuru kar raha hai...")
                                                                                                                                                                                                                                                                                                                                                                updater.start_polling()
                                                                                                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                                                                                                # Web server ko chalaayein taaki UptimeRobot use ping kar sake
                                                                                                                                                                                                                                                                                                                                                                                        run_web_server()
                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                        updater.idle()
                                                                                                                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                                                                                                                    logging.error("BOT_TOKEN nahi mila! Kripya environment variable set karein.")