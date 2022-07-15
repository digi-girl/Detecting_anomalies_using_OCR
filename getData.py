from connection import mysql

class getDatas(object):
    def __init__(self):
        self.cursor=mysql.connect().cursor()
    def getAllData(self):
        self.cursor.execute("select * from user")
        aData=self.cursor.fetchall()
        return aData
    def getOne(self,id):
        query_string = "select * from user where id_user = %s"
        self.cursor.execute(query_string, (id,))
        aData = self.cursor.fetchall()
        return aData
    def get_doc_user(self,id):
        query_string = "select doc1sur2,doc2sur2,id_client from user u,user_files uf where u.id_user = uf.id_client and id_client = %s"
        self.cursor.execute(query_string, (id,))
        aData = self.cursor.fetchall()
        self.cursor.close()
        return aData
