# test_mqtt_router.py
import pytest
from mqttclient.mqttlib.mqtt_router import MQTTRouter


@pytest.fixture
def parameters_001():
    return {
        'env': {
            'type': 'string',
            'lookup': ['qa'],
            'comment': 'Only qa is running on the AWS servers.',
        },
        'channel': {
            'type': 'string',
            'lookup': ['backend', 'gateway'],
        },
        'version': {
            'type': 'string'
        },
        'id': {
            'type': 'string',
            'regex': '([0-9]{4})[-]([0-9]{4})[-][0-9]{4}',
            'examples': ['0000-0000-0000', '1234-1234-1234', '0890-0920-1203']
        },
        'command': {
            'type': 'string',
            'lookup': ['report']
        }
    }


class TestRouter:

    def setup_class(self):
        """ setup_class called once for the class """
        pass

    def teardown_class(self):
        """ teardown_class called once for the class """
        pass

    def setup_method(self):
        """ setup_method called for every method """
        pass

    def teardown_method(self):
        """ teardown_method called for every method """
        pass

    def test_add_topic(self):
        router = MQTTRouter()
        router.add('/foo')
        results = router.match('/foo')
        assert results.matched

    def test_parameterized_topic(self, parameters_001):

        router = MQTTRouter()
        router.add('/<env>/<channel>/<version>/<id>/<command>', parameters_001)
        results = router.match('/qa/backend/v1/1234-1234-1234/report')
        assert results.matched
        assert results.vars['env'] == 'qa'
        assert results.vars['channel'] == 'backend'
        assert results.vars['version'] == 'v1'
        assert results.vars['id'] == '1234-1234-1234'
        assert results.vars['command'] == 'report'

    def test_parameterized_topic_bad_regex(self, parameters_001):

        router = MQTTRouter()
        router.add('/<env>/<channel>/<version>/<id>/<command>', parameters_001)
        results = router.match('/qa/backend/v1/foo/report')
        assert not results.matched
        assert results.errors[0]
        assert results.errors[0]['msg'] == "Value foo does not match required Regular Expression ([0-9]{4})[-]([0-9]{4})[-][0-9]{4}"
