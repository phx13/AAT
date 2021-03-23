from typing import List


class DBHelper:
    # reference. 23 march https://stackoverflow.com/questions/68645/are-static-class-variables-possible-in-python
    ENCODE_PAIR = ',,,'
    ENCODE_NEXT_ITEM = '&&&'

    @staticmethod
    def list_model(result):
        list_model = []
        dict_model = {}
        for k, v in result:
            if not k.startswith('_sa_instance_state'):
                dict_model[k] = v
        list_model.append(dict_model)
        return list_model

    @staticmethod
    def join_list_model(result):
        join_list_model = []
        for obj1, obj2 in result:
            dict_model = {}
            for k1, v1 in obj1.__dict__.items():
                if not k1.startswith('_sa_instance_state'):
                    if not k1 in dict_model:
                        dict_model[k1] = v1
            for k2, v2 in obj2.__dict__.items():
                if not k2.startswith('_sa_instance_state'):
                    if not k2 in dict_model:
                        dict_model[k2] = v2
            join_list_model.append(dict_model)
        return join_list_model

    @staticmethod
    def encode(s1: tuple, s2: tuple) -> str:
        return f'{s1[0]}{DBHelper.ENCODE_PAIR}{s1[1]}{DBHelper.ENCODE_NEXT_ITEM}{s2[0]}{DBHelper.ENCODE_PAIR}{s2[1]}'

    @staticmethod
    def decode(sr_raws: List[str], responses: dict) -> List[dict]:
        """
        This produces a list of the form
        [
            {
                'statement': statement1
                'responses': {
                    'Strongly disagree': x
                    ...
                    'Strongly agree': y
            },
            {
                'statement': statement2
                'responses': {
                    'Strongly disagree': w
                    ...
                    'Strongly agree': z
            }
        ]
        """
        statement_counts = []
        for sr_map in sr_raws:
            qas = sr_map.split(DBHelper.ENCODE_NEXT_ITEM)
            for qa in qas:
                q, a = qa.split(DBHelper.ENCODE_PAIR)
                # print([s['statement'] for s in statement_counts])
                if not any(s['statement'] == q for s in statement_counts):
                    # print(f'{q} not in {statement_counts}\n')
                    statement_counts.append({
                        'statement': q,
                        'responses': {response: 0 for response in responses.values()}
                    })
                for sc in statement_counts:
                    if sc['statement'] == q:
                        response = responses[int(a)]
                        sc['responses'][response] = sc['responses'][response] + 1
        return statement_counts
