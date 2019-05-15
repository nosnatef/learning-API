import requests
import config
from PyQt5.QtWidgets import *

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

def get_textbook(access_token,p1,p2,p3,p4):
    
    academic_year = str(p1);
    term = str(p2);
    subject = str(p3);
    course_number = str(p4);
    #academic_year = input("Enter Academic Year:");
    #term = input("Enter term (Fall, Winter, Spring, Summer):");
    #subject = input("Enter subject (abbreviation):");
    #course_number = input("Enter course number:");

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
    return str(res['data']);

def visualize():
    app = QApplication([])
    window = QWidget();
    button = QPushButton('Click')
    text_height = 25;
    text_year = QTextEdit(placeholderText='year');
    text_year.setMaximumHeight(text_height);
    text_term = QTextEdit(placeholderText='term');
    text_term.setMaximumHeight(text_height);
    text_subject = QTextEdit(placeholderText='subject');
    text_subject.setMaximumHeight(text_height);
    text_number = QTextEdit(placeholderText='number');
    text_number.setMaximumHeight(text_height);
    text_result = QTextEdit(placeholderText="result");

    def on_button_clicked():
        result_text = get_textbook(get_access_token(),text_year.toPlainText(),text_term.toPlainText(),text_subject.toPlainText(),text_number.toPlainText());
        text_result.setPlainText(result_text);


    button.clicked.connect(on_button_clicked)
    
    vbox = QVBoxLayout();
    vbox.addWidget(text_year);
    vbox.addWidget(text_term);
    vbox.addWidget(text_subject);
    vbox.addWidget(text_number);
    vbox.addWidget(button);
    vbox.addWidget(text_result);

    window.setLayout(vbox);

    window.show();

    app.exec_()

#access = get_access_token();
#get_textbook(access);

visualize();

