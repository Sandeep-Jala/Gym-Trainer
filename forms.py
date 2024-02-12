from flask_wtf import FlaskForm
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, IntegerField, RadioField,FloatField
from wtforms.validators import DataRequired, Length
class UserInfoForm(FlaskForm):

    name = StringField('NAME:', 
    					validators=[DataRequired(), Length(min=2,max=20)])
    weight = IntegerField('WEIGHT:', validators=[DataRequired(message="No valid value")])
    height = FloatField('HEIGHT:', validators=[DataRequired(message="No valid value")] )
    age = IntegerField('AGE:', validators=[DataRequired(message="No valid value")])
    gender = RadioField('GENDER',choices=[('Male','Male'),('Female','Female')],default='Male',validators=[DataRequired()])
    physical_activity=RadioField('PHYSICAL ACTIVITY',
	    						choices=[
	    									('value1','Sedentary(little or no exercise)'),
	    									('value2','Light Active(1-3 days/week)'),
	    									('value3','Moderately Active(3-5 days/week)'),
	    									('value4','Very Active(6-7 days/week)'),
	    									('value5','Super Active(twice/day)')

	    								],
	    						default='value1',
	    						validators=[DataRequired()])
    submit = SubmitField('Submit')
