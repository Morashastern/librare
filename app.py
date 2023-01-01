import json
import sqlite3
from flask import Request,request
from sqlalchemy import Column, Integer, DateTime
from flask import Flask, Request , flash, url_for, redirect, render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
import time
from datetime import timedelta
from datetime import datetime
from flask_cors import CORS
#create  db



app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Library.sqlite3'
app.config['SECRET_KEY']="random string"
db = SQLAlchemy(app)
books_days_by_type={1:10,2:5,3:2}


class Books(db.Model):
    id = db.Column('book_id', db.Integer, primary_key = True)
    Name_book = db.Column(db.String(100))
    Author = db.Column(db.String(50))
    YearPublished = db.Column(db.Integer())
    Type_book = db.Column(db.Integer())
    books = db.relationship('Loans', backref='books')
    def __init__(self, Name_book, Author,YearPublished,Type_book):
        self.Name_book = Name_book
        self.Author = Author
        self.YearPublished = YearPublished
        self.Type_book = Type_book

class Customers(db.Model):
    id = db.Column('customer_id', db.Integer, primary_key = True)
    Name_cus = db.Column(db.String(100))
    City_cus = db.Column(db.String(50))
    Age_cus = db.Column(db.Integer())
    customers = db.relationship('Loans', backref='customers')
    def __init__(self, Name_cus, City_cus,Age_cus):
        self.Name_cus = Name_cus
        self.City_cus = City_cus
        self.Age_cus = Age_cus

class Loans(db.Model):
    id = db.Column('Loan_id',db.Integer, primary_key = True)
    Loandate = db.Column(db.String())
    Returndate = db.Column(db.String())
   
    customer_id = db.Column(db.Integer,db.ForeignKey('customers.customer_id'))
    book_id = db.Column(db.Integer,db.ForeignKey('books.book_id'))
    

    def __init__(self,Loandate=0,Returndate=0, customer_id=0, book_id=0):
        self.Loandate = Loandate
        self.Returndate = Returndate
        self.customer_id = customer_id
        self.book_id = book_id
        




@app.route("/")
def hello():
    return "hello world"
######crud book#####
@app.route('/Books/<id>/',methods =['GET','DELETE','PUT'])
@app.route('/Books/',methods =['GET','POST'])
def c_books(id=0):
    if request.method =='POST':
        request.data=request.get_json()
        Name_book=request.data["Name_book"]
        Author = request.data['Author']
        YearPublished = request.data['YearPublished']
        Type_book = request.data['Type_book']
        newBook=Books(Name_book, Author, YearPublished,Type_book)
        db.session.add(newBook)
        db.session.commit()
        
        return "A New Book added"
        

    if request.method =='GET':
        res=[]
        for book in Books.query.all():
            res.append({"id_book":book.id,"book_name": book.Name_book,"Author":book.Author,"YearPublished":book.YearPublished,"Type":book.Type_book})
        return (json.dumps(res))

    if request.method=='DELETE':
         del_book=Books.query.get(id)
         db.session.delete(del_book)
         db.session.commit()
         return("book deleted")


        
    if request.method=='PUT':
         update_book = Books.query.get(id)
         Name_book=request.json['Name_book']
         Author = request.json['Author']
         YearPublished = request.json['YearPublished']
         Type_book = request.json['Type_book']
        
         update_book.Name_book=Name_book
         update_book.Author=Author
         update_book.YearPublished=YearPublished
         update_book.Type_book=Type_book
         db.session.commit()
         return("book updated")
################crud customers####################
@app.route('/Customers/<id>/',methods =['GET','DELETE','PUT'])
@app.route('/Customers/',methods =['GET','POST'])
def c_customers(id=0):
    if request.method =='POST':
        request.data=request.get_json()
        Name_cus=request.data["Name_cus"]
        City_cus = request.data['City_cus']
        Age_cus = request.data['Age_cus']
        newCustomer=Customers(Name_cus, City_cus, Age_cus)
        db.session.add(newCustomer)
        db.session.commit()
        
        return "A New customer added"
        

    if request.method =='GET':
        res=[]
        for customer in Customers.query.all():
            res.append({"id":customer.id,"Name_customer": customer.Name_cus,"City":customer.City_cus,
            "Age":customer.Age_cus})
        return (json.dumps(res))

    if request.method=='DELETE':
         del_customer=Customers.query.get(id)
         db.session.delete(del_customer)
         db.session.commit()
         return("customer deleted")


        
    if request.method=='PUT':
         update_customer = Customers.query.get(id)
         Name_cus=request.json['Name_cus']
         City_cus = request.json['City_cus']
         Age_cus = request.json['Age_cus']
         
         update_customer.Name_cus=Name_cus
         update_customer.City_cus=City_cus
         update_customer.Age_cus=Age_cus
         db.session.commit()
         return("customer updated")


         #########crud loans##########

   
         #####
@app.route('/Loans/<id>/',methods =['GET','DELETE','PUT'])
@app.route('/Loans/',methods =['GET','POST'])
def c_loans(id=0):
    if request.method =='POST':
        request.data=request.get_json()
        Loandate = request.data['Loandate']
        customer_id=request.data['customer_id']
        book_id = request.data['book_id']
        loanbook=Books.query.get(book_id)####get specific book 
        
        Returndate= datetime.strptime(Loandate, "%Y-%m-%d")+ timedelta(days=books_days_by_type[loanbook.Type_book])
        #######creat return dates according to book type
        
        newLoan=Loans(Loandate,Returndate.date(),customer_id, book_id)
        db.session.add(newLoan)
        db.session.commit()
        
        return "A New loan added"
        

    if request.method =='GET':
        res=[]
        

        for Loan,Book,Customer in db.session.query(Loans,Books,Customers).join(Books).join(Customers):
            compare_date = datetime.strptime(Loan.Returndate, "%Y-%m-%d")#date of return
            today =  datetime.now() #today
    
            loan_status=[]
            if (today.date() < compare_date.date()):
                loan_status = "on time"
            elif (today.date() == compare_date.date()): 
                loan_status = "due today!"
            else:
                loan_status = "late"
            res.append({"Loan_id":Loan.id,
            "Loandate":Loan.Loandate,
            "Returndate":Loan.Returndate,
            "loan_status":loan_status,
            "customer_id": Loan.customer_id,
            "Customer name":Customer.Name_cus,
            "BookId":Loan.book_id,
            "Book name":Book.Name_book})

        

        return (json.dumps(res))

    if request.method=='DELETE':
         del_loan=Loans.query.get(id)
         db.session.delete(del_loan)
         db.session.commit()
         return("loan deleted")


        
    if request.method=='PUT':
         update_loan = Loans.query.get(id)
         Loandate=request.json['Loandate']
         Returndate = request.json['Returndate']
         customer_id = request.json['customer_id']
         book_id = request.json['book_id']
        
         update_loan.Loandate=Loandate
         update_loan.Returndate=Returndate
         update_loan.customer_id=customer_id
         update_loan.book_id=book_id
         db.session.commit()
         return("loan updated")

if __name__ == '__main__':
    with app.app_context():db.create_all()
    app.run(debug = True)