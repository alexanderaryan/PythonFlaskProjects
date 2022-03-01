import re
import pandas as pd
import emoji,string
from collections import Counter
import numpy
import logging


logging.basicConfig(handlers = [logging.FileHandler('logfile.log', 'w', 'utf-8')],
           format = '%(levelname)s: %(message)s',
                    datefmt = '%m-%d %H:%M',
                    level=logging.INFO
)

# Creating an object
logger = logging.getLogger()


def startsWithDateTime(s, date_pattern):
    result = re.match(date_pattern, s)
    # print (result,s)
    if result:
        return True

    return False

def  tosplitauthor(s):
    try:
        author = s.split('-')[1].split(':')[0]

    except:
        author=None
    else:
        logger.info(author, " - Author Found")


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
    else:
        if s.count(':') == 1 and s.count("changed the subject")==0 :
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
    data_frame_data = {'dd_pattern': [
        '^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)(\d{2}|\d{4}), (([0-9]|)[0-9]):([0-9][0-9])(\s*)(([a|p]m)*|([A|P]M)*)*(\s*)-',
        []],
                       'mm_pattern': [
                           '^(((0)[0-9]|[0-9])|((1)[0-2]))(\/)(([0-2][0-9]|(3)[0-1])|[1-9])(\/)(\d{2}|\d{4}), (([0-9]|)[0-9]):([0-9][0-9])(\s*)(([a|p]m)*|([A|P]M)*)*(\s*)-',
                           []]}

    conversationPath = filename

    logger.info("%s is the file name passed", filename)
    for date_pattern in data_frame_data.values():
        with open(conversationPath, encoding="utf-8") as fp:
            fp.readline()  # Skipping first line of the file (usually contains information about end-to-end encryption)

            messageBuffer = []  # Buffer to capture intermediate output for multi-line messages
            date, time, author = None, None, None  # Intermediate variables to keep track of the current message being processed

            while True:
                line = fp.readline()
                # print (line)
                if not line:  # Stop reading further if end of file has been reached
                    date_pattern[1].append([date, time, author, ' '.join(messageBuffer)])
                    break
                # print (line)
                line = line.strip()  # Guarding against erroneous leading and trailing whitespaces

                if startsWithDateTime(line, date_pattern[0]):  # If a line starts with a Date Time pattern, then this indicates the beginning of a new message
                    if len(messageBuffer) > 0:  # Check if the message buffer contains characters from previous iterations
                        # print (messageBuffer)
                        date_pattern[1].append([date, time, author, ' '.join(messageBuffer)])  # Save the tokens from the previous message in parsedData
                    messageBuffer.clear()  # Clear the message buffer so that it can be used for the next message
                    date, time, author, message = getDataPoint(line)  # Identify and extract tokens from the line
                    # print (date, time, author, message)
                    messageBuffer.append(message)  # Append message to buffer

                else:
                    messageBuffer.append(line)  # If a line doesn't start with a Date Time pattern, then it is part of a multi-line message. So, just append to buffer

    if len(data_frame_data['dd_pattern'][1]) > len(data_frame_data['mm_pattern'][1]):
        parsedData = data_frame_data['dd_pattern'][1]
    else:
        parsedData = data_frame_data['mm_pattern'][1]




    logger.info("Parsed the file completely!")

    if parsedData[0][0]!=None:

        logger.info ("Parsed value is not None. Creating data frame")
        df = pd.DataFrame(parsedData, columns=['Date', 'Time', 'Author', 'Message'])
        logger.info("Data Frame Successfully Created")


        author_value_counts = df['Author'].value_counts()  # Number of messages per author

        media_messages_df = df[df['Message'] == '<Media omitted>']

        author_media_messages_value_counts = media_messages_df['Author'].value_counts()

        df['Letter_Count'] = df['Message'].apply(lambda s: len(s))
        logger.info("Letter count column created")

        df['Emoji_Count'] = df['Message'].apply(lambda s: emoji.emoji_count(s))
        logger.info("Emoji count column created")

        df['Emojis'] = df['Message'].apply(lambda s: [n for n in s if emoji.demojize(n) != n \
                                                      and emoji.demojize(n).count('skin_tone')==0\
                                                      and  emoji.demojize(n).count('male_sign')==0])

        logger.info("Emojis are separated from Messages")

        df['Word_Count'] = df['Message'].apply(lambda s: len([w for w in s.split(' ') if w not in string.punctuation
                                                              and emoji.emoji_count(w)==0]))


        logger.info("Word count column created")


        emoji_data = df[df.Emojis.apply(lambda s: s if s != [] else None).notnull()]

        emoji_list = Counter([n for ind, val in emoji_data.Emojis.items() for n in val]).most_common(10)
        logger.info("Emoji list created")
        #df['Letter_Count'].sum(), df['Word_Count'].sum(),\
        #df['Emoji_Count'].sum(), df.Message.count(), df.Author.count()

        df['Changed_Author'] = df.loc[
            (df['Author'].isnull()) & (df['Message'].str.contains('changed|deleted', regex=True))].Message.apply(
            lambda s: re.sub(r' (changed|deleted).*$', '', s) if re.sub(r' (changed|deleted).*$','',s)!= 'You' and re.sub(r' (changed|deleted).*$','',s).count('security code')!=1 else numpy.NaN)

        logger.info("Group name Changed/deleted Authors column created")

        df['Added_Author'] = df.loc[
            (df['Author'].isnull()) & (df['Message'].str.contains('added', regex=True))].Message.apply(
            lambda s: re.sub(r' added.*$', '', s))

        logger.info("Group Name Added Authors column created")

        df['Removed_Author'] = df.loc[
            (df['Author'].isnull()) & (df['Message'].str.contains('removed', regex=True))].Message.apply(
            lambda s: re.sub(r' removed.*$', '', s))

        logger.info("Group Name removed Authors column Created")

        df['Left_People'] = df.loc[
            (df['Author'].isnull()) & (df['Message'].str.contains('left$', regex=True))].Message.apply(
            lambda s: re.sub(r' left$', '', s))

        logger.info("People left from group column Created")

        logger.info("Total Message Sent : %d", df.count().Author)
        logger.info("Users Contributed Count : %s", df['Author'].nunique())
        #logger.info("Users Contributed : ", df['Author'].dropna().unique())


        longest_message, longest_msg = df['Word_Count'].max(), df.iloc[df.Word_Count.idxmax()][['Message', 'Author']]

        logger.info("Longest Message is identified sucessfully!")



        msg_emoji = df.groupby(['Author']).sum()['Emoji_Count']
        group_name_emoji = df.groupby(['Changed_Author']).sum()['Emoji_Count']


        sent_emoji = msg_emoji.add(group_name_emoji, fill_value=0).apply(lambda s: int(s))

        msg_word_by_author = df.groupby(['Author']).sum()['Word_Count']
        changed_word_by_author = df.groupby(['Changed_Author']).sum()['Word_Count']
        #logger.info("Total Words : ", df[(df['Author'].notnull()) | (df['Changed_Author'].notnull())].Word_Count.sum())
        words_by_author = msg_word_by_author.add(changed_word_by_author, fill_value=0).apply(lambda s: int(s))

        author_media_messages_value_counts = author_media_messages_value_counts.apply(lambda s: int(s))


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
        logger.info("Stacked emoji out of messages calculated")

        group_emoji_stacked_data = emoji_per_person_usage_cal(emoji_list, group_name_emoji)
        logger.info("Stacked emoji out of group name change calculated")


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
                            logger.error("Value Error in combining message and group stacked emoji")
                        else:
                            name_col = msg_emoji_stacked_data['Name'].index(
                                group_emoji_stacked_data['Name'][value.index(val)])

                            msg_emoji_stacked_data[key][name_col] += val

        emoji_stacked_data = [[m for m in msg_emoji_stacked_data.keys()]]
        logger.info("Stacked Emoji values for graph is calculated!")


        emoji_stacked_data.append(
            (numpy.asarray([n for n in msg_emoji_stacked_data.values()], dtype=object).transpose()).tolist())

        final_df = pd.concat([author_value_counts, sent_emoji, author_media_messages_value_counts, words_by_author], axis=1,
                             join="outer").astype(dtype='Int64').fillna(0)
        final_output = [[m, n[0], n[-3], n[-2], n[-1]] for m, n in [[n, list(j)] for n, j in final_df.iterrows()]]


        logger.info("Cumulative list for cumulative column graph is calculated")



        total_members_list = sorted(df['Author'].dropna().unique())


        time_group = pd.to_datetime(df['Time']).apply(lambda s: str(s.hour))

        time_group = [n for n in time_group.value_counts()[:10].items()]

        format_type = ["%d/%m/%Y", "%m/%d/%Y", "%d/%m/%y", "%m/%d/%y"]

        for ft in format_type:
            try:
                dt_group = pd.to_datetime(df['Date'], format=ft, errors='raise')
            except:
                logger.warning("Date Format failed %s", ft)
            else:
                logger.info("Date Format used %s", ft)


        #max_date = pd.to_datetime(df['Date'] + ' ' + df['Time'], errors='ignore').max()
        #min_date = pd.to_datetime(df['Date'] + ' ' + df['Time'], errors='ignore').min()
        max_date = dt_group.max().date()
        min_date = dt_group.min().date()


        date_diff = max_date - min_date

        try:
            max_date = str(max_date) + ' ' + df['Time'][df['Time'].last_valid_index()]
        except:
            logger.error("Cannot find maximun time of the chat")
        else:
            pass
        try:
            min_date = str(min_date) + ' ' + df['Time'][0]
        except:
            logger.error("Cannot find the minimum time of the chat")
        else:
            pass

        total = [('days', date_diff.days),
                 ('messages', int(df.count().Author)),
                 ('media', int(author_media_messages_value_counts.sum())),
                 ('emojis', int(df['Emoji_Count'].sum())),
                 ('words', int(df['Word_Count'].sum())),
                 ('letters', int(df['Letter_Count'].sum()))
                 ]

        logger.info("Total data of the group calculated ! ")

        word_list = pd.Series(' '.join(df.loc[~(
            df['Message'].str.contains('<Media.* | omitted>.$', regex=True))
                                       & (df['Message'].apply(lambda s: [w for w in s.split(' ') if emoji.emoji_count(w)==0]))].Message).lower().split()).value_counts()[:10]

        date_group = df.groupby('Date')



        try:

            most = [('texts sent by ', author_value_counts.idxmax(), int(author_value_counts.max())),
                ('emoji sent by', sent_emoji.idxmax(), int(sent_emoji.max())),
                ('media shared by ', author_media_messages_value_counts.idxmax(), int(author_media_messages_value_counts.max())),
                ('Used Word is ', word_list.idxmax(), int(word_list.max())),
                ('Used Emoji is ', emoji_list[0][0], int(emoji_list[0][1])),
                ('Texted Day is ', date_group.Message.count().idxmax(), int(date_group.Message.count().max()))
                ]
            logger.info("Most values of the group calculated ! ")
        except:
            logger.warning("Error in calculating 'Most Values'!!")
            try:
                most = [('texts sent', author_value_counts.idxmax(), int(author_value_counts.max())),
                    ('emoji sent', sent_emoji.idxmax(), int(sent_emoji.max())),
                    ('media shared', author_media_messages_value_counts.idxmax(),
                     int(author_media_messages_value_counts.max())),
                    ('Used Word', word_list.idxmax(), int(word_list.max())),
                    ('Used Emoji', "",0),
                    ('Texted Day', date_group.Message.count().idxmax(), int(date_group.Message.count().max()))
                    ]
                logger.warning("Emoji count is zero in the group!")
            except:

                try:

                    most = [('texts sent', author_value_counts.idxmax(), int(author_value_counts.max())),
                            ('emoji sent', sent_emoji.idxmax(), int(sent_emoji.max())),
                            ('media shared', "",0),
                            ('Used Word', word_list.idxmax(), int(word_list.max())),
                            ('Used Emoji', emoji_list[0][0], int(emoji_list[0][1])),
                            ('Texted Day', date_group.Message.count().idxmax(), int(date_group.Message.count().max()))]
                    logger.warning("Media count is zero in the group!")
                except:
                    most = [('texts sent', author_value_counts.idxmax(), int(author_value_counts.max())),
                            ('emoji sent', sent_emoji.idxmax(), int(sent_emoji.max())),
                            ('media shared', "", 0),
                            ('Used Word', word_list.idxmax(), int(word_list.max())),
                            ('Used Emoji', "",0),
                            ('Texted Day', date_group.Message.count().idxmax(), int(date_group.Message.count().max()))]
                    logger.warning("Media and Emoji count are zero in the group!")
                else:
                    pass
            else:
                pass
        
        else:
            logger.info("Exited after calculating 'Most Values' of the group ! ")


        sent_emoji = [(m, n) for m, n in sent_emoji.sort_values(ascending=False).items()]

        word_list = [(m, n) for m, n in word_list.items()]

        logger.info("Top 10 Emoji List and Word list are created!")

        long_day_list = df.loc[df['Date'] == date_group.Message.count().idxmax(), ['Author', 'Message']]

        long_day_list = [(author.Author, author.Message) for author in long_day_list.itertuples()]

        longest_msg_count, longest_msg = int(df['Word_Count'].max()),\
                                         df.iloc[df.Word_Count.idxmax()][['Message', 'Author','Date']]
        logger.info("Calculating all the time related info of the group!")


        # year_group = pd.to_datetime(df['Date']).apply(lambda s: str(s.year)+' ' +str(s.month_name()))
        year_group = dt_group.apply(lambda s: str(s.year) + ' ' + str(s.month_name()))

        year_group = [n for n in year_group.value_counts()[:10].items()]

        # cal_group = pd.to_datetime(df['Date'],format=("%d/%m/%Y"),errors='ignore')

        cal_group = [n for n in dt_group.value_counts()[:50].items()]

        logger.info("Calculated all the time related info of the group!")

        times_calculator = {1: 'Once', 2: 'Twice', 3: 'Thrice'}
        changed_auth = [(name, times_calculator.setdefault(count, str(count) + ' times')) for name, count in
                        df.groupby(df['Changed_Author']).count()['Message'].iteritems()]
        left_people = [(name, times_calculator.setdefault(count, str(count) + ' times')) for name, count in
                       df.groupby(df['Left_People']).count()['Message'].iteritems()]
        removed_people = [(name, times_calculator.setdefault(count, str(count) + ' times')) for name, count in
                          df.groupby(df['Removed_Author']).count()['Message'].iteritems()]
        added_people = [(name, times_calculator.setdefault(count, str(count) + ' times')) for name, count in
                        df.groupby(df['Added_Author']).count()['Message'].iteritems()]



        logger.info("Events of the group calculated")


        #print (changed_auth,'Change')
        #print(removed_people, 'removed')
        #print(left_people, 'left')
        #print(added_people, 'add')

        return max_date,min_date,emoji_list,word_list,emoji_stacked_data,final_output,total_members_list,total,\
               most,longest_msg_count,str(longest_msg.Author),time_group,year_group,cal_group,changed_auth,left_people,\
               removed_people, added_people
    else:
        logger.error( "%s is an Invalid File!!",filename)
        return None


