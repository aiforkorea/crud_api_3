#apps/auth/models.py
from apps import db, login_manager  # apps에서 db 및 login_manager를 import
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash 
#hash import
from datetime import datetime
class User(db.Model, UserMixin): 
# db.Model, UserMixin 상속하는 User 클래스 생성
    __tablename__= "users" #삭제시, 테이블 이름은 Model 이름 소문자 
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String, index=True)
    email=db.Column(db.String, unique=True, index= True)
    password_hash=db.Column(db.String)
    is_admin=db.Column(db.Boolean,default=False)
    created_at=db.Column(db.DateTime, default= datetime.now)
    updated_at=db.Column(db.DateTime, default= datetime.now, onupdate=datetime.now)

    # --- THIS IS THE CRITICAL PART ---
    # The 'password' property and its setter
    @property
    def password(self):
        """
        Prevent direct reading of the password.
        Attempting to read `user.password` will raise an AttributeError.
        """
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self, password):
        """
        Hashes the plain-text password and stores it in password_hash.
        This allows you to do `user.password = "mysecretpassword"`.
        """
        self.password_hash = generate_password_hash(password)
    # Method to check password (you likely already have this or check_password)
    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)
    # 비밀번호 체크
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    # Flask-Login required methods
    @property
    def is_authenticated(self):
        return True
    @property
    def is_active(self):
        return True
    @property
    def is_anonymous(self):
        return False
    def __repr__(self):
        return f'<User {self.username}>'
    # 이메일 중복 체크
    def is_duplicate_email(self):
        return User.query.filter_by(email=self.email).first() is not None
    # flask-login에서 사용자 ID를 문자열로 반환하기 위한 함수
    # 이 함수는 Flask-Login이 사용자 객체를 로드할 때 사용됨
    def get_id(self):
        return str(self.id)
    # 현재 로그인하고 있는 사용자 정보 취득 함수 설정 - apps/__init__.py에서도 정의(현재 중복)
    # 데코레이터는 사용자객체로드과정을 Flask-Login에게 알려줌
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
