import types

class FlatIterator:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list

    def __iter__(self):
        self.list_iter = iter(self.list_of_list)
        self.nested_list = []
        self.cursor = -1
        return self

    def __next__(self):
        self.cursor += 1
        if len(self.nested_list) == self.cursor:  # если курсор в конце вложенного списка, то "обнуляем" список и курсор
            self.nested_list = None
            self.cursor = 0
            while not self.nested_list:  # если вложенные списки закончились, то получаем StopIteration
                self.nested_list = next(self.list_iter)  # если  список пустой, то получаем следующий вложенный список
        return self.nested_list[self.cursor]


def flat_generator(list_of_lists):
    for flat_list in list_of_lists:
        for elem in flat_list:
            yield elem

def test_1():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    print('Итератор')
    for item in FlatIterator(list_of_lists_1):
        print(item)

    print('\n')
    print('Генератор')
    for item in flat_generator(list_of_lists_1):
        print(item)

    # long_lol = 0
    # for i in list_of_lists_1:
    #     long_lol += len(i)
    # print(long_lol)


    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)


if __name__ == '__main__':
    test_1()

