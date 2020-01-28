from datetime import datetime
import re
import sqlite3
import emoji


class Chat(object):

    def __init__(self, filename, your_name):
        self.fileopen = open(filename, "r", encoding="utf8")
        self.filename = filename.split("WhatsApp Chat with ")[-1]
        self.linecount = 0
        self.mediacount=0
        self.event = 0
        self.ot = 0
        self.your_name = your_name
        self.name = ''
        self.msg = ''
        self.media = ''
        self.emoji = ''
        self.emojicount = ''
        self.d = Chat_data_analytics(self.your_name)

    def messagesplitter(self):
        for n in self.fileopen.readlines():
            msglist = n.split('-')

            if re.findall("\d\d/\d\d/\d\d\d\d,", n):
                dattime = datetime.strptime(str(msglist[0].replace(',','').strip()),"%d/%m/%Y %I:%M %p")

                try:
                    if "<Media omitted>" in msglist[1].split(':')[1]:
                        self.mediacount += 1
                        self.media = msglist[1].split(':')[1].strip()
                        self.name = msglist[1].split(':')[0].strip()
                        self.d.executequery(dattime,self.name,None,self.media,None)

                except:
                    self.event += 1
                    if " left" in msglist[1]:
                        self.name = msglist[1].split('left')[0].strip()
                    elif " changed" in msglist[1]:
                        self.name = msglist[1].split('changed')[0].strip()
                    elif " added" in msglist[1]:
                        self.name = msglist[1].split('added')[0].strip()
                    self.msg = msglist[1].strip()
                    if self.name == 'You':
                        self.name = self.your_name
                    self.d.executequery(dattime, self.name, self.msg, None,None)

                else:
                    if "<Media omitted>" not in msglist[1].split(':')[1]:
                        self.ot += 1
                        msg = msglist[1].split(':')[1]
                        self.emoji = ""
                        for letter in msg:
                            #if letter.isalnum()==False and letter not in ["?","."]:
                            if emoji.demojize(letter)!=letter:
                                self.emoji = self.emoji + letter
                                #print (self.emoji)
                        self.msg= msglist[1].split(':')[1].strip()
                        self.name = msglist[1].split(':')[0].strip()
                        if self.emoji != "":
                            self.d.executequery(dattime, self.name, self.msg, None,self.emoji)
                        else:
                            self.d.executequery(dattime, self.name, self.msg, None, None)
                self.linecount += 1
        self.d.conn.commit()
        self.d.select_data()
        self.d.conn.close()


class Databaseclass(object):
    conn = sqlite3.connect("chatilizer.db",detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

    cursor = conn.cursor()

    # create a table
    try:
        cursor.execute("drop table chat")
    except:
        cursor.execute("""CREATE TABLE chat
                      (MOMENT timestamp, SOURCE text, MESSAGE text, 
                       MEDIA text, EMOJI text) 
                   """)
    else:
        cursor.execute("""CREATE TABLE chat
                              (MOMENT timestamp, SOURCE text, MESSAGE text, 
                               MEDIA text, EMOJI text) 
                           """)

    def __init__(self):
        self.insert_query = """INSERT INTO CHAT (moment, source, message, 
                       media, emoji) values (?,?,?,?,?)"""

    def executequery(self,moment,source,message,media,emoji):
    # insert some data
        values = (moment,source,message,media,emoji)
        self.cursor.execute(self.insert_query,values)
        # save data to database


class Chat_data_analytics(Databaseclass,Chat):
    def __init__(self,name):
        Databaseclass.__init__(self)
        self.name = name
        self.select_source_query = """SELECT distinct(replace(source,'You','{}')) from chat where source not in ('');""".format(self.name)
        #self.mode_to_be_calculated = ['MESSAGE','MEDIA','EMOJI']
        self.mode_to_be_calculated = {'MESSAGE':"Select source,count(message) from chat where source<>'' group by source",
                                      'MEDIA':"Select source,count(media) from chat where source<>'' group by source",
                                      'EMOJI':"Select source,sum(length(emoji)) from chat where source<>'' group by source"}
        self.first_message_moment = """SELECT min(moment),SOURCE from chat where source<>'' order by moment;"""
        self.event_to_be_calculated = ['% changed%','% added %','% left']
        self.event_dictionary = {1:'Once',2:'Twice',3:'Thrice'}
        self.event_type_dictionary = {"added": "Added people in this group %s",
                                      "changed":"Changed this group name/icon %s",
                                      "left":"Left this group %s"}
        self.event_query = """Select source,count(*) from chat where message like ? group by source"""
        self.message_count_query = """select count(message) from chat where source<>''"""
        #print (self.select_source_query)
        self.source_list = []
        self.emoji_count_query = """select sum(length(emoji)) from chat where EMOJI is not null"""


    def select_data(self):
        self.cursor.execute(self.message_count_query)
        total_message_count = self.cursor.fetchall()[0][0]

        self.cursor.execute(self.emoji_count_query)
        emoji_count = self.cursor.fetchall()[0][0]

        self.cursor.execute(self.first_message_moment)
        first_message_collection = self.cursor.fetchone()
        print("*"+chat.filename.strip(".txt")+"*","conversation has it's first message since", first_message_collection[0], "sent by ", first_message_collection[1])

        self.cursor.execute(self.select_source_query)
        source_collection = self.cursor.fetchall()
        for source in source_collection:
            self.source_list.append(source[0])
        print ("There are ",len(self.source_list),"Participants in this group. They are", ",".join(self.source_list).upper())
        print(chat.linecount, "is the total number of messages")


        for every in self.mode_to_be_calculated.keys():
            message_mode=every+'S'
            print ("*"+message_mode.replace('MEDIAS','MEDIA')+"*")
            #print (self.mode_to_be_calculated[every])
            self.cursor.execute(self.mode_to_be_calculated[every])
            message_count = self.cursor.fetchall()
            if every=='MESSAGE':
                print (total_message_count, "is the number of messages shared in text")
            elif every=='MEDIA':
                print (chat.mediacount,"is the number of media shared")
            elif every == 'EMOJI':
                print(emoji_count, "is the total emojis shared")
            for msg_cnt in message_count:
                print (msg_cnt[0].capitalize(),"sent ", msg_cnt[1], message_mode.replace('MEDIAS','MEDIA'))

        if len(self.source_list)>2:
            for event in self.event_to_be_calculated:
                #print (event)
                event_type=event.replace('%','').strip()
                print("*"+event_type.upper()+"*")
                self.cursor.execute(self.event_query,(event,))
                #self.cursor.execute(self.event_query%event)
                event_count = self.cursor.fetchall()
                #print (event_count)
                #print (self.event_query)

                for events in event_count:
                    times = self.event_dictionary.setdefault(events[1], str(events[1]) + " times")
                    print (events[0],
                           self.event_type_dictionary[event_type.lower()]%times)



if __name__ == '__main__':
    chat = Chat("D:\Localgit\PythonWork\ChatAnalyzer\WhatsApp Chat with Sukhanubavam 😈.txt","Alex")
    chat.messagesplitter()

