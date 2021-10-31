"""add quotes v4

Revision ID: cf63c89ac363
Revises: 27c6ca82d677
Create Date: 2021-10-24 17:40:37.486903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "cf63c89ac363"
down_revision = "27c6ca82d677"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """INSERT INTO all_quotes (quote, context) VALUES
            ('Magiging ganyan ako', 'Xander on becoming like Ippo Makunouchi from Hajime no Ippo'),
            ('I love Fat Fook', 'Xander loving fat fucks... I mean Xander''s favorite eating place at UPTC'),
            ('Taga-Antipolo ako... taga-Pasig ako... taga-Rizal ako... taga-Pateros ako... taga-Makati ako... taga-Las Piñas ako... taga-White Plains ako... taga-Cainta ako... taga-Sampaloc Manila ako', 'Xander flexing the number of houses that he has'),
            ('May bahay ako sa Hong Kong', 'Xander on why he''s Chinese'),
            ('Serotonin lang habol ko', 'Xander dealing with his depression'),
            ('Meta slave ako', 'Xander in every game that he plays'),
            ('Nagkalagnat ako dahil sa lamig ng panahon', 'Xander on his body fucking him up'),
            ('Sa Samal (Island in Davao) ako galing, doon ako ipinanganak', 'Xander on where he was born...'),
            ('May gstring ka ba Stanley?', 'Xander on his fascination with G-strings'),
            ('HELP HELP HELP HELP', 'Xander in every coop game'),
            ('The #1 hater is myself', 'Xander on his haters'),
            ('I started hating myself, February 1, 2020, 8:59 PM', 'Xander on his most recent breakup'),
            ('Love is only a construct', 'Xander being a love guru'),
            ('Never ko pang naranasan maging mahirap', 'Xander looking down on poor people'),
            ('Send dick pics', 'Xander thirsting over Dick Gordon');"""
    )


def downgrade():
    pass
