from abc import abstractmethod, ABC
import datetime

from resource.db_resource.local_model import Language, TitleStarSign, StarSign

class BaseStatus(ABC):
    def init(self):
        pass

    @abstractmethod
    def insert_on_conflict_update(self):
        """

        :return:
        """
        pass


class DefaultLanguage(BaseStatus):
    """
        self.languages is massive of objects Language
    """

    def __init__(self):
        self.Ukrainian = Language(title='Українська', id_=1)
        self.Russian = Language(title='Русский', id_=2)
        self.English = Language(title='English', id_=3)

        self.languages = [self.Russian, self.English]

        self.id_language_filter = {i.id_: True for i in self.languages}


    def insert_on_conflict_update(self):
        for i_ in self.languages:
            insert_ = f"""
                insert into language (id_language, title)
                values (
                    {i_.id_},
                    '{i_.title}'
                )
            """

            update_ = f"""
                UPDATE language
                SET title='{i_.title}'
                WHERE id_language={i_.id_} 
            """

            yield insert_, update_


class DefaultStarSign(DefaultLanguage):
    def __init__(self):
        super().__init__()

        self.Aquarius = StarSign(
            id_=1,
            title=[
                TitleStarSign(lang=self.Russian, title='Водолей'),
                TitleStarSign(lang=self.Ukrainian, title='Водолій'),
                TitleStarSign(lang=self.English, title='Aquarius')
            ],
            start_date="21.01",
            end_date="19.02"
        )
        self.Pisces = StarSign(
            id_=2,
            title=[
                TitleStarSign(lang=self.Russian, title='Рыбы'),
                TitleStarSign(lang=self.Ukrainian, title='Риби'),
                TitleStarSign(lang=self.English, title='Pisces')
            ],
            start_date="20.02",
            end_date="20.03"
        )
        self.Aries = StarSign(
            id_=3,
            title=[
                TitleStarSign(lang=self.Russian, title='Овен'),
                TitleStarSign(lang=self.Ukrainian, title='Овен'),
                TitleStarSign(lang=self.English, title='Aries')
            ],
            start_date="21.03",
            end_date="20.04"
        )
        self.Taurus = StarSign(
            id_=4,
            title=[
                TitleStarSign(lang=self.Russian, title='Телец'),
                TitleStarSign(lang=self.Ukrainian, title='Телець'),
                TitleStarSign(lang=self.English, title='Taurus')
            ],
            start_date="21.04",
            end_date="21.05"
        )
        self.Gemini = StarSign(
            id_=5,
            title=[
                TitleStarSign(lang=self.Russian, title='Близнецы'),
                TitleStarSign(lang=self.Ukrainian, title='Близнята'),
                TitleStarSign(lang=self.English, title='Gemini')
            ],
            start_date="22.05",
            end_date="21.06"
        )
        self.Cancer = StarSign(
            id_=6,
            title=[
                TitleStarSign(lang=self.Russian, title='Рак'),
                TitleStarSign(lang=self.Ukrainian, title='Рак'),
                TitleStarSign(lang=self.English, title='Cancer')
            ],
            start_date="22.06",
            end_date="22.07"
        )
        self.Leo = StarSign(
            id_=7,
            title=[
                TitleStarSign(lang=self.Russian, title='Лев'),
                TitleStarSign(lang=self.Ukrainian, title='Лев'),
                TitleStarSign(lang=self.English, title='Leo')
            ],
            start_date="23.07",
            end_date="21.08"
        )
        self.Virgo = StarSign(
            id_=8,
            title=[
                TitleStarSign(lang=self.Russian, title='Дева'),
                TitleStarSign(lang=self.Ukrainian, title='Діва'),
                TitleStarSign(lang=self.English, title='Virgo')
            ],
            start_date="22.08",
            end_date="23.09"
        )
        self.Libra = StarSign(
            id_=9,
            title=[
                TitleStarSign(lang=self.Russian, title='Весы'),
                TitleStarSign(lang=self.Ukrainian, title='Терези'),
                TitleStarSign(lang=self.English, title='Libra')
            ],
            start_date="24.09",
            end_date="23.10"
        )
        self.Scorpio = StarSign(
            id_=10,
            title=[
                TitleStarSign(lang=self.Russian, title='Скорпион'),
                TitleStarSign(lang=self.Ukrainian, title='Скорпіон'),
                TitleStarSign(lang=self.English, title='Scorpio')
            ],
            start_date="24.10",
            end_date="22.11"
        )
        self.Sagittarius = StarSign(
            id_=11,
            title=[
                TitleStarSign(lang=self.Russian, title='Стрелец'),
                TitleStarSign(lang=self.Ukrainian, title='Стрілець'),
                TitleStarSign(lang=self.English, title='Sagittarius')
            ],
            start_date="23.11",
            end_date="22.12"
        )
        self.Capricorn = StarSign(
            id_=12,
            title=[
                TitleStarSign(lang=self.Russian, title='Козерог'),
                TitleStarSign(lang=self.Ukrainian, title='Козоріг'),
                TitleStarSign(lang=self.English, title='Capricorn')
            ],
            start_date="23.12",
            end_date="20.01"
        )

        self.__star_sign_by_id = {}
        self.__check_object_on_star_sign()

    def insert_on_conflict_update(self):
        for i in self.__star_sign_by_id:
            insert_ = f"""
                   INSERT INTO star_sign (id_star_sign, title_ru, title_ua, title_en)
                   VALUES (
                       {i},
                       '{self.__star_sign_by_id[i].get_title_by_lang[self.Russian.id_].title}',
                       '{self.__star_sign_by_id[i].get_title_by_lang[self.Ukrainian.id_].title}',
                       '{self.__star_sign_by_id[i].get_title_by_lang[self.English.id_].title}'
                   )
               """

            update_ = f"""
                   UPDATE star_sign
                   SET title_ru = '{self.__star_sign_by_id[i].get_title_by_lang[self.Russian.id_].title}',
                       title_ua = '{self.__star_sign_by_id[i].get_title_by_lang[self.Ukrainian.id_].title}',
                       title_en = '{self.__star_sign_by_id[i].get_title_by_lang[self.English.id_].title}'
                   WHERE id_star_sign={i} 
               """
            yield insert_, update_

    def __check_object_on_star_sign(self):
        for i in self.__dict__:
            if isinstance(self.__dict__[i], StarSign):
                self.__star_sign_by_id[self.__dict__[i].id_] = self.__dict__[i]

    def get_dict_star_sign(self):
        return self.__star_sign_by_id

    def star_sign_title_by_lang(self, id_star_sign: int, id_lang: int)->str:
        return self.__star_sign_by_id[id_star_sign].get_title_by_lang[id_lang].title

    # TODO unit test
    def star_sign_by_date(self, date: datetime.datetime):
        cur_date = None
        id_star_sign_1 = None
        id_star_sign_2 = None

        for i in self.__star_sign_by_id:
            if self.__star_sign_by_id[i].startDate.month == date.month:
                cur_date = self.__star_sign_by_id[i].startDate
                id_star_sign_1 = i
            if self.__star_sign_by_id[i].endDate.month == date.month:
                id_star_sign_2 = i

        assert isinstance(cur_date, datetime.date)
        assert isinstance(id_star_sign_1, int)
        assert isinstance(id_star_sign_2, int)

        return id_star_sign_2 if date.day < cur_date.day else id_star_sign_1
