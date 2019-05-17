from PyQt5 import QtWidgets
import requests

import config


client_id = config.API_CONFIG['client_id']
client_secret = config.API_CONFIG['client_secret']


def get_access_token():
    url = 'https://api.oregonstate.edu/oauth2/token'
    req = requests.post(url, data={
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    })
    res = req.json()

    try:
        access_token = res['access_token']
    except KeyError:
        access_token = 'Error'
    return access_token


def get_textbook(
        access_token,
        academic_year,
        term,
        subject,
        course_number,
        section=None):
    url = 'https://api.oregonstate.edu/v1/textbooks'
    textbook_params = {
        'academicYear': academic_year,
        'term': term,
        'subject': subject,
        'courseNumber': course_number
    }
    if section:
        textbook_params['section'] = section
    req = requests.get(url, params=textbook_params, headers={
        'Authorization': f'Bearer {access_token}'
    })
    res = req.json()
    try:
        return res['data']
    except KeyError:
        return res['userMessage'] + '\n' + res['developerMessage']


def pretty_textbook(textbooks):
    if not textbooks:
        return 'No textbook for this course.'
    try:
        textbooks[0]['id']
    except KeyError:
        return textbooks
    except TypeError:
        return 'Course not exist.'
    count = 1
    ret = ''
    for textbook in textbooks:
        ret += 'Textbook ' + str(count) + ':\n'
        try:
            text_attr = textbook['attributes']
            ret += f"Title: {text_attr['title']}\n"
            ret += f"Author: {text_attr['author']}\n"
            ret += f"Edition: {text_attr['edition']}\n"
            ret += f"Year: {text_attr['copyrightYear']}\n"
            ret += f"New Book Price: {text_attr['priceNewUSD']}\n"
            ret += f"Used Book Price: {text_attr['priceUsedUSD']}\n"
            ret += '\n'
            count += 1
        except KeyError:
            ret += 'Bad data of this textbook. \n\n'
    return ret


def get_textbox(placeholder, height=25):
    ret = QtWidgets.QTextEdit(placeholderText=placeholder)
    ret.setMaximumHeight(height)
    return ret


def visualize():
    app = QtWidgets.QApplication([])
    window = QtWidgets.QWidget()
    button = QtWidgets.QPushButton('Click')

    text_year = get_textbox('year')
    text_term = get_textbox('term')
    text_subject = get_textbox('subject')
    text_number = get_textbox('number')
    text_section = get_textbox('section')
    text_result = QtWidgets.QTextEdit(placeholderText='result')

    example_label_year = QtWidgets.QLabel('Example: 2019')
    example_label_term = QtWidgets.QLabel('Example: Spring')
    example_label_subject = QtWidgets.QLabel('Example: CS')
    example_label_number = QtWidgets.QLabel('Example: 161')
    example_label_section = QtWidgets.QLabel('(Optional) Example: 001')

    def on_button_clicked():
        ac = get_access_token()
        if ac == 'Error':
            result_text = 'Credential Error. Check config file.'
        else:
            text_year_text = text_year.toPlainText()
            text_subject_text = text_subject.toPlainText()
            text_number_text = text_number.toPlainText()
            text_term_text = text_term.toPlainText()
            text_section_text = text_section.toPlainText()
            result_text = get_textbook(
                ac,
                text_year_text,
                text_term_text,
                text_subject_text,
                text_number_text,
                text_section_text
            )
            result_text = pretty_textbook(result_text)
        text_result.setPlainText(str(result_text))

    button.clicked.connect(on_button_clicked)

    widget_list = [
                text_year,
                example_label_year,
                text_term,
                example_label_term,
                text_subject,
                example_label_subject,
                text_number,
                example_label_number,
                text_section,
                example_label_section,
                button,
                text_result]

    vbox = QtWidgets.QVBoxLayout()

    for widget in widget_list:
        vbox.addWidget(widget)

    window.setLayout(vbox)

    window.show()

    app.exec_()


visualize()
