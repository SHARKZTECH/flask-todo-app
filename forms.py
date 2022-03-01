from flask_wtf import FlaskForm 
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import Email,EqualTo,DataRequired

class TodoForm(FlaskForm):
    title=StringField("Todo Title",validators=[DataRequired()], render_kw={"placeholder": "Todo......"})
    submit=SubmitField("ADD")