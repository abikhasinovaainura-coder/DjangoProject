from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Category, Medicine, Order, OrderItem
from django.db.models import Q
import json

TRANSLATIONS = {
    'kk': {
        'title': 'PharmOnline - Онлайн Дәріхана',
        'catalog': 'Каталог',
        'stock': 'Қойма қоры',
        'about': 'Біз туралы',
        'whatsapp': 'Жедел байланыс',
        'cart': 'Себет',
        'my_orders': 'Менің тапсырыстарым',
        'search_placeholder': 'Дәрілерді іздеу...',
        'all_categories': 'Барлық санаттар',
        'stock_count': 'Қоймада',
        'add_to_cart': 'Себетке қосу',
        'out_of_stock': 'Тауар жоқ',
        'chat_title': 'Фармацевт-Көмекші',
        'bot_welcome': 'Сәлеметсіз бе! Мен онлайн-дәріхананың көмекшімін. Сізге қандай дәрі керек?',
        'chat_placeholder': 'Сұрағыңызды жазыңыз...',
        'send': 'Жіберу',
        'ask_question': 'Сұрақ қою',
        'checkout': 'Тапсырыс беру',
        'empty_cart': 'Себетіңіз бос',
        'total': 'Барлығы:',
        # "Біз туралы" бетінің аудармалары
        'about_title': 'PharmOnline туралы',
        'about_subtitle': 'Сіздің сенімді онлайн дәріханаңыз',
        'about_desc': 'PharmOnline — бұл сапалы дәрі-дәрмекті, медициналық бұйымдарды және витаминдерді үйден шықпай-ақ қолжетімді бағамен сатып алуға мүмкіндік беретін заманауи онлайн платформа.',
        'our_mission': 'Біздің мақсатымыз',
        'mission_text': 'Әрбір азаматқа қажетті дәрі-дәрмекті жылдам, қауіпсіз және ыңғайлы түрде жеткізу, денсаулықты сақтауды әркім үшін оңай ету.',
        'why_us': 'Неліктен бізді таңдайды?',
        'feature_1': 'Тек түпнұсқа және сапалы дәрілер',
        'feature_2': 'Kaspi QR және Kaspi Перевод арқылы оңай төлем',
        'feature_3': 'Жедел жеткізу қызметі',
        'feature_4': 'Білікті фармацевттердің онлайн көмегі',
        'contact_info': 'Байланыс ақпараты:',
        'phone_label': 'Телефон:',
        'email_label': 'Email:',
        'address_label': 'Мекенжай:',
        'address_val': 'Төле би көшесі 64, Тараз қаласы',
        # Чат-бот қосымша сөздері
        'chat_empty': 'Сұрағыңызды жазыңызшы.',
        'chat_thanks': 'Оқасы жоқ! Денсаулығыңызға мықтылық тілейміз! Көмек керек болса хабарласыңыз.',
        'chat_price_info': 'Барлық дәрілердің бағасын жоғарғы мәзірдегі «Каталог» бөлімінен көре аласыз!',
        'chat_contact': 'Біздің жедел байланыс және WhatsApp нөміріміз: +7 (705) 887-33-07',
        'chat_default': 'Бұл сұрақ бойынша нақты ақпарат таппадым. Толық ақпарат алу немесе тапсырыс беру үшін WhatsApp арқылы хабарласыңыз: +7 (705) 887-33-07',
        'in_stock': 'Қоймада бар',
        'out_stock': 'Қоймада жоқ',
        'no_desc': 'Сипаттамасы жоқ.',
        'price': 'Бағасы',
        'status': 'Күйі',
        'desc': 'Сипаттамасы'
    },
    'ru': {
        'title': 'PharmOnline - Онлайн Аптека',
        'catalog': 'Каталог',
        'stock': 'Запасы склада',
        'about': 'О нас',
        'whatsapp': 'Связь в WhatsApp',
        'cart': 'Корзина',
        'my_orders': 'Мои заказы',
        'search_placeholder': 'Поиск лекарств...',
        'all_categories': 'Все категории',
        'stock_count': 'В наличии',
        'add_to_cart': 'В корзину',
        'out_of_stock': 'Нет в наличии',
        'chat_title': 'Фармацевт-Помощник',
        'bot_welcome': 'Здравствуйте! Я помощник онлайн-аптеки. Какое лекарство вам нужно?',
        'chat_placeholder': 'Напишите свой вопрос...',
        'send': 'Отправить',
        'ask_question': 'Задать вопрос',
        'checkout': 'Оформить заказ',
        'empty_cart': 'Ваша корзина пуста',
        'total': 'Итого:',
        # Переводы для страницы "О нас"
        'about_title': 'О PharmOnline',
        'about_subtitle': 'Ваша надежная онлайн-аптека',
        'about_desc': 'PharmOnline — это современная онлайн-платформа, позволяющая покупать качественные лекарства, медицинские изделия и витамины по доступным ценам, не выходя из дома.',
        'our_mission': 'Наша миссия',
        'mission_text': 'Быстро, безопасно и удобно доставлять необходимые лекарства каждому гражданину, делая заботу о здоровье доступной для всех.',
        'why_us': 'Почему выбирают нас?',
        'feature_1': 'Только оригинальные и качественные лекарства',
        'feature_2': 'Легкая оплата через Kaspi QR и Kaspi Перевод',
        'feature_3': 'Служба экспресс-доставки',
        'feature_4': 'Онлайн-помощь квалифицированных фармацевтов',
        'contact_info': 'Контактная информация:',
        'phone_label': 'Телефон:',
        'email_label': 'Email:',
        'address_label': 'Адрес:',
        'address_val': 'улица Толе би 64, город Тараз',
        # Дополнительные ответы чат-бота
        'chat_empty': 'Пожалуйста, напишите свой вопрос.',
        'chat_thanks': 'Пожалуйста! Желаем крепкого здоровья! Обращайтесь, если понадобится помощь.',
        'chat_price_info': 'Вы можете посмотреть цены на все лекарства в разделе «Каталог» в верхнем меню!',
        'chat_contact': 'Наш номер телефона и WhatsApp для связи: +7 (705) 887-33-07',
        'chat_default': 'К сожалению, я не нашел точной информации по вашему запросу. Для получения подробной информации или заказа свяжитесь через WhatsApp: +7 (705) 887-33-07',
        'in_stock': 'В наличии',
        'out_stock': 'Нет в наличии',
        'no_desc': 'Нет описания.',
        'price': 'Цена',
        'status': 'Статус',
        'desc': 'Описание'
    },
    'en': {
        'title': 'PharmOnline - Online Pharmacy',
        'catalog': 'Catalog',
        'stock': 'Stock',
        'about': 'About Us',
        'whatsapp': 'WhatsApp',
        'cart': 'Cart',
        'my_orders': 'My Orders',
        'search_placeholder': 'Search medicines...',
        'all_categories': 'All categories',
        'stock_count': 'In stock',
        'add_to_cart': 'Add to cart',
        'out_of_stock': 'Out of stock',
        'chat_title': 'Pharmacy Assistant',
        'bot_welcome': 'Hello! I am the online pharmacy assistant. What medicine do you need?',
        'chat_placeholder': 'Type your question...',
        'send': 'Send',
        'ask_question': 'Ask a question',
        'checkout': 'Checkout',
        'empty_cart': 'Your cart is empty',
        'total': 'Total:',
        # Translations for "About Us"
        'about_title': 'About PharmOnline',
        'about_subtitle': 'Your reliable online pharmacy',
        'about_desc': 'PharmOnline is a modern online platform that allows you to buy quality medicines, medical devices, and vitamins at affordable prices without leaving your home.',
        'our_mission': 'Our Mission',
        'mission_text': 'To deliver necessary medicines quickly, safely, and conveniently to every citizen, making health care accessible to everyone.',
        'why_us': 'Why Choose Us?',
        'feature_1': 'Only original and quality medicines',
        'feature_2': 'Easy payment via Kaspi QR and Kaspi Transfer',
        'feature_3': 'Express delivery service',
        'feature_4': 'Online assistance from qualified pharmacists',
        'contact_info': 'Contact Information:',
        'phone_label': 'Phone:',
        'email_label': 'Email:',
        'address_label': 'Address:',
        'address_val': '64 Tole bi street, Taraz city',
        # Chatbot extra translations
        'chat_empty': 'Please write your question.',
        'chat_thanks': 'You are welcome! We wish you good health! Feel free to reach out if you need help.',
        'chat_price_info': 'You can view the prices of all medicines in the "Catalog" section in the top menu!',
        'chat_contact': 'Our hotline and WhatsApp number: +7 (705) 887-33-07',
        'chat_default': 'I could not find exact information regarding this query. For more details or to place an order, please contact us via WhatsApp: +7 (705) 887-33-07',
        'in_stock': 'In stock',
        'out_stock': 'Out of stock',
        'no_desc': 'No description.',
        'price': 'Price',
        'status': 'Status',
        'desc': 'Description'
    }
}


