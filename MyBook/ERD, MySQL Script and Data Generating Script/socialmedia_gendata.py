#Script Used to Generate data for socialmedia database
import csv
import random
from time import time
import datetime
from decimal import Decimal
import string
from faker import Faker
from werkzeug.security import generate_password_hash, check_password_hash

USER_COUNT = 10
PROFILE_COUNT = 10
POST_COUNT = 500
COMMENT_COUNT = 10
GROUP_COUNT = 10
IMAGE_COUNT = 10

#keep track of unique keys for relationship table. If 
unique = set()
    
fake = Faker()


def create_csv_user():
    with open('users.csv', 'w', newline='') as csvfile:
        fieldnames = ['firstname', 'lastname', 'email', 'password_hash']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(USER_COUNT):
            #Generating password causing delay in script all psswords set to 123
            #p = fake.password()
            #ph = generate_password_hash(p, method='pbkdf2:sha256')
            
            ph = 'pbkdf2:sha256:150000$zH5gtyOx$c83f593d8507618930760b7dfb1b0b3fb8614bd63509eec60e9ff309e73c366b'
            writer.writerow(
                {
                    'firstname': fake.first_name(),
                    'lastname': fake.last_name(),
                    'email': fake.email(),
                    'password_hash': ph,
                    
                }
            )

def create_csv_phone():
    with open('telephone.csv', 'w', newline='') as csvfile:
        fieldnames = ['userid','telephoneno', 'areacode'] 
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in range(USER_COUNT):
            writer.writerow(
                {
                    'userid': i+1,
                    'telephoneno': fake.phone_number(),
                    'areacode': fake.country_calling_code(),
                }
            )

def create_csv_test():
    with open('telephone.csv', 'w', newline='') as csvfile:
        fieldnames = ['userid','telephoneno', 'areacode'] 
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in range(USER_COUNT):
            writer.writerow(
                {
                    'userid': i+1,
                    'telephoneno': fake.phone_number(),
                    'areacode': fake.country_calling_code(),
                }
            )
            
            
def create_csv_address():
    with open('address.csv', 'w', newline='') as csvfile:
        fieldnames = ['userid','streetname','city', 'country']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in range(USER_COUNT):
            writer.writerow(
                {
                    'userid': i+1,
                    'streetname': fake.street_name(),
                    'city': fake.city(),
                    'country': fake.country(),
                }
            )
            
            
def create_csv_profile():
    with open('profile.csv', 'w', newline='') as csvfile:
        fieldnames = ['userid','dob','gender','nickname']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(PROFILE_COUNT):
           
            writer.writerow(
                {
                    'userid': i+1,
                    'dob': fake.date_of_birth().strftime('%Y-%m-%d'),
                    'gender': random.choice(['Male', 'Female']),
                    'nickname': fake.user_name(),
                }
            )

def create_csv_image():
    with open('image.csv', 'w', newline='') as csvfile:
        fieldnames = ['image_name', 'directory']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(IMAGE_COUNT):
           
            writer.writerow(
                {
                    'image_name': fake.sentence(random.randrange(1,3)),
                    'directory': 'uploads/default.png',
                }
            )

