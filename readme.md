```
$ django-admin.py startproject \
      --extension=py,conf,md,txt \
      --site_name="Example Name" \
      --site_url="example.com" \
      --template=https://github.com/blackrobot/django-skeleton/archive/master.zip \
      "example_project"
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
