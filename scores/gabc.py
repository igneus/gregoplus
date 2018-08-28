import json

class Gabc:
    """ knows how to build gabc from a Score """

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
            header.append("office-part: " + self._score.get_office_part_display())

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
