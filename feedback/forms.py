from django import forms
from .models import FeedbackModel
from django.core.validators import RegexValidator


ERROR_LIST = {
    'name': {
        'required': 'Укажите как к вам обращаться!',
        'min_length': 'Имя указано неверно!',
        'max_length': 'В это поле можно ввести до 50-ти символов!'
    },
    'email': {
        'invalid': 'Неправильно набран почтовый адрес!',
    },
    'phone_number': {
        'invalid': 'Номер телефона должен быть введен в формате: "+(999)99-9999999"'  # ToDo: html validator
    }
}


phone_regex = RegexValidator(regex=r'^\+?1?\(?1?\d{3}\)?1?\-?1?\d{2}\-?1?\d{7}$', code='invalid')


class FeedbackForm(forms.ModelForm):
    user_is_authenticated = None

    class Meta:
        model = FeedbackModel
        fields = ['name',  'email', 'phone_number', 'preferred', 'content']

    name = forms.CharField(
        label='Как к вам обрящаться?',
        help_text='Указать обязательно',
        max_length=50,
        min_length=4,
        error_messages=ERROR_LIST['name'],
    )
    content = forms.CharField(
        widget=forms.Textarea,
        label='Сообщение',
        help_text='Кроме вас и меня это сообщение никто не прочитает',
        required=False
    )
    email = forms.EmailField(
        error_messages=ERROR_LIST['email'],
        label='Адрес электронной почты',
        required=False,
        help_text='На эту почту будет отправлено автоматическое уведомление.'
    )
    phone_number = forms.CharField(
        validators=[phone_regex],
        error_messages=ERROR_LIST['phone_number'],
        label='Номер телефона',
        required=False,
        help_text='Формат +(999)-99-9999999'
    )
    preferred = forms.ChoiceField(
        choices=(
            ('n', 'не указан',),
            ('p', 'по телефону',),
            ('e', 'по электронной почте',),
        ),
        required=False,
        # initial='n',
        label='Предпочитаемый способ связи',
        help_text='Можно указать оставленный вами способ связи',
    )
    honeypot = forms.CharField(
        required=False,
        label='Ловушка для спамеров',
    )

    def clean(self):  # ToDo: проверку preferred & email or phone
        cleaned_data = super().clean()
        phone_number = cleaned_data.get('phone_number')
        email = cleaned_data.get('email')
        preferred = cleaned_data.get('preferred')
        if not email:
            if not phone_number:
                if not self.user_is_authenticated:
                    self.add_error('phone_number', 'либо номер телефона')
                    self.add_error('email', 'либо email')
                    raise forms.ValidationError('Обязательно, либо авторизоваться, либо заполнить хотябы одно поле из '
                                                'ниже перечисленных!')
        if preferred == 'n':
            pass
        elif preferred == 'p' and not phone_number:
            self.add_error('phone_number', 'наберите номер')
            self.add_error('preferred', 'или выберите иной способ связи')
            raise forms.ValidationError('Ваш предпочитаемый способ связи не заполнен!')
        elif preferred == 'e' and not email:
            self.add_error('email', 'введите e-mail')
            self.add_error('preferred', 'или выберите иной способ связи')
            raise forms.ValidationError('Ваш предпочитаемый способ связи не заполнен!')


