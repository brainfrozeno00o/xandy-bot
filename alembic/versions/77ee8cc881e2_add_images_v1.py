"""add images v1

Revision ID: 77ee8cc881e2
Revises: 125f10978131
Create Date: 2021-11-13 08:21:43.749997

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77ee8cc881e2'
down_revision = '125f10978131'
branch_labels = None
depends_on = None


def upgrade():
    # insert initial image links
    op.execute(
        """INSERT INTO all_images (image_link) VALUES
            ('https://media.discordapp.net/attachments/360290757610962954/893757713664852038/xander.png'),
            ('https://media.discordapp.net/attachments/360290757610962954/893757785987231794/unknown_1.png'),
            ('https://media.discordapp.net/attachments/893759325393289256/901420249101008936/NGVL7394.JPG?width=450&height=676'),
            ('https://media.discordapp.net/attachments/893759325393289256/901420323390496788/IMG_6417.JPG'),
            ('https://media.discordapp.net/attachments/893759325393289256/901420635207655474/IMG_5947.JPG'),
            ('https://media.discordapp.net/attachments/893759325393289256/901421757972480020/unknown.png?width=524&height=676'),
            ('https://media.discordapp.net/attachments/893759325393289256/901424690000691280/IMG_4499.jpg?width=901&height=676'),
            ('https://media.discordapp.net/attachments/893759325393289256/901425135075082260/IMG_6210.jpg?width=508&height=676'),
            ('https://media.discordapp.net/attachments/893759325393289256/901425149847437332/IMG_5742.jpg?width=508&height=676'),
            ('https://media.discordapp.net/attachments/893759325393289256/901425183460581386/IMG_3711.jpg?width=507&height=676'),
            ('https://media.discordapp.net/attachments/893759325393289256/901425227723075604/IMG_3661.jpg?width=507&height=676'),
            ('https://media.discordapp.net/attachments/893759325393289256/901425241333592114/IMG_5756.jpg?width=901&height=676')"""
    )



def downgrade():
    pass
