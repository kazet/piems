from lark import Lark


parser = Lark('''start: expression_l1
            expression_l1: expression_l2 plus expression_l1 | expression_l2 minus expression_l1 | expression_l2

            plus: "+"
            minus: "-"

            expression_l2: expression_l3 | const multiply expression_l3 | expression_l3 (multiply | divide) const

            multiply: "*"
            divide: "/"

            const: NUMBER

            expression_l3: "(" expression_l1 ")" | time_interval_raw | time_interval_calculated

            time_interval_raw: [time_interval_raw_hour] [time_interval_raw_minute]
            time_interval_raw_hour: NUMBER "h"
            time_interval_raw_minute: NUMBER "m"

            time_interval_calculated: time "to" time
            time: two_digits ":" two_digits
            two_digits: DIGIT DIGIT

            %import common.NUMBER
            %import common.DIGIT
            %ignore " "
            %ignore "\\n"
         ''')
