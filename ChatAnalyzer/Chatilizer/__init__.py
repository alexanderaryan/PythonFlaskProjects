from flask import Flask,redirect,render_template,session,flash
from Chatilizer.chat import dataframe_parse,logger
from Chatilizer.forms import UpdateUserForm
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['UPLOAD_FOLDER'] = "D:\Localgit\PuppyFlask\PythonWork\ChatAnalyzer"
#app.config['UPLOAD_FOLDER'] = "CHATILYTIKZ/files/home/CHATILYTIKZ/ChatAnalyzer/files"
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
app.config['RECAPTCHA_OPTIONS']= {'theme':'dark'}

@app.route('/',methods=['GET','POST'])
def index():

    form = UpdateUserForm()

    logger.error(form.errors)
    logger.info(form.data)

    if form.validate_on_submit():
        logger.info("Filename received from user %s",form.chat_file.data.filename)
        session['filename'] = secure_filename(form.chat_file.data.filename)
        if form.chat_file.data.filename.count("WhatsApp Chat with")==1:
            session['file_name'] = form.chat_file.data.filename.split("WhatsApp Chat with")[1].split('.txt')[0]
            logger.info("Valid Whatsapp file deducted %s", session['file_name'])

        else:
            session['file_name'] = form.chat_file.data.filename
            logger.warning("Invalid Whatsapp file deducted %s", session['file_name'])
        session['file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], session['filename'])
        try:
            form.chat_file.data.save(session['file_path'])
        except:
            logger.error("Unable to save file in the path %s",session['file_path'])
        else:
            logger.info("File saved successfully in the path %s",session['file_path'])

        #session['parsedData'] = dataframe_parse(session['file_path'])
        try:
            session['max_date'],session['min_date'],session['emoji_list'], \
            session['word_list'],session['emoji_stacked_data'], \
            session['final_output'],session['total_members'],session['total'],\
                session['most'],session['longest_msg_count'],\
                session['longest_msg_Author'],session['time_group'],\
                session['year_group'],session['cal_group'],\
                session['changed_auth'],session['left_people'],\
            session['removed_people'],session['added_people']= dataframe_parse(
                session['file_path'])


            #print (session['emoji_list'],session['emoji_stacked_data'], session['sent_emoji'],session['final_output'])
            logger.info("Session data %s",session)



        except:
            flash("Is this a valid Chat file? Check it.","Asshole!!")
            logger.error("Invalid File Submitted!!")
            return render_template('index.html', form=form,flash=flash)
        else:

            if os.path.exists(session['file_path']):
                os.remove(session['file_path'])
                logger.info("Deleted the source file of the session %s", session['file_path'])
            else:
                logger.error("No .txt files in the directory")

            return render_template("results.html", filename=session["file_name"],
                                   max_date=session['max_date'],
                                   min_date=session['min_date'],
                                   emoji_list=session['emoji_list'],
                                   word_list=session['word_list'],
                                   emoji_stacked_data_title=session['emoji_stacked_data'][0],
                                   emoji_stacked_data=session['emoji_stacked_data'][1],
                                   final_output=session['final_output'],
                                   total_members=session['total_members'],
                                   total=session['total'], most=session['most'],
                                   longest_msg_count=session['longest_msg_count'],
                                   longest_msg_Author=session['longest_msg_Author'],
                                   time_group=session['time_group'],
                                   year_group=session['year_group'],
                                   cal_group=session['cal_group'],
                                   changed_auth=session['changed_auth'],
                                   left_people=session['left_people'],
                                   removed_people=session['removed_people'],
                                   added_people=session['added_people']
                                   )

    return render_template('index.html',form=form,flash=form.errors)

@app.route("/demo")
def howto():
    return render_template("howto.html")