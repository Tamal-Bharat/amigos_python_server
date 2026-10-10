from datetime import datetime


class DateTimeUtil():

    def getCurrentDateTime(self)-> str:
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%d.%m.%Y %H:%M:%S")
        return formatted_datetime

    def getCurrentDate(self)-> str:
        current_datetime = datetime.now()
        formatted_date = current_datetime.strftime("%d.%m.%Y")
        return formatted_date

    def getCurrentTime(self)-> str:
            current_datetime = datetime.now()
            formatted_time = current_datetime.strftime("%H:%M:%S")
            return formatted_time