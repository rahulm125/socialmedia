# Social Media Simple Website using Python Flask Framework


## Requirements:
1. Python v 3.9
2. MySQL database name 'socialmediadb'

## Steps to run
1. Clone the repo and navigate to it using terminal
2. Create new python environment: ``` python -m venv appenv ```
3. Activate the python environment in terminal: ``` eg. ./appenv/scripts/activate ```
4. Install required packages using: ``` pip install -r requirements.txt ```
5. Initialize migrations using: ``` flask db init ```
6. Create migrations using: ``` flask db migrate ```
7. Apply migrations to database(create tables): ``` flask db upgrade ```
8. Open MySQL and in socialmediadb database run following query(to add some default data):
```sh
   INSERT INTO web_settings (name, favicon, logo, copyrights, lsliderone, lonedesc, lonephoto, lslidertwo, ltwodesc, ltwophoto, lsliderthree, lthreedesc, lthreephoto, swebheading, sdesc, lphoto, signup) VALUES ('Social Media', 'favicon.png', 'logo.png', 'Social Media @2023', 'Social Media', 'Social Media', 'login.png', 'Social Media', 'Social Media', 'album1.jpg', 'Social Media', 'Social Media', 'album3.jpg', 'Social Media', 'Social Media', 'user.jpg', TRUE);
```
7. Run the app using: ``` python app.py ```
8. Go to link(it will take you to login page): ``` http://127.0.0.1:5000/admin ```
9. Click on signup and create admin user.
10. Go to ``` http://127.0.0.1:5000/ ``` and create user accounts or login.



