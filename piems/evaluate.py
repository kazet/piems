from decimal import Decimal

from lark import Tree

from . import hmtime
from . import parser


def _evaluate_tree(t: Tree):
    if t.data == 'start':
        child, = tuple(t.children)
        return _evaluate_tree(child)
    elif t.data in ['expression_l1', 'expression_l2', 'expression_l3']:
        if len(t.children) == 1:
            time, = tuple(t.children)
            return _evaluate_tree(time)
        elif len(t.children) == 3:
            time, op, expr = tuple(t.children)
            if op.data == 'plus':
                return _evaluate_tree(time) + _evaluate_tree(expr)
            elif op.data == 'minus':
                return _evaluate_tree(time) - _evaluate_tree(expr)
            elif op.data == 'multiply':
                return _evaluate_tree(time) * _evaluate_tree(expr)
            elif op.data == 'divide':
                return _evaluate_tree(time) / _evaluate_tree(expr)
            else:
                assert False, f"unknown operator: {op}"
        else:
            assert False, "illegal number of children"
    elif t.data == 'const':
        number, = tuple(t.children)
        return Decimal(number)
    elif t.data == 'time_interval_raw':
        result = hmtime.HMTimeInterval()
        for child in t.children:
            number, = tuple(child.children)
            number = Decimal(number)
            if child.data == 'time_interval_raw_hour':
                result += hmtime.HMTimeInterval(hours=number)
            elif child.data == 'time_interval_raw_minute':
                result += hmtime.HMTimeInterval(minutes=number)
        return result
    elif t.data == 'time_interval_calculated':
        time_1, time_2 = tuple(t.children)
        time_1 = _evaluate_tree(time_1)
        time_2 = _evaluate_tree(time_2)
        return time_1.distance_until(time_2)
    elif t.data == 'time':
        hour, minute = tuple(t.children)
        hour = _evaluate_tree(hour)
        minute = _evaluate_tree(minute)
        return hmtime.HMTime(hour, minute)
    elif t.data == 'two_digits':
        digit_1, digit_2 = tuple(t.children)
        return Decimal(digit_1 + digit_2)
    else:
        assert False, f"unknown vertex: {t.data}"


def evaluate(s: str):
    tree = parser.parser.parse(s)
    return _evaluate_tree(tree)
