## Задача 1. Перевозка вакцины

### Что нужно сделать

Грузовик перевозит очень важную вакцину.

Условия хранения этой вакцины весьма необычные — в отсеке должна быть температура -18 ± 2 градуса. Если температурный
режим был нарушен, вакцина считается испорченной.

Для проверки состояния вакцины применяется датчик, который раз в час измеряет температуру внутри контейнера. Если
температура в контейнере была вне указанной хотя бы три часа, температурный режим считается нарушенным.

Реализуйте функцию, которая по номеру грузовика определяет, испортилась ли вакцина, с помощью
таблицы `table_truck_with_vaccine`.

```python
def check_if_vaccine_has_spoiled(
        cursor: sqlite3.Cursor,
        truck_number: str
) -> bool:
    ...
```

### Советы и рекомендации

* [Оператор BETWEEN](https://www.sqlitetutorial.net/sqlite-between/)
* [Оператор EXISTS](https://www.sqlitetutorial.net/sqlite-exists/)

### Что оценивается

Определение испорченности вакцины происходит через выборку с условием.
