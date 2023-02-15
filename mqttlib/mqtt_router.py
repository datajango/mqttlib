# Copyright 2023 Anthony L. Leotta
import re


class MQTTRouteMatch():
    def __init__(self) -> None:
        self.matched = False
        self.topic = None
        self.route = None
        self.vars = {}
        self.errors = []


class MQTTRouter():

    def __init__(self) -> None:
        self.topics = {}

    def add(self, route, topic, params=None):
        paths = topic.split('/')
        parameters = {}

        parts = []

        cleaned_paths = []
        for path in paths:
            path = path.strip()

            if len(path) == 0:
                continue

            cleaned_paths.append(path)

            if path[0] == '<' and path[-1] == '>':
                # This is a parameter
                tmp = path[1:-1]
                if tmp.find('=')>-1:
                    tmp_parts = tmp.split('=')
                    name = tmp_parts[0]
                    constant_value = tmp_parts[1]
                    is_constant = True
                else:
                    name = tmp
                    is_constant = False

                parameters[name] = {}

                if params and name in params:
                    parameter_settings = params[name]
                else:
                    parameter_settings = {
                        'type': 'string'
                    }


                data = {
                    'path': path,
                    'name': name,
                    'is_parameter': True,
                    'is_constant': is_constant,
                    'parameter_settings': parameter_settings
                }

                if is_constant:
                    data.update( {'constant_value': constant_value})

                parts.append(data)
            else:
                parts.append({
                    'path': path,
                    'is_parameter': False
                })

        self.topics[topic] = {
            'route': route,
            'parts': parts,
            'params': params,
            'parameters': parameters
        }

    def match(self, topic):
        route_match = MQTTRouteMatch()
        route_match.matched = False

        # add leading forward slash if it does not exist
        if topic is None:
            return route_match

        if topic[0] != '/':
            tmp = '/' + topic
            topic = tmp

        # strip trailing forward slash
        if topic[-1] == '/':
            topic = topic[:-1]

        tmp = topic.strip()
        paths = tmp.split('/')
        filtered_paths = []
        for path in paths:
            if len(path)>0:
                filtered_paths.append(path)

        for match_topic, settings in self.topics.items():
            # print("trying to match")
            # print(f"{match_topic}")
            # print("to")
            # print(f"{topic}")
            if len(filtered_paths) == len(settings['parts']):
                if self.match_topics(match_topic, filtered_paths, settings, route_match):
                    break

        return route_match

    def match_topics(self, topic, paths, settings, route_match):

        route_match.matched = False
        route_match.topic = None

        for index, path in enumerate(paths):
            part = settings['parts'][index]
            if not part['is_parameter']:
                if part['path'] != path:
                    return False
            else:
                if not self.match_parameter(part, path, route_match):
                    return False

        route_match.matched = True
        route_match.route = settings['route']
        route_match.topic = topic

        return True

    def match_parameter(self, part, path, route_match):

        path = path.strip()

        if part['is_constant'] == True:
            if part['constant_value'] != path:
                return False
            else:
                route_match.vars[part['name']] = path
                return True

        if 'parameter_settings' in part['parameter_settings']:
            if 'type' in part['parameter_settings']:
                param_type = part['parameter_settings']['type']
            else:
                param_type = 'string'
        else:
            param_type = 'string'

        if 'parameter_settings' in part['parameter_settings']:
            if 'lookup' in part['parameter_settings']:
                param_lookup = part['parameter_settings']['lookup']
            else:
                param_lookup = None
        else:
            param_lookup = None

        if 'parameter_settings' in part['parameter_settings']:
            if 'regex' in part['parameter_settings']:
                regex = part['parameter_settings']['regex']
                res = re.match(regex, path)
                if res:
                    route_match.vars[part['name']] = path
                    return True
                else:
                    route_match.errors.append({
                        'path': path,
                        'type': 'regex',
                        'msg': f"Value {path} does not match required Regular Expression {regex}"
                    })

                    return False

        if param_lookup:
            if path in param_lookup:
                route_match.vars[part['name']] = path
                return True
            else:
                return False
        else:
            route_match.vars[part['name']] = path
            return True



