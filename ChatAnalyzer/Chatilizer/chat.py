import re
import pandas as pd
import emoji,string
from collections import Counter
import numpy


def startsWithDateTime(s):
    pattern = '^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)(\d{2}|\d{4}), (([0-9]|)[0-9]):([0-9][0-9]) ([a|p]m) -'
    result = re.match(pattern, s)
    if result:
        return True
    return False

def  tosplitauthor(s):
    try:
        author = s.split('-')[1].split(':')[0]
        print (author)
    except:
        author=None
        print (author,s)
    else:
        print (author)


def startsWithAuthor(s):
    patterns = [
        '([\w]+):',                        # First Name
        '([\w]+[\s]+[\w]+):',              # First Name + Last Name
        '([\w]+[\s]+[\w]+[\s]+[\w]+):',    # First Name + Middle Name + Last Name
        '([+]\d{2} \d{5} \d{5}):',         # Mobile Number (India)
        '([+]\d{2} \d{3} \d{3} \d{4}):',   # Mobile Number (US)
        '([+]\d{2} \d{4} \d{7})'           # Mobile Number (Europe)
    ]
    pattern = '^' + '|'.join(patterns)
    result = re.match(pattern, s)
    if result:
        return True
    return False


def getDataPoint(line):
    # line = 18/06/17, 22:47 - Loki: Why do you have 2 numbers, Banner?

    splitLine = line.split(' - ')  # splitLine = ['18/06/17, 22:47', 'Loki: Why do you have 2 numbers, Banner?']

    dateTime = splitLine[0]  # dateTime = '18/06/17, 22:47'

    date, time = dateTime.split(', ')  # date = '18/06/17'; time = '22:47'

    message = ' '.join(splitLine[1:])  # message = 'Loki: Why do you have 2 numbers, Banner?'

    if startsWithAuthor(message):  # True
        splitMessage = message.split(': ')  # splitMessage = ['Loki', 'Why do you have 2 numbers, Banner?']
        author = splitMessage[0]  # author = 'Loki'
        message = ' '.join(splitMessage[1:])  # message = 'Why do you have 2 numbers, Banner?'
    else:
        author = None
    return date, time, author, message

