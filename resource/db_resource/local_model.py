from datetime import datetime

class Language:
    def __init__(self, title: str, id_: int):
        assert type(title) == str
        assert type(id_) == int

        self.title = title
        self.id_ = id_


class UserProfileStatus:
    def __init__(self, title: str, id_: int):
        assert type(title) == str
        assert type(id_) == int

        self.title = title
        self.id_ = id_


class TitleStarSign:
    def __init__(self, lang: Language, title: str):
        assert isinstance(lang, Language)
        assert isinstance(title, str)

        self.id_lang = lang.id_
        self.title = title


class StarSign:
    def __init__(self, id_: int, title: list, start_date: str, end_date: str):
        assert isinstance(id_, int)
        assert isinstance(title, list)

        self.id_ = id_
        self.title = title
        self.startDate = datetime.strptime(start_date, "%d.%m").date()
        self.endDate = datetime.strptime(end_date, "%d.%m").date()

        self.get_title_by_lang = {i.id_lang: i for i in self.title}


class DetailFeeling:
    def __init__(self, lang: Language, title: str):
        assert isinstance(lang, Language)
        assert isinstance(title, str)

        self.id_lang = lang.id_
        self.title = title


# TODO check DetailFeeling check on type
class Feeling:
    def __init__(self, detail: list, id_: int):
        assert type(detail) == list
        assert type(id_) == int

        self.detail = detail
        self.id_ = id_

        self.get_detail_by_lang = {i.id_lang: i for i in self.detail}


#TODO отрефакторить более явная связь между классами
class DetailSendFeelingStatus:
    def __init__(self, lang: Language, title: str):
        assert isinstance(lang, Language)
        assert isinstance(title, str)

        self.id_lang = lang.id_
        self.title = title


# TODO check on all language
# TODO check on double
class SendFeelingStatus:
    def __init__(self, title: str, detail: list, id_: int):
        assert type(title) == str
        assert type(detail) == list
        assert type(id_) == int

        self.title = title
        self.detail = detail
        self.id_ = id_

        self.get_detail_by_lang = {i.id_lang: i for i in self.detail}


#TODO отрефакторить более явная связь между классами
class DetailSendFeelingAction:
    def __init__(self, lang: Language, title: str, body: str):
        assert isinstance(lang, Language)
        assert isinstance(title, str)
        assert isinstance(body, str)

        self.id_lang = lang.id_
        self.title = title
        self.body = body


# TODO check on double lang
class SendFeelingAction:
    def __init__(self, title: str, detail_for_sender: list, detail_for_receiver: list, id_: int):
        assert type(title) == str
        assert type(detail_for_sender) == list
        assert type(detail_for_receiver) == list
        assert type(id_) == int

        self.id_ = id_
        self.title = title
        self.detailForSender = detail_for_sender
        self.detailForReceiver = detail_for_receiver

        self.get_detail_for_sender_by_lang = {i.id_lang: i for i in self.detailForSender}
        self.get_detail_for_receiver_by_lang = {i.id_lang: i for i in self.detailForReceiver}
