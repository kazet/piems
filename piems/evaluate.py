from decimal import Decimal, getcontext, Context

from lark import Tree

from . import hourminutetime
from . import parser


def _evaluate_tree(t: Tree, context: Context):
    if t.data == 'start':
        child, = tuple(t.children)
        return _evaluate_tree(child, context)
    elif t.data in ['expression_l1', 'expression_l2', 'expression_l3']:
        if len(t.children) == 1:
            time, = tuple(t.children)
            return _evaluate_tree(time, context)
        elif len(t.children) == 3:
            time, op, expr = tuple(t.children)
            if op.data == 'plus':
                return _evaluate_tree(time, context) + _evaluate_tree(expr, context)
            elif op.data == 'minus':
                return _evaluate_tree(time, context) - _evaluate_tree(expr, context)
            elif op.data == 'multiply':
                return _evaluate_tree(time, context) * _evaluate_tree(expr, context)
            elif op.data == 'divide':
                return _evaluate_tree(time, context) / _evaluate_tree(expr, context)
            else:
                assert False, f"unknown operator: {op}"
        else:
            assert False, "illegal number of children"
    elif t.data == 'const':
        number, = tuple(t.children)
        return Decimal(number, context)
    elif t.data == 'time_interval_raw':
        result = hourminutetime.HourMinuteTimeInterval()
        for child in t.children:
            number, = tuple(child.children)
            number = Decimal(number, context)
            if child.data == 'time_interval_raw_hour':
                result += hourminutetime.HourMinuteTimeInterval(hours=number)
            elif child.data == 'time_interval_raw_minute':
                result += hourminutetime.HourMinuteTimeInterval(minutes=number)
        return result
    elif t.data == 'time_interval_calculated':
        time_1, time_2 = tuple(t.children)
        time_1 = _evaluate_tree(time_1, context)
        time_2 = _evaluate_tree(time_2, context)
        return time_1.distance_until(time_2)
    elif t.data == 'time':
        hour, minute = tuple(t.children)
        hour = _evaluate_tree(hour, context)
        minute = _evaluate_tree(minute, context)
        return hourminutetime.HourMinuteTime(hour, minute)
    elif t.data == 'two_digits':
        digit_1, digit_2 = tuple(t.children)
        return Decimal(digit_1 + digit_2, context)
    else:
        assert False, f"unknown vertex: {t.data}"


def evaluate(s: str, precision: int = 10):
    context = getcontext()
    context.prec = precision
    tree = parser.parser.parse(s)
    return _evaluate_tree(tree, context=context)
