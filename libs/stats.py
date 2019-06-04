# This Python file uses the following encoding: utf-8
import numpy as np
import libs.storage as strg

def process():
    data = np.array(strg.data)
    mean = data.mean()
    std = data.std()
    n = len(strg.data)

    fillInter(mean, std)

    strg.cleared_data = []
    strg.mistakes = []
    strg.str_cleared_data = ''
    strg.str_mistakes = ''

    crit = calcCharlierCrit(n)

    strg.inter += 'Критичексое значение = {}\nКрит. знач. * СКО = {}\n'.format(crit, crit * std)
    strg.inter += '{:10} {:10} {:10}\n'.format('Значение', '|x-Mx|', 'Промах?')

    applyCriteria(data, mean, std, crit)

    strg.str_cleared_data = ' '.join(str(i) for i in strg.cleared_data)
    strg.str_mistakes = ' '.join(str(i) for i in strg.mistakes)

@np.vectorize
def applyCriteria(x, mean, std, crit):
    if abs(x - mean) > crit * std:
        strg.mistakes.append(float(x))
        strg.inter += '{:10f} {:10f} {:10}\n'.format(x, abs(x - mean), 'Да')
    else:
        strg.cleared_data.append(float(x))
        strg.inter += '{:10f} {:10f} {:10}\n'.format(x, abs(x - mean), 'Нет')

def calcCharlierCrit(n):
    return (0.212204493 + 0.897158545 * np.log(n)) / (1 + 0.181570415 * np.log(n) - 0.00715123 * (np.log(n)) ** 2)

def fillInter(mean, std):
    strg.inter = 'Среднее = {}\nСКО = {}\n'.format(mean, std)