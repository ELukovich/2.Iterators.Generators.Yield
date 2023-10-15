import types

class FlatIterator:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list

    def __iter__(self):
        self.list_iter = iter(self.list_of_list)
        self.nested_list = []
        return self

    def __next__(self):
        while True:
            try:
                self.nested_element = next(self.list_iter)  # получаем следующий элемент списка
            except StopIteration:  # получаем StopIteration, если следующего элемента нет
                if not self.nested_list:  # если не осталось элементов, получаем StopIteration
                    raise StopIteration
                else:
                    self.list_iter = self.nested_list.pop()  # или получаем следующий элемент
                    continue
            if isinstance(self.nested_element, list):  # проверяем следующий элемент (список или нет)
                self.nested_list.append(self.list_iter)  # если список, то добавляем в очередь
                self.list_iter = iter(self.nested_element)  # и смещаем указатель текущего итератора
            else:  # если элемент не список, то возвращаем этот элемент
                return self.nested_element

def flat_generator(list_of_list):
    for elem in list_of_list:
        if isinstance(elem, list):  # проверяем список или нет
            for nested_elem in flat_generator(elem):  # если список, то снова вызываем
                yield nested_elem
        else:
            yield elem

def test_3():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    print('Итератор для любой вложенности')
    for item in FlatIterator(list_of_lists_2):
        print(item)

    print('\n')
    print('Генератор для любой вложенности')
    for item in flat_generator(list_of_lists_2):
        print(item)

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']

    assert isinstance(flat_generator(list_of_lists_2), types.GeneratorType)


if __name__ == '__main__':
    test_3()