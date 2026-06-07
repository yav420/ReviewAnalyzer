# mypy: ignore-errors
"""Формы Flask-WTF (с защитой от CSRF)."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class RegisterForm(FlaskForm):
    """Форма регистрации."""

    username = StringField("Логин", validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=4, max=128)])
    submit = SubmitField("Зарегистрироваться")


class LoginForm(FlaskForm):
    """Форма входа."""

    username = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class AnalyzeForm(FlaskForm):
    """Форма отправки отзыва на анализ."""

    text = TextAreaField(
        "Текст отзыва",
        validators=[DataRequired(), Length(min=1, max=5000)],
    )
    submit = SubmitField("Анализировать")
