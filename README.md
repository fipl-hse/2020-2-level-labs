# Лабораторные работы для 2-го курса ФПЛ (2020/2021)

В рамках предмета 
["Программирование для лингвистов"](https://www.hse.ru/edu/courses/375328211) 
в НИУ ВШЭ - Нижний Новгород.

Преподаватели: 

* [Демидовский Александр Владимирович](https://www.hse.ru/staff/demidovs) - лектор
* Кащихин Андрей Николаевич - ассистент лектора
* Ураев Дмитрий Юрьевич - ассистент лектора
* Кузнецова Валерия Андреевна - ассистент лектора

План лабораторных работ:

1. TBD (to be defined)
2. TBD (to be defined)
3. TBD (to be defined)
4. TBD (to be defined)

## Дополнительные материалы

1. Mark Lutz. 
   [Learning Python](https://www.amazon.com/Learning-Python-5th-Mark-Lutz/dp/1449355730).
2. Mark Lutz. 
   [Programming Python: Powerful Object-Oriented Programming](https://www.amazon.com/Programming-Python-Powerful-Object-Oriented/dp/0596158106)
3. Хирьянов Тимофей Фёдорович. Видеолекции. 
   [Практика программирования на Python 3](https://www.youtube.com/watch?v=fgf57Sa5A-A&list=PLRDzFCPr95fLuusPXwvOPgXzBL3ZTzybY) 
4. Хирьянов Тимофей Фёдорович. Видеолекции. 
   [Алгоритмы и структуры данных на Python 3](https://www.youtube.com/watch?v=KdZ4HF1SrFs&list=PLRDzFCPr95fK7tr47883DFUbm4GeOjjc0)
5. [Official Python 3 documentation](https://docs.python.org/3/).


## Запуск тестов

Для запуска тестов выполните следующую команду:

```bash
python -m unittest discover -p "*_test.py" -s .
```

## Что делать если в родительском репозитории есть изменения и они мне нужны?

1. Создаем `upstream` таргет в репозитории:

```bash
git remote add upstream https://github.com/fipl-hse/2020-2-level-labs
```

2. Получаем данные об изменениях в удаленном репозитории:

```bash
git fetch upstream
```

3. Обновляем свой репозиторий с изменениями из удаленного репозитория:

```bash
git merge upstream/master
```
