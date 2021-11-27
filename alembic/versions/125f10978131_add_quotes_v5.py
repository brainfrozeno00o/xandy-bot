"""add quotes v5

Revision ID: 125f10978131
Revises: cf63c89ac363
Create Date: 2021-11-12 21:14:42.372197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '125f10978131'
down_revision = 'cf63c89ac363'
branch_labels = None
depends_on = None


def upgrade():
    # basically insert the next batch of quotes for v1.2.0
    op.execute(
        """INSERT INTO all_quotes (quote, context) VALUES
            ('Nasa belly button lang natin yung 5''2"... 6 ft na ako', 'Xander boasting his height'),
            ('Sarap barilin nito ni Madame Ping ang daldal', 'Xander annoyed by Madame Ping'),
            ('LGTM', 'Xander approving pull requests on Github'),
            ('guys madaming iron dito', 'Xander Castillo mining Iron Ore while his teammates are dying'),
            ('tangina mo josh', 'Xander Castillo mercilessly slaughtering Fugative while he is cutting a tree'),
            ('guys i have brought iron for everyone', 'Xander Castillio bringing home ore but used everything for his own equipment'),
            ('Nalipat ako sa devops', 'Xander feeling like Mr. Worldwide at EY'),
            ('Parang programmer lang ako rito', 'Xander Castillo looking down on devs'),
            ('akin na lang pwet mo', 'Xander saying this to all the women he meets'),
            ('Alam mo yung genderless banyo? Ako yun. Kung hindi mo alam, alamin mo', 'Xander Castillo''s advice to Elmo for Len-chan'),
            ('Alam mo mushroom ako?... Mushrooms are asexual', 'Xander Castillo''s advice to Elmo for Len-chan'),
            ('I listen to BTS 24/7 even when I''m asleep', 'Xander being proud to be part of the ARMY')"""
    )


def downgrade():
    pass
