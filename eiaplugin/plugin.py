"""
This file is the main entry point for your plugin. It is loaded by Tutor.

Implements the AWS SES email services
- AWS account: 120088116466
- https://us-east-1.console.aws.amazon.com/ses/home?region=us-east-1#/account
- Verified email identity: eiaeducation.org


AWS sending limits
- Daily sending quota: 50,000 emails per 24-hour period
- Maximum send rate: 14 emails per second

AWS IAM user credentials
- user: https://us-east-1.console.aws.amazon.com/iam/home#/users/details/ses-smtp-user.20240229-070321
"""
from __future__ import annotations

import os
from glob import glob

# pylint: disable=w0611
import click
import importlib_resources
from dotenv import load_dotenv
from tutor import hooks

from .__about__ import __version__

load_dotenv()

########################################
# CONFIGURATION
########################################
config = {
    "defaults": {
        "VERSION": __version__,
        # ACE Channel settings
        "ACE_CHANNEL_DEFAULT_EMAIL": 'sailthru_email',
        "ACE_CHANNEL_TRANSACTIONAL_EMAIL": 'django_email',

        # AWS SES settings
        "AWS_SES_REGION_NAME": os.environ.get('AWS_SES_REGION_NAME', "us-east-1"),
        "AWS_SES_REGION_ENDPOINT": os.environ.get('AWS_SES_REGION_ENDPOINT', "email.us-east-1.amazonaws.com"),

        # AWS SES email settings
        "EMAIL_BACKEND": "django.core.mail.backends.smtp.EmailBackend",
        "EMAIL_HOST": os.environ.get('EIAPLUGIN_EMAIL_HOST', "email-smtp.us-east-1.amazonaws.com"),
        "EMAIL_HOST_USER": os.environ.get('EIAPLUGIN_EMAIL_HOST_USER', "SET-ME-IN-EIAPLUGIN"),
        "EMAIL_HOST_PASSWORD": os.environ.get('EIAPLUGIN_EMAIL_HOST_PASSWORD', "SET-ME-IN-EIAPLUGIN"),
        "EMAIL_PORT": os.environ.get('EIAPLUGIN_EMAIL_PORT', 587),
        "EMAIL_USE_TLS": os.environ.get('EIAPLUGIN_EMAIL_USE_TLS', True),
        "DEFAULT_FROM_EMAIL": os.environ.get('EIAPLUGIN_DEFAULT_FROM_EMAIL', "contact@eiaeducation.org"),

        # other lesser used openedx email settings
        "LTI_USER_EMAIL_DOMAIN": "eiaeducation.org",
        "SSL_AUTH_EMAIL_DOMAIN": "eiaeducation.org",
    },
}

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"EIAPLUGIN_{key}", value) for key, value in config.get("defaults", {}).items()]
)

hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        # Add settings that don't have a reasonable default for all users here.
        # For instance: passwords, secret keys, etc.
        # Each new setting is a pair: (setting_name, unique_generated_value).
        # Prefix your setting names with 'EIAPLUGIN_'.
        # For example:
        ### ("EIAPLUGIN_SECRET_KEY", "{{ 24|random_string }}"),
    ]
)

hooks.Filters.CONFIG_OVERRIDES.add_items(
    [
        # Danger zone!
        # Add values to override settings from Tutor core or other plugins here.
        # Each override is a pair: (setting_name, new_value). For example:
        ### ("PLATFORM_NAME", "My platform"),
    ]
)


########################################
# INITIALIZATION TASKS
########################################

# To add a custom initialization task, create a bash script template under:
# eiaplugin/templates/eiaplugin/tasks/
# and then add it to the MY_INIT_TASKS list. Each task is in the format:
# ("<service>", ("<path>", "<to>", "<script>", "<template>"))
MY_INIT_TASKS: list[tuple[str, tuple[str, ...]]] = [
    # For example, to add LMS initialization steps, you could add the script template at:
    # eiaplugin/templates/eiaplugin/tasks/lms/init.sh
    # And then add the line:
    ### ("lms", ("eiaplugin", "tasks", "lms", "init.sh")),
]


# For each task added to MY_INIT_TASKS, we load the task template
# and add it to the CLI_DO_INIT_TASKS filter, which tells Tutor to
# run it as part of the `init` job.
for service, template_path in MY_INIT_TASKS:
    full_path: str = str(
        importlib_resources.files("eiaplugin")
        / os.path.join("templates", *template_path)
    )
    with open(full_path, encoding="utf-8") as init_task_file:
        init_task: str = init_task_file.read()
    hooks.Filters.CLI_DO_INIT_TASKS.add_item((service, init_task))


