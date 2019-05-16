import requests
import config
import json
from PyQt5 import QtWidgets


client_id = config.API_CONFIG['client_id']
client_secret = config.API_CONFIG['client_secret']

def get_access_token():
    url = "https://api.oregonstate.edu/oauth2/token"
    req = requests.post(url,data={
        'grant_type':'client_credentials',
        'client_id':client_id,
        'client_secret':client_secret
    })
    res = req.json()

    try:
        access_token = res['access_token']
    except KeyError:
        access_token = "Error"
    return access_token

def get_textbook(access_token,academic_year,term,subject,course_number):

    url = "https://api.oregonstate.edu/v1/textbooks"
    req = requests.get(url,params={
        "academicYear":academic_year,
        "term":term,
        "subject":subject,
        "courseNumber":course_number
    },headers={
        "Authorization":"Bearer " + access_token
    })
    res = req.json()
    try:
        res['data']
    except KeyError:
        return res['userMessage'] + "\n" + res['developerMessage']
    return res['data']

def pretty_textbook(textbooks):
    try:
        textbooks[0]['id']
    except (TypeError,KeyError) as e:
        return textbooks;
    except (IndexError) as e:
        return "Course not exist."
    count = 1
    ret = ""
    for textbook in textbooks:
        ret += "Textbook " + str(count) + ":\n"
        try:
            ret += "Title: " + textbook['attributes']['title'] + "\n"
            ret += "Author: " + textbook['attributes']['author'] + "\n"
            ret += "Edition: " + str(textbook['attributes']['edition']) + "\n"
            ret += "Year: " + str(textbook['attributes']['copyrightYear']) + "\n"
            ret += "New Book Price: " + str(textbook['attributes']['priceNewUSD']) + "\n"
            ret += "Used Book Price: " + str(textbook['attributes']['priceUsedUSD']) + "\n"
            ret += "\n"
            count += 1
        except (TypeError, KeyError) as e:
            ret += "Bad data of this textbook. \n\n"
    return ret

def visualize():
    app = QtWidgets.QApplication([])
    window = QtWidgets.QWidget()
    button = QtWidgets.QPushButton('Click')
    text_height = 25
    text_year = QtWidgets.QTextEdit(placeholderText='year')
    text_year.setMaximumHeight(text_height)
    text_term = QtWidgets.QTextEdit(placeholderText='term')
    text_term.setMaximumHeight(text_height)
    text_subject = QtWidgets.QTextEdit(placeholderText='subject')
    text_subject.setMaximumHeight(text_height)
    text_number = QtWidgets.QTextEdit(placeholderText='number')
    text_number.setMaximumHeight(text_height)
    text_result = QtWidgets.QTextEdit(placeholderText="result")

    example_label_year = QtWidgets.QLabel("Example: 2019")
    example_label_term = QtWidgets.QLabel("Example: Spring")
    example_label_subject = QtWidgets.QLabel("Example: CS")
    example_label_number = QtWidgets.QLabel("Example: 161")

    def on_button_clicked():
        ac = get_access_token()
        if ac == "Error":
            result_text = "Credential Error. Check config file."
        else:
            result_text = get_textbook(ac,text_year.toPlainText(),text_term.toPlainText(),text_subject.toPlainText(),text_number.toPlainText())
            result_text = pretty_textbook(result_text)
        text_result.setPlainText(str(result_text))


    button.clicked.connect(on_button_clicked)
    
    vbox = QtWidgets.QVBoxLayout()
    vbox.addWidget(text_year)
    vbox.addWidget(example_label_year)
    
    vbox.addWidget(text_term)
    vbox.addWidget(example_label_term)

    vbox.addWidget(text_subject)
    vbox.addWidget(example_label_subject)
    
    vbox.addWidget(text_number)
    vbox.addWidget(example_label_number)

    vbox.addWidget(button)
    vbox.addWidget(text_result)

    window.setLayout(vbox)

    window.show()

    app.exec_()

visualize()

