from django import forms
from Users.models import User

class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_names', 'email', 'gender', 'birthday', 'password')

class UpdateUserForm(forms.ModelForm):
    password = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={
                'autocomplete': 'new-password',
            }),        
        required=False,
        help_text="Deja 'Nueva contraseña' en blanco para mantener la contraseña que ya tiene el usuario.",
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_names', 'email', 'gender', 'birthday')

    def save(self, commit=True):
        user = super().save(commit=False)
        pwd = self.cleaned_data.get('password')
        if pwd:
            user.set_password(pwd) 
        if commit:
            user.save()
        return user