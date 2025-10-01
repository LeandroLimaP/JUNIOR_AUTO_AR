from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from sqlalchemy.orm import joinedload
from models import DatabaseManager, ModelFactory, Client, Vehicle, Service, Part, ServicePart
import datetime

app = Flask(__name__)
app.config.from_object(Config)
db_manager = DatabaseManager(app.config["SQLALCHEMY_DATABASE_URI"])

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rotas para Clientes
@app.route('/clients')
def clients():
    session = db_manager.get_session()
    try:
        all_clients = session.query(Client).all()
        return render_template('clients.html', clients=all_clients)
    finally:
        session.close()

@app.route('/client/new', methods=['GET', 'POST'])
def new_client():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        email = request.form['email']
        
        session = db_manager.get_session()
        try:
            client = ModelFactory.create_model('Client', name=name, address=address, phone=phone, email=email)
            session.add(client)
            session.commit()
            flash('Cliente adicionado com sucesso!', 'success')
            return redirect(url_for('clients'))
        except Exception as e:
            session.rollback()
            flash(f'Erro ao adicionar cliente: {str(e)}', 'danger')
        finally:
            session.close()
    
    return render_template('new_client.html')

@app.route('/client/edit/<int:client_id>', methods=['GET', 'POST'])
def edit_client(client_id):
    session = db_manager.get_session()
    try:
        client = session.query(Client).get(client_id)
        
        if not client:
            flash('Cliente não encontrado!', 'danger')
            return redirect(url_for('clients'))
        
        if request.method == 'POST':
            client.name = request.form['name']
            client.address = request.form['address']
            client.phone = request.form['phone']
            client.email = request.form['email']
            
            session.commit()
            flash('Cliente atualizado com sucesso!', 'success')
            return redirect(url_for('clients'))
        
        return render_template('edit_client.html', client=client)
    except Exception as e:
        session.rollback()
        flash(f'Erro ao editar cliente: {str(e)}', 'danger')
        return redirect(url_for('clients'))
    finally:
        session.close()

@app.route('/client/delete/<int:client_id>', methods=['POST'])
def delete_client(client_id):
    session = db_manager.get_session()
    try:
        client = session.query(Client).get(client_id)
        
        if not client:
            flash('Cliente não encontrado!', 'danger')
            return redirect(url_for('clients'))
        
        session.delete(client)
        session.commit()
        flash('Cliente excluído com sucesso!', 'success')
        return redirect(url_for('clients'))
    except Exception as e:
        session.rollback()
        flash(f'Erro ao excluir cliente: {str(e)}', 'danger')
        return redirect(url_for('clients'))
    finally:
        session.close()

# Rotas para Veículos
@app.route('/vehicles')
def vehicles():
    session = db_manager.get_session()
    try:
        all_vehicles = session.query(Vehicle).options(joinedload(Vehicle.client)).all()
        return render_template('vehicles.html', vehicles=all_vehicles)
    finally:
        session.close()

@app.route('/vehicle/new', methods=['GET', 'POST'])
def new_vehicle():
    session = db_manager.get_session()
    try:
        if request.method == 'POST':
            make = request.form['make']
            model = request.form['model']
            year = int(request.form['year'])
            license_plate = request.form['license_plate']
            client_id = int(request.form['client_id'])
            
            vehicle = ModelFactory.create_model('Vehicle', make=make, model=model, year=year, 
                                              license_plate=license_plate, client_id=client_id)
            session.add(vehicle)
            session.commit()
            flash('Veículo adicionado com sucesso!', 'success')
            return redirect(url_for('vehicles'))
        
        clients = session.query(Client).all()
        return render_template('new_vehicle.html', clients=clients)
    except Exception as e:
        session.rollback()
        flash(f'Erro ao adicionar veículo: {str(e)}', 'danger')
        return redirect(url_for('vehicles'))
    finally:
        session.close()

@app.route('/vehicle/edit/<int:vehicle_id>', methods=['GET', 'POST'])
def edit_vehicle(vehicle_id):
    session = db_manager.get_session()
    try:
        vehicle = session.query(Vehicle).get(vehicle_id)
        
        if not vehicle:
            flash('Veículo não encontrado!', 'danger')
            return redirect(url_for('vehicles'))
        
        if request.method == 'POST':
            vehicle.make = request.form['make']
            vehicle.model = request.form['model']
            vehicle.year = int(request.form['year'])
            vehicle.license_plate = request.form['license_plate']
            vehicle.client_id = int(request.form['client_id'])
            
            session.commit()
            flash('Veículo atualizado com sucesso!', 'success')
            return redirect(url_for('vehicles'))
        
        clients = session.query(Client).all()
        return render_template('edit_vehicle.html', vehicle=vehicle, clients=clients)
    except Exception as e:
        session.rollback()
        flash(f'Erro ao editar veículo: {str(e)}', 'danger')
        return redirect(url_for('vehicles'))
    finally:
        session.close()

@app.route('/vehicle/delete/<int:vehicle_id>', methods=['POST'])
def delete_vehicle(vehicle_id):
    session = db_manager.get_session()
    try:
        vehicle = session.query(Vehicle).get(vehicle_id)
        
        if not vehicle:
            flash('Veículo não encontrado!', 'danger')
            return redirect(url_for('vehicles'))
        
        session.delete(vehicle)
        session.commit()
        flash('Veículo excluído com sucesso!', 'success')
        return redirect(url_for('vehicles'))
    except Exception as e:
        session.rollback()
        flash(f'Erro ao excluir veículo: {str(e)}', 'danger')
        return redirect(url_for('vehicles'))
    finally:
        session.close()

