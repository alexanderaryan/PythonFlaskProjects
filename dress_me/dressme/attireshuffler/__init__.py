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
        #self.shirt = shirts
        #self.pants = pants
        self.main_combo = []

    def create_combo(self, shirt, pants):
        if len(shirt) > len(pants):
            for m in range(len(shirt)):
                for n in range(len(shirt)):
                    self.main_combo.append((self.shirt[m] , self.pants[n - 1]))
                    m -= 1
        else:
            for m in range(len(pants)):
                for n in range(len(shirt)):
                    self.main_combo.append((pants[m] , shirt[n - 1]))
                    m -= 1
        return self.main_combo

    def alter_the_sequence(self, shirt, pants):

        def pair_check(li):
            for ind, val in enumerate(li):
                if li[ind] == li[ind - 1] or li[ind][0] == li[ind - 1][0] or li[ind][1] == li[ind - 1][1]:
                    return True

        def pair_swap(li):
            for ind, val in enumerate(li):
                while li[ind] == li[ind - 1] or li[ind][0] == li[ind - 1][0] or li[ind][1] == li[ind - 1][1]:
                    li[ind - len(shirt)], li[ind] = li[ind], li[ind - (len(shirt))]

        li = self.create_combo(shirt, pants)
        while pair_check(li):
            pair_swap(li)


class CalenderDress(DressMe):

    def __init__(self):
        DressMe.__init__(self)

        self.cal = calendar.Calendar(firstweekday=0)
        self.dress = []
        self.calendar_date = []

    def create_calendar(self,from_time, to_time, week_off):
        for date in datetime_range(start=datetime(from_time[0], from_time[1], from_time[2]), end=datetime(to_time[0], to_time[1], to_time[2])):
            if date.timetuple()[6] not in (days_number['Saturday'], days_number['Sunday']):
                self.calendar_date.append(date.strftime("%A, %d-%B-%Y "))

    def create_schedule(self):

        if len(self.main_combo)>len(self.calendar_date):
            self.dress = list(zip(self.calendar_date, self.main_combo))
            print (self.dress)
        else:
            while self.calendar_date != []:
                self.dress.append(list(zip(self.calendar_date[:len(self.main_combo)],self.main_combo)))
                self.calendar_date=self.calendar_date[len(self.main_combo):]

            print (self.dress)


cal_dress = CalenderDress()

if __name__ == '__main__':
    shirt = ['blue shirt',"yellow shirt","whiteshirt"]

    pants = ['black chino','green formal','white checked']

    cal_dress = CalenderDress()
    #cal_dress.create_combo()
    #print (cal_dress.main_combo)
    cal_dress.alter_the_sequence(shirt,pants)
    print (cal_dress.main_combo)
    cal_dress.create_calendar((2020, 2, 7), (2020, 8, 29),(5,6))
    cal_dress.create_schedule()






