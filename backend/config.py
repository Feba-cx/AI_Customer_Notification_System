class Config:
    SECRET_KEY = "sales_notification_secret"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/sales_notification"

    SQLALCHEMY_TRACK_MODIFICATIONS = False