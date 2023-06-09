from tests.base_case import BaseTestCase
import json


class TestQuotes(BaseTestCase):
    def test_get_quotes(self):
        response = self.client.get(f"/v1/quote?name=Gandalf", headers=self.headers)
        self.assertEqual(response.status_code, 200, response.data)
        data = json.loads(response.data.decode('utf-8'))
        assert isinstance(data, dict)

    def test_get_quotes_not_found(self):
        response = self.client.get(f"/v1/quote?name=LewisFranklin", headers=self.headers)
        self.assertEqual(response.status_code, 404, response.data)

    def test_get_quotes_name_not_provided(self):
        response = self.client.get(f"/v1/quote?name=", headers=self.headers)
        self.assertEqual(response.status_code, 404, response.data)

    def test_get_quotes_no_character_provided(self):
        response = self.client.get(f"/v1/quote", headers=self.headers)
        self.assertEqual(response.status_code, 404, response.data)

    def test_get_quotes_invalid_query_parameter(self):
        response = self.client.get(f"/v1/quote?names=Gandalf", headers=self.headers)
        self.assertEqual(response.status_code, 404, response.data)

