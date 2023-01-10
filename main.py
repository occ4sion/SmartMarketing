from pipeline import *

def main():
    command = ''
    while command not in {'FIT', 'PREDICT', 'QUERY'}:
        command = input('Введите команду\nFIT для дообучения\nPREDICT для предсказания\nQUERY для выполнения запроса к БД')
    path = ''
    while path == '':
        path = input('Пожалуйста введите путь до данных: ')
    path += '/' if path[-1] != '/' else ''
    if command == 'FIT':
        scores = fit(path)
        print(f"Результаты до обучения {scores['old']}\nРезультаты после обучения {scores['new']}")
    elif command == 'PREDICT':
        result = predict(path)
        if result:
            print(f"Предсказания находятся в файле {path+'predictions.csv'}")
    elif command == 'QUERY':
        result = clickhouse(input("Введите параметры для подключения в формате param1=value1, param2=value2..."), input("Введите команду: "))
    return 0

if __name__ == '__main__':
    main()