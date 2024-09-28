from sqlalchemy import create_engine, Column, Integer, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Query the first 10 records
def get_transaction_by_nameOrig(nameOrig):
    transaction = session.query(Transaction).filter(Transaction.nameOrig == nameOrig).first()
    if transaction:
        # Convert the SQLAlchemy object to a dictionary
        transaction_dict = {column.name: getattr(transaction, column.name) for column in transaction.__table__.columns}
        return transaction_dict
    return None


# first_10_records = session.query(Transaction).limit(10).all()

# Print the records
# for record in first_10_records:
#     print(record.__dict__)
