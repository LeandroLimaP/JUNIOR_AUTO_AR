from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import datetime

Base = declarative_base()

# Padrão Singleton para o gerenciador de banco de dados
class DatabaseManager:
    """
    Implementação do padrão Singleton para gerenciar a conexão com o banco de dados.
    Garante que apenas uma instância do gerenciador de banco de dados seja criada.
    """
    _instance = None
    
    def __new__(cls, db_uri='sqlite:///autoar.db'):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.engine = create_engine(db_uri)
            cls._instance.Session = sessionmaker(bind=cls._instance.engine)
            Base.metadata.create_all(cls._instance.engine)
        return cls._instance
    
    def get_session(self):
        """Retorna uma nova sessão do banco de dados."""
        return self.Session()

# Tabela de associação entre Service e Part
service_part = Table(
    'service_part',
    Base.metadata,
    Column('service_id', Integer, ForeignKey('services.id'), primary_key=True),
    Column('part_id', Integer, ForeignKey('parts.id'), primary_key=True)
)

# Modelos de dados
class Client(Base):
    """Modelo para representar clientes."""
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(200))
    phone = Column(String(20))
    email = Column(String(100))
    
    # Relacionamento com veículos
    vehicles = relationship("Vehicle", back_populates="client", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Client(id={self.id}, name='{self.name}')>"

class Vehicle(Base):
    """Modelo para representar veículos."""
    __tablename__ = 'vehicles'
    
    id = Column(Integer, primary_key=True)
    make = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    year = Column(Integer)
    license_plate = Column(String(20), unique=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    
    # Relacionamentos
    client = relationship("Client", back_populates="vehicles")
    services = relationship("Service", back_populates="vehicle", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Vehicle(id={self.id}, make='{self.make}', model='{self.model}', license_plate='{self.license_plate}')>"

class Service(Base):
    """Modelo para representar serviços."""
    __tablename__ = 'services'
    
    id = Column(Integer, primary_key=True)
    description = Column(String(200), nullable=False)
    cost = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'))
    
    # Relacionamentos
    vehicle = relationship("Vehicle", back_populates="services")
    parts = relationship("Part", secondary=service_part, back_populates="services")
    
    def __repr__(self):
        return f"<Service(id={self.id}, description='{self.description}', cost={self.cost})>"

class Part(Base):
    """Modelo para representar peças."""
    __tablename__ = 'parts'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    
    # Relacionamentos
    services = relationship("Service", secondary=service_part, back_populates="parts")
    
    def __repr__(self):
        return f"<Part(id={self.id}, name='{self.name}', price={self.price}, stock={self.stock})>"

class ServicePart(Base):
    """Modelo para representar a quantidade de peças usadas em um serviço."""
    __tablename__ = 'service_part_quantity'
    
    service_id = Column(Integer, ForeignKey('services.id'), primary_key=True)
    part_id = Column(Integer, ForeignKey('parts.id'), primary_key=True)
    quantity = Column(Integer, default=1)
    
    def __repr__(self):
        return f"<ServicePart(service_id={self.service_id}, part_id={self.part_id}, quantity={self.quantity})>"

# Padrão Factory Method para criação de modelos
class ModelFactory:
    """
    Implementação do padrão Factory Method para criar instâncias de diferentes modelos.
    Permite a criação de objetos sem especificar a classe exata a ser instanciada.
    """
    @staticmethod
    def create_model(model_name, **kwargs):
        """
        Cria uma instância de um modelo específico com base no nome do modelo.
        
        Args:
            model_name (str): Nome do modelo a ser criado ('Client', 'Vehicle', 'Service', 'Part').
            **kwargs: Argumentos nomeados para inicializar o modelo.
            
        Returns:
            Uma instância do modelo especificado.
            
        Raises:
            ValueError: Se o nome do modelo não for reconhecido.
        """
        if model_name == 'Client':
            return Client(**kwargs)
        elif model_name == 'Vehicle':
            return Vehicle(**kwargs)
        elif model_name == 'Service':
            return Service(**kwargs)
        elif model_name == 'Part':
            return Part(**kwargs)
        else:
            raise ValueError(f"Unknown model: {model_name}")

# Exemplo de como o padrão Adapter poderia ser implementado
class ExternalLoggerAdapter:
    """
    Exemplo de como o padrão Adapter poderia ser implementado para adaptar
    um sistema de log externo à interface esperada pelo sistema.
    """
    def __init__(self, external_logger):
        self.external_logger = external_logger
    
    def log(self, message, level='INFO'):
        """
        Adapta a interface do logger externo para a interface esperada pelo sistema.
        
        Args:
            message (str): Mensagem a ser registrada.
            level (str): Nível de log ('INFO', 'WARNING', 'ERROR').
        """
        if level == 'INFO':
            self.external_logger.info(message)
        elif level == 'WARNING':
            self.external_logger.warn(message)
        elif level == 'ERROR':
            self.external_logger.error(message)
        else:
            self.external_logger.debug(message)

# Exemplo de como o padrão Facade poderia ser implementado
class WorkshopServiceFacade:
    """
    Exemplo de como o padrão Facade poderia ser implementado para fornecer
    uma interface simplificada para operações complexas envolvendo múltiplos modelos.
    """
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def register_service_with_parts(self, vehicle_id, service_description, service_cost, parts_list):
        """
        Registra um novo serviço com peças associadas em uma única operação.
        
        Args:
            vehicle_id (int): ID do veículo.
            service_description (str): Descrição do serviço.
            service_cost (float): Custo do serviço.
            parts_list (list): Lista de dicionários com 'part_id' e 'quantity'.
            
        Returns:
            Service: O serviço criado.
        """
        session = self.db_manager.get_session()
        try:
            # Criar o serviço
            service = Service(
                description=service_description,
                cost=service_cost,
                vehicle_id=vehicle_id
            )
            session.add(service)
            session.flush()  # Para obter o ID do serviço
            
            # Adicionar as peças ao serviço
            for part_info in parts_list:
                part = session.query(Part).get(part_info['part_id'])
                if part:
                    service.parts.append(part)
                    # Registrar a quantidade
                    service_part = ServicePart(
                        service_id=service.id,
                        part_id=part.id,
                        quantity=part_info['quantity']
                    )
                    session.add(service_part)
                    
                    # Atualizar o estoque
                    part.stock -= part_info['quantity']
            
            session.commit()
            return service
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
