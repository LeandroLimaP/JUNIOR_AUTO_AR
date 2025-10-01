from models import Base, DatabaseManager, Client, Vehicle, Service, Part
import datetime

def init_db():
    """Inicializa o banco de dados e adiciona alguns dados de exemplo."""
    print("Inicializando o banco de dados...")
    
    # Criar instância do DatabaseManager (Singleton)
    db_manager = DatabaseManager()
    
    # Criar todas as tabelas
    Base.metadata.create_all(db_manager.engine)
    
    # Obter uma sessão
    session = db_manager.get_session()
    
    try:
        # Verificar se já existem dados
        if session.query(Client).count() > 0:
            print("O banco de dados já contém dados. Pulando a inserção de dados de exemplo.")
            return
        
        # Adicionar clientes de exemplo
        print("Adicionando dados de exemplo...")
        
        # Clientes
        client1 = Client(name="Giudison Torres", address="Av Senador Robert Kennedy, 123", phone="940028922", email="giudisontorres@gmail.com")
        client2 = Client(name="Andrew Matheus", address="Avenida Principal, 456", phone="934313218", email="andrewmatheus@gmail.com")
        client3 = Client(name="Leandro Lima", address="Rua ilheus, 40", phone="988066050", email="leandrolima@gmail.com")
        client4 = Client(name="Gabriel Henrique", address="Rua itabuna, 150", phone="986909790", email="gabrielhenrique@gmail.com")
        session.add_all([client1, client2, client3, client4])
        session.flush()  # Para obter os IDs dos clientes
        
        # Veículos
        vehicle1 = Vehicle(make="Toyota", model="Corolla", year=2020, license_plate="QYN1C75", client_id=client4.id)
        vehicle2 = Vehicle(make="Honda", model="Civic", year=2020, license_plate="QYK1H26", client_id=client3.id)
        vehicle3 = Vehicle(make="Ford", model="Focus", year=2018, license_plate="QYL1B69", client_id=client1.id)
        vehicle4 = Vehicle(make="Bmw", model="X1", year=2018, license_plate="GAY1V24", client_id=client2.id)
        session.add_all([vehicle1, vehicle2, vehicle3, vehicle4])
        session.flush()  # Para obter os IDs dos veículos
        
        # Peças
        part1 = Part(name="Bobina Magnética", price=360.00, stock=40)
        part2 = Part(name="Filtro de Ar", price=45.00, stock=60)
        part3 = Part(name="Valvula torre", price=560.00, stock=10)
        part4 = Part(name="Núcleo Evaporador", price=1470.00, stock=5)
        session.add_all([part1, part2, part3, part4])
        session.flush()  # Para obter os IDs das peças
        
        # Serviços
        service1 = Service(description="Troca de bobina e filtro", cost=400.00, date=datetime.datetime.now(), vehicle_id=vehicle1.id)
        service1.parts.append(part1)
        service1.parts.append(part4)
        
        service2 = Service(description="Revisão completa", cost=750.00, date=datetime.datetime.now(), vehicle_id=vehicle2.id)
        service2.parts.append(part1)
        service2.parts.append(part2)
        service2.parts.append(part3)
        service2.parts.append(part4)
        
        session.add_all([service1, service2])
        
        # Commit para salvar todas as alterações
        session.commit()
        print("Dados de exemplo adicionados com sucesso!")
        
    except Exception as e:
        session.rollback()
        print(f"Erro ao adicionar dados de exemplo: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    init_db()
