from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import TextAreaField, TextField, SelectField, StringField, PasswordField, HiddenField, SelectMultipleField
from wtforms.validators import DataRequired, Email, InputRequired, Required
from wtforms.fields.html5 import DateField
from wtforms import (SubmitField, SelectMultipleField, widgets)

coun= [('Afghanistan','Afghanistan') , ('Albania','Albania') , ('Algeria','Algeria') , ('Andorra','Algeria') , ('Angola','Angola') , ('Antigua and Barbuda','Antigua and Barbuda') , ('Argentina','Argentina') , ('Armenia','Armenia') , ('Australia','Australia') , ('Austria','Austria') , ('Azerbaijan','Azerbaijan') , ('Bahamas','Bahamas') , ('Bahrain','Bahrain') , ('Bangladesh','Bangladesh') , ('Barbados','Barbados') , ('Belarus','Belarus') , ('Belgium','Belgium') , ('Belize','Belize') , ('Benin','Benin') , ('Bhutan','Bhutan') , ('Bolivia','Bolivia') , ('Bosnia and Herzegovina','Bosnia and Herzegovina') , ('Botswana','Botswana') , ('Brazil','Brazil') , ('Brunei','Brunei') , ('Bulgaria','Bulgaria') , ('Burkina Faso','Burkina Faso') , ('Burundi','Burundi') , ('Denmark','Denmark') , ('Djibouti','Djibouti') , ('Dominica','Dominica') , ('Dominican Republic','Dominican Republic') , ('Ecuador','Ecuador') , ('Egypt','Egypt') , ('El Salvador','El Salvador') , ('Equatorial Guinea','Equatorial Guinea') , ('Eritrea','Eritrea') , ('Estonia','Estonia') , ('Eswatini (formerly Swaziland)','Eswatini (formerly Swaziland)') , ('Ethiopia','Ethiopia') , ('Fiji','Fiji') , ('Finland','Finland') , ('France','France') , ('Gabon','Gabon') , ('Gambia','Gambia') , ('Georgia','Georgia') , ('Germany','Germany') , ('Ghana','Ghana') , ('Greece','Greece') , ('Grenada','Grenada') , ('Guatemala','Guatemala') , ('Guinea','Guinea') ]
# ('Guinea-Bissau'.'Guinea-Bissau') , ('Guyana','Guyana') , ('Haiti','Haiti') , ('Honduras','Honduras') , ('Hungary','Hungary') , ('Iceland','Iceland') , ('India','India') , ('Indonesia','Indonesia') , ('Iran','Iran') , ('Iraq','Iraq') , ('Ireland','Ireland') , ('Israel','Israel') , ('Italy','Italy') , ('Jamaica','Jamaica') , ('Japan','Japan') , ('Jordan','Jordan') , ('Kazakhstan','Kazakhstan') , ('Kenya','Kenya') , ('Kiribati','Kiribati') , ('Kosovo','Kosovo') , ('Kuwait','Kuwait') , ('Kyrgyzstan','Kyrgyzstan') , ('Laos','Laos') , ('Latvia','Latvia') , ('Lebanon','Lebanon') , ('Lesotho','Lesotho') , ('Liberia','Liberia') , ('Libya','Libya') , ('Liechtenstein','Liechtenstein') , ('Lithuania','Lithuania') , ('Luxembourg','Luxembourg') , ('Madagascar','Madagascar') , ('Malawi','Malawi') , ('Malaysia','Malaysia') , ('Maldives','Maldives') , ('Mali','Mali') , ('Malta','Malta') , ('Marshall Islands','Marshall Islands') , ('Mauritania','Mauritania') , ('Mauritius','Mauritius') , ('Mexico','Mexico') , ('Micronesia','Micronesia') , ('Moldova','Moldova') , ('Monaco','Monaco') , ('Mongolia','Mongolia') , ('Montenegro','Montenegro')  ('Morocco','Morocco')  ('Mozambique','Mozambique') , ('Myanmar (formerly Burma)','Myanmar (formerly Burma)') , ('Namibia','Namibia') , ('Nauru','Nauru') , ('Nepal','Nepal') , ('Netherlands','Netherlands') , ('New Zealand','New Zealand') , ('Nicaragua','Nicaragua') , ('Niger','Niger')]
# ('Nigeria','Nigeria') , ('North Korea','North Korea') , ('North Macedonia (formerly Macedonia)','North Macedonia (formerly Macedonia)') , ('Norway','Norway') , ('Oman','Oman') , ('Pakistan','Pakistan') , ('Palau','Palau') , ('Palestine','Palestine') , ('Panama','Panama') , ('Papua New Guinea','Papua New Guinea') , ('Paraguay','Paraguay') , ('Peru','Peru') , ('Philippines','Philippines') , ('Poland','Poland') , ('Portugal','Portugal') , ('Qatar','Qatar') , ('Romania','Romania') , ('Russia','Russia') , ('Rwanda','Rwanda') , ('Saint Kitts and Nevis','Saint Kitts and Nevis') , ('Saint Lucia','Saint Lucia') , ('Saint Vincent and the Grenadines','Saint Vincent and the Grenadines') , ('Samoa','Samoa') , ('San Marino','San Marino') , ('Sao Tome and Principe','Sao Tome and Principe') , ('Saudi Arabia','Saudi Arabia') , ('Senegal','Senegal') , ('Serbia','Serbia') , ('Seychelles','Seychelles') , ('Sierra Leone','Sierra Leone') , ('Singapore','Singapore') , ('Slovakia','Slovakia') , ('Slovenia','Slovenia') , ('Solomon Islands','Solomon Islands') , ('Somalia','Somalia') , ('South Africa','South Africa') , ('South Korea','South Korea') , ('South Sudan','South Sudan') , ('Spain','Spain') , ('Sri Lanka','Sri Lanka') , ('Sudan','Sudan') , ('Suriname','Suriname') , ('Sweden','Sweden') , ('Switzerland','Switzerland') , ('Syria','Syria') , ('Taiwan','Taiwan') , ('Tajikistan','Tajikistan') , ('Tanzania','Tanzania') , ('Thailand','Thailand') , ('Timor-Leste','Timor-Leste') , ('Togo','Togo') , ('Tonga','Tonga') , ('Trinidad and Tobago','Trinidad and Tobago') , ('Tunisia','Tunisia') , ('Turkey','Turkey') , ('Turkmenistan','Turkmenistan') , ('Tuvalu','Tuvalu') , ('Uganda','Uganda') , ('Ukraine','Ukraine') , ('United Arab Emirates','United Arab Emirates') , ('United Kingdom','United Kingdom') , ('United States of America','United States of America') , ('Uruguay','Uruguay') , ('Uzbekistan','Uzbekistan') , ('Vanuatu','Vanuatu') , ('Vatican City','Vatican City') , ('Venezuela','Venezuela') , ('Vietnam','Vietnam') , ('Yemen','Yemen') , ('Zambia','Zambia' ),('Zimbabwe','Zimbabwe') ] 
class RegForm(FlaskForm):
    firstname = TextField('First Name:', validators = [DataRequired()])
    lastname = TextField('Last Name:', validators = [DataRequired()])
    email = TextField('Email:', validators = [DataRequired(), Email()], render_kw={"placeholder": "e.g. jdoe@example.com"})
    password = PasswordField('Password:', validators = [DataRequired()])
    con_pass = PasswordField('Confirm Password:', validators= [InputRequired()])
    telephone_no = TextField('Telephone Number:', validators = [DataRequired()])
    street_name = TextField('Street Name:', validators = [DataRequired()])
    city = TextField('City:', validators = [DataRequired()])
    country = SelectField('Country', choices=coun)
    area_code = TextField('Area Code:', validators = [DataRequired()])

