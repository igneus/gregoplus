import json

class Gabc:
    """ knows how to build gabc from a Score """

    OFFICE_PART_TABLE = {
        'al': 'Alleluia',
        'an': 'Antiphona',
        'ca': 'Canticum',
        'co': 'Communio',
        'gr': 'Graduale',
        'hy': 'Hymnus',
        'in': 'Introitus',
        'im': 'Improperia',
        'ky': 'Kyriale',
        'of': 'Offertorium',
        'ps': 'Psalmus',
        're': 'Responsorium',
        'rb': 'Responsorium breve',
        'se': 'Sequentia',
        'tr': 'Tractus',
        'or': 'Toni Communes',
        'pr': 'Praefationes in tono solemni',
        'va': 'Varia',
    }

    def __init__(self, score):
        self._score = score

    def __str__(self):
        content = json.loads(self._score.gabc)

        if isinstance(content, str):
            gabc = content;
        elif isinstance(content, list):
            gabcs = []
            for e in content:
                if e[0] == 'gabc':
                    gabcs.append(e[1])

        # TODO: load and print chant sources

        header = []
        header.append("name: " + self._score.incipit)

        if self._score.office_part:
            part = self._score.office_part
            part_name = part
            if part in self.OFFICE_PART_TABLE:
                part_name = self.OFFICE_PART_TABLE[part]
            header.append("office-part: " + part_name)

        fields = [
            'mode',
            'transcriber',
            'commentary',
        ]
        for field_name in fields:
            field_value = getattr(self._score, field_name)
            if field_value:
                header.append(field_name + ": " + field_value)

        verses = ''
        if self._score.gabc_verses:
            verses = "\n" + self._score.gabc_verses

        return \
            ";\n".join(header) + ";\n" + \
            "%%\n" + \
            gabc + verses
