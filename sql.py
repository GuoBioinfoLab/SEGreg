#!/usr/bin/python

from sqlalchemy import create_engine, text, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql

Base = declarative_base()

class Product(Base):
    __tablename__ = 'TCGA'

    id = Column(Integer, Sequence('id'), primary_key=True)
    cancer = Column(String)
    gene = Column(String)
    loci_start = Column(Integer)
    loci_end = Column(Integer)

    def __repr__(self):
        print "<Product(id='%d', cancer='%s',gene='%s', loci_start='%d', loci_end='%d')>"\
               %(self.id, self.cancer, self.gene, self.loci_start, self.loci_end)


DB_CON_STR = 'mysql+mysqldb://'
engine = create_engine(DB_CON_STR, echo=False) #True will turn on the logging

Session = sessionmaker(bind=engine)
session = Session()

#eg1 via class
#res = session.query(Product).filter(Product.id==1).one()
res = session.query(Product).filter(text("id=1")).one()
print res.id, res.cancer, res.gene, res.loci_start, res.loci_end


#eg2 via sql
sql = text("select * from products")
res = session.execute(sql).fetchall()

for row in res:
        for col in row:
           print col,
        print

session.close()
