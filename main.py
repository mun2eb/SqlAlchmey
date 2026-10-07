#it is used to connect data base
from sqlalchemy import create_engine,Column,Integer,String
#session is used for crud operations  and base is used to create tables
from sqlalchemy.orm import sessionmaker,declarative_base
from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session


app = FastAPI()

#database_url is variable
database_url = "sqlite:///./test.db"
#like a bridge which connects with data base where we declare databaselinka and connect_args for more setting
engine = create_engine(
    database_url,
    connect_args={"check_same_thread": False}
)
#this is like waiter
session=sessionmaker(bind=engine)

Base = declarative_base()
#same like base model in sqlalchemy it is used to make the table name is the name of table like down there is
# value given index is for fast searching and primary key is for unique value
class Todo(Base):
    __tablename__="todos"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    compl= Column(String)

Base.metadata.create_all(bind = engine)
#it is a basic operation like when there is u need to work try runs and if there is some error finally run#
#yield is use to  give access of database to fast api# 
def get_db():
    db= session()
    try:
        yield db
    finally:
        db.close()



@app.get("/")
def view():
    return{
        "msg":"db connected"
    }

@app.post("/todos")
def create_todo(title:str,db:Session = Depends(get_db)):
    todo = Todo (title=title,compl="False")
    
    #db.add(todo) → Adds the object to the database session.
#db.commit() → Saves the changes permanently to the database.
#db.refresh(todo) → Updates the object with the latest database data.

    db.add(todo)
    db.commit()
    db.refresh(todo)
    return{
        "msg":todo
    }
@app.get("/todos")
def get_todos(db:Session = Depends(get_db)):
    #query is used to view data data and all()means everthing
    todos=db.query(Todo).all()
    return{
        "Total": len(todos),
        "Data":todos
    }
@app.get("/todos/{get_id}")
def get_spec(get_id:int,db:Session=Depends(get_db)):
    #filter is used to filter like in this we give condition and first mean first entry
    todo = db.query(Todo).filter(Todo.id == get_id).first()
    return{
    "msg":todo
}

@app.put("/todos/{get_id}")
def change(get_id:int,title:str ,db:Session=Depends(get_db)):
   todo = db.query(Todo).filter(Todo.id == get_id).first()
   todo.title=title
   db.commit()
   db.refresh(todo)
   return{
       "data":todo
   }
@app.delete ("/todos/{get_id}")
def dele(get_id:int,db:Session=Depends(get_db)):
        todo = db.query(Todo).filter(Todo.id == get_id).first()
        db.delete(todo)
        db.commit()
     
        return{
               "data":todo
           }






   
