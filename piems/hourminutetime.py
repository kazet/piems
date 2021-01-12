from decimal import Decimal


class HourMinuteTimeInterval:
    def __init__(self, hours: Decimal = 0, minutes: Decimal = 0):
        self._minutes = hours * 60 + minutes

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        result = ''
        hours = self._minutes // 60
        if hours != 0:
            result += f"{hours}h"

        minutes = self._minutes - 60 * hours
        if minutes != 0:
            if result != '':
                result += ' '
            result += f"{minutes}m"
        return result

    def __add__(self, obj):
        assert isinstance(obj, HourMinuteTimeInterval)
        return HourMinuteTimeInterval(minutes=self._minutes + obj._minutes)

    def __mul__(self, obj):
        assert isinstance(obj, Decimal)
        return HourMinuteTimeInterval(minutes=self._minutes * obj)

    def __truediv__(self, obj):
        assert isinstance(obj, Decimal)
        return HourMinuteTimeInterval(minutes=self._minutes / obj)

    def __rmul__(self, obj):
        return self.__mul__(obj)

    def __sub__(self, obj):
        assert isinstance(obj, HourMinuteTimeInterval)
        return HourMinuteTimeInterval(minutes=self._minutes - obj._minutes)

    def __eq__(self, other):
        if not isinstance(other, HourMinuteTimeInterval):
            return False
        return self._minutes == other._minutes


class HourMinuteTime:
    def __init__(self, hour: Decimal = 0, minute: Decimal = 0):
        self._hour = hour
        self._minute = minute

    def as_minutes_from_midnight(self) -> Decimal:
        return self._hour * 60 + self._minute

    def distance_until(self, obj: "HourMinuteTime"):
        if obj.as_minutes_from_midnight() > self.as_minutes_from_midnight():
            return HourMinuteTimeInterval(minutes=obj.as_minutes_from_midnight() - self.as_minutes_from_midnight())
        else:
            return HourMinuteTimeInterval(
                minutes=Decimal(24 * 60) - self.as_minutes_from_midnight() + obj.as_minutes_from_midnight())
