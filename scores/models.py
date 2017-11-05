from django.db import models

class Score(models.Model):
    # see https://github.com/gregorio-project/GregoBase/blob/master/include/txt.php
    OFFICE_PART_CHOICES = (
        ('al', 'Alleluia'),
        ('an', 'Antiphona'),
        ('ca', 'Canticum'),
        ('co', 'Communio'),
        ('gr', 'Graduale'),
        ('hy', 'Hymnus'),
        ('im', 'Improperia'),
        ('in', 'Introitus'),
        ('ky', 'Kyriale'),
        ('of', 'Offertorium'),
        ('or', 'Toni Communes'),
        ('pr', 'Praefationes in tono solemni'),
        ('ps', 'Offertorium'),
        ('rb', 'Responsorium breve'), # "breve" is correct
        ('re', 'Responsorium'),
        ('se', 'Sequentia'),
        ('tr', 'Tractus'),
        ('va', 'Varia'),
    )
    version = models.CharField(max_length=128)
    incipit = models.CharField(max_length=256)
    initial = models.IntegerField
    office_part = models.CharField(
        max_length=16,
        db_column='office-part',
        choices=OFFICE_PART_CHOICES,
    )
    mode = models.CharField(max_length=8)
    class Meta:
        db_table = 'gregobase_chants'
