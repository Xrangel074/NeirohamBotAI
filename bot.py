import os
import anthropic
import telebot

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
ANTHROPIC_KEY  = os.environ["ANTHROPIC_KEY"]
ALLOWED_CHAT   = int(os.environ["ALLOWED_CHAT"])  # -5238995051

bot    = telebot.TeleBot(TELEGRAM_TOKEN)
client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

SYSTEM_PROMPT = """Ты грубый и дерзкий бот Minecraft клана. Отвечаешь коротко, по-русски, с матом и сарказмом как Нейрохам. Максимум 2-3 предложения."""

@bot.message_handler(func=lambda m: True)
def handle(message):
    # Только из нашей группы
    if message.chat.id != ALLOWED_CHAT:
        return

    text = message.text or ""

    # Игнорируем сообщения от ботов
    if message.from_user.is_bot:
        # Но если это наш Minecraft бот — отвечаем
        if "спрашивает:" not in text:
            return
        # Извлекаем вопрос: "nick спрашивает: текст"
        question = text.split("спрашивает:")[-1].strip()
    else:
        question = text

    if not question:
        return

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=200,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": question}]
        )
        answer = response.content[0].text
        bot.reply_to(message, answer)
    except Exception as e:
        print(f"Ошибка: {e}")

print("Бот запущен...")
bot.infinity_polling()
