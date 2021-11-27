"""add quotes v2

Revision ID: ec529ca1e474
Revises: 03829f2fd589
Create Date: 2021-10-24 17:37:28.415881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ec529ca1e474"
down_revision = "03829f2fd589"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """INSERT INTO all_quotes (quote, context) VALUES
            ('I can cry on command', 'Xander''s amazing talent'),
            ('il ya? yun yung parang ako yung pabebe', 'Xander and his philosophy'),
            ('Kokomi is the shittiest 5*', 'Xander on asserting that Yoimiya is the best character in Genshin'),
            ('Kapag nagka-Qiqi ako, pupull ako sa Hu Tao banner para sa C1 Hu Tao tapos goodbye Yoimiya', 'Xander on his god pulls'),
            ('Maganda legs ko parang kpop idol', 'Xander on his amazing legs'),
            ('Syempre mainit ako', 'Xander on his amazing figure'),
            ('Kumuha ako Starbucks planner', 'Xander on spreading COVID'),
            ('0% body fat ako', 'Xander on his workout results'),
            (E'Team lead: "Let me check up with the scrum master"\nXander in his head: "You''re already speaking with him"', 'Xander on his ''tasks'' at EY'),
            ('I like being exploited', 'Xander on his ''tasks'' at EY'),
            ('Naiihi ako kapag excited ako', 'Xander while playing chess'),
            ('I love children', 'Xander on why he wants to be a pediatrician... pedo'),
            ('Oyasumi Punpun is my favorite manga', 'Xander on his favorite manga'),
            ('120 wpm ko', 'Xander on how fast he types'),
            ('I never tilt on any game', 'Xander asserting his PMA');"""
    )


def downgrade():
    pass
