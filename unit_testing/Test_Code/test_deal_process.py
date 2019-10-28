#from unittest.mock import MagicMock
import mock
from unittest import TestCase
from source_code.deal_process import DealProcess


def mock_get_data(self):
    print('mocked function called')
    mocked_object = mock.MagicMock()
    mocked_object.eodMarker = True
    return [mocked_object]


class TestDealProcess(TestCase):

    @mock.patch('source_code.third_party.DealData.get_data', mock_get_data)
    def test_today_deals(self):
        _deals = DealProcess().today_deals()
        self.assertEqual(_deals[-1].eodMarker, True)




