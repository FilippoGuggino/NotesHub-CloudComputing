# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Note(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, title: str=None, author: str=None, _date: date=None, text: str=None, subject: str=None):  # noqa: E501
        """Note - a model defined in Swagger

        :param title: The title of this Note.  # noqa: E501
        :type title: str
        :param author: The author of this Note.  # noqa: E501
        :type author: str
        :param _date: The _date of this Note.  # noqa: E501
        :type _date: date
        :param text: The text of this Note.  # noqa: E501
        :type text: str
        :param subject: The subject of this Note.  # noqa: E501
        :type subject: str
        """
        self.swagger_types = {
            'title': str,
            'author': str,
            '_date': date,
            'text': str,
            'subject': str
        }

        self.attribute_map = {
            'title': 'title',
            'author': 'author',
            '_date': 'date',
            'text': 'text',
            'subject': 'subject'
        }

        self._title = title
        self._author = author
        self.__date = _date
        self._text = text
        self._subject = subject

    @classmethod
    def from_dict(cls, dikt) -> 'Note':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Note of this Note.  # noqa: E501
        :rtype: Note
        """
        return util.deserialize_model(dikt, cls)

    @property
    def title(self) -> str:
        """Gets the title of this Note.


        :return: The title of this Note.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title: str):
        """Sets the title of this Note.


        :param title: The title of this Note.
        :type title: str
        """
        if title is None:
            raise ValueError("Invalid value for `title`, must not be `None`")  # noqa: E501

        self._title = title

    @property
    def author(self) -> str:
        """Gets the author of this Note.


        :return: The author of this Note.
        :rtype: str
        """
        return self._author

    @author.setter
    def author(self, author: str):
        """Sets the author of this Note.


        :param author: The author of this Note.
        :type author: str
        """
        if author is None:
            raise ValueError("Invalid value for `author`, must not be `None`")  # noqa: E501

        self._author = author

    @property
    def _date(self) -> date:
        """Gets the _date of this Note.


        :return: The _date of this Note.
        :rtype: date
        """
        return self.__date

    @_date.setter
    def _date(self, _date: date):
        """Sets the _date of this Note.


        :param _date: The _date of this Note.
        :type _date: date
        """
        if _date is None:
            raise ValueError("Invalid value for `_date`, must not be `None`")  # noqa: E501

        self.__date = _date

    @property
    def text(self) -> str:
        """Gets the text of this Note.


        :return: The text of this Note.
        :rtype: str
        """
        return self._text

    @text.setter
    def text(self, text: str):
        """Sets the text of this Note.


        :param text: The text of this Note.
        :type text: str
        """
        if text is None:
            raise ValueError("Invalid value for `text`, must not be `None`")  # noqa: E501

        self._text = text

    @property
    def subject(self) -> str:
        """Gets the subject of this Note.


        :return: The subject of this Note.
        :rtype: str
        """
        return self._subject

    @subject.setter
    def subject(self, subject: str):
        """Sets the subject of this Note.


        :param subject: The subject of this Note.
        :type subject: str
        """
        if subject is None:
            raise ValueError("Invalid value for `subject`, must not be `None`")  # noqa: E501

        self._subject = subject
