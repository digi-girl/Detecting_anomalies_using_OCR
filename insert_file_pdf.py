from connection import mysql

class Save:
    def __init__(self):
        self.cursor=mysql.connect().cursor()
    def convertToBinary(self,filename):
        with open(filename,'rb') as file:
            self.binarydata=file.read()
        return self.binarydata
    def convertBinaryToFile(self,binarydata,filename):
        with open(filename,'wb') as file:
            file.write(binarydata)
    def insert(self):
        query_string ="""insert  into user_files (doc1sur2,	doc2sur2,id_client) values (%s,%s,%s)"""
        convertDoc1=self.convertToBinary("static/docs/doc1sur2.pdf")
        convertDoc2=self.convertToBinary("static/docs/doc2sur2.pdf")
        self.cursor.execute(query_string, (convertDoc1,convertDoc2,1,))
        mysql.connect().commit()
        print("comitted saved")
        self.cursor.close()