def dataframe_parse(filename):
    parsedData = []  # List to keep track of data so it can be used by a Pandas dataframe
    conversationPath = filename
    with open(conversationPath, encoding="utf-8") as fp:
        fp.readline()  # Skipping first line of the file (usually contains information about end-to-end encryption)

        messageBuffer = []  # Buffer to capture intermediate output for multi-line messages
        date, time, author = None, None, None  # Intermediate variables to keep track of the current message being processed

        while True:
            line = fp.readline()
            if not line:  # Stop reading further if end of file has been reached
                parsedData.append([date, time, author, ' '.join(messageBuffer)])
                break
            # print (line)
            line = line.strip()  # Guarding against erroneous leading and trailing whitespaces
            if startsWithDateTime(
                    line):  # If a line starts with a Date Time pattern, then this indicates the beginning of a new message
                if len(messageBuffer) > 0:  # Check if the message buffer contains characters from previous iterations
                    # print (messageBuffer)
                    parsedData.append([date, time, author,
                                       ' '.join(messageBuffer)])  # Save the tokens from the previous message in parsedData
                messageBuffer.clear()  # Clear the message buffer so that it can be used for the next message
                date, time, author, message = getDataPoint(line)  # Identify and extract tokens from the line
                messageBuffer.append(message)  # Append message to buffer

            else:
                messageBuffer.append(
                    line)  # If a line doesn't start with a Date Time pattern, then it is part of a multi-line message. So, just append to buffer


    print (parsedData[0][0])
    if parsedData[0][0]!=None:

        print ("Entered")
        df = pd.DataFrame(parsedData, columns=['Date', 'Time', 'Author', 'Message'])

        print (df.head())

        author_value_counts = df['Author'].value_counts()  # Number of messages per author

        media_messages_df = df[df['Message'] == '<Media omitted>']

        author_media_messages_value_counts = media_messages_df['Author'].value_counts()

        df['Letter_Count'] = df['Message'].apply(lambda s: len(s))

        df['Emoji_Count'] = df['Message'].apply(lambda s: emoji.emoji_count(s))
        df['Emojis'] = df['Message'].apply(lambda s: [n for n in s if emoji.demojize(n) != n \
                                                      and emoji.demojize(n).count('skin_tone')==0\
                                                      and  emoji.demojize(n).count('male_sign')==0])

        df['Word_Count'] = df['Message'].apply(lambda s: len([w for w in s.split(' ') if w not in string.punctuation]))

        emoji_data = df[df.Emojis.apply(lambda s: s if s != [] else None).notnull()]

        emoji_list = Counter([n for ind, val in emoji_data.Emojis.items() for n in val]).most_common(10)

        df['Letter_Count'].sum(), df['Word_Count'].sum(), df['Emoji_Count'].sum(), df.Message.count(), df.Author.count()

        df['Changed_Author'] = df.loc[
            (df['Author'].isnull()) & (df['Message'].str.contains('changed|deleted', regex=True))].Message.apply(
            lambda s: re.sub(r' (changed|deleted).*$', '', s) if re.sub(r' (changed|deleted).*$','',s)!= 'You' else numpy.NaN)


        df['Added_Author'] = df.loc[
            (df['Author'].isnull()) & (df['Message'].str.contains('added', regex=True))].Message.apply(
            lambda s: re.sub(r' added.*$', '', s))


        df['Removed_Author'] = df.loc[
            (df['Author'].isnull()) & (df['Message'].str.contains('removed', regex=True))].Message.apply(
            lambda s: re.sub(r' removed.*$', '', s))


        df['Left_People'] = df.loc[
            (df['Author'].isnull()) & (df['Message'].str.contains('left$', regex=True))].Message.apply(
            lambda s: re.sub(r' left$', '', s))

        print("Total Message Sent : ", df.count().Author)
        print("Users Contributed Count : ", df['Author'].nunique())
        print("Users Contributed : ", df['Author'].dropna().unique())

        print(df['Word_Count'].max())
        longest_message, longest_msg = df['Word_Count'].max(), df.iloc[df.Word_Count.idxmax()][['Message', 'Author']]

        print("""Longest Message is sent by : " """, longest_msg.Author, """" and the message has : """, longest_message,
              """ words""")

        print("Total Emoji Sent : ", df[df['Author'].notnull()].Emoji_Count.sum())
        msg_emoji = df.groupby(['Author']).sum()['Emoji_Count']
        group_name_emoji = df.groupby(['Changed_Author']).sum()['Emoji_Count']


        sent_emoji = msg_emoji.add(group_name_emoji, fill_value=0).apply(lambda s: int(s))

        msg_word_by_author = df.groupby(['Author']).sum()['Word_Count']
        changed_word_by_author = df.groupby(['Changed_Author']).sum()['Word_Count']
        print("Total Words : ", df[(df['Author'].notnull()) | (df['Changed_Author'].notnull())].Word_Count.sum())
        words_by_author = msg_word_by_author.add(changed_word_by_author, fill_value=0).apply(lambda s: int(s))

        author_media_messages_value_counts = author_media_messages_value_counts.apply(lambda s: int(s))
        print(type(author_media_messages_value_counts))
        print(type(words_by_author))
        print(type(sent_emoji))
        print(type(author_media_messages_value_counts))

        def emoji_per_person_usage_cal(emoji_list, emoji_values):
            emoji_stacked_data = {'Name': []}
            for emo in emoji_list:
                for author, data in emoji_values:
                    if emoji_stacked_data['Name'].count(author) == 0:
                        emoji_stacked_data['Name'].append(author)

                    if not emoji_stacked_data.get(emo[0]):
                        emoji_stacked_data[emo[0]] = []
                        emoji_stacked_data[emo[0]].append(
                            [n for ind, val in data.items() for n in val if val != []].count(emo[0]))
                    else:
                        emoji_stacked_data[emo[0]].append(
                            [n for ind, val in data.items() for n in val if val != []].count(emo[0]))
            return emoji_stacked_data

        emoji_data = df[df.Emojis.apply(lambda s: s if s != [] else None).notnull()]
        emoji_list = Counter([n for ind, val in emoji_data.Emojis.items() for n in val]).most_common(10)

        message_emoji = df.groupby(['Author']).Emojis
        group_name_emoji = df.groupby(['Changed_Author']).Emojis

        msg_emoji_stacked_data = emoji_per_person_usage_cal(emoji_list, message_emoji)

        group_emoji_stacked_data = emoji_per_person_usage_cal(emoji_list, group_name_emoji)

        # print (msg_emoji_stacked_data)
        # print (group_emoji_stacked_data)

        for key, value in group_emoji_stacked_data.items():
            if key != 'Name':

                if sum(value) > 0:
                    # print (value)
                    greater_value = [ind for ind, val in enumerate(value) if val > 0]
                    for val in greater_value:
                        # print (group_emoji_stacked_data['Name'][value.index(val)],key)
                        try:
                            msg_emoji_stacked_data['Name'].index(group_emoji_stacked_data['Name'][value.index(val)])
                        except:
                            pass
                        else:
                            name_col = msg_emoji_stacked_data['Name'].index(
                                group_emoji_stacked_data['Name'][value.index(val)])
                            # print (name_col)
                            # print (msg_emoji_stacked_data[key][name_col])
                            msg_emoji_stacked_data[key][name_col] += val
                            # print (msg_emoji_stacked_data[key][name_col])
        emoji_stacked_data = [[m for m in msg_emoji_stacked_data.keys()]]

        emoji_stacked_data.append(
            (numpy.asarray([n for n in msg_emoji_stacked_data.values()], dtype=object).transpose()).tolist())

        final_df = pd.concat([author_value_counts, sent_emoji, author_media_messages_value_counts, words_by_author], axis=1,
                             join="outer").astype(dtype='Int64').fillna(0)
        final_output = [[m, n[0], n[-3], n[-2], n[-1]] for m, n in [[n, list(j)] for n, j in final_df.iterrows()]]


        print(final_output)



        total_members_list = sorted(df['Author'].dropna().unique())
        max_date = pd.to_datetime(df['Date'] + ' ' + df['Time'], errors='ignore').max()
        min_date = pd.to_datetime(df['Date'] + ' ' + df['Time'], errors='ignore').min()

        date_diff = max_date - min_date

        total = [('days', date_diff.days),
                 ('messages', int(df.count().Author)),
                 ('media', int(author_media_messages_value_counts.sum())),
                 ('emojis', int(df['Emoji_Count'].sum())),
                 ('words', int(df['Word_Count'].sum())),
                 ('letters', int(df['Letter_Count'].sum()))
                 ]

        print (total,"inside total")
        word_list = pd.Series(' '.join(df.loc[~(
            df['Message'].str.contains('<Media.* | omitted>.$', regex=True))].Message).lower().split()).value_counts()[:10]

        date_group = df.groupby('Date')

        print ("before most")

        try:
            print ("try")
            most = [('texts sent', author_value_counts.idxmax(), int(author_value_counts.max())),
                ('emoji sent', sent_emoji.idxmax(), int(sent_emoji.max())),
                ('media shared', author_media_messages_value_counts.idxmax(), int(author_media_messages_value_counts.max())),
                ('Used Word', word_list.idxmax(), int(word_list.max())),
                ('Used Emoji', emoji_list[0][0], int(emoji_list[0][1])),
                ('Texted Day', date_group.Message.count().idxmax(), int(date_group.Message.count().max()))
                ]
            print (most,"most")
        except:
            print ("except")
            try:
                most = [('texts sent', author_value_counts.idxmax(), int(author_value_counts.max())),
                    ('emoji sent', sent_emoji.idxmax(), int(sent_emoji.max())),
                    ('media shared', author_media_messages_value_counts.idxmax(),
                     int(author_media_messages_value_counts.max())),
                    ('Used Word', word_list.idxmax(), int(word_list.max())),
                    ('Used Emoji', "",0),
                    ('Texted Day', date_group.Message.count().idxmax(), int(date_group.Message.count().max()))
                    ]
            except:
                try:

                    most = [('texts sent', author_value_counts.idxmax(), int(author_value_counts.max())),
                            ('emoji sent', sent_emoji.idxmax(), int(sent_emoji.max())),
                            ('media shared', "",0),
                            ('Used Word', word_list.idxmax(), int(word_list.max())),
                            ('Used Emoji', emoji_list[0][0], int(emoji_list[0][1])),
                            ('Texted Day', date_group.Message.count().idxmax(), int(date_group.Message.count().max()))]
                except:
                    most = [('texts sent', author_value_counts.idxmax(), int(author_value_counts.max())),
                            ('emoji sent', sent_emoji.idxmax(), int(sent_emoji.max())),
                            ('media shared', "", 0),
                            ('Used Word', word_list.idxmax(), int(word_list.max())),
                            ('Used Emoji', "",0),
                            ('Texted Day', date_group.Message.count().idxmax(), int(date_group.Message.count().max()))]
                else:
                    pass
            else:
                pass
        
        else:
            print (most,"most")


        sent_emoji = [(m, n) for m, n in sent_emoji.sort_values(ascending=False).items()]

        word_list = [(m, n) for m, n in word_list.items()]

        long_day_list = df.loc[df['Date'] == date_group.Message.count().idxmax(), ['Author', 'Message']]

        long_day_list = [(author.Author, author.Message) for author in long_day_list.itertuples()]

        longest_msg_count, longest_msg = int(df['Word_Count'].max()),\
                                         df.iloc[df.Word_Count.idxmax()][['Message', 'Author','Date']]

        time_group = pd.to_datetime(df['Time']).apply(lambda s: str(s.hour))

        time_group = [n for n in time_group.value_counts()[:10].items()]

        year_group = pd.to_datetime(df['Date']).apply(lambda s: str(s.year) + ' ' + str(s.month_name()))

        year_group = [n for n in year_group.value_counts()[:10].items()]

        cal_group = pd.to_datetime(df['Date'])

        cal_group = [n for n in cal_group.value_counts()[:50].items()]
        print (cal_group)

        return max_date,min_date,emoji_list,word_list,emoji_stacked_data,sent_emoji,final_output,total_members_list,total,\
               most,longest_msg_count,str(longest_msg.Author),time_group,year_group,cal_group
    else:
        print ("Invalid file")
        return None


