# socialmedia


requirements:
python v 3.9
mysql database name 'socialmediadb'
in socialmediadb database run following query(to add some default data):
INSERT INTO web_settings (name, favicon, logo, copyrights, lsliderone, lonedesc, lonephoto, lslidertwo, ltwodesc, ltwophoto, lsliderthree, lthreedesc, lthreephoto, swebheading, sdesc, lphoto, signup)
VALUES ('Social Media', 'favicon.png', 'logo.png', 'Social Media @2023', 'Social Media', 'Social Media', 'login.png', 'Social Media', 'Social Media', 'album1.jpg', 'Social Media', 'Social Media', 'album3.jpg', 'Social Media', 'Social Media', 'user.jpg', TRUE);

create new python environment
activate the python environment in terminal
install required packages using: pip install -r requirements.txt
