# Local Development
1.  Check out the repo:

        $ git clone git://github.com/blenderbox/{{ project_name }}.git

1.  Create a virtual environment:

        $ mkvirtualenv {{ project_name }} --no-site-packages

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
        $ python source/manage.py migrate --fake

    **Note**: Don't run fake migrations. This is bad.

1.  Startup your server:

        $ python source/manage.py runserver


## Python + Virtualenv on a Mac
[These instructions](http://www.thisisthegreenroom.com/2011/installing-python-numpy-scipy-matplotlib-and-ipython-on-lion/),
worked for me.  I followed them up to the `virtualenvwrapper`
installation, then added this line to my ~/.bashrc (or ~/.zshrc) file,
after my PATH declarations.

    $ source /usr/local/share/python/virtualenvwrapper.sh