import csv
from collections import defaultdict

import_file_name = 'Corp_Summary.csv'
export_file_name = 'Final_Summary.csv'


def read_rows():
    with open(import_file_name, mode='r', encoding='utf-8', newline='') as file:
        reader = csv.DictReader(file, delimiter=';')
        return list(reader)


def report_hierarchy(rows):
    hierarchy = defaultdict(set)
    for row in rows:
        hierarchy[row['Департамент']].add(row['Отдел'])

    print('-----НАЧАЛО ОТЧЕТА-----')
    for department, divisions in hierarchy.items():
        print(f'В департамент "{department}" входят отделы: \
              {', '.join(f'"{dev}"' for dev in divisions)}')
    print('-----КОНЕЦ ОТЧЕТА-----')


def build_summary(rows):
    summary = dict()

    for row in rows:
        if row['Департамент'] not in summary:
            wage = int(row['Оклад'])
            summary[row['Департамент']] = {
                'Число работников': 1,
                'Минимальная з/п': wage,
                'Максимальная з/п': wage,
                'Средняя з/п': wage,
                'Фонд оплаты труда': wage
            }
        else:
            wage = int(row['Оклад'])
            department = summary[row['Департамент']]
            department['Число работников'] += 1
            department['Фонд оплаты труда'] += wage
            department['Средняя з/п'] = round(department['Фонд оплаты труда'] /
                                              department['Число работников'], 2)

            if wage < department['Минимальная з/п']:
                department['Минимальная з/п'] = wage
            if wage > department['Максимальная з/п']:
                department['Максимальная з/п'] = wage

    return summary


def report_summary(summary):
    dep_number = 1
    print('-----НАЧАЛО ОТЧЕТА-----')
    for department, info in summary.items():
        print('-' * 10)
        print(f'{dep_number}) Сводная информация для департамента "{department}"')
        print(f'В департаменте работают людей: {info["Число работников"]}')
        print(f'Средняя з/п в департаменте: {info["Средняя з/п"]:.2f} руб.')
        print(f'Минимальная з/п: {info["Минимальная з/п"]} руб.')
        print(f'Максимальная з/п: {info["Максимальная з/п"]} руб.')
        dep_number += 1
    print('-----КОНЕЦ ОТЧЕТА-----')


def export_summary(summary):
    FIELDS = [
        'Число работников', 'Минимальная з/п',
        'Максимальная з/п', 'Средняя з/п'
        ]

    with open(export_file_name, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')

        header = ['Департамент'] + FIELDS
        writer.writerow(header)

        for department, info in summary.items():
            row = [department] + list(info.values())[:4]
            writer.writerow(row)


def do_report(type: int) -> None:
    rows = read_rows()
    if not rows:
        print('В файле нет информации')
        return

    if type == 1:
        report_hierarchy(rows)

    elif type in [2, 3]:
        summary = build_summary(rows)

        if type == 2:
            report_summary(summary)

        if type == 3:
            export_summary(summary)


if __name__ == '__main__':
    do_report(1)