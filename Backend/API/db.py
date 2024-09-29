from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime


#Change the database URL to your own database URL
DATABASE_URL = 'mysql+pymysql://Fabio:Fabio@10.111.37.148:3306/db'

engine = create_engine(DATABASE_URL, echo=True)
# Define the base class for ORM models
Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'Transactions'
    steps = Column(Integer)
    type = Column(String(50))
    amount = Column(DECIMAL(10, 2))
    nameOrig = Column(String(50), primary_key=True)
    oldbalanceOrg = Column(DECIMAL(10, 2))
    newbalanceOrig = Column(DECIMAL(10, 2))
    nameDest = Column(String(50))    
    oldbalanceDest = Column(DECIMAL(10, 2))
    newbalanceDest = Column(DECIMAL(10, 2))
    isfraud = Column(Integer)
    isflaggedFraud = Column(Integer)
    effectiveDate = Column(DateTime, default=datetime.now)


# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# get transaction by nameOrig
def get_transaction_by_nameOrig(nameOrig):
    transaction = session.query(Transaction).filter(Transaction.nameOrig == nameOrig).first()
    if transaction:
        # Convert the SQLAlchemy object to a dictionary
        transaction_dict = {column.name: getattr(transaction, column.name) for column in transaction.__table__.columns}
        return transaction_dict
    return None

# get transaction by the last 10 dates
def get_transactions_in_blocks(pageNum):
    pageNum = int(pageNum)
    transactions_per_block = 10
    offset_value = (pageNum - 1) * transactions_per_block

    # Query the transactions, order by date in descending order, apply limit and offset for pagination
    transactions = (session.query(Transaction)
                    .order_by(Transaction.effectiveDate.desc())  # Assuming Transaction.date is the timestamp column
                    .limit(transactions_per_block)
                    .offset(offset_value)
                    .all())
    
    # Convert the result to a list of dictionaries
    transactions_list = [{column.name: getattr(transaction, column.name) for column in transaction.__table__.columns}
                         for transaction in transactions]
    
    return transactions_list


# Create a new transaction
def create_transaction(data):
    session.rollback()
    new_transaction = Transaction(
        nameOrig=data.get('nameOrig'),
        steps=data.get('steps'),
        type=data.get('type'),
        amount=data.get('amount'),
        oldbalanceOrg=data.get('oldbalanceOrg'),
        newbalanceOrig=data.get('newbalanceOrig'),
        nameDest=data.get('nameDest'),
        oldbalanceDest=data.get('oldbalanceDest'),
        newbalanceDest=data.get('newbalanceDest'),
        isfraud=data.get('isfraud'),
        isflaggedFraud=data.get('isflaggedFraud'),
    )
    session.add(new_transaction)
    session.commit()
    return new_transaction
