import calendar
# from random import shuffle
import itertools as it
from datetime import datetime, timedelta





def datetime_range(start=None, end=None):
    span = end - start
    for day in range(span.days + 1):
        yield (start + timedelta(days=day))


days_number = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}


class DressMe(object):

    def __init__(self):
        self.shirt = []
        self.pants = []
        self.main_combo = []

    def create_combo(self, shirt, pants):
        self.main_combo = []
        self.shirt=shirt
        self.pants=pants
        if len(shirt) > len(pants):
            for m in range(len(shirt)):
                for n in range(len(pants)):
                    #print (m,n)
                    #print (shirt[m])
                    #print (pants[n-1])
                    self.main_combo.append((shirt[m] , pants[n - 1]))
                    m -= 1
        else:
            for m in range(len(pants)):
                for n in range(len(shirt)):
                    self.main_combo.append((shirt[n] , pants[m - 1]))
                    n -= 1

        main_combo = self.main_combo
        return self.main_combo

    def remove_the_dress(self,main_list,remove_list):
        for every_dress in remove_list:
            try:
                main_list.remove(every_dress)
            except:
                print (every_dress,"not in ",main_list)
            else:
                continue
        return main_list

    def alter_the_sequence(self, li):

        def pair_check(li, change):
            for ind, val in enumerate(li):
                if change == 'All':
                    if li[ind] == li[ind - 1] or li[ind][0] == li[ind - 1][0] or li[ind][1] == li[ind - 1][1]:
                        print(li)
                        print(li[ind], 'all')
                        print(li[ind - 1], 'all')
                        return True
                elif change == 'Shirt':
                    if li[ind] == li[ind - 1] or li[ind][0] == li[ind - 1][0]:
                        print(li)
                        print(li[ind], 's')
                        print(li[ind - 1], 's')
                        return True
                elif change == 'Pairs':
                    print(li[ind], li[ind - 1])
                    if li[ind] == li[ind - 1]:
                        print(li)
                        print(li[ind], 'p')
                        print(li[ind - 1], 'p')
                        return True

        def pair_swap(li, change):
            for ind, val in enumerate(li):
                if change == 'All':
                    all_loop = 0
                    while (li[ind] == li[ind - 1] or li[ind][0] == li[ind - 1][0] or li[ind][1] == li[ind - 1][\
                        1]) and all_loop * 2 <= len(li):
                        li[ind - len(self.shirt)], li[ind] = li[ind], li[ind - len(self.shirt)]
                        all_loop += 1
                        print('all')
                elif change == 'Shirt':
                    shirt_loop = 0
                    while (li[ind] == li[ind - 1] or li[ind][0] == li[ind - 1][0]) and shirt_loop * 2 <= len(\
                            li):
                        li[ind - len(self.shirt)], li[ind] = li[ind], li[ind - len(self.shirt)]
                        shirt_loop += 1
                        print('shirt')
                elif change == 'Pairs':
                    pair_loop = 0
                    while li[ind] == li[ind - 1] and pair_loop * 2 < len(li):
                        li[ind - len(self.shirt)], li[ind] = li[ind], li[ind - len(self.shirt)]
                        pair_loop += 1
                        print('pants')
        all_loop_check = 0
        shirt_loop_check = 0
        pair_loop_check = 0
        while pair_check(li, 'All'):
            if all_loop_check <= len(li):
                pair_swap(li, 'All')
                all_loop_check += 1
            else:
                print('ended all')
                while pair_check(li, 'Shirt'):
                    if shirt_loop_check <= len(li):
                        pair_swap(li, 'Shirt')
                        shirt_loop_check += 1
                    else:
                        print('ended shirt')
                        while pair_check(li, 'Pairs'):
                            if pair_loop_check <= len(li):
                                pair_swap(li, 'Pairs')
                                pair_loop_check += 1
                            else:
                                print('ended pairs')
                                break
                        break
                break
        self.main_combo = li
        return self.main_combo




class CalenderDress(DressMe):

    def __init__(self):
        DressMe.__init__(self)

        self.cal = calendar.Calendar(firstweekday=0)
        self.dress = []
        self.calendar_date = []

    def create_calendar(self, from_time, to_time, week_off):
        self.calendar_date = []
        for date in datetime_range(start=datetime(from_time[0], from_time[1], from_time[2]), end=datetime(to_time[0], to_time[1], to_time[2])):
            #if date.timetuple()[6] not in (days_number['Saturday'], days_number['Sunday']):
            if date.timetuple()[6] not in week_off:
                self.calendar_date.append((date.strftime("%A"), date.strftime("%d-%B-%Y ")))

    def create_schedule(self):
        print ('I am in ')
        print (self.main_combo,"main now")
        print (self.calendar_date,"schedule")
        self.dress = []
        if len(self.main_combo) > len(self.calendar_date):

            print ('inside if')
            self.dress = list(zip(self.calendar_date, self.main_combo))
            add_list=[]
            add_list.append(self.dress)
            return add_list
        else:

            while self.calendar_date != []:
                self.dress.append(list(zip(self.calendar_date[:len(self.main_combo)],self.main_combo)))
                self.calendar_date=self.calendar_date[len(self.main_combo):]
            print (self.main_combo)
            print (self.dress,"is here")
            return self.dress


cal_dress = CalenderDress()

if __name__ == '__main__':
    shirt = ['blue shirt',"yellow shirt","whiteshirt"]

    pants = ['black chino','green formal','white checked']

    cal_dress = CalenderDress()
    x=cal_dress.create_combo(shirt,pants)
    #print (cal_dress.main_combo)
    cal_dress.alter_the_sequence(x)
    #print (cal_dress.main_combo)
    cal_dress.create_calendar((2020, 2, 7), (2020, 8, 29),(5,6))
    cal_dress.create_schedule()