class LoginForm(FlaskForm):
    e_mail = StringField('Email:', validators= [InputRequired()])
    password = PasswordField('Password:', validators= [InputRequired()])

gen =  [('Female', 'Female'), ('Male', 'Male')] 
class ModAboutForm(FlaskForm):
    dob = DateField('Date of Birth:', format='%Y-%m-%d')
    gender = SelectField('Gender', choices=gen)
    nickname = TextField('Nickname:', validators= [InputRequired()])

class AdminForm(FlaskForm):
    username = StringField('Username:', validators= [InputRequired()])
    password = PasswordField('Password:', validators= [InputRequired()])

class CPostForm(FlaskForm):
    description = TextAreaField('Description:', validators= [InputRequired()])
    autocomplete_group = StringField('autocomplete_input', validators=[DataRequired()])
    photo = FileField('Photo', validators= [FileRequired(),FileAllowed(['jpg', 'png', 'Images only!'])])

class UppForm(FlaskForm):
    photo = FileField('Photo', validators= [FileRequired(),FileAllowed(['jpg', 'png', 'Images only!'])])

class Addcom_PostForm(FlaskForm):
    usr_text = StringField('Description', validators= [InputRequired()])
    pi_d = HiddenField('', validators= [InputRequired()])

class SearchForm(FlaskForm):
    searchbar = StringField('')

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class AddFriendForm(FlaskForm):
    f_id = HiddenField('', validators= [InputRequired()])
    my_choices = [('1', 'Relative'), ('2', 'School'), ('3', 'Work')]
    g_id = MultiCheckboxField("Select", choices = my_choices, default = ['1','2','3'], coerce=int, validators=[DataRequired()]      )

class CGroupForm(FlaskForm):
    groupname = StringField('Group Name', validators= [InputRequired()])

class GroupForm(FlaskForm):
    groupsearch = StringField('')
    aesearch = StringField('Add Editor Search')

class ACESearchForm(FlaskForm):
    acesearchbar = StringField('Content Editor Search')
