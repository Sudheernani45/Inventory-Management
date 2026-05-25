class config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "mysecret123"


    # ---------- photos ----------
    UPLOAD_FOLDER = 'static/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'jfif'}


    # ---------- pagination ----------
    ITEMS_PER_PAGE = 20          # records shown per page across all list views
    LIMIT_PER_PAGE = 20          # kept for backward-compat (same value)


    # ---------- email ----------
    MAIL_SERVER         = 'smtp.gmail.com'
    MAIL_PORT           = 587
    MAIL_USE_TLS        = True
    MAIL_USERNAME       = 'sudheernani3345@gmail.com'
    MAIL_PASSWORD       = 'txzkoufsuvgdgqup'
    MAIL_DEFAULT_SENDER = 'sudheernani3345@gmail.com'

    