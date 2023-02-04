from bson.objectid import ObjectId
from models.models import Database
from datetime import date


class Mongo(Database):
    def __init__(self, collection):
        self.db = Mongo.db_name[collection]

    def add_project(self, title, subtitle, url, body):
        """
        Proje eklemek için kullanılacak
        """
        new_data = {"title": title,
                    "subtitle": subtitle,
                    "img_url": url,
                    "body": body,
                    "comment": []
                    }
        self.db.insert_one(new_data)

    def get_projects(self):
        """
        iterable bir pymongo objesi döndürüyor.For loop ile 
        döngüye alıp dictionary methodlarını uygulayabilirsiniz.
        Örnek Sonuç: <pymongo.cursor.Cursor object at 0x7fdc3ba6e1d0>
        """
        projects = self.db.find()
        return projects

    def get_project(self, id):
        """
        ID sini girdiğiniz kayıdı döndürüyor.
        type: dict
        """
        objInstance = ObjectId(id)
        project = self.db.find_one({"_id": objInstance})
        return project

    def delete_project(self, id):
        """
        ID si girilen kayıdı collection dan siler.
        """
        objInstance = ObjectId(id)
        self.db.delete_one({"_id": objInstance})

    def update_project(self, id, new_title, new_subtitle, new_url, new_body):
        """
        id ye Hangi proje değişcekse onun ID sini veriyoruz.
        Geri kalanları formdan gelen yeni datalar.
        """
        project = self.get_project(id)
        old_query = {"title": project["title"]}
        new_query = {"$set": {
            "title": new_title,
            "subtitle": new_subtitle,
            "img_url": new_url,
            "body": new_body
        }}
        self.db.update_one(old_query, new_query)

    def add_comment(self, id, text, author):
        """
        id ye hangi proye yorum eklenicekse onun ID si
        'text' ve 'author' Formdan gelen bilgiler için.
        """
        objInstance = ObjectId(id)
        project_filter = {"_id": objInstance}
        new_values = self.db.find_one(project_filter)["comment"]
        new_values.append({"text": text,
                           "author": author,
                           "date": date.today().strftime("%B %d, %Y")
                           })
        self.db.update_one(project_filter, {"$set": {"comment": new_values}})

    def get_comments(self, id):
        """
        id nin ait olduğu projenin içinde olan yorumları
        liste şeklinde döndürür.
        Type : List
        """
        objInstance = ObjectId(id)
        project_filter = {"_id": objInstance}
        comments = self.db.find_one(project_filter)["comment"]
        return comments

    def delete_comment(self, id, comment):
        """
        id ye projenin ID sini veriyoruz 
        comment e [text, author, date] şeklinde bir liste veriyoruz.
        """
        all_comments = self.get_comments(id)
        for data in all_comments:
            text = data["text"]
            author = data["author"]
            date = data["date"]
            if text in comment and author in comment and date in comment:
                all_comments.pop(all_comments.index(data))
                self.db.update_one({"comment": data}, {
                                   "$set": {"comment": all_comments}})

    def delete_comments(self, id):
        """
        ID si verilen projenin tüm yorumlarını siler.
        """
        objInstance = ObjectId(id)
        self.db.update_one({"_id": objInstance}, {"$set": {"comment": []}})
