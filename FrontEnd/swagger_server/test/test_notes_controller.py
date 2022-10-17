# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.note import Note  # noqa: E501
from swagger_server.test import BaseTestCase


class TestNotesController(BaseTestCase):
    """NotesController integration test stubs"""

    def test_add_note(self):
        """Test case for add_note

        Add a new note
        """
        body = Note()
        response = self.client.open(
            '/v1/Note',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_note(self):
        """Test case for delete_note

        Deletes a note
        """
        response = self.client.open(
            '/v1/Note/{noteTitle}'.format(noteTitle='noteTitle_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_find_notes_by_author(self):
        """Test case for find_notes_by_author

        Finds Notes by author
        """
        query_string = [('author', 'author_example')]
        response = self.client.open(
            '/v1/Note/findByAuthor',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_find_notes_by_date(self):
        """Test case for find_notes_by_date

        Finds Notes by date
        """
        query_string = [('_date', '2013-10-20')]
        response = self.client.open(
            '/v1/Note/findByDate',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_find_notes_by_subject(self):
        """Test case for find_notes_by_subject

        Finds Notes by subject
        """
        query_string = [('subject', 'subject_example')]
        response = self.client.open(
            '/v1/Note/findBySubject',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_note_by_title(self):
        """Test case for get_note_by_title

        Find note by title
        """
        response = self.client.open(
            '/v1/Note/{noteTitle}'.format(noteTitle='noteTitle_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_note(self):
        """Test case for update_note

        Update an existing note
        """
        body = Note()
        response = self.client.open(
            '/v1/Note',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
