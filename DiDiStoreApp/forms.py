from django import forms
from django.contrib.auth.models import User

from DiDiStoreApp.models import Profile, Order


class ProfileUserForm(forms.ModelForm):
    first_name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={"required class":"registration_inputs","id":"name"}))
    last_name = forms.CharField(label="Фамилия", widget=forms.TextInput(attrs={"required class":"registration_inputs","id":"name"}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"required class":"registration_inputs","id":"email"}))
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={"required class":"registration_inputs","id":"surname"}))
    password = forms.CharField(label="Пароль ", widget=forms.PasswordInput(attrs={"required class":"registration_inputs","id":"pass"}))

    class Meta:
        model = User
        fields = ["first_name","last_name","email","username","password"]



class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"required class":"registration_inputs","placeholder":"Логин"}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={"required class":"registration_inputs","placeholder":"Пароль"}))

class ProfielExtrForm(forms.ModelForm):
    address = forms.CharField(label="Адрес",widget=forms.TextInput(attrs={"required class":"registration_inputs","placeholder":"Адрес",}))
    photo = forms.ImageField(label="Фото",widget=forms.FileInput(attrs={"required class":"registration_inputs","placeholder":"Фото",}))
    iin = forms.CharField(label="ИИН",widget=forms.TextInput(attrs={"required class":"registration_inputs","placeholder":"Иин",}))
    bank_iin = forms.CharField(label="Банковский счет",widget=forms.TextInput(attrs={"required class":"registration_inputs","placeholder":"Банковский счёт",}))
    cvv_iin = forms.CharField(label="CVV",widget=forms.TextInput(attrs={"required class":"registration_inputs","placeholder":"CVV",}))

    class Meta:
        model = Profile
        fields = ["address","photo","iin","bank_iin","cvv_iin"]


PAYMENT_MED = (
    ("Картой", "Картой"),
    ("Наличкой", "Наличкой"),
)
class OrderCreateForm(forms.ModelForm):
    address = forms.CharField(label="Адрес", widget=forms.TextInput(
        attrs={"class":"form__input", "placeholder": "Адрес", }))
    iin = forms.CharField(label="ИИН", widget=forms.TextInput(
        attrs={"class":"form__input", "placeholder": "Иин", }))
    bank_iin = forms.CharField(label="Банковский счет", widget=forms.TextInput(
        attrs={"class":"form__input", "placeholder": "Банковский счёт", }))
    cvv_iin = forms.CharField(label="Банковский счет", widget=forms.TextInput(
        attrs={"class":"form__input", "placeholder": "CVV", }))
    payment_method = forms.ChoiceField(choices=PAYMENT_MED, widget=forms.RadioSelect(attrs={"class":"from__checkbox","placeholder":"Метод Оплаты"}))
    name = forms.CharField(label="Имя",
                                 widget=forms.TextInput(attrs={"class":"form__input", "id": "name"}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class":"form__input","id":"email"}))
    phone = forms.CharField(label="Банковский счет", widget=forms.TextInput(
        attrs={"class":"form__input", "placeholder": "Номер", }))
    class Meta:
        model = Order
        fields = ['name', 'email', 'phone', 'address','bank_iin','cvv_iin','iin','payment_method']

