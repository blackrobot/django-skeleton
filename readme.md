# Local Development
1.  Check out the repo:

        $ git clone git://github.com/blenderbox/{{ project_name|lower }}.git

1.  Create a virtual environment:

        $ mkvirtualenv {{ project_name|lower }} --distribute

1.  Enter your vitrtual environment, and install the packages:

        $ workon {{ project_name|lower }}
        $ pip install -r requirements.txt

1.  Grab some Sass

        $ gem install sass / sudo gem install sass

1.  Copy settings/local.py.example to local.py, and customize with your
    database info:

        $ cp source/settings/local.py.example source/settings/local.py

1.  Create your database, then run syncdb and fake migrations:

        $ python manage.py syncdb --all

1.  Startup your server:

        $ python manage.py runserver