def get_current_language(request):
    return request.session.get('lang', 'kk')


def set_language(request, lang_code):
    if lang_code in ['kk', 'ru', 'en']:
        request.session['lang'] = lang_code
    referer = request.META.get('HTTP_REFERER', '/')
    return redirect(referer)


def catalog_view(request):
    lang = get_current_language(request)
    categories = Category.objects.all()
    medicines = Medicine.objects.all()
    query = request.GET.get('q')
    category_id = request.GET.get('category')

    if query:
        medicines = medicines.filter(name_kk__icontains=query) | medicines.filter(name_ru__icontains=query)
    if category_id:
        medicines = medicines.filter(category_id=category_id)

    context = {
        'categories': categories,
        'medicines': medicines,
        'current_lang': lang,
        't': TRANSLATIONS[lang],
    }
    return render(request, 'core/catalog.html', context)


def stock_view(request):
    lang = get_current_language(request)
    medicines = Medicine.objects.all()
    context = {'medicines': medicines, 'current_lang': lang, 't': TRANSLATIONS[lang]}
    return render(request, 'core/stock.html', context)


def about_view(request):
    lang = get_current_language(request)
    context = {'current_lang': lang, 't': TRANSLATIONS[lang]}
    return render(request, 'core/about.html', context)


def add_to_cart(request, medicine_id):
    cart = request.session.get('cart', {})
    str_id = str(medicine_id)
    cart[str_id] = cart.get(str_id, 0) + 1
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('core:catalog')


