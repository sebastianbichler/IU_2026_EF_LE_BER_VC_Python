from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
import data_manager
from models import Vegetable, Bed, Customer, Order, SubscriptionBox

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.jinja_env.globals.update(enumerate=enumerate)

# Ensure data is loaded when app starts
data_manager.load_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vegetables', methods=['GET', 'POST'])
def vegetables():
    if request.method == 'POST':
        try:
            name = request.form['name']
            sort = request.form['sort']
            bed_id = int(request.form['bed_id'])
            plant_date = datetime.strptime(request.form['plant_date'], '%Y-%m-%d')
            harvest_date = datetime.strptime(request.form['harvest_date'], '%Y-%m-%d')
            shelf_life = int(request.form['shelf_life'])
            amount = float(request.form['amount'])

            veg = Vegetable(
                name=name, sort=sort, plant_date=plant_date,
                harvest_date=harvest_date, bed_id=bed_id,
                shelf_life_days=shelf_life, amount=amount
            )
            data_manager.vegetables.append(veg)
            data_manager.save_data()
            return redirect(url_for('vegetables'))
        except ValueError as e:
            return f"Error: {e}", 400

    return render_template('vegetables.html', vegetables=data_manager.vegetables, beds=data_manager.beds)

@app.route('/beds', methods=['GET', 'POST'])
def beds():
    if request.method == 'POST':
        try:
            # Simple ID generation
            if not data_manager.beds:
                new_id = 1
            else:
                new_id = max(b.id for b in data_manager.beds) + 1
            
            name = request.form['name']
            size = float(request.form['size'])

            bed = Bed(id=new_id, name=name, size_m2=size)
            data_manager.beds.append(bed)
            data_manager.save_data()
            return redirect(url_for('beds'))
        except ValueError as e:
            return f"Error: {e}", 400

    return render_template('beds.html', beds=data_manager.beds)

@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    if request.method == 'POST':
        try:
            veg_idx = int(request.form['veg_idx'])
            amount = float(request.form['amount'])
            
            if 0 <= veg_idx < len(data_manager.vegetables):
                veg = data_manager.vegetables[veg_idx]
                data_manager.inventory.add_harvest(veg, amount)
                data_manager.save_data()
            return redirect(url_for('inventory'))
        except ValueError:
            return "Error", 400

    fresh_items = list(data_manager.inventory.get_fresh_items())
    expired_items = list(data_manager.inventory.get_expired_items())
    total_amount = data_manager.inventory.get_total_amount()
    
    return render_template('inventory.html', 
                           fresh_items=fresh_items, 
                           expired_items=expired_items, 
                           total_amount=total_amount,
                           vegetables=data_manager.vegetables)

@app.route('/customers', methods=['GET', 'POST'])
def customers():
    if request.method == 'POST':
        name = request.form['name']
        species = request.form['species']
        sub_type = request.form['subscription_type']
        
        customer = Customer(name=name, species=species, subscription_type=sub_type)
        data_manager.customers.append(customer)
        data_manager.save_data()
        return redirect(url_for('customers'))

    return render_template('customers.html', customers=data_manager.customers)

@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'POST':
        try:
            cust_idx = int(request.form['customer_idx'])
            veg_indices = request.form.getlist('veg_indices') # list of strings
            days = int(request.form['days'])
            price = float(request.form['price'])
            
            if 0 <= cust_idx < len(data_manager.customers):
                customer = data_manager.customers[cust_idx]
                
                selected_vegs = []
                for idx_str in veg_indices:
                    idx = int(idx_str)
                    if 0 <= idx < len(data_manager.vegetables):
                        selected_vegs.append(data_manager.vegetables[idx])
                
                order = Order(
                    customer=customer,
                    vegetables=selected_vegs,
                    delivery_date=datetime.now() + timedelta(days=days),
                    price=price
                )
                data_manager.orders.append(order)
                data_manager.save_data()
                return redirect(url_for('orders'))
        except ValueError:
            return "Error", 400

    return render_template('orders.html', 
                           orders=data_manager.orders, 
                           customers=data_manager.customers, 
                           vegetables=data_manager.vegetables)

@app.route('/finances')
def finances():
    from services import calculate_profit
    # No input for costs in this simple view, assuming 0 costs for quick view or just verifying revenue
    # To be proper, we might need a form to input costs, but let's just show revenue for now.
    
    revenue = sum(o.price for o in data_manager.orders)
    return render_template('finance.html', revenue=revenue, orders=data_manager.orders)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
