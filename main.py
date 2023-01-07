from pipeline import fit, predict

def main():
    command = ''
    while command not in {'FIT', 'PREDICT'}:
        command = input('Введите команду FIT для дообучения или PREDICT для предсказания:\n')
    path = ''
    while path == '':
        path = input('Пожалуйста введите путь до данных: ')
    path += '/' if path[-1] != '/' else ''
    if command == 'FIT':
        scores = fit(path)
        print(f"Результаты до обучения {scores['old']}\nРезультаты после обучения {scores['new']}")
    else:
        result = predict(path)
        if result:
            print(f"Предсказания находятся в файле {path+'predictions.csv'}")

    return 0

if __name__ == '__main__':
    main()