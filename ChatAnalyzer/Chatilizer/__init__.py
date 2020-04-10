from flask import Flask,redirect,render_template,session,flash
from Chatilizer.chat import dataframe_parse
from Chatilizer.forms import UpdateUserForm
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['UPLOAD_FOLDER'] = "D:\Localgit\PuppyFlask\PythonWork\ChatAnalyzer"


@app.route('/',methods=['GET','POST'])
def index():

    form = UpdateUserForm()

    print (form.errors)
    print (form.data)

    if form.validate_on_submit():
        print (form.chat_file.data.filename)
        session['filename'] = secure_filename(form.chat_file.data.filename)
        if form.chat_file.data.filename.count("WhatsApp Chat with")==1:
            session['file_name'] = form.chat_file.data.filename.split("WhatsApp Chat with")[1].split('.txt')[0]
        else:
            session['file_name'] = form.chat_file.data.filename
        session['file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], session['filename'])
        form.chat_file.data.save(session['file_path'])

        #session['parsedData'] = dataframe_parse(session['file_path'])
        try:
            session['max_date'],session['min_date'],session['emoji_list'], \
            session['emoji_stacked_data'], session['sent_emoji'],\
            session['final_output'],session['total_members'],session['total'],\
                session['most']= dataframe_parse(
                session['file_path'])
            print ('*'*24)

            #print (session['emoji_list'],session['emoji_stacked_data'], session['sent_emoji'],session['final_output'])
            print (type(session['final_output']))
            print(type(session['emoji_stacked_data']))
            print(type(session['emoji_list']))
            print(type(session['sent_emoji']))
            print (session['total_members'])
            print (type(session['total']))


        except:
            flash="Invalid Chat file"
            print ("Poda fool")
            return render_template('index.html', form=form,flash=flash)
        else:
            return render_template("results.html", filename=session["file_name"],
                                   max_date=session['max_date'],
                                   min_date=session['min_date'], sent_emoji=session['sent_emoji'],
                                   emoji_list=session['emoji_list'],
                                   emoji_stacked_data_title=session['emoji_stacked_data'][0],
                                   emoji_stacked_data=session['emoji_stacked_data'][1],
                                   final_output=session['final_output'],
                                   total_members=session['total_members'],
                                   total=session['total'], most=session['most'])

    return render_template('index.html',form=form)

"""
@app.route('/result')
def result():
    emoji_list, emoji_stacked_data,sent_emoji = dataframe_func("D:\Localgit\PuppyFlask\PythonWork\ChatAnalyzer\WhatsApp Chat with 👊 வாழு..!! வாழ விடு.!! 💦.txt")
    print (emoji_list)
    print (sent_emoji)
    return render_template("index.html",sent_emoji=sent_emoji,emoji_list=emoji_list,emoji_stacked_data_title=emoji_stacked_data[0],emoji_stacked_data=emoji_stacked_data[1])
"""


