"""add quotes v3

Revision ID: 27c6ca82d677
Revises: ec529ca1e474
Create Date: 2021-10-24 17:40:34.975477

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "27c6ca82d677"
down_revision = "ec529ca1e474"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """INSERT INTO all_quotes (quote, context) VALUES
            ('Durugin mo ulit ako mamaya Josh', 'Xander when playing chess'),
            ('Eden Hazard is the greatest football player of all time; he has one for all', 'Xander being delusional'),
            ('SJG Corporation will be a household name', 'Xander on becoming the next JYP/YG'),
            ('White belt na ako sa Lean Six Sigma', 'Xander on getting certificates'),
            ('Hindi ako nag-iisip most of the time', 'Xander on his learning methods'),
            ('Para akong robot, natututo ako on demand', 'Xander on his learning methods'),
            ('I don''t just learn, I digi-volve', 'Xander on his learning methods'),
            ('Kung pwede lang ipahid sa katawan ko [iyung text]', 'Xander on reading long text'),
            ('Brute force tayo', 'Xander when solving every puzzle'),
            ('[My] schedule is full... daming dates eh!', 'Xander being a chick magnet'),
            ('Yoimiya is the best character in the game', 'Xander showing his love for Yoimiya'),
            ('HAHAHAHAHAHAHAHAHAHAHAHAHA', 'Xander laughing at a black guy eating a burger'),
            ('Gawa muna ako ng gatas', 'Xander before making milk with water for 30 minutes'),
            ('Pwede ba microwave yung peach mango pie kasama lalagyan', 'Xander about to eat Buko Pie'),
            ('I know I''m a sex symbol but a statue of me?! On Ayala Ave.?! Oh, well, I''m not gonna complain', 'Xander being the ultimate sex symbol');"""
    )


def downgrade():
    pass
