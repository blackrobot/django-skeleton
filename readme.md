        $ export SITE_NAME="My Website" && export PROJECT_URL="my-website.com"
        $ curl http://... | bash -s "my_project "My Project" "my-project.com"

```sh

$ django-admin.py startproject \
    --template=https://github.com/blackrobot/django-skeleton/archive/master.zip \
    --extension=py,conf,md \
    "project_name"

$ cd project_name

$ sed -i 's/{site_name}/My Website/g' * && \
  sed -i 's/{project_url}/my-website\.com/g' *
```

# Local Development
1.  Check out the repo:

        $ git clone git://github.com/blenderbox/{{ project_name }}.git

1.  Create a virtual environment:

        $ mkvirtualenv {{ project_name }} --distribute

1.  Enter your vitrtual environment, and install the packages:

        $ workon {{ project_name }}
        $ easy_install pip
        $ pip install -r requirements.txt

    **Note**: You'll need to install memcached, and tools to install all of
    the requirements. For ubuntu:

        $ sudo apt-get install memcached
        $ sudo apt-get install libmemcached-dev libmemcached-tools

1.  Grab some Sass

        $ gem install sass / sudo gem install sass

1.  Copy settings/local.py.example to local.py, and customize with your
    database info:

        $ cp source/settings/local.py.example source/settings/local.py

1.  Create your database, then run syncdb and fake migrations:

        $ python source/manage.py syncdb --all

1.  Startup your server:

        $ python source/manage.py runserver
