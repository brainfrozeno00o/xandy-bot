"""add quotes v1

Revision ID: 03829f2fd589
Revises: 37fe55eaa92f
Create Date: 2021-10-24 17:15:35.105606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "03829f2fd589"
down_revision = "37fe55eaa92f"
branch_labels = None
depends_on = None


def upgrade():
    # basically insert the first 15 quotes
    op.execute(
        """INSERT INTO all_quotes (quote, context) VALUES
            ('Quitters don''t quit', 'Xander while losing in a chess game'),
            ('Boiled or steamed ko lang kinakain yung saging', 'Xander on how he eats his bananas'),
            ('Scrum master naman ako', 'Xander on learning Scrum methodology'),
            ('Suwerte mo naman, nakuha mo Ayaka, Yoimiya, Raiden. Parang burger nakuha mo; Yoimiya is the burger and Raiden and Ayaka are the buns', 'Xander on CJ''s characters (even if CJ doesn''t have Yoimiya)'),
            ('Yung Alibaba magiging Alibabye na yan', 'Xander on building the SJG franchise'),
            ('Our leaders started from being call center agents - That''s a bad thing to say in a website', 'Xander mocking call center agents'),
            ('More legs please', 'Xander on all IZ*ONE members'' legs, especially the minor members'),
            ('Ganda ng legs', 'Xander on all IZ*ONE members'' legs, especially the minor members'),
            (E'Danao: "Kaya mo maglakad na 54 KM/Hr na speed?"\nXander: "Oo"', 'Xander on how one of his houses is walking distance from BGC'),
            ('Syempre hindi ako lalabas', 'Xander on getting his Starbucks planner'),
            ('SAP God na ako', E'Xander on his ''tasks'' at EY'),
            ('Kaya ko na gawin yung 20 [exercises] nang walang guide ng trainer', 'Xander on learning MySQL'),
            ('Kaming mga new hire nakatambay lang', 'Xander 4 months into his work'),
            ('Eto pinapakinggan ko ngayon Art of War', 'Xander on what he listens to during his free time'),
            ('I like self-help books. They help me feel happy', 'Xander on reading self-help books');"""
    )


def downgrade():
    pass
