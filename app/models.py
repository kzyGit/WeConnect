import uuid

class Business(object):
    business_list = []
    
    def __init__(self, business_name, about, location, contacts):
        self.businessid=str(uuid.uuid4())
        self.business_name = business_name
        self.location=location
        self.about=about
        self.contacts=contacts
        self.reviews= []


    def save(self, instance):
        Business.business_list.append(instance)

    def get_all(self):
        return Business.business_list

    def delete(self):
        return Business.business_list.remove(self)

class User(object):
    user = []
    def __init__(self, username, email, password):
        self.userid=str(uuid.uuid4())
        self.username = username
        self.email=email
        self.password=password

    def save(self,instance):
        User.user.append(instance)

class Review(object):

    def __init__(self, title, content):

        self.id=str(uuid.uuid4())
        self.title = title
        self.content = content
        


