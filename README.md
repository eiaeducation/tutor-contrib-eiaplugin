# eiaplugin plugin for [tutor](https://docs.tutor.edly.io)

eiaplugin plugin for Tutor

## Installation

.. code-block:: bash

    pip install git+https://github.com/eiaeducation/tutor-contrib-eiaplugin

## Usage

    ```console
    tutor plugins enable eiaplugin

    tutor config save --set EMAIL_HOST='email-smtp.us-east-1.amazonaws.com' \
                    --set EMAIL_HOST_USER='aws-iam-key' \
                    --set EMAIL_HOST_PASSWORD='aws-iam-secret' \
                    --set EMAIL_PORT=587 \
                    --set EMAIL_USE_TLS=true  \
                    --set LTI_USER_EMAIL_DOMAIN='eiaeducation.org' \
                    --set SSL_AUTH_EMAIL_DOMAIN='eiaeducation.org' \
    ```

## Defaults

    ```python
        EMAIL_HOST = "email-smtp.us-east-1.amazonaws.com"
        EMAIL_PORT = 587
        EMAIL_USE_TLS = True
        LTI_USER_EMAIL_DOMAIN = "eiaeducation.org"
        SSL_AUTH_EMAIL_DOMAIN = "eiaeducation.org"
    ```

## Support

| Author       | [Lawrence McDaniel](https://www.linkedin.com/in/lawrencemcdaniel/) |
|--------------|--------------------------------------------------------|
| email        | [lpm0073@gmail.com](mailto:lpm0073@gmail.com)          |
| whatsapp     | [+1 (617) 834-6172](tel:+16178346172)                  |
| web          | [lawrencemcdaniel.com](https://lawrencemcdaniel.com/)  |
