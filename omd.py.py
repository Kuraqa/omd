from collections import Counter
from itertools import groupby


def task1() -> None:
    moscow = {201, 202, 203, 204}
    kazan = {203, 204, 205, 206}

    # что можно забрать в любом из двух городов
    goods_in_both_cities = moscow & kazan
    print(f"Товары в обоих городах: {goods_in_both_cities}")

    # что есть только в Москве
    goods_only_moscow = moscow - kazan
    print(f"Только в Москве: {goods_only_moscow}")

    # что есть только в Казани
    goods_only_kazan = kazan - moscow
    print(f"Только в Казани: {goods_only_kazan}")

    # сколько разных товаров на обоих складах вместе
    all_goods = moscow | kazan
    print(f"Всего уникальных товаров: {len(all_goods)}")


def task2() -> None:

    queries = [
        "чехол",
        "iphone",
        "чехол",
        "наушники",
        "iphone",
        "iphone",
        "кабель",
        "чехол",
        "iphone",
    ]

    # сколько всего поисковых запросов в ленте
    print(f'Всего выполнено {len(queries)} запросов')

    # cколько раз ввели каждый запрос
    count_queries = Counter(queries)
    for query, num in count_queries.items():
        print(f'Были введены {num} запросов "{query}"')

    # какой запрос вводили чаще всего
    most_common_query, count = count_queries.most_common(1)[0]
    print(f'Самый популырный запрос {most_common_query} был введен {count} раз')

    # какую долю всех поисков он занимает
    total_num_queries = sum(num for query, num in count_queries.items())
    print(f'Самый популырный запрос {most_common_query} составляет \
           {round(count / total_num_queries * 100, 2)}% от всех запросов')

    # какие запросы встретились один раз
    one_time_queries = [
        f'"{query}"'
        for query, num
        in count_queries.items()
        if num == 1
    ]
    print(f'Запросы, введённые один раз: {", ".join(one_time_queries)}')


def task3() -> None:

    orders = [
        {"id": 1, "buyer": "anya", "status": "delivered", "amount": 900},
        {"id": 2, "buyer": "boris", "status": "returned", "amount": 4_500},
        {"id": 3, "buyer": "anya", "status": "delivered", "amount": 1_500},
        {"id": 4, "buyer": "vera", "status": "delivered", "amount": 3_200},
        {"id": 5, "buyer": "boris", "status": "delivered", "amount": 700},
        {"id": 6, "buyer": "gleb", "status": "returned", "amount": 2_100},
    ]

    # на какую сумму оформили возвраты
    total_returned_money = sum(
        order['amount']
        for order in orders
        if order['status'] == 'returned'
    )
    print(f'Всего было возвращено {total_returned_money} д.е.')

    # кто хотя бы раз вернул заказ
    buyers_who_returned = {
        order['buyer']
        for order
        in orders
        if order['status'] == 'returned'
    }
    print(f'Покупатели, которые хотя бы 1 раз вернули товар: \
          {", ".join(buyers_who_returned)}')

    # сколько заказов доставлено покупателю
    delivered_orders_amounts = [
        order['amount']
        for order in orders
        if order['status'] == 'delivered'
    ]
    count_delivered_orders = len(delivered_orders_amounts)
    print(f'Всего были доставлены {count_delivered_orders} заказа')

    # средний чек доставленных заказов
    if count_delivered_orders != 0:
        avg_check = sum(delivered_orders_amounts) / count_delivered_orders
        print(f'Средняя сумма доставленного заказа {avg_check} д.е.')
    else:
        print('Доставленных товаров нет')


def task4() -> None:
    days = [
        {"day": "пн", "orders": 20, "revenue": 40_000, "returns": 2},
        {"day": "вт", "orders": 16, "revenue": 19_200, "returns": 4},
        {"day": "ср", "orders": 25, "revenue": 55_000, "returns": 1},
        {"day": "чт", "orders": 10, "revenue": 12_000, "returns": 3},
        {"day": "пт", "orders": 30, "revenue": 48_000, "returns": 3},
    ]

    # выручку за всю неделю
    print(f'Общая выручка: {sum(date['revenue'] for date in days)} д.е.')

    # день с самой большой выручкой
    day_with_max_revenue = max(days, key=lambda x: x['revenue'])
    print(f'День с самой большой выручкой - {day_with_max_revenue["day"]}')

    # среднюю выручку на один заказ в каждый день
    for day in days:
        print(f'Средняя выручка в {day["day"]} - {day["revenue"] / day["orders"]} д.е.')

    # дни, где возвратов больше 20% заказов
    days_with_many_returns = [
        day['day']
        for day in days
        if day['returns'] / day['orders'] > 0.2
    ]
    print('Дни, где возвратов больше 20%:', ', '.join(days_with_many_returns))


def task5() -> None:
    reviews = [
        {"id": 1, "product": "Чехол", "stars": 5},
        {"id": 1, "product": "Чехол", "stars": 3},
        {"id": 1, "product": "Чехол", "stars": 4},
        {"id": 2, "product": "Наушники", "stars": 2},
        {"id": 2, "product": "наушники", "stars": 2},
        {"id": 2, "product": "НАУШНИКИ", "stars": 5},
        {"id": 3, "product": "Планшет", "stars": 5},
        {"id": 4, "product": "Колонка", "stars": 4},
        {"id": 4, "product": "Колонка", "stars": 4},
        {"id": 5, "product": "Кабель", "stars": 1},
    ]

    for review in reviews:
        review['product'] = review['product'].lower()
    reviews_sorted = sorted(reviews, key=lambda x: x['product'])

    mean_rating_reviews = {}

    # среднюю оценку каждого товара
    for product, group in groupby(reviews_sorted, key=lambda x: x['product']):
        ratings = [review['stars'] for review in group]
        mean_rating = sum(ratings) / len(ratings)
        mean_rating_reviews[product] = (len(ratings), mean_rating)
        print(f'Средний рейтинг у "{product}": {mean_rating}')

    # худший товар по средней оценке среди тех, у кого хотя бы два отзыва
    eligible_products = {
        name: rating_count
        for name, rating_count
        in mean_rating_reviews.items()
        if rating_count[0] >= 2
    }
    worst_product = min(eligible_products,
                        key=lambda x: eligible_products[x][1])
    print(f'Худший товар с минимум 2 отзывами - "{worst_product}"')

    # сколько отзывов на 1 или 2 звезды
    one_or_two_stars_reviews = [
        product
        for product
        in reviews
        if product['stars'] in (1, 2)
    ]
    one_or_two_stars_reviews_count = len(one_or_two_stars_reviews)
    print(f'Всего {one_or_two_stars_reviews_count} отзыва имеют 1/2 звезды')

    # какую долю всех отзывов они составляют
    share = one_or_two_stars_reviews_count / len(reviews) * 100
    print(f'Они составляют {share:.2f}% от всех отзывов')


def main() -> None:
    task1()
    task2()
    task3()
    task4()
    task5()


if __name__ == '__main__':
    main()