# Rotas para Serviços
@app.route('/services')
def services():
    session = db_manager.get_session()
    try:
        all_services = session.query(Service).options(joinedload(Service.vehicle)).all()
        return render_template('services.html', services=all_services)
    finally:
        session.close()

@app.route('/service/new', methods=['GET', 'POST'])
def new_service():
    session = db_manager.get_session()
    try:
        if request.method == 'POST':
            description = request.form['description']
            cost = float(request.form['cost'])
            vehicle_id = int(request.form['vehicle_id'])
            
            service = ModelFactory.create_model('Service', description=description, cost=cost, 
                                              vehicle_id=vehicle_id, date=datetime.datetime.now())
            session.add(service)
            session.commit()
            flash('Serviço adicionado com sucesso!', 'success')
            return redirect(url_for('services'))
        
        vehicles = session.query(Vehicle).all()
        return render_template('new_service.html', vehicles=vehicles)
    except Exception as e:
        session.rollback()
        flash(f'Erro ao adicionar serviço: {str(e)}', 'danger')
        return redirect(url_for('services'))
    finally:
        session.close()

@app.route('/service/edit/<int:service_id>', methods=['GET', 'POST'])
def edit_service(service_id):
    session = db_manager.get_session()
    try:
        service = session.query(Service).get(service_id)
        
        if not service:
            flash('Serviço não encontrado!', 'danger')
            return redirect(url_for('services'))
        
        if request.method == 'POST':
            service.description = request.form['description']
            service.cost = float(request.form['cost'])
            service.vehicle_id = int(request.form['vehicle_id'])
            
            session.commit()
            flash('Serviço atualizado com sucesso!', 'success')
            return redirect(url_for('services'))
        
        vehicles = session.query(Vehicle).all()
        return render_template('edit_service.html', service=service, vehicles=vehicles)
    except Exception as e:
        session.rollback()
        flash(f'Erro ao editar serviço: {str(e)}', 'danger')
        return redirect(url_for('services'))
    finally:
        session.close()

@app.route('/service/delete/<int:service_id>', methods=['POST'])
def delete_service(service_id):
    session = db_manager.get_session()
    try:
        service = session.query(Service).get(service_id)
        
        if not service:
            flash('Serviço não encontrado!', 'danger')
            return redirect(url_for('services'))
        
        session.delete(service)
        session.commit()
        flash('Serviço excluído com sucesso!', 'success')
        return redirect(url_for('services'))
    except Exception as e:
        session.rollback()
        flash(f'Erro ao excluir serviço: {str(e)}', 'danger')
        return redirect(url_for('services'))
    finally:
        session.close()

# Rotas para Peças
@app.route('/parts')
def parts():
    session = db_manager.get_session()
    try:
        all_parts = session.query(Part).all()
        return render_template('parts.html', parts=all_parts)
    finally:
        session.close()

@app.route('/part/new', methods=['GET', 'POST'])
def new_part():
    session = db_manager.get_session()
    try:
        if request.method == 'POST':
            name = request.form['name']
            price = float(request.form['price'])
            stock = int(request.form['stock'])
            
            part = ModelFactory.create_model('Part', name=name, price=price, stock=stock)
            session.add(part)
            session.commit()
            flash('Peça adicionada com sucesso!', 'success')
            return redirect(url_for('parts'))
        
        return render_template('new_part.html')
    except Exception as e:
        session.rollback()
        flash(f'Erro ao adicionar peça: {str(e)}', 'danger')
        return redirect(url_for('parts'))
    finally:
        session.close()

@app.route('/part/edit/<int:part_id>', methods=['GET', 'POST'])
def edit_part(part_id):
    session = db_manager.get_session()
    try:
        part = session.query(Part).get(part_id)
        
        if not part:
            flash('Peça não encontrada!', 'danger')
            return redirect(url_for('parts'))
        
        if request.method == 'POST':
            part.name = request.form['name']
            part.price = float(request.form['price'])
            part.stock = int(request.form['stock'])
            
            session.commit()
            flash('Peça atualizada com sucesso!', 'success')
            return redirect(url_for('parts'))
        
        return render_template('edit_part.html', part=part)
    except Exception as e:
        session.rollback()
        flash(f'Erro ao editar peça: {str(e)}', 'danger')
        return redirect(url_for('parts'))
    finally:
        session.close()

@app.route('/part/delete/<int:part_id>', methods=['POST'])
def delete_part(part_id):
    session = db_manager.get_session()
    try:
        part = session.query(Part).get(part_id)
        
        if not part:
            flash('Peça não encontrada!', 'danger')
            return redirect(url_for('parts'))
        
        session.delete(part)
        session.commit()
        flash('Peça excluída com sucesso!', 'success')
        return redirect(url_for('parts'))
    except Exception as e:
        session.rollback()
        flash(f'Erro ao excluir peça: {str(e)}', 'danger')
        return redirect(url_for('parts'))
    finally:
        session.close()

# Inicialização do banco de dados
    db_manager = DatabaseManager()
    Base.metadata.create_all(db_manager.engine)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    # Inicializa o banco de dados
    db_manager.create_all()
    app.run(debug=True)
