import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime

class Firebase_client:
    def __init__(self):
        # Use a service account
        cred = credentials.Certificate('/home/takuma/settings/firebase_account_key.json')
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.count = 0

    def set_firebase(self, u_col_name, data, u_doc_name=None):
        if u_doc_name is None:
            u_doc_name = str(self.count)
            self.count = self.count + 1
        now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        doc_ref = self.db.collection(u_col_name).document(u_doc_name)
        doc_ref.set(data)

    def get_firebase_collection(self, u_col_name):
        users_ref = self.db.collection(u_col_name)
        docs = users_ref.get()
        for doc in docs:
            print(u'{} => {}'.format(doc.id, doc.to_dict()))


if __name__ == '__main__':
    cli = Firebase_client()
    data = {
        u'key': u'test',
        u'value': u'aaaaa'
    }
    cli.set_firebase(u'sample', data)
    data = {
        u'key': u'test',
        u'value': u'bbbaa'
    }
    cli.set_firebase(u'sample', data)
    cli.get_firebase_collection(u'sample')
