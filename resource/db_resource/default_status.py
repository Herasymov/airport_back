from abc import abstractmethod, ABC
from .local_model import (
    UserProfileStatus,
    SendFeelingStatus,
    DetailSendFeelingStatus,
    DetailSendFeelingAction,
    SendFeelingAction
)
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


class DefaultUserProfileStatus(BaseStatus):
    """
    """

    def __init__(self):
        self.deactivate = UserProfileStatus(title='deactivate', id_=1)
        self.activate = UserProfileStatus(title='activate', id_=2)
        self.deleted = UserProfileStatus(title='deleted', id_=3)
        self.ban = UserProfileStatus(title='ban', id_=4)

        self.__status_by_id = {}
        self.__check_object_on_status()

    def __check_object_on_status(self):
        for i in self.__dict__:
            if isinstance(self.__dict__[i], UserProfileStatus):
                self.__status_by_id[self.__dict__[i].id_] = self.__dict__[i]

    def convert_id_in_is_activate(self, id_status: int)->bool:
        return True if id_status == self.activate.id_ else False

    def check_ban_account(self, id_status: int)->bool:
        return True if id_status == self.ban.id_ else False

    def insert_on_conflict_update(self):
        for i_ in self.__status_by_id.values():
            insert_ = f"""
                insert into user_status (id_user_status, title)
                values (
                    {i_.id_},
                    '{i_.title}'
                )
            """

            update_ = f"""
                UPDATE user_status
                SET title='{i_.title}'
                WHERE id_user_status={i_.id_} 
            """

            yield insert_, update_



# TODO разница текстовок для отпраителя и получателя в detail
class DefaultSendFeelingStatus(DefaultLanguage):

    def __init__(self):
        super().__init__()

        self.sent = SendFeelingStatus(
            id_=1,
            title='sent',
            detail=[
                DetailSendFeelingStatus(lang=self.English, title="Feeling was sent"),
                DetailSendFeelingStatus(lang=self.Russian, title="Чувство было отправлено")
            ]
        )
        self.resent = SendFeelingStatus(
            id_=2,
            title='resent',
            detail=[
                DetailSendFeelingStatus(lang=self.English, title="Feeling was resend"),
                DetailSendFeelingStatus(lang=self.Russian, title="Чувство было повторно отправлено")
            ]
        )
        self.withdrawn = SendFeelingStatus(
            id_=3,
            title='withdrawn',
            detail=[
                DetailSendFeelingStatus(lang=self.English, title="Feeling was withdrawn"),
                DetailSendFeelingStatus(lang=self.Russian, title="Чувство было снято")
            ]
        )
        self.expired = SendFeelingStatus(
            id_=4,
            title='expired',
            detail=[
                DetailSendFeelingStatus(lang=self.English, title="Feeling was expired"),
                DetailSendFeelingStatus(lang=self.Russian, title="Чувство истекло")
            ]
        )
        self.match = SendFeelingStatus(
            id_=5,
            title='match',
            detail=[
                DetailSendFeelingStatus(lang=self.English, title="Feeling was match"),
                DetailSendFeelingStatus(lang=self.Russian, title="Чувство совпало")
            ]
        )

        self.__status_by_id = {}
        self.__check_object_on_status()

        # check for all lang
        for i in self.__status_by_id.values():
            assert set([y.id_lang for y in i.get_detail_by_lang.values()]) == set([i.id_ for i in self.languages])


    # TODO или в рамках тнзакции достават параметр из сущности sent_feeling не передавая парамеров
    @staticmethod
    async def update_status_history(id_feeling_status, id_sent_feeling, conn):
        create_date = await conn.fetchval(f"""
            insert into send_feeling_status_history (ref_id_sent_feeling, ref_id_feeling_status)
            values ({id_sent_feeling}, {id_feeling_status})
            returning create_date
        """)

        return create_date

    def get_detail_title_by_id_and_lang(self, id_send_feeling_status: int, id_lang: int)->str:
       return self.__status_by_id[id_send_feeling_status].get_detail_by_lang[id_lang].title

    def __check_object_on_status(self):
        for i in self.__dict__:
            if isinstance(self.__dict__[i], SendFeelingStatus):
                self.__status_by_id[self.__dict__[i].id_] = self.__dict__[i]

    def insert_on_conflict_update(self):
        for i in self.__status_by_id.values():
            insert_ = f"""
                insert into feeling_status (id_send_feeling_status, title)
                values (
                    {i.id_},
                    '{i.title}'
                )
            """

            update_ = f"""
                UPDATE feeling_status
                SET title='{i.title}'
                WHERE id_send_feeling_status={i.id_} 
            """

            yield insert_, update_


