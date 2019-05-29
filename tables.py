from flask_table import Table, Col, DatetimeCol


class Entries(Table):
    classes = ['table', 'table-striped', 'table-bordered', 'table-condensed']
    id = Col('Id', show=False)
    name = Col('Name')
    date = DatetimeCol('Date')
    text = Col('Text')
