from django.contrib.auth.models import User, Group
from django.conf import settings

from registration.views import RegistrationView as BaseRegistrationView

from landmatrix.forms import CustomRegistrationForm
from editor.models import UserRegionalInfo


class RegistrationView(BaseRegistrationView):
    success_url = '/'

    def get_form_class(self):
        return CustomRegistrationForm

    def register(self, form):
        def generate_username(first_name, last_name):
            val = "{0}.{1}".format(first_name.replace(' ', '.'), last_name).lower()
            x = 0
            while True:
                if x == 0 and User.objects.filter(username=val).count() == 0:
                    return val[:30]
                else:
                    new_val = "{0}{1}".format(val, x)
                    if User.objects.filter(username=new_val).count() == 0:
                        return new_val[:30]
                x += 1
                if x > 1000000:
                    raise Exception("Name is super popular!")
        user = form.save(commit=False)
        # Update first and last name for user
        user.first_name = form.cleaned_data['first_name'][:30]
        user.last_name = form.cleaned_data['last_name'][:30]
        user.username = generate_username(user.first_name, user.last_name)
        user.email = user.email[:254]
        user.save()
        group, created = Group.objects.get_or_create(name='Reporters')
        user.groups.add(group)

        UserRegionalInfo.objects.create(
            user=user,
            phone=form.cleaned_data['phone'],
            information=form.cleaned_data['information'],
        )

        self.login(user)

    def login(self, user):
        """
        Log in a user without requiring credentials (using ``login`` from
        ``django.contrib.auth``, first finding a matching backend).

        """
        from django.contrib.auth import load_backend, login
        if not hasattr(user, 'backend'):
            for backend in settings.AUTHENTICATION_BACKENDS:
                if user == load_backend(backend).get_user(user.pk):
                    user.backend = backend
                    break
        if hasattr(user, 'backend'):
            return login(self.request, user)

    def get_success_url(self, new_user=None):
        """
        Returns the supplied success URL.
        """
        next = self.request.POST.get('next', '')
        if next:
            return next
        else:
            return self.success_url