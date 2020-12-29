from datetime import datetime

class ConvertDateFormat:
    def __init__(self):
        self.format = "%Y-%m-%d"

    def convert_string_to_date(self, date: str)->datetime.date:
        try:
            return datetime.strptime(date, self.format).date()
        except:
            raise ValueError

    def convert_date_to_str(self, date: datetime)->str:
        try:
            return date.strftime(self.format)
        except:
            import traceback
            traceback.print_exc()
            raise ValueError
