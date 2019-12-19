import datetime
import re
import sqlite3
import emoji

class Databaseclass():
    conn = sqlite3.connect("chatilizer.db",detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

    cursor = conn.cursor()

    # create a table
    cursor.execute("drop table chat")
    cursor.execute("""CREATE TABLE chat
                      (moment datetime, source text, message text, 
                       media text, emoji text) 
                   """)

    def __init__(self):
        self.insert_query = """INSERT INTO CHAT (moment, source, message, 
                       media, emoji) values (?,?,?,?,?)"""

    def executequery(self,moment,source,message,media,emoji):
    # insert some data
        values = (moment,source,message,media,emoji)
        self.cursor.execute(self.insert_query,values)
        # save data to database





class Chat():
    d = Databaseclass()
    def __init__(self,filename):
        self.fileopen = open(filename, "r", encoding="utf8")
        self.linecount = 0
        self.mediacount=0
        self.event = 0
        self.ot = 0
        self.name = ''
        self.msg = ''
        self.media = ''
        self.emoji = ''
        self.emojicount = ''
    def messagesplitter(self):
        for n in self.fileopen.readlines():
            msglist = n.split('-')
            if re.findall("\d\d/\d\d/\d\d\d\d", n):
                dattime = msglist[0]

                try:
                    if "<Media omitted>" in msglist[1].split(':')[1]:
                        self.mediacount += 1
                        self.media = msglist[1].split(':')[1]
                        self.name = msglist[1].split(':')[0]
                        self.d.executequery(dattime,self.name,'',self.media,'')

                except:
                    self.event += 1
                    self.name = msglist[1].split()[0]
                    self.msg = msglist[1]
                    self.d.executequery(dattime, self.name, self.msg, '','')

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
                        self.msg= msglist[1].split(':')[1]
                        self.name = msglist[1].split(':')[0]
                        self.d.executequery(dattime, self.name, self.msg, '',self.emoji)

                self.linecount += 1
        self.d.conn.commit()
        self.d.conn.close()





if __name__ == '__main__':
    chat = Chat("D:\Localgit\PythonWork\ChatAnalyzer\WhatsApp.txt")
    chat.messagesplitter()
    print(chat.linecount, "is the number of messages")
    print(chat.mediacount, " is the media count sent")
    print(chat.event, " is the event count ")
    print (chat.ot, " is the total message count")