def create_csv_profile_pic():
    with open('profile_pic.csv', 'w', newline='') as csvfile:
        fieldnames = ['profile_id','image_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(PROFILE_COUNT):
            
            writer.writerow(
                {
                    'profile_id': i+1,
                    'image_id': random.randrange(1, IMAGE_COUNT),
                }
            )

def create_csv_adds():
    with open('adds.csv', 'w', newline='') as csvfile:
        fieldnames = ['image_id','user_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(IMAGE_COUNT):
            
            writer.writerow(
                {
                    'image_id': i+1,
                    'user_id': random.randrange(1, USER_COUNT),
                }
            )

            
def create_csv_post():
    with open('post.csv', 'w', newline='') as csvfile:
        fieldnames = ['post_id', 'description', 'post_date', 'post_time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(POST_COUNT):
           
            writer.writerow(
                {                  
                    'description': fake.sentence(random.randrange(3,10)),
                    'post_date': fake.date(),
                    'post_time': fake.time(),             
                }
            )

def create_csv_post_image():
    with open('post_image.csv', 'w', newline='') as csvfile:
        fieldnames = ['post_id', 'image_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(POST_COUNT):
            p = random.randrange(1, POST_COUNT)
            im = random.randrange(1, IMAGE_COUNT)
            primary_key = str(p)+str(im)
            
            while (primary_key in unique or (p==im)):
                print(primary_key, p, im)
                p = random.randrange(1, POST_COUNT)
                im = random.randrange(1, IMAGE_COUNT)
                primary_key = str(p)+str(im)
            
            writer.writerow(
                {
                    'post_id': p,
                    'image_id': im,
                }
            )
            unique.add(primary_key)            

def create_csv_submits():
    with open('submits.csv', 'w', newline='') as csvfile:
        fieldnames = ['post_id','user_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(POST_COUNT):
            
            writer.writerow(
                {
                    'post_id': i+1,
                    'user_id': random.randrange(1, USER_COUNT),
                }
            )
            
def create_csv_comment():
    with open('comment.csv', 'w', newline='') as csvfile:
        fieldnames = ['post_id','usr_text', 'com_date','com_time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(COMMENT_COUNT):
           
            writer.writerow(
                {
                    'post_id': random.randrange(1, POST_COUNT),
                    'usr_text': fake.sentence(random.randrange(3,10)),
                    'com_date': fake.date(),
                    'com_time': fake.time(),
                }
            )

def create_csv_commented():
    with open('commented.csv', 'w', newline='') as csvfile:
        fieldnames = ['user_id', 'com_id', 'post_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(COMMENT_COUNT):
            writer.writerow(
                {
                    'user_id': random.randrange(1, USER_COUNT),
                    'com_id': i+1,
                    'post_id': random.randrange(1, POST_COUNT),
                }
            )            

def create_csv_group1():
    with open('group1.csv', 'w', newline='') as csvfile:
        fieldnames = ['group_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(4, GROUP_COUNT):
           
            writer.writerow(
                {
                    'group_name': fake.sentence(random.randrange(1,3)),
                    
                }
            )

def create_csv_friend_with():
    with open('friends_with.csv', 'w', newline='') as csvfile:
        fieldnames = ['user_id', 'friend_id', 'group_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(USER_COUNT):
            u = random.randrange(1, USER_COUNT)
            f = random.randrange(1, USER_COUNT)
            primary_key = str(u)+str(f)
            
            while (primary_key in unique or (u==f)):
                   print(primary_key, u, f)
                   u = random.randrange(1, USER_COUNT)
                   f = random.randrange(1, USER_COUNT)
                   primary_key = str(u)+str(f)
            
            writer.writerow(
                {
                    'user_id': u,
                    'friend_id': f,
                    'group_id': random.randrange(1, 4),
                }
            )
            unique.add(primary_key)

def create_csv_creates():
    with open('creates.csv', 'w', newline='') as csvfile:
        fieldnames = ['editor_id', 'group_id', 'user_id', 'create_date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(GROUP_COUNT):
            u = random.randrange(1, USER_COUNT)
            e = random.randrange(1, USER_COUNT)
            primary_key = str(u)+str(e)
            
            while (primary_key in unique or (u==e)):
                   print(primary_key, u, e)
                   u = random.randrange(1, USER_COUNT)
                   e = random.randrange(1, USER_COUNT)
                   primary_key = str(u)+str(e)
            
            writer.writerow(
                {
                    'editor_id': e,
                    'group_id': random.randrange(1, GROUP_COUNT),
                    'user_id': u,
                    'create_date': fake.date(),
                }
            )
            unique.add(primary_key)

def create_csv_joins():
    with open('creates.csv', 'w', newline='') as csvfile:
        fieldnames = ['user_id', 'group_id','join_date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(GROUP_COUNT):
            u = random.randrange(1, USER_COUNT)
            e = random.randrange(1, USER_COUNT)
            primary_key = str(u)+str(e)
            
            while (primary_key in unique or (u==e)):
                   print(primary_key, u, e)
                   u = random.randrange(1, USER_COUNT)
                   e = random.randrange(1, USER_COUNT)
                   primary_key = str(u)+str(e)
            
            writer.writerow(
                {
                    'user_id': u,
                    'group_id': random.randrange(1, GROUP_COUNT),
                    'join_date': fake.date(),
                }
            )
            unique.add(primary_key)

def create_csv_belongs():
    with open('belongs.csv', 'w', newline='') as csvfile:
        fieldnames = ['post_id','group_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(POST_COUNT):
            
            writer.writerow(
                {
                    'post_id': i+1,
                    'group_id': random.randrange(1, GROUP_COUNT),
                }
            )
         

if __name__ == '__main__':

    create_csv_image()
    create_csv_user()
    create_csv_phone()
    create_csv_address()
    create_csv_profile()
    create_csv_image()
    create_csv_profile_pic()
    create_csv_adds()
    create_csv_post()
    create_csv_post_image()
    create_csv_submits()
    create_csv_comment()
    create_csv_commented()
    create_csv_group1()

    create_csv_friend_with()
    unique = set()
    
    create_csv_creates()
    unique = set()

    create_csv_joins()
    unique = set()

    create_csv_belongs()

    
    
    
    
    

