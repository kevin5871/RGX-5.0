import pymongo
import logging
from cryptography.fernet import Fernet

class login1() :
    def login(self, db, id1, pw, mode=0) :
        test_collection = db.test_collection
        list = test_collection.find({"id" : id1}, {"_id" : 0})
        for x in list :
            f = open('assets/account.bin', 'rb')
            key = 0 
            key = f.readline()
            ci = Fernet(key) 
            text = x['pw']
            decrypt = ci.decrypt(text)
            decrypt = decrypt.decode()
            if(decrypt == pw) :
                if(mode == 0) :
                    #print("Login Success!")
                    logging.info('Login Success!')
                else :
                    #print("Register Complete (2/2) | Verification Success!")
                    logging.info('Register Complete (2/2) | Verification Success!')
                #print("id : " + str(x['id']) + "\nscore : " + str(x['score']))
                return 0, x
            elif(decrypt != pw) :
                #print("Password Incorrect")
                logging.error('Password Incorrect!')
                return 1, None
            else :
                #print("Login Error")
                logging.critical('Login Error')
                return -1, None

    def register(self, db, id1, pw) : 
        if (len(id1) < 2 or id1.find(' ') != -1) :
            return -3, None
        elif (len(pw) < 4) :
            return -4, None
        else :
            test_collection = db.test_collection
            f = open('assets/account.bin', 'rb')
            key = 0 
            key = f.readline()
            ci = Fernet(key) 
            text = ci.encrypt(pw.encode())
            f.close()
            post = {
            "id" : id1,
            "pw" : text,
            "level" : 1,
            "exp" : 0
            }
            test_collection.insert_one(post)
            #print("Register Complete (1/2) | Send to server complete!")
            logging.info('Register Complete (1/2) | Send to server complete!')
            #print("Verifying...")
            logging.info('Verifying...')
            stat = self.login(db, id1, pw, 1)
            return stat

    def update(self, id1, upscore) :
        a = open('password.txt', 'r').readline()
        client = pymongo.MongoClient("mongodb+srv://new-user1:%s@cluster0.d9loi.gcp.mongodb.net/test?ssl=true&ssl_cert_reqs=CERT_NONE&retryWrites=true&w=majority&serverSelectionTimeoutMS=5000" % a)
        db = client.test
        db.test_collection.update_one({'id' : id1},{'$set':{'score' : upscore}},upsert=False)

    # Main Start
    def main(self, id1, pw) :
        a = open('password.txt', 'r').readline()
        client = pymongo.MongoClient("mongodb+srv://new-user1:%s@cluster0.d9loi.gcp.mongodb.net/test?ssl=true&ssl_cert_reqs=CERT_NONE&retryWrites=true&w=majority&serverSelectionTimeoutMS=5000"% a)
        db = client.test
        test_collection = db.test_collection
        list = test_collection.find({"id" : id1}, {"_id" : 0, "id" : 1})
        count = test_collection.count_documents({"id" : id1})
        if(count != 0) :
            #print("Account Alreay exists. Proceeding to Login...")
            logging.info('Account Already exists. Proceeding to Login...')
            stat, a = self.login(db, id1, pw)
            if(stat == 0) :
                return a
            else :
                return stat
        else :
            #print("No Account Find, Proceeding to Register...")
            logging.warning("No account Find, Proceeding to Reigster...")
            stat, a = self.register(db, id1, pw)
            if(stat == 0) :
                return a
            else :
                return stat
