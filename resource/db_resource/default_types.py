from abc import abstractmethod, ABC

from .local_model import Feeling, DetailFeeling
from .default_values import DefaultLanguage


class BaseStatus(ABC):
    def init(self):
        pass

    @abstractmethod
    def insert_on_conflict_update(self):
        """

        :return:
        """
        pass


class DefaultFeeling(DefaultLanguage):
    def __init__(self):
        super().__init__()

        self.iLikeYou = Feeling(
            id_=1,
            detail=[
                DetailFeeling(lang=self.English, title="i like you"),
                DetailFeeling(lang=self.Russian, title="ты мне нравишся")
            ]
        )
        self.iLoveYou = Feeling(
            id_=2,
            detail=[
                DetailFeeling(lang=self.English, title="i love you"),
                DetailFeeling(lang=self.Russian, title="я люблю тебя")
            ]
        )
        self.iWantYou = Feeling(
            id_=3,
            detail=[
                DetailFeeling(lang=self.English, title="i want you"),
                DetailFeeling(lang=self.Russian, title="я хочу тебя")
            ]
        )
        self.iAmSorry = Feeling(
            id_=4,
            detail=[
                DetailFeeling(lang=self.English, title="i am sorry"),
                DetailFeeling(lang=self.Russian, title="я прошу прощения")
            ]
        )
        self.iWantBreakUp = Feeling(
            id_=5,
            detail=[
                DetailFeeling(lang=self.English, title="i want to break up"),
                DetailFeeling(lang=self.Russian, title="я хочу расстаться")
            ]
        )

        self.__feeling_by_id = {}
        self.__check_object_on_feeling()

        # check for all lang
        for i in self.__feeling_by_id.values():
            assert set([y.id_lang for y in i.get_detail_by_lang.values()]) == set([i.id_ for i in self.languages])


    def check_id_feeling(self, id_feeling: int):
        if not self.__feeling_by_id.get(id_feeling, False):
            raise ValueError

    def get_detail_title_by_id_and_lang(self, id_feeling_status: int, id_lang: int)->str:
       """
            get Feeling detail title by some lang
       :param id_feeling_status:
       :param id_lang:
       :return:
       """
       return self.__feeling_by_id[id_feeling_status].get_detail_by_lang[id_lang].title

    def __check_object_on_feeling(self):
        for i in self.__dict__:
            if isinstance(self.__dict__[i], Feeling):
                self.__feeling_by_id[self.__dict__[i].id_] = self.__dict__[i]

    def insert_on_conflict_update(self):
        for i in self.__feeling_by_id.values():
            insert_ = f"""
                   INSERT INTO feeling (id_feeling, title)
                   VALUES (
                       {i.id_},
                       '{i.get_detail_by_lang[self.English.id_].title}'
                   )
               """

            update_ = f"""
                   UPDATE feeling
                   SET title = '{i.get_detail_by_lang[self.English.id_].title}'
                   WHERE id_feeling={i.id_} 
               """
            yield insert_, update_
