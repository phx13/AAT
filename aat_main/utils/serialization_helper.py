from typing import List


class SerializationHelper:
    # reference. 23 march https://stackoverflow.com/questions/68645/are-static-class-variables-possible-in-python
    ENCODE_PAIR = ',,,'
    ENCODE_NEXT_ITEM = '&&&'

    @staticmethod
    def model_to_list(models):
        list_data = []
        for model in models:
            dict_data = {}
            for k, v in model.__dict__.items():
                if not k.startswith('_sa_instance_state'):
                    dict_data[k] = v
            list_data.append(dict_data)
        return list_data

    @staticmethod
    def join_model_to_list(join_models):
        list_data = []
        for obj1, obj2 in join_models:
            dict_data = {}
            for k1, v1 in obj1.__dict__.items():
                if not k1.startswith('_sa_instance_state'):
                    if not k1 in dict_data:
                        dict_data[k1] = v1
            for k2, v2 in obj2.__dict__.items():
                if not k2.startswith('_sa_instance_state'):
                    if not k2 in dict_data:
                        dict_data[k2] = v2
            list_data.append(dict_data)
        return list_data

    @staticmethod
    def encode(s1: tuple, s2: tuple) -> str:

        return f'{s1[0]}{SerializationHelper.ENCODE_PAIR}{s1[1]}{SerializationHelper.ENCODE_NEXT_ITEM}{s2[0]}{SerializationHelper.ENCODE_PAIR}{s2[1]}'

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
            qas = sr_map.split(SerializationHelper.ENCODE_NEXT_ITEM)
            for qa in qas:
                q, a = qa.split(SerializationHelper.ENCODE_PAIR)
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
