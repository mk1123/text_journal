from flask_table import Table, Col, DatetimeCol


class Entries(Table):
    classes = ['table', 'table-striped', 'table-bordered', 'table-condensed']
    id = Col('Id', show=False)
    phone_num = Col('Phone number')
    date = DatetimeCol('Date')
    text = Col('Text')
