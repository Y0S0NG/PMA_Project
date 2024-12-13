from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        if not SocialAccount.objects.filter(user=user).exists():
            SocialAccount.objects.create(
                user=user,
                provider=sociallogin.account.provider,
                uid=sociallogin.account.uid,
                extra_data=sociallogin.account.extra_data,
            )
        return user
