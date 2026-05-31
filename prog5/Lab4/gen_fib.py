import functools

def fib_elem_gen():
    """Генератор, возвращающий элементы ряда Фибоначчи"""
    a = 0
    b = 1

    while True:
        yield a
        res = a + b
        a = b
        b = res



def my_genn():
    """Сопрограмма"""

    itt = fib_elem_gen()
    while True:
        number_of_fib_elem = yield
        l = [next(itt) for _ in range(number_of_fib_elem)]
        yield l
    



def fib_coroutine(g):
    @functools.wraps(g)
    def inner(*args, **kwargs):
        gen = g(*args, **kwargs)
        gen.send(None)
        return gen
    return inner



my_genn = fib_coroutine(my_genn)

def fib(n):
    gen = my_genn()
    return(gen.send(n))



class FibonacchiLst:
    def fib_elem_gen():
        a = 0
        b = 1

        while True:
            yield a
            res = a + b
            a = b
            b = res

    g = fib_elem_gen()

    def go_fib(self, max):
        """Функция рассчитывает ряд фибоначи с элементами меньше входного максимума"""
        g = fib_elem_gen()
        list = []
        el = next(g)
        while el <= max:
            list.append(el)
            el = next(g)
            
        return(list)


    def __init__(self, instance):
        self.instance = instance   
        self.idx = 0
    
    def __iter__(self):
        return self 

    def __next__(self):
        """
        Функция прокручивает исходный список, по каждому элементу генерируя список фибоначи и проверяя наличие элемента в этом списке.
        """
        while True:
            try:
                res = self.instance[self.idx] 
                fiblst = self.go_fib(res)

            except IndexError:
                raise StopIteration
            
            if res in fiblst:
                self.idx += 1
                return res
            self.idx += 1

            

print(list(FibonacchiLst([1, 4, 24, 2, 5, 13, 22, 28, 31, 8, 17, 74])))
print(list(FibonacchiLst([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1])))
