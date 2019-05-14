import requests;
import config

client_id = config.API_CONFIG['client_id'];
client_secret = config.API_CONFIG['client_secret'];

def get_access_token():
    url = "https://api.oregonstate.edu/oauth2/token";
    req = requests.post(url,data={
        'grant_type':'client_credentials',
        'client_id':client_id,
        'client_secret':client_secret
    });
    res = req.json();

    access_token = res['access_token'];
    return access_token;

def get_textbook(access_token):
    academic_year = input("Enter Academic Year:");
    term = input("Enter term (Fall, Winter, Spring, Summer):");
    subject = input("Enter subject (abbreviation):");
    course_number = input("Enter course number:");

    url = "https://api.oregonstate.edu/v1/textbooks";
    req = requests.get(url,params={
        "academicYear":academic_year,
        "term":term,
        "subject":subject,
        "courseNumber":course_number
    },headers={
        "Authorization":"Bearer " + access_token
    });
    res = req.json();
    print(res);


access = get_access_token();
get_textbook(access);

