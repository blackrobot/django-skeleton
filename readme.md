# Creating a django project
Run this in the shell, and pass the script: the project name, the
project title, and the project url. For example: my_proj "My Project"
my-project.com

```
$ curl https://raw.github.com/gist/d380fc34972be01ceefe/4b28dafbc3a7266f6e5ac771ef660666a34993c5/startproject.sh | \
  bash -s 
```

https://gist.github.com/d380fc34972be01ceefe



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