########################################
# DOCKER IMAGE MANAGEMENT
########################################


# Images to be built by `tutor images build`.
# Each item is a quadruple in the form:
#     ("<tutor_image_name>", ("path", "to", "build", "dir"), "<docker_image_tag>", "<build_args>")
hooks.Filters.IMAGES_BUILD.add_items(
    [
        # To build `myimage` with `tutor images build myimage`,
        # you would add a Dockerfile to templates/eiaplugin/build/myimage,
        # and then write:
        ### (
        ###     "myimage",
        ###     ("plugins", "eiaplugin", "build", "myimage"),
        ###     "docker.io/myimage:{{ EIAPLUGIN_VERSION }}",
        ###     (),
        ### ),
    ]
)


# Images to be pulled as part of `tutor images pull`.
# Each item is a pair in the form:
#     ("<tutor_image_name>", "<docker_image_tag>")
hooks.Filters.IMAGES_PULL.add_items(
    [
        # To pull `myimage` with `tutor images pull myimage`, you would write:
        ### (
        ###     "myimage",
        ###     "docker.io/myimage:{{ EIAPLUGIN_VERSION }}",
        ### ),
    ]
)


# Images to be pushed as part of `tutor images push`.
# Each item is a pair in the form:
#     ("<tutor_image_name>", "<docker_image_tag>")
hooks.Filters.IMAGES_PUSH.add_items(
    [
        # To push `myimage` with `tutor images push myimage`, you would write:
        ### (
        ###     "myimage",
        ###     "docker.io/myimage:{{ EIAPLUGIN_VERSION }}",
        ### ),
    ]
)


########################################
# TEMPLATE RENDERING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

hooks.Filters.ENV_TEMPLATE_ROOTS.add_items(
    # Root paths for template files, relative to the project root.
    [
        str(importlib_resources.files("eiaplugin") / "templates"),
    ]
)

hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    # For each pair (source_path, destination_path):
    # templates at ``source_path`` (relative to your ENV_TEMPLATE_ROOTS) will be
    # rendered to ``source_path/destination_path`` (relative to your Tutor environment).
    # For example, ``eiaplugin/templates/eiaplugin/build``
    # will be rendered to ``$(tutor config printroot)/env/plugins/eiaplugin/build``.
    [
        ("eiaplugin/build", "plugins"),
        ("eiaplugin/apps", "plugins"),
    ],
)


########################################
# PATCH LOADING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

# For each file in eiaplugin/patches,
# apply a patch based on the file's name and contents.
for path in glob(str(importlib_resources.files("eiaplugin") / "patches" / "*")):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))


########################################
# CUSTOM JOBS (a.k.a. "do-commands")
########################################

# A job is a set of tasks, each of which run inside a certain container.
# Jobs are invoked using the `do` command, for example: `tutor local do importdemocourse`.
# A few jobs are built in to Tutor, such as `init` and `createuser`.
# You can also add your own custom jobs:


# To add a custom job, define a Click command that returns a list of tasks,
# where each task is a pair in the form ("<service>", "<shell_command>").
# For example:
### @click.command()
### @click.option("-n", "--name", default="plugin developer")
### def say_hi(name: str) -> list[tuple[str, str]]:
###     """
###     An example job that just prints 'hello' from within both LMS and CMS.
###     """
###     return [
###         ("lms", f"echo 'Hello from LMS, {name}!'"),
###         ("cms", f"echo 'Hello from CMS, {name}!'"),
###     ]


# Then, add the command function to CLI_DO_COMMANDS:
## hooks.Filters.CLI_DO_COMMANDS.add_item(say_hi)

# Now, you can run your job like this:
#   $ tutor local do say-hi --name="Lawrence McDaniel"


#######################################
# CUSTOM CLI COMMANDS
#######################################

# Your plugin can also add custom commands directly to the Tutor CLI.
# These commands are run directly on the user's host computer
# (unlike jobs, which are run in containers).

# To define a command group for your plugin, you would define a Click
# group and then add it to CLI_COMMANDS:


### @click.group()
### def eiaplugin() -> None:
###     pass


### hooks.Filters.CLI_COMMANDS.add_item(eiaplugin)


# Then, you would add subcommands directly to the Click group, for example:


### @eiaplugin.command()
### def example_command() -> None:
###     """
###     This is helptext for an example command.
###     """
###     print("You've run an example command.")


# This would allow you to run:
#   $ tutor eiaplugin example-command
