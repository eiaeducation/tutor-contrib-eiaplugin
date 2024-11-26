# eiaplugin plugin for [tutor](https://docs.tutor.edly.io)

EIA Open edX tutor plugin for managing integration to AWS Simple Email Service (SES).

## Installation

```console
ssh -i ~/.ssh/eia-openedx-redwood.pem -o IdentitiesOnly=yes ubuntu@eiaeducation.org
source venv/bin/activate
pip install git+https://github.com/eiaeducation/tutor-contrib-eiaplugin
tutor plugins enable eiaplugin
tutor plugins list
```

To monitor email log data:

```console
tutor local logs --tail=100 -f lms lms-worker smtp
```

To review email settings in your production environment

```console
tutor local run lms sh
   cd lpm/envs/tutor
   cat production.py
```

To uninstall:

```console
tutor plugins disable eiaplugin
pip uninstall tutor-contrib-eiaplugin -y
```

## Usage

```console
tutor plugins enable eiaplugin

tutor config save --set EIAPLUGIN_AWS_SES_REGION_NAME='us-east-1' \
                  --set EIAPLUGIN_AWS_SES_REGION_ENDPOINT='email.us-east-1.amazonaws.com' \
                  --set EIAPLUGIN_EMAIL_HOST='email-smtp.us-east-1.amazonaws.com' \
                  --set EIAPLUGIN_EMAIL_HOST_USER='aws-iam-key' \
                  --set EIAPLUGIN_EMAIL_HOST_PASSWORD='aws-iam-secret' \
                  --set EIAPLUGIN_EMAIL_PORT=587 \
                  --set EIAPLUGIN_EMAIL_USE_TLS=true  \
                  --set EIAPLUGIN_ACE_CHANNEL_DEFAULT_EMAIL='sailthru_email' \
                  --set EIAPLUGIN_ACE_CHANNEL_TRANSACTIONAL_EMAIL='django_email' \
                  --set EIAPLUGIN_LTI_USER_EMAIL_DOMAIN='eiaeducation.org' \
                  --set EIAPLUGIN_SSL_AUTH_EMAIL_DOMAIN='eiaeducation.org' \
```

## Defaults

```python
EIAPLUGIN_EMAIL_HOST = "email-smtp.us-east-1.amazonaws.com"
EIAPLUGIN_EMAIL_PORT = 587
EIAPLUGIN_EMAIL_USE_TLS = True
EIAPLUGIN_LTI_USER_EMAIL_DOMAIN = "eiaeducation.org"
EIAPLUGIN_SSL_AUTH_EMAIL_DOMAIN = "eiaeducation.org"
```

## AWS Simple Email Service (SES)

The Open edX platform uses AWS SES as the backend SMTP email service, running from the us-east-1 data center. 
See [https://us-east-1.console.aws.amazon.com/ses/](https://us-east-1.console.aws.amazon.com/ses/home?region=us-east-1#/smtp) for settings details.

### Important Configuration Notes

- username / password must be generated using the ['Create SMTP credentials'](https://console.aws.amazon.com/iam/home?SESRegion=us-east-1#/users/smtp/create) action button on the top-right of the AWS SES Settings console page
- EIAPLUGIN_EMAIL_HOST_USER is the AWS IAM key pair 'key' generated from this utility
- EIAPLUGIN_EMAIL_HOST_PASSWORD is the AWS IAM key pair 'secret' generated form this utility
- review the existing settings on the production server by opening the file /home/ubuntu/.local/share/tutor/config.yml

## edx ACE

A `send_mail()` channel for edX ACE.

This is both useful for providing an alternative to Sailthru and to debug ACE mail by
inspecting `django.core.mail.outbox`.

Example:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
DEFAULT_FROM_EMAIL = 'contact@eiaeducation.org'

ACE_CHANNEL_DEFAULT_EMAIL = 'sailthru_email'
ACE_CHANNEL_TRANSACTIONAL_EMAIL = 'django_email'

ACE_ENABLED_CHANNELS = [
    'sailthru_email',
    'django_email',
]
```

## Support

| Author       | [Lawrence McDaniel](https://www.linkedin.com/in/lawrencemcdaniel/) |
|--------------|--------------------------------------------------------|
| email        | [lpm0073@gmail.com](mailto:lpm0073@gmail.com)          |
| whatsapp     | [+1 (617) 834-6172](tel:+16178346172)                  |
| web          | [lawrencemcdaniel.com](https://lawrencemcdaniel.com/)  |
