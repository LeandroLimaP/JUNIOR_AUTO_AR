class Config:
    """Configurações da aplicação Flask."""
    
    # Configuração do Flask
    SECRET_KEY = 'chave-secreta-para-desenvolvimento'
    DEBUG = True
    
    # Configuração do SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///autoar.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