def cart_view(request):
    lang = get_current_language(request)
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for med_id, quantity in cart.items():
        try:
            medicine = Medicine.objects.get(id=med_id)
            item_total = medicine.price * quantity
            total_price += item_total
            cart_items.append({
                'medicine': medicine,
                'quantity': quantity,
                'item_total': item_total
            })
        except Medicine.DoesNotExist:
            continue

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'current_lang': lang,
        't': TRANSLATIONS[lang],
    }
    return render(request, 'core/cart.html', context)


def create_order(request):
    if request.method == 'POST':
        full_name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        payment_type = request.POST.get('payment_type')

        cart = request.session.get('cart', {})
        if not cart:
            return redirect('core:cart')

        total_price = 0
        order_items_data = []

        for med_id, quantity in cart.items():
            try:
                med = Medicine.objects.get(id=med_id)

                if med.stock < quantity:
                    quantity = med.stock

                if quantity <= 0:
                    continue

                item_total = med.price * quantity
                total_price += item_total

                order_items_data.append({
                    'medicine': med,
                    'quantity': quantity,
                    'price': med.price
                })
            except Medicine.DoesNotExist:
                continue

        if not order_items_data:
            return redirect('core:cart')

        order = Order.objects.create(
            full_name=full_name,
            phone=phone,
            address=address,
            total_price=total_price,
            payment_type=payment_type,
            is_completed=False
        )

        for item in order_items_data:
            med = item['medicine']
            qty = item['quantity']

            OrderItem.objects.create(
                order=order,
                medicine=med,
                quantity=qty,
                price=item['price']
            )

            med.stock -= qty
            if med.stock < 0:
                med.stock = 0
            med.save()

        user_orders = request.session.get('user_orders', [])
        user_orders.append(order.id)
        request.session['user_orders'] = user_orders

        request.session['cart'] = {}
        request.session.modified = True

        return render(request, 'core/order_success.html', {'order': order})

    return redirect('core:cart')


