import time
import requests


class Betfair(object):
    api_url = None

    def __init__(self, api_url):
        self.set_api_url(api_url)

    @classmethod
    def set_api_url(cls, api_url: str) -> None:
        cls.api_url = api_url

    @classmethod
    def get_table_details(cls, retry_wait=5, max_retry=3):
        try:
            resp = requests.get(cls.api_url + '/tables-details')

        except ValueError as e:
            if max_retry <= 0:
                raise ValueError(str(e))

            max_retry -= 1
            time.sleep(retry_wait)

            return cls.get_table_details(retry_wait=retry_wait)

        return resp.json()

    @classmethod
    def get_table_mapping(cls, table_details):
        return {v['physicalTableName']: k for k, v in table_details['physicalTables'].items()}

    @classmethod
    def get_table_results(self, table_name):
        table_details = self.get_table_details()
        table_mapping = self.get_table_mapping(table_details)

        if table_name not in table_mapping.keys():
            raise ValueError('invalid table name')

        table_results = table_details['results'][table_mapping[table_name]]['physicalTablesResults']

        results = []

        for x in table_results:
            item = {'number': x['number'], 'color': x['color'], 'ts': x['unixTimestamp']}
            results.append(item)

        return results
