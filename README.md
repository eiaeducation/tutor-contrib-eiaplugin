# eiaplugin plugin for [tutor](https://docs.tutor.edly.io)

eiaplugin plugin for Tutor

## Installation

```console
ssh -i ~/.ssh/eia-openedx-redwood.pem -o IdentitiesOnly=yes ubuntu@eiaeducation.org
source venv/bin/activate
pip install git+https://github.com/eiaeducation/tutor-contrib-eiaplugin
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

## Support

| Author       | [Lawrence McDaniel](https://www.linkedin.com/in/lawrencemcdaniel/) |
|--------------|--------------------------------------------------------|
| email        | [lpm0073@gmail.com](mailto:lpm0073@gmail.com)          |
| whatsapp     | [+1 (617) 834-6172](tel:+16178346172)                  |
| web          | [lawrencemcdaniel.com](https://lawrencemcdaniel.com/)  |
