
import unittest
from main import Model


class TestModelParametr(unittest.TestCase):
    
    def test_model_parameter(self):
        '''
        тест __ini__
        параметр класса:
        -должен иметь тип данных: int or float
        тест на поднятие исключения TypeError,
        '''
        with self.assertRaises(TypeError):
            model = Model('asd')
        
    def test_model_parametr_negative(self):
        '''
        тест __init__
        параметр класса:
        -не должен быть отрицательным
        тест на поднятие исключения ValueError,
        '''
        with self.assertRaises(ValueError):
            model = Model(-1)


class TestModelMethod(unittest.TestCase):
    
    def setUp(self):
        print('Start: Running setUp')
        self.model = Model(10)
    
    #def tearDown(self):
    #    print('Finish: Running tearDown')

    def test_mi_to_km(self):
        # model = Model(10)
        km = self.model.mi_to_km()
        self.assertEqual(km, 16.09344)

    def test_km_to_mi(self):
        # model = Model(10)
        mi = self.model.km_to_mi()
        self.assertEqual(mi, 6.2137119223733395)

# СДЕЛАТЬ ЧЕРЕЗ ЦИКЛ РАБОТАЕТ НЕ КОРРЕКТНО!!!
    def test_property_value(self):
        ''' 
        буфер:
        - может преобразовать полученное
        значение в тип данных: int, float   
        - тест на вызов исключения: TypeError
        '''
        print('0')
        #model = Model(10)
        with self.assertRaises(TypeError):
            #self.model.value = ''
            print('1')
            self.model.value = None
            print('2')
            self.model.value = 123
            #self.model.value = 'asd'
            #self.model.value = False

 





