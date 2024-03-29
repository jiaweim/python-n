from collections import defaultdict


def test_list():
    s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
    d = defaultdict(list)
    for k, v in s:
        d[k].append(v)  # 必须通过 [] 访问
    assert list(d) == ['yellow', 'blue', 'red']
    assert d['yellow'] == [1, 3]
    assert d['blue'] == [2, 4]
    assert d['red'] == [1]


def test_set_default():
    s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
    d = {}
    for k, v in s:
        d.setdefault(k, []).append(v)
    assert list(d) == ['yellow', 'blue', 'red']


def test_int():
    s = 'mississippi'
    d = defaultdict(int)
    for k in s:
        d[k] += 1
    list(d).sort()


def test_lambda():
    def constant_factory(value):
        return lambda: value

    d = defaultdict(constant_factory('<DAO>'))
    assert d['a'] == "<DAO>"


def test_lambda2():
    dd_pair = defaultdict(lambda: [0, 0])
    dd_pair[2][1] = 1
    assert dd_pair[2] == [0, 1]
