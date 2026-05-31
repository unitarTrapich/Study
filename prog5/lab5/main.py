from currency_class import CurrenciesLst



if __name__ == '__main__':
    
    cl = CurrenciesLst()
    request1 = cl.getter()
    print(request1)
    cl.setter(('CHF','RSD','TMT','CZK'))
    cl.visualiser()