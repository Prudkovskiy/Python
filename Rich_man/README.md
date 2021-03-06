Сумасшедший богач
===
Один сумасшедший богач на старости лет впал в маразм и стал еще более сумасшедшим. Он решил отдать половину своих богатств тому, кто выиграет в математической игре.

## Правила игры 
Изначально каждый игрок начинает с нулевой суммой. Он может либо получить у богача 1 миллион сантиков, либо отдать ему 1 миллион сантиков, либо получить от богача ту же сумму, которая есть у него сейчас.

Выигрывает тот, кто за минимальное количество действий наберет сумму, равную половине состояния богача.

На беду других игроков, нашелся человек, который что-то слышал про жадные алгоритмы и двоичную систему счисления (возможно это вы).

## Формат входных данных
В стандартном потоке записано единственное натуральное число - размер половины состояния богача (в миллионах).

## Формат результата
Каждая строка выхода содержит ровно одну операцию ```inc, dec или dbl``` из кратчайшей последовательности действий для победы.

Если кто-то решил отнимать деньги у умалишенных людей - значит, он очень жадный.

Поэтому если решений несколько, выведите то, в котором больше операций удвоения суммы (и отдавать деньги невменяемым людям стоит только при крайней необходимости).

Результат работы программы выводится в стандартный поток вывода.

**Пример:**

| Входные данные       |  Результат работы             |
| ------------- |:------------------|
| 23     | inc |
| |dbl|
| |inc|
| |dbl|
| |dbl|
| |dbl|
| |dec|