# TODO добавить остальные сущности экшенов
class DefaultSendFeelingAction(DefaultLanguage):

    def __init__(self):
        super().__init__()

        self.addedHintPhoneNumber = SendFeelingAction(
            id_=2,
            title='added hint phone number',
            detail_for_sender=[
                DetailSendFeelingAction(lang=self.English, title="You added hint", body="Phone number"),
                DetailSendFeelingAction(lang=self.Russian, title="Вы добаивили подсказку", body="Номер телефона")
            ],
            detail_for_receiver=[
                DetailSendFeelingAction(lang=self.English, title="They added hint", body="Phone part"),
                DetailSendFeelingAction(lang=self.Russian, title="Отправитель добавил подсказку", body="Часть номера")
            ]
        )

        self.addedHintGender = SendFeelingAction(
            id_=3,
            title='added hint gender',
            detail_for_sender=[
                DetailSendFeelingAction(lang=self.English, title="You added hint", body="Gender"),
                DetailSendFeelingAction(lang=self.Russian, title="Вы добаивили подсказку", body="Пол")
            ],
            detail_for_receiver=[
                DetailSendFeelingAction(lang=self.English, title="They added hint", body="Gender"),
                DetailSendFeelingAction(lang=self.Russian, title="Отправитель добавил подсказку", body="Пол")
            ]
        )

        self.addedHintStarSign = SendFeelingAction(
            id_=4,
            title='added hint star sign',
            detail_for_sender=[
                DetailSendFeelingAction(lang=self.English, title="You added hint", body="Star sign"),
                DetailSendFeelingAction(lang=self.Russian, title="Вы добаивили подсказку", body="Знак зодиака")
            ],
            detail_for_receiver=[
                DetailSendFeelingAction(lang=self.English, title="They added hint", body="Star sign"),
                DetailSendFeelingAction(lang=self.Russian, title="Отправитель добавил подсказку", body="Знак зодиака")
            ]
        )


        self.__status_by_id = {}
        self.__check_object_on_status()

        # check for all lang
        for i in self.__status_by_id.values():
            assert set([y.id_lang for y in i.get_detail_for_sender_by_lang.values()]) == set([i.id_ for i in self.languages])
            assert set([y.id_lang for y in i.get_detail_for_receiver_by_lang.values()]) == set([i.id_ for i in self.languages])


    # TODO обработать уникальность индекса для одной записи не может быть много открытий статусов
    @staticmethod
    async def update_status_history(id_sent_feeling: int, id_send_feeling_action_type: int, conn):
        create_date = await conn.fetchval(f"""
            insert into send_feeling_action_history (ref_id_send_feeling, ref_id_send_feeling_action_type)
            values ({id_sent_feeling}, {id_send_feeling_action_type})
            returning create_date
        """)

        return create_date

    # TODO переписать это метод
    def get_detail_title_by_id_and_lang(self, id_send_feeling_status: int, id_lang: int)->str:
       return self.__status_by_id[id_send_feeling_status].get_detail_by_lang[id_lang].title

    def __check_object_on_status(self):
        for i in self.__dict__:
            if isinstance(self.__dict__[i], SendFeelingAction):
                self.__status_by_id[self.__dict__[i].id_] = self.__dict__[i]

    def insert_on_conflict_update(self):
        for i in self.__status_by_id.values():

            insert_ = f"""
                insert into send_feeling_action_type (id_send_feeling_action_type, title)
                values (
                    {i.id_},
                    '{i.title}'
                )
            """

            update_ = f"""
                UPDATE send_feeling_action_type
                SET title='{i.title}'
                WHERE id_send_feeling_action_type={i.id_} 
            """

            yield insert_, update_
