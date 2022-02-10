from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,IntegerField,SelectField,RadioField,FloatField
from wtforms.validators import DataRequired,NumberRange
from .models import Asset

all_coins = []#(asset.identifier, asset.name) for asset in Asset.query.all()]

class user_profile(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    experience = RadioField('Trade Experience',
                       choices=[('Beginner', "Beginner"), ('Intermediate', "Intermediate"), ("Advance", "Advance")],
                       default='Beginner')
    fav_crypto = SelectField('Favourite Crypto Currency', choices = all_coins)
    bio = TextAreaField('Bio', validators=[DataRequired()])
    submit = SubmitField("Submit")



class deal(FlaskForm):
    # can get the only the assets that  the user has in the select field. For that I need the wallet DB
    # for now will leave it like that 02/02/2022
    trade_currency = SelectField('Select the Currency to sell', choices = all_coins,validators=[DataRequired()])
    accepted_currency = SelectField('Accepted Currency', choices = all_coins, validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    submit = SubmitField("Publish")


class buy(FlaskForm): # When user is trying to buy a specific coin from the market -  they Click it thats where this form will be used
    amount = FloatField('Amount', validators=[DataRequired()])
    submit = SubmitField("Purchase")

class sell(FlaskForm):# When user is trying to Sell a specific coin on the market -  they Click the coin thats where this form will be used
    amount = FloatField('Amount', validators=[DataRequired()])
    submit = SubmitField("Sell")

class quick_buy_market(FlaskForm):
    """
    a quick buy option where user can instantly buy by selecting the coin
    User will select the coin and the amount he is willing to purchase.
    when  the above happens
    The a message will display -  You will get - x amount
    proceed to payment (Which will be through Credit Card)
    """
    currency = SelectField('Crypto Currency', choices=all_coins, validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    submit = SubmitField("Purchase")





class review(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post Review')

class credit_card(FlaskForm):
    card_holder_name = StringField('Card Holder Name', validators=[DataRequired()])
    card_number = IntegerField('Card Number', validators=[DataRequired(), NumberRange(min=16,
                                                                                      message="Error! The card number must be of 16 digits.")])
    MONTH_CHOICES = [('Jan', 'January'), ('Feb', 'February'), ('Mar', 'March'), ('Apr', 'April'),
                     ('May', 'May'), ('Jun', 'June'), ('Jul', 'July'), ('Aug', 'August'),
                     ('Sep', 'September'), ('Oct', 'October'), ('Nov', 'November'), ('Dec', 'December')]
    month = SelectField('Month', choices=MONTH_CHOICES)

    YEAR_CHOICES = [('0', '2021'), ('1', '2022'), ('2', '2023'), ('3', '2024'), ('4', '2025'), ('5', '2026'),
                    ('6', '2027'), ('7', '2028'), ('8', '2029'), ('9', '2030'), ('10', '2031'), ('11', '2032')]
    year = SelectField('Year', choices=YEAR_CHOICES)

    cvv = IntegerField('CVV', validators=[DataRequired(), NumberRange(min=3,
                                                                      message="Error! The CVV number must be of 3 digits.")])

    submit = SubmitField('Pay')

