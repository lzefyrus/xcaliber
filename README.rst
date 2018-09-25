===============================
Xcaliber iGaming
===============================

Xcaliber test project


Quickstart
----------

Run the following commands to bootstrap your environment ::

    git clone https://github.com/lzefyrus/xgaming
    cd xgaming
    pipenv install --dev
    cp .env.example .env
    npm install
    npm start  # run the webpack dev server and flask server using concurrently

You will see a pretty welcome screen.

Once you have installed your DBMS, run the following to create your app's
database tables and perform the initial migration ::

    flask db init
    flask db migrate
    flask db upgrade
    npm start

You need a Redis server 4 with ReJson plugin


