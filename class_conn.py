from connection import mysql

class connect:
    def __init__(self):
        self.cursor=mysql.connect().cursor()