def my_orders_view(request):
    lang = get_current_language(request)
    user_order_ids = request.session.get('user_orders', [])
    orders = Order.objects.filter(id__in=user_order_ids).order_by('-created_at')

    context = {
        'orders': orders,
        'current_lang': lang,
        't': TRANSLATIONS[lang],
    }
    return render(request, 'core/my_orders.html', context)


def chatbot_api(request):
    if request.method == 'POST':
        # Хабарламаны JSON немесе POST арқылы қабылдау
        try:
            data = json.loads(request.body)
            msg = data.get('message', '').strip()
        except:
            msg = request.POST.get('message', '').strip()

        # Сайтта таңдалған ағымдағы тілді алу
        lang = get_current_language(request)
        t = TRANSLATIONS[lang]

        if not msg:
            return JsonResponse({'reply': t['chat_empty']})

        msg_lower = msg.lower()

        # 1. Сәлемдесу
        if any(w in msg_lower for w in ['сәлем', 'салем', 'привет', 'hello', 'hi', 'қайырлы', 'здравствуй']):
            return JsonResponse({'reply': t['bot_welcome']})

        # 2. Рақмет
        if any(w in msg_lower for w in ['рахмет', 'спасибо', 'thanks', 'thank you']):
            return JsonResponse({'reply': t['chat_thanks']})

        # 3. Дәрі іздеу
        medicines = Medicine.objects.filter(
            Q(name_kk__icontains=msg) |
            Q(name_ru__icontains=msg) |
            Q(name_en__icontains=msg)
        )

        if medicines.exists():
            med = medicines.first()

            # Тілге сәйкес дәрі атын және сипаттамасын таңдау
            if lang == 'ru':
                med_name = med.name_ru or med.name_kk
                desc = med.description_ru or med.description_kk or t['no_desc']
            elif lang == 'en':
                med_name = med.name_en or med.name_kk
                desc = med.description_en or med.description_kk or t['no_desc']
            else:
                med_name = med.name_kk or med.name_ru
                desc = med.description_kk or med.description_ru or t['no_desc']

            stock_status = f"{t['in_stock']} ({med.stock} дана)." if med.stock > 0 else t['out_stock']

            reply = f"💊 **{med_name}**\n💰 {t['price']}: {med.price} ₸\n📦 {t['status']}: {stock_status}\n📝 {t['desc']}: {desc}"
            return JsonResponse({'reply': reply})

        # 4. Баға туралы сұрақ
        if any(w in msg_lower for w in ['баға', 'цена', 'стоимость', 'price', 'cost']):
            return JsonResponse({'reply': t['chat_price_info']})

        # 5. Байланыс / WhatsApp
        if any(w in msg_lower for w in ['жедел', 'whatsapp', 'номер', 'байланыс', 'контакт', 'phone', 'call']):
            return JsonResponse({'reply': t['chat_contact']})

        # 6. Әдепкі жауап
        return JsonResponse({'reply': t['chat_default']})

    return JsonResponse({'reply': 'Қате сұрау / Invalid request'})


def update_cart(request, medicine_id, action):
    cart = request.session.get('cart', {})
    str_id = str(medicine_id)

    if str_id in cart:
        if action == 'inc':
            cart[str_id] += 1
        elif action == 'dec':
            cart[str_id] -= 1
            if cart[str_id] <= 0:
                del cart[str_id]
        elif action == 'remove':
            del cart[str_id]

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('core:cart')