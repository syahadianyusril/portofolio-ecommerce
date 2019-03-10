import logging, sys
from blueprints import app, manager, db
from logging.handlers import RotatingFileHandler
from blueprints.user import Users
import getpass

if __name__ == '__main__':
    formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    log_handler = RotatingFileHandler("%s/%s" % (app.root_path, 'storage/log/app.log'), maxBytes=10000, backupCount=10)
    log_handler.setLevel(logging.INFO)
    log_handler.setFormatter(formatter)
    app.logger.addHandler(log_handler)

    try:
        if sys.argv[1] == 'createadmin':
            admin_name = input("Masukkan Nama : ")
            admin_email = input("Masukkan Email : ")
            admin_phone_number = input("Masukkan No. Telp : ")
            admin_username = input("Masukkan Admin Username : ")
            admin_password = getpass.getpass("Masukkan Admin Password : ")
            admin = Users(None, admin_name, admin_email, admin_phone_number, admin_username, admin_password, "admin")
            db.session.add(admin)
            db.session.commit()
            print("Admin created.")
            exit(1)
        elif sys.argv[1] == 'db':
            manager.run()
        else:
            app.run(debug=False, host='0.0.0.0', port=8080)
    except IndexError as e:
        app.run(debug=True, host='0.0.0.0', port=8080)

