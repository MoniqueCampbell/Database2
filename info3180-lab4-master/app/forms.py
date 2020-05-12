from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import TextAreaField, TextField, SelectField, StringField, PasswordField, HiddenField, SelectMultipleField
from wtforms.validators import DataRequired, Email, InputRequired, Required
from wtforms.fields.html5 import DateField

# coun=[('Afghanistan','Afghanistan')],[('Albania','Albania')],[('Algeria','Algeria')],[('Andorra','Algeria')],[('Angola','Angola')],[('Antigua and Barbuda','Antigua and Barbuda')],[('Argentina','Argentina')],[('Armenia','Armenia')],[('Australia','Australia')],

# [('Austria','Austria')]

# [('Azerbaijan','Azerbaijan')]

# [('Bahamas','Bahamas')]

# [('Bahrain','Bahrain')]

# [('Bangladesh','Bangladesh')]

# [('Barbados','Barbados')]

# [('Belarus','Belarus')]

# [('Belgium','Belgium')]

# [('Belize','Belize')]

# [('Benin','Benin')]

# [('Bhutan','Bhutan')]

# [('Bolivia','Bolivia')]

# [('Bosnia and Herzegovina','Bosnia and Herzegovina')]

# [('Botswana','Botswana')]

# [('Brazil','Brazil')]

# [('Brunei','Brunei')]

# [('Bulgaria','Bulgaria')]

# [('Burkina Faso','Burkina Faso')]

# [('Burundi','Burundi')]

# [('Denmark','Denmark')]

# Djibouti

# Dominica

# Dominican Republic

# Ecuador

# Egypt

# El Salvador

# Equatorial Guinea

# Eritrea

# Estonia

# Eswatini (formerly Swaziland)

# Ethiopia

# F

# Fiji

# Finland

# France

# G

# Gabon

# Gambia

# Georgia

# Germany

# Ghana

# Greece

# Grenada

# Guatemala

# Guinea

# Guinea-Bissau

# Guyana

# H

# Haiti

# Honduras

# Hungary

# I

# Iceland

# India

# Indonesia

# Iran

# Iraq

# Ireland

# Israel

# Italy

# J

# Jamaica

# Japan

# Jordan

# K

# Kazakhstan

# Kenya

# Kiribati

# Kosovo

# Kuwait

# Kyrgyzstan

# L

# Laos

# Latvia

# Lebanon

# Lesotho

# Liberia

# Libya

# Liechtenstein

# Lithuania

# Luxembourg

# M

# Madagascar

# Malawi

# Malaysia

# Maldives

# Mali

# Malta

# Marshall Islands

# Mauritania

# Mauritius

# Mexico

# Micronesia

# Moldova

# Monaco

# Mongolia

# Montenegro

# Morocco

# Mozambique

# Myanmar (formerly Burma)

# N

# Namibia

# Nauru

# Nepal

# Netherlands

# New Zealand

# Nicaragua

# Niger

# Nigeria

# North Korea

# North Macedonia (formerly Macedonia)

# Norway

# O

# Oman

# P

# Pakistan

# Palau

# Palestine

# Panama

# Papua New Guinea

# Paraguay

# Peru

# Philippines

# Poland

# Portugal

 

# Q

# Qatar

# R

# Romania

# Russia

# Rwanda

# S

# Saint Kitts and Nevis

# Saint Lucia

# Saint Vincent and the Grenadines

# Samoa

# San Marino

# Sao Tome and Principe

# Saudi Arabia

# Senegal

# Serbia

# Seychelles

# Sierra Leone

# Singapore

# Slovakia

# Slovenia

# Solomon Islands

# Somalia

# South Africa

# South Korea

# South Sudan

# Spain

# Sri Lanka

# Sudan

# Suriname

# Sweden

# Switzerland

# Syria

# T

# Taiwan

# Tajikistan

# Tanzania

# Thailand

# Timor-Leste

# Togo

# Tonga

# Trinidad and Tobago

# Tunisia

# Turkey

# Turkmenistan

# Tuvalu

# U

# Uganda

# Ukraine

# United Arab Emirates (UAE)

# United Kingdom (UK)

# United States of America (USA)

# Uruguay

# Uzbekistan

# V

# Vanuatu

# Vatican City (Holy See)

# Venezuela

# Vietnam

# Y

# Yemen

# Z

# Zambia

# [('Zimbabwe','Zimbabwe')]
class RegForm(FlaskForm):
    firstname = TextField('First Name:', validators = [DataRequired()])
    lastname = TextField('Last Name:', validators = [DataRequired()])
    email = TextField('Email:', validators = [DataRequired(), Email()], render_kw={"placeholder": "e.g. jdoe@example.com"})
    password = PasswordField('Password:', validators = [DataRequired()])
    con_pass = PasswordField('Confirm Password:', validators=[InputRequired()])
    telephone_no = TextField('Telephone Number:', validators = [DataRequired()])
    street_name = TextField('Street Name:', validators = [DataRequired()])
    city = TextField('City:', validators = [DataRequired()])
    country = TextField('Country:', validators = [DataRequired()])
    area_code = TextField('Area Code:', validators = [DataRequired()])

class LoginForm(FlaskForm):
    e_mail = StringField('Email:', validators=[InputRequired()])
    password = PasswordField('Password:', validators=[InputRequired()])

gen = [('Female', 'Female'), ('Male', 'Male')]
class ModAboutForm(FlaskForm):
    dob = DateField('Date of Birth:', format='%Y-%m-%d')
    gender = SelectField('Gender', choices=gen)
    nickname = TextField('Nickname:', validators=[InputRequired()])

class AdminForm(FlaskForm):
    username = StringField('Username:', validators=[InputRequired()])
    password = PasswordField('Password:', validators=[InputRequired()])

class CPostForm(FlaskForm):
    description = TextAreaField('Description:', validators=[InputRequired()])
    photo = FileField('Photo', validators=[FileRequired(),FileAllowed(['jpg', 'png', 'Images only!'])])

class UppForm(FlaskForm):
    photo = FileField('Photo', validators=[FileRequired(),FileAllowed(['jpg', 'png', 'Images only!'])])

class Addcom_PostForm(FlaskForm):
    usr_text = StringField('Description', validators=[InputRequired()])
    pi_d = HiddenField('', validators=[InputRequired()])

class SearchForm(FlaskForm):
    searchbar = StringField('')

class AddFriendForm(FlaskForm):
    f_id = HiddenField('', validators=[InputRequired()])
    g_id = SelectMultipleField('', choices = [('1','Relative'),('2', 'School')])
class CGroupForm(FlaskForm):
    groupname = StringField('Group Name', validators=[InputRequired()])

class GroupForm(FlaskForm):
    groupsearch = StringField('')
    
    aesearch = StringField('Add Editor Search')
