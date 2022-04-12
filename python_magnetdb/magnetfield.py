from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Session, select
from .database import engine
from .queries import query_mpart

from .models import Magnet
from .models import MSite
from .models import MPart

from wtforms import Field, FieldList
from wtforms.widgets import TextInput, ListWidget, TableWidget
from wtforms.validators import DataRequired, Length

class MPartListField(Field):
    widget = TextInput() # ListWidget() # TableWidget() 

    def _value(self):
        print("_value:", self.data)
        if self.data:
            res = []
            for part in self.data:
                print("_value: part=", part.name)
                res.append(part.name)
            return ', '.join(res)
        else:
            return ''

    def process_formdata(self, mparts: List[MPart]):
        print("process_formdata")
        if mparts:
            self.data = [ part.name for part in mparts]
        else:
            self.data = []

class MagnetListField(Field):
    widget = TextInput() # ListWidget() # TableWidget() 

    def _value(self):
        # print("MagnetListField: _value:", self.data)
        if self.data:
            res = []
            for part in self.data:
                print("MagnetListField: _value: part=", part.name)
                res.append(part.name)
            return ', '.join(res)
        else:
            return ''

    def process_formdata(self, mparts: List[str]):
        # print("MagnetListField: process_formdata:", type(mparts))
        # print("MagnetListField: mparts=", mparts)
        if mparts:
            self.data = []
            with Session(engine) as session:
                for part in mparts:
                    # print("part:", part)
                    sql = select(Magnet).where(Magnet.name == part)
                    res = session.exec(sql)
                    for obj in res:
                        # print("obj:", obj)
                        self.data.append(obj)
        else:
            self.data = []

class BetterMagnetListField(MagnetListField):
    def __init__(self, label='', validators=None, remove_duplicates=True, **kwargs):
        super(BetterMagnetListField, self).__init__(label, validators, **kwargs)
        self.remove_duplicates = remove_duplicates

    def process_formdata(self, valuelist):
        super(BetterMagnetListField, self).process_formdata(valuelist)
        if self.remove_duplicates:
            self.data = list(self._remove_duplicates(self.data))
        print("Better:", type(self.data[0]))

    @classmethod
    def _remove_duplicates(cls, seq):
        """Remove duplicates in a case insensitive, but case preserving manner"""
        # print("BetterMagnetListField remove_duplicates:", seq)
        d = {}
        for item in seq:
            # print("BetterMagnetListField item:", item)
            if item.name not in d:
                d[item.name] = True
                yield item