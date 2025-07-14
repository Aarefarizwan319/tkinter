import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from datetime import datetime, timedelta
import threading

class HotelRestaurantManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel & Restaurant Manager")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')

        # Game state
        self.money = 10000
        self.level = 1
        self.experience = 0
        self.exp_needed = 100
        self.reputation = 50
        self.cleanliness = 100

        # Staff
        self.staff = {
            'chefs': 2,
            'waiters': 3,
            'cleaners': 1,
            'receptionists': 1
        }

        # Rooms
        self.rooms = {
            'single': {'total': 5, 'occupied': 0, 'price': 100},
            'double': {'total': 3, 'occupied': 0, 'price': 150},
            'suite': {'total': 1, 'occupied': 0, 'price': 300}
        }

        # Menu
        self.menu = {
            'Burger': {'price': 15, 'cost': 5, 'time': 10},
            'Pizza': {'price': 20, 'cost': 8, 'time': 15},
            'Pasta': {'price': 18, 'cost': 6, 'time': 12},
            'Salad': {'price': 12, 'cost': 4, 'time': 5},
            'Steak': {'price': 35, 'cost': 15, 'time': 20}
        }

        # Orders and bookings
        self.orders = []
        self.bookings = []
        self.customers_waiting = []

        # Game loop
        self.running = True
        self.last_update = time.time()

        self.create_widgets()
        self.start_game_loop()

    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Top info panel
        info_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        info_frame.pack(fill='x', pady=(0, 10))

        # Money, Level, Reputation
        self.money_label = tk.Label(info_frame, text=f"Money: ${self.money}", 
                                   bg='#34495e', fg='#ecf0f1', font=('Arial', 12, 'bold'))
        self.money_label.pack(side='left', padx=10, pady=5)

        self.level_label = tk.Label(info_frame, text=f"Level: {self.level}", 
                                   bg='#34495e', fg='#ecf0f1', font=('Arial', 12, 'bold'))
        self.level_label.pack(side='left', padx=10, pady=5)

        self.exp_label = tk.Label(info_frame, text=f"EXP: {self.experience}/{self.exp_needed}", 
                                 bg='#34495e', fg='#ecf0f1', font=('Arial', 12, 'bold'))
        self.exp_label.pack(side='left', padx=10, pady=5)

        self.rep_label = tk.Label(info_frame, text=f"Reputation: {self.reputation}%", 
                                 bg='#34495e', fg='#ecf0f1', font=('Arial', 12, 'bold'))
        self.rep_label.pack(side='left', padx=10, pady=5)

        self.clean_label = tk.Label(info_frame, text=f"Cleanliness: {self.cleanliness}%", 
                                   bg='#34495e', fg='#ecf0f1', font=('Arial', 12, 'bold'))
        self.clean_label.pack(side='left', padx=10, pady=5)

        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)

        # Restaurant tab
        self.create_restaurant_tab()

        # Hotel tab
        self.create_hotel_tab()

        # Staff tab
        self.create_staff_tab()

        # Upgrades tab
        self.create_upgrades_tab()

        # Kitchen tab
        self.create_kitchen_tab()

    def create_restaurant_tab(self):
        restaurant_frame = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(restaurant_frame, text='Restaurant')

        # Left panel - Menu and Orders
        left_panel = tk.Frame(restaurant_frame, bg='#bdc3c7', relief='raised', bd=2)
        left_panel.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        # Menu section
        menu_label = tk.Label(left_panel, text="MENU", bg='#bdc3c7', fg='#2c3e50', 
                             font=('Arial', 14, 'bold'))
        menu_label.pack(pady=10)

        menu_frame = tk.Frame(left_panel, bg='#bdc3c7')
        menu_frame.pack(fill='x', padx=10)

        for item, details in self.menu.items():
            item_frame = tk.Frame(menu_frame, bg='#ecf0f1', relief='raised', bd=1)
            item_frame.pack(fill='x', pady=2)

            tk.Label(item_frame, text=f"{item} - ${details['price']}", 
                    bg='#ecf0f1', fg='#2c3e50', font=('Arial', 10)).pack(side='left', padx=5)

            tk.Button(item_frame, text="Add to Order", 
                     command=lambda i=item: self.add_to_order(i),
                     bg='#27ae60', fg='white', font=('Arial', 8)).pack(side='right', padx=5)

        # Current orders section
        orders_label = tk.Label(left_panel, text="CURRENT ORDERS", bg='#bdc3c7', fg='#2c3e50', 
                               font=('Arial', 14, 'bold'))
        orders_label.pack(pady=(20, 10))

        self.orders_listbox = tk.Listbox(left_panel, bg='#ecf0f1', fg='#2c3e50', 
                                        font=('Arial', 10), height=8)
        self.orders_listbox.pack(fill='x', padx=10)

        # Right panel - Customers and Service
        right_panel = tk.Frame(restaurant_frame, bg='#95a5a6', relief='raised', bd=2)
        right_panel.pack(side='right', fill='both', expand=True, padx=5, pady=5)

        customers_label = tk.Label(right_panel, text="WAITING CUSTOMERS", bg='#95a5a6', fg='#2c3e50', 
                                  font=('Arial', 14, 'bold'))
        customers_label.pack(pady=10)

        self.customers_listbox = tk.Listbox(right_panel, bg='#ecf0f1', fg='#2c3e50', 
                                           font=('Arial', 10), height=10)
        self.customers_listbox.pack(fill='x', padx=10)

        service_frame = tk.Frame(right_panel, bg='#95a5a6')
        service_frame.pack(fill='x', padx=10, pady=10)

        tk.Button(service_frame, text="Serve Customer", command=self.serve_customer,
                 bg='#e74c3c', fg='white', font=('Arial', 12, 'bold')).pack(fill='x', pady=2)

        tk.Button(service_frame, text="Clean Tables", command=self.clean_tables,
                 bg='#f39c12', fg='white', font=('Arial', 12, 'bold')).pack(fill='x', pady=2)

    def create_hotel_tab(self):
        hotel_frame = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(hotel_frame, text='Hotel')

        # Reception section
        reception_frame = tk.Frame(hotel_frame, bg='#bdc3c7', relief='raised', bd=2)
        reception_frame.pack(fill='x', padx=10, pady=10)

        reception_label = tk.Label(reception_frame, text="RECEPTION", bg='#bdc3c7', fg='#2c3e50', 
                                  font=('Arial', 14, 'bold'))
        reception_label.pack(pady=10)

        # Room status
        rooms_frame = tk.Frame(reception_frame, bg='#bdc3c7')
        rooms_frame.pack(fill='x', padx=10, pady=10)

        self.room_labels = {}
        for room_type, details in self.rooms.items():
            room_frame = tk.Frame(rooms_frame, bg='#ecf0f1', relief='raised', bd=1)
            room_frame.pack(fill='x', pady=2)

            label_text = f"{room_type.title()} Rooms: {details['occupied']}/{details['total']} - ${details['price']}/night"
            self.room_labels[room_type] = tk.Label(room_frame, text=label_text, 
                                                  bg='#ecf0f1', fg='#2c3e50', font=('Arial', 10))
            self.room_labels[room_type].pack(side='left', padx=5)

            tk.Button(room_frame, text="Book", 
                     command=lambda rt=room_type: self.book_room(rt),
                     bg='#3498db', fg='white', font=('Arial', 8)).pack(side='right', padx=5)

        # Current bookings
        bookings_label = tk.Label(hotel_frame, text="CURRENT BOOKINGS", bg='#ecf0f1', fg='#2c3e50', 
                                 font=('Arial', 14, 'bold'))
        bookings_label.pack(pady=10)

        self.bookings_listbox = tk.Listbox(hotel_frame, bg='#bdc3c7', fg='#2c3e50', 
                                          font=('Arial', 10), height=8)
        self.bookings_listbox.pack(fill='x', padx=10)

        # Hotel management buttons
        management_frame = tk.Frame(hotel_frame, bg='#ecf0f1')
        management_frame.pack(fill='x', padx=10, pady=10)

        tk.Button(management_frame, text="Check-in Customer", command=self.checkin_customer,
                 bg='#27ae60', fg='white', font=('Arial', 12, 'bold')).pack(side='left', padx=5)

        tk.Button(management_frame, text="Check-out Customer", command=self.checkout_customer,
                 bg='#e74c3c', fg='white', font=('Arial', 12, 'bold')).pack(side='left', padx=5)

        tk.Button(management_frame, text="Clean Rooms", command=self.clean_rooms,
                 bg='#f39c12', fg='white', font=('Arial', 12, 'bold')).pack(side='left', padx=5)

    def create_staff_tab(self):
        staff_frame = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(staff_frame, text='Staff Management')

        staff_label = tk.Label(staff_frame, text="STAFF MANAGEMENT", bg='#ecf0f1', fg='#2c3e50', 
                              font=('Arial', 16, 'bold'))
        staff_label.pack(pady=20)

        self.staff_labels = {}
        for staff_type, count in self.staff.items():
            staff_row = tk.Frame(staff_frame, bg='#bdc3c7', relief='raised', bd=2)
            staff_row.pack(fill='x', padx=20, pady=5)

            label_text = f"{staff_type.title()}: {count}"
            self.staff_labels[staff_type] = tk.Label(staff_row, text=label_text, 
                                                    bg='#bdc3c7', fg='#2c3e50', font=('Arial', 12))
            self.staff_labels[staff_type].pack(side='left', padx=10, pady=10)

            hire_cost = 1000 + (count * 200)
            tk.Button(staff_row, text=f"Hire (+${hire_cost})", 
                     command=lambda st=staff_type, cost=hire_cost: self.hire_staff(st, cost),
                     bg='#27ae60', fg='white', font=('Arial', 10)).pack(side='right', padx=10, pady=10)

        # Staff efficiency display
        efficiency_frame = tk.Frame(staff_frame, bg='#95a5a6', relief='raised', bd=2)
        efficiency_frame.pack(fill='x', padx=20, pady=20)

        tk.Label(efficiency_frame, text="STAFF EFFICIENCY", bg='#95a5a6', fg='#2c3e50', 
                font=('Arial', 14, 'bold')).pack(pady=10)

        self.efficiency_text = tk.Text(efficiency_frame, height=6, bg='#ecf0f1', fg='#2c3e50', 
                                      font=('Arial', 10))
        self.efficiency_text.pack(fill='x', padx=10, pady=10)

        self.update_efficiency_display()

    def create_upgrades_tab(self):
        upgrades_frame = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(upgrades_frame, text='Upgrades')

        upgrades_label = tk.Label(upgrades_frame, text="BUSINESS UPGRADES", bg='#ecf0f1', fg='#2c3e50', 
                                 font=('Arial', 16, 'bold'))
        upgrades_label.pack(pady=20)

        # Room upgrades
        room_upgrades = tk.Frame(upgrades_frame, bg='#bdc3c7', relief='raised', bd=2)
        room_upgrades.pack(fill='x', padx=20, pady=10)

        tk.Label(room_upgrades, text="ROOM UPGRADES", bg='#bdc3c7', fg='#2c3e50', 
                font=('Arial', 14, 'bold')).pack(pady=10)

        upgrades_list = [
            ("Add Single Room", 5000, lambda: self.add_room('single')),
            ("Add Double Room", 8000, lambda: self.add_room('double')),
            ("Add Suite", 15000, lambda: self.add_room('suite')),
            ("Kitchen Equipment", 3000, lambda: self.upgrade_kitchen()),
            ("Better Furniture", 4000, lambda: self.upgrade_furniture()),
            ("Marketing Campaign", 2000, lambda: self.marketing_campaign())
        ]

        for upgrade_name, cost, func in upgrades_list:
            upgrade_row = tk.Frame(room_upgrades, bg='#ecf0f1', relief='raised', bd=1)
            upgrade_row.pack(fill='x', padx=10, pady=2)

            tk.Label(upgrade_row, text=f"{upgrade_name} - ${cost}", 
                    bg='#ecf0f1', fg='#2c3e50', font=('Arial', 10)).pack(side='left', padx=5)

            tk.Button(upgrade_row, text="Buy", command=lambda c=cost, f=func: self.buy_upgrade(c, f),
                     bg='#9b59b6', fg='white', font=('Arial', 8)).pack(side='right', padx=5)

    def create_kitchen_tab(self):
        kitchen_frame = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(kitchen_frame, text='Kitchen')

        kitchen_label = tk.Label(kitchen_frame, text="KITCHEN OPERATIONS", bg='#ecf0f1', fg='#2c3e50', 
                                font=('Arial', 16, 'bold'))
        kitchen_label.pack(pady=20)

        # Cooking queue
        cooking_frame = tk.Frame(kitchen_frame, bg='#bdc3c7', relief='raised', bd=2)
        cooking_frame.pack(fill='x', padx=20, pady=10)

        tk.Label(cooking_frame, text="COOKING QUEUE", bg='#bdc3c7', fg='#2c3e50', 
                font=('Arial', 14, 'bold')).pack(pady=10)

        self.cooking_listbox = tk.Listbox(cooking_frame, bg='#ecf0f1', fg='#2c3e50', 
                                         font=('Arial', 10), height=8)
        self.cooking_listbox.pack(fill='x', padx=10, pady=10)

        # Kitchen stats
        stats_frame = tk.Frame(kitchen_frame, bg='#95a5a6', relief='raised', bd=2)
        stats_frame.pack(fill='x', padx=20, pady=10)

        tk.Label(stats_frame, text="KITCHEN STATISTICS", bg='#95a5a6', fg='#2c3e50', 
                font=('Arial', 14, 'bold')).pack(pady=10)

        self.kitchen_stats = tk.Text(stats_frame, height=6, bg='#ecf0f1', fg='#2c3e50', 
                                    font=('Arial', 10))
        self.kitchen_stats.pack(fill='x', padx=10, pady=10)

        self.update_kitchen_stats()

    def add_to_order(self, item):
        customer_name = f"Customer {random.randint(1, 999)}"
        order_time = time.time()
        order = {
            'customer': customer_name,
            'item': item,
            'time': order_time,
            'status': 'pending'
        }
        self.orders.append(order)
        self.update_orders_display()

        # Add to cooking queue
        cooking_time = self.menu[item]['time']
        self.cooking_listbox.insert(tk.END, f"{item} for {customer_name} - {cooking_time}s")

        # Start cooking in background
        threading.Thread(target=self.cook_order, args=(order,), daemon=True).start()

    def cook_order(self, order):
        cook_time = self.menu[order['item']]['time']
        # Reduce time based on chef count
        actual_time = max(1, cook_time - (self.staff['chefs'] * 2))
        time.sleep(actual_time)

        order['status'] = 'ready'
        self.update_orders_display()

        # Remove from cooking queue
        self.root.after(0, self.update_cooking_queue)

    def update_cooking_queue(self):
        # Clear and rebuild cooking queue
        self.cooking_listbox.delete(0, tk.END)
        for order in self.orders:
            if order['status'] == 'pending':
                item = order['item']
                customer = order['customer']
                cook_time = self.menu[item]['time']
                self.cooking_listbox.insert(tk.END, f"{item} for {customer} - {cook_time}s")

    def serve_customer(self):
        ready_orders = [order for order in self.orders if order['status'] == 'ready']
        if not ready_orders:
            messagebox.showinfo("No Orders", "No orders ready to serve!")
            return

        order = ready_orders[0]
        self.orders.remove(order)

        # Calculate payment and tip
        price = self.menu[order['item']]['price']
        tip = random.randint(0, price // 2)
        total = price + tip

        self.money += total
        self.experience += 10
        self.reputation += random.randint(1, 3)

        self.update_displays()
        self.update_orders_display()

        messagebox.showinfo("Order Served", f"Served {order['item']} to {order['customer']}\nPayment: ${price}\nTip: ${tip}\nTotal: ${total}")

    def book_room(self, room_type):
        if self.rooms[room_type]['occupied'] >= self.rooms[room_type]['total']:
            messagebox.showwarning("Room Full", f"No {room_type} rooms available!")
            return

        customer_name = f"Guest {random.randint(1, 999)}"
        check_in = datetime.now()
        check_out = check_in + timedelta(days=random.randint(1, 7))

        booking = {
            'customer': customer_name,
            'room_type': room_type,
            'check_in': check_in,
            'check_out': check_out,
            'price': self.rooms[room_type]['price']
        }

        self.bookings.append(booking)
        self.rooms[room_type]['occupied'] += 1

        self.update_bookings_display()
        self.update_room_labels()

        messagebox.showinfo("Booking Confirmed", f"Booked {room_type} room for {customer_name}")

    def checkin_customer(self):
        if not self.bookings:
            messagebox.showinfo("No Bookings", "No bookings to check in!")
            return

        booking = self.bookings[0]
        payment = booking['price']
        self.money += payment
        self.experience += 15
        self.reputation += random.randint(1, 2)

        self.update_displays()
        messagebox.showinfo("Check-in", f"Checked in {booking['customer']}\nPayment: ${payment}")

    def checkout_customer(self):
        if not self.bookings:
            messagebox.showinfo("No Bookings", "No bookings to check out!")
            return

        booking = self.bookings.pop(0)
        self.rooms[booking['room_type']]['occupied'] -= 1

        # Additional payment for extra days
        days_stayed = (booking['check_out'] - booking['check_in']).days
        extra_payment = booking['price'] * max(0, days_stayed - 1)

        if extra_payment > 0:
            self.money += extra_payment
            messagebox.showinfo("Check-out", f"Checked out {booking['customer']}\nExtra payment: ${extra_payment}")
        else:
            messagebox.showinfo("Check-out", f"Checked out {booking['customer']}")

        self.update_bookings_display()
        self.update_room_labels()
        self.update_displays()

    def hire_staff(self, staff_type, cost):
        if self.money < cost:
            messagebox.showwarning("Insufficient Funds", f"Need ${cost} to hire {staff_type}!")
            return

        self.money -= cost
        self.staff[staff_type] += 1

        self.update_displays()
        self.update_staff_labels()
        self.update_efficiency_display()

        messagebox.showinfo("Staff Hired", f"Hired 1 {staff_type[:-1]}!")

    def buy_upgrade(self, cost, upgrade_func):
        if self.money < cost:
            messagebox.showwarning("Insufficient Funds", f"Need ${cost} for this upgrade!")
            return

        self.money -= cost
        upgrade_func()
        self.update_displays()

    def add_room(self, room_type):
        self.rooms[room_type]['total'] += 1
        self.update_room_labels()
        messagebox.showinfo("Room Added", f"Added 1 {room_type} room!")

    def upgrade_kitchen(self):
        # Improve cooking efficiency
        for item in self.menu:
            self.menu[item]['time'] = max(1, self.menu[item]['time'] - 1)
        messagebox.showinfo("Kitchen Upgraded", "Kitchen equipment upgraded! Faster cooking times!")

    def upgrade_furniture(self):
        self.reputation += 10
        messagebox.showinfo("Furniture Upgraded", "Better furniture installed! Reputation increased!")

    def marketing_campaign(self):
        # Generate more customers
        self.reputation += 5
        messagebox.showinfo("Marketing Campaign", "Marketing campaign launched! More customers coming!")

    def clean_tables(self):
        if self.staff['cleaners'] == 0:
            messagebox.showwarning("No Cleaners", "Hire cleaners to clean tables!")
            return

        self.cleanliness = min(100, self.cleanliness + 10)
        self.reputation += 1
        self.update_displays()
        messagebox.showinfo("Cleaning", "Tables cleaned! Cleanliness improved!")

    def clean_rooms(self):
        if self.staff['cleaners'] == 0:
            messagebox.showwarning("No Cleaners", "Hire cleaners to clean rooms!")
            return

        self.cleanliness = min(100, self.cleanliness + 15)
        self.reputation += 2
        self.update_displays()
        messagebox.showinfo("Cleaning", "Rooms cleaned! Cleanliness improved!")

    def update_displays(self):
        self.money_label.config(text=f"Money: ${self.money}")
        self.level_label.config(text=f"Level: {self.level}")
        self.exp_label.config(text=f"EXP: {self.experience}/{self.exp_needed}")
        self.rep_label.config(text=f"Reputation: {self.reputation}%")
        self.clean_label.config(text=f"Cleanliness: {self.cleanliness}%")

        # Check for level up
        if self.experience >= self.exp_needed:
            self.level += 1
            self.experience = 0
            self.exp_needed = int(self.exp_needed * 1.5)
            messagebox.showinfo("Level Up!", f"Congratulations! You reached level {self.level}!")

    def update_orders_display(self):
        self.orders_listbox.delete(0, tk.END)
        for order in self.orders:
            status = "✓ Ready" if order['status'] == 'ready' else "⏳ Cooking"
            self.orders_listbox.insert(tk.END, f"{order['item']} for {order['customer']} - {status}")

    def update_bookings_display(self):
        self.bookings_listbox.delete(0, tk.END)
        for booking in self.bookings:
            check_in = booking['check_in'].strftime("%m/%d")
            check_out = booking['check_out'].strftime("%m/%d")
            self.bookings_listbox.insert(tk.END, 
                f"{booking['customer']} - {booking['room_type']} ({check_in} to {check_out})")

    def update_room_labels(self):
        for room_type, label in self.room_labels.items():
            details = self.rooms[room_type]
            label_text = f"{room_type.title()} Rooms: {details['occupied']}/{details['total']} - ${details['price']}/night"
            label.config(text=label_text)

    def update_staff_labels(self):
        for staff_type, label in self.staff_labels.items():
            label.config(text=f"{staff_type.title()}: {self.staff[staff_type]}")

    def update_efficiency_display(self):
        self.efficiency_text.delete(1.0, tk.END)
        efficiency_text = "STAFF EFFICIENCY REPORT:\n\n"

        # Calculate efficiency based on staff count
        chef_efficiency = min(100, self.staff['chefs'] * 25)
        waiter_efficiency = min(100, self.staff['waiters'] * 20)
        cleaner_efficiency = min(100, self.staff['cleaners'] * 30)
        reception_efficiency = min(100, self.staff['receptionists'] * 40)

        efficiency_text += f"Kitchen Efficiency: {chef_efficiency}%\n"
        efficiency_text += f"Service Efficiency: {waiter_efficiency}%\n"
        efficiency_text += f"Cleanliness Efficiency: {cleaner_efficiency}%\n"
        efficiency_text += f"Reception Efficiency: {reception_efficiency}%\n\n"
        efficiency_text += "Higher efficiency = Faster service & happier customers!"

        self.efficiency_text.insert(1.0, efficiency_text)

    def update_kitchen_stats(self):
        self.kitchen_stats.delete(1.0, tk.END)
        stats_text = "KITCHEN STATISTICS:\n\n"

        total_orders = len(self.orders)
        ready_orders = len([o for o in self.orders if o['status'] == 'ready'])
        cooking_orders = total_orders - ready_orders

        stats_text += f"Total Orders: {total_orders}\n"
        stats_text += f"Orders Cooking: {cooking_orders}\n"
        stats_text += f"Orders Ready: {ready_orders}\n"
        stats_text += f"Kitchen Staff: {self.staff['chefs']} chefs\n\n"
        stats_text += "MENU ITEMS:\n"

        for item, details in self.menu.items():
            stats_text += f"{item}: ${details['price']} (Cook time: {details['time']}s)\n"

        self.kitchen_stats.insert(1.0, stats_text)

    def start_game_loop(self):
        def game_loop():
            while self.running:
                current_time = time.time()
                # Update stats every 5 seconds
                if current_time - self.last_update >= 5:
                    self.last_update = current_time

                    # Simulate reputation decay
                    self.reputation = max(0, self.reputation - 1)

                    # Simulate cleanliness decay
                    self.cleanliness = max(0, self.cleanliness - 1)

                    # Random chance of new customer if rep is high
                    if self.reputation >= 60 and random.random() < 0.3:
                        new_customer = f"Customer {random.randint(1000, 9999)}"
                        self.customers_waiting.append(new_customer)
                        self.customers_listbox.insert(tk.END, new_customer)

                    self.root.after(0, self.update_displays)
                    self.root.after(0, self.update_kitchen_stats)

                time.sleep(1)

                threading.Thread(target=game_loop, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelRestaurantManager(root)
    root.mainloop()
