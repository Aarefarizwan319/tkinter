import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from datetime import datetime, timedelta
import threading
from PIL import Image, ImageTk
import pygame
import math

class HotelRestaurantManager:
    def __init__(self, root):
        self.root = root
        self.root.title("🌟 Hotel & Restaurant Manager 🌟")
        self.root.geometry("1280x900")
        self.root.configure(bg='#2c3e50')
        
        # Initialize pygame for sound
        pygame.mixer.init()
        
        # Load sounds
        self.sounds = {
            'order': pygame.mixer.Sound('sounds/order.wav'),
            'cooking': pygame.mixer.Sound('sounds/cooking.wav'),
            'money': pygame.mixer.Sound('sounds/money.wav'),
            'level_up': pygame.mixer.Sound('sounds/level_up.wav'),
            'clean': pygame.mixer.Sound('sounds/clean.wav')
        }
        
        # Game state
        self.money = 10000
        self.level = 1
        self.experience = 0
        self.exp_needed = 100
        self.reputation = 50
        self.cleanliness = 100
        self.day = 1
        self.time_of_day = 8  # 8 AM
        self.day_length = 60  # seconds
        self.is_night = False
        self.satisfaction = 75
        
        # Staff
        self.staff = {
            'chefs': 2,
            'waiters': 3,
            'cleaners': 1,
            'receptionists': 1
        }
        
        # Staff animations
        self.staff_animations = {
            'chefs': [],
            'waiters': [],
            'cleaners': [],
            'receptionists': []
        }
        
        # Rooms
        self.rooms = {
            'single': {'total': 5, 'occupied': 0, 'price': 100, 'dirty': 0},
            'double': {'total': 3, 'occupied': 0, 'price': 150, 'dirty': 0},
            'suite': {'total': 1, 'occupied': 0, 'price': 300, 'dirty': 0}
        }
        
        # Menu
        self.menu = {
            'Burger': {'price': 15, 'cost': 5, 'time': 10, 'popularity': 0},
            'Pizza': {'price': 20, 'cost': 8, 'time': 15, 'popularity': 0},
            'Pasta': {'price': 18, 'cost': 6, 'time': 12, 'popularity': 0},
            'Salad': {'price': 12, 'cost': 4, 'time': 5, 'popularity': 0},
            'Steak': {'price': 35, 'cost': 15, 'time': 20, 'popularity': 0}
        }
        
        # Orders and bookings
        self.orders = []
        self.bookings = []
        self.customers_waiting = []
        
        # Character images
        self.load_character_images()
        
        # Game loop
        self.running = True
        self.last_update = time.time()
        
        self.create_widgets()
        self.start_game_loop()
        self.start_day_night_cycle()
    
    def load_character_images(self):
        """Load character sprites for animation"""
        try:
            # Chef animations
            for i in range(1, 5):
                img = Image.open(f"sprites/chef_{i}.png").resize((50, 80))
                self.staff_animations['chefs'].append(ImageTk.PhotoImage(img))
            
            # Waiter animations
            for i in range(1, 5):
                img = Image.open(f"sprites/waiter_{i}.png").resize((50, 80))
                self.staff_animations['waiters'].append(ImageTk.PhotoImage(img))
            
            # Cleaner animations
            for i in range(1, 5):
                img = Image.open(f"sprites/cleaner_{i}.png").resize((50, 80))
                self.staff_animations['cleaners'].append(ImageTk.PhotoImage(img))
            
            # Receptionist animations
            for i in range(1, 5):
                img = Image.open(f"sprites/receptionist_{i}.png").resize((50, 80))
                self.staff_animations['receptionists'].append(ImageTk.PhotoImage(img))
            
            # Customer images
            self.customer_images = []
            for i in range(1, 6):
                img = Image.open(f"sprites/customer_{i}.png").resize((60, 90))
                self.customer_images.append(ImageTk.PhotoImage(img))
            
        except Exception as e:
            print(f"Couldn't load images: {e}")
            # Create placeholder images if real images aren't available
            colors = ['red', 'blue', 'green', 'yellow', 'purple']
            self.customer_images = []
            for color in colors:
                img = Image.new('RGB', (60, 90), color)
                self.customer_images.append(ImageTk.PhotoImage(img))
            
            for staff_type in self.staff_animations:
                for i in range(4):
                    img = Image.new('RGB', (50, 80), 'gray')
                    self.staff_animations[staff_type].append(ImageTk.PhotoImage(img))
    
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Top info panel
        info_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        info_frame.pack(fill='x', pady=(0, 10))
        
        # Day/time display
        self.day_label = tk.Label(info_frame, text=f"Day {self.day} | {self.time_of_day}:00", 
                                bg='#34495e', fg='#f1c40f', font=('Arial', 12, 'bold'))
        self.day_label.pack(side='left', padx=10, pady=5)
        
        # Money, Level, Reputation
        self.money_label = tk.Label(info_frame, text=f"💰 ${self.money}", 
                                  bg='#34495e', fg='#2ecc71', font=('Arial', 12, 'bold'))
        self.money_label.pack(side='left', padx=10, pady=5)
        
        self.level_label = tk.Label(info_frame, text=f"🏆 Level {self.level}", 
                                  bg='#34495e', fg='#ecf0f1', font=('Arial', 12, 'bold'))
        self.level_label.pack(side='left', padx=10, pady=5)
        
        self.exp_label = tk.Label(info_frame, text=f"📊 EXP: {self.experience}/{self.exp_needed}", 
                                bg='#34495e', fg='#ecf0f1', font=('Arial', 12, 'bold'))
        self.exp_label.pack(side='left', padx=10, pady=5)
        
        # Reputation progress bar
        rep_frame = tk.Frame(info_frame, bg='#34495e')
        rep_frame.pack(side='left', padx=10, pady=5)
        tk.Label(rep_frame, text="Rep:", bg='#34495e', fg='#ecf0f1', font=('Arial', 10)).pack(side='left')
        self.rep_bar = ttk.Progressbar(rep_frame, orient='horizontal', length=100, mode='determinate')
        self.rep_bar.pack(side='left')
        self.rep_bar['value'] = self.reputation
        
        # Cleanliness progress bar
        clean_frame = tk.Frame(info_frame, bg='#34495e')
        clean_frame.pack(side='left', padx=10, pady=5)
        tk.Label(clean_frame, text="Clean:", bg='#34495e', fg='#ecf0f1', font=('Arial', 10)).pack(side='left')
        self.clean_bar = ttk.Progressbar(clean_frame, orient='horizontal', length=100, mode='determinate')
        self.clean_bar.pack(side='left')
        self.clean_bar['value'] = self.cleanliness
        
        # Satisfaction progress bar
        sat_frame = tk.Frame(info_frame, bg='#34495e')
        sat_frame.pack(side='left', padx=10, pady=5)
        tk.Label(sat_frame, text="Satisfaction:", bg='#34495e', fg='#ecf0f1', font=('Arial', 10)).pack(side='left')
        self.sat_bar = ttk.Progressbar(sat_frame, orient='horizontal', length=100, mode='determinate')
        self.sat_bar.pack(side='left')
        self.sat_bar['value'] = self.satisfaction
        
        # Animation canvas
        self.animation_canvas = tk.Canvas(main_frame, bg='#2c3e50', height=100, highlightthickness=0)
        self.animation_canvas.pack(fill='x', pady=5)
        
        # Draw staff animations
        self.draw_staff_animations()
        
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
        
        # Stats tab
        self.create_stats_tab()
    
    def draw_staff_animations(self):
        """Draw animated staff characters"""
        self.animation_canvas.delete("all")
        
        # Draw day/night background
        bg_color = '#1a2b3c' if self.is_night else '#7fb3d5'
        self.animation_canvas.config(bg=bg_color)
        
        # Draw sun/moon
        if self.is_night:
            self.animation_canvas.create_oval(50, 20, 90, 60, fill='#f7dc6f', outline='#f1c40f')
            self.animation_canvas.create_text(70, 40, text="🌙", font=('Arial', 20))
        else:
            self.animation_canvas.create_oval(50, 20, 90, 60, fill='#f1c40f', outline='#f39c12')
            self.animation_canvas.create_text(70, 40, text="☀️", font=('Arial', 20))
        
        # Draw staff
        x_positions = [150, 250, 350, 450, 550, 650]
        staff_types = ['chefs', 'waiters', 'cleaners', 'receptionists']
        
        for i, staff_type in enumerate(staff_types):
            count = self.staff[staff_type]
            for j in range(count):
                if j < 3:  # Only show up to 3 of each staff type
                    x = x_positions[i] + (j * 60)
                    frame = (int(time.time() * 3) % 4)  # Animate based on time
                    img = self.staff_animations[staff_type][frame]
                    self.animation_canvas.create_image(x, 60, image=img, anchor='center')
                    self.animation_canvas.create_text(x, 100, text=staff_type[:-1].title(), 
                                                     fill='white', font=('Arial', 8))
    
    def create_restaurant_tab(self):
        restaurant_frame = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(restaurant_frame, text='🍽️ Restaurant')
        
        # Left panel - Menu and Orders
        left_panel = tk.Frame(restaurant_frame, bg='#bdc3c7', relief='raised', bd=2)
        left_panel.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        # Menu section
        menu_label = tk.Label(left_panel, text="🍴 MENU", bg='#bdc3c7', fg='#2c3e50', 
                             font=('Arial', 14, 'bold'))
        menu_label.pack(pady=10)
        
        menu_frame = tk.Frame(left_panel, bg='#bdc3c7')
        menu_frame.pack(fill='x', padx=10)
        
        for item, details in self.menu.items():
            item_frame = tk.Frame(menu_frame, bg='#ecf0f1', relief='raised', bd=1)
            item_frame.pack(fill='x', pady=2)
            
            # Add popularity stars
            stars = '★' * (details['popularity'] // 20)
            if not stars:
                stars = '☆'
                
            tk.Label(item_frame, text=f"{item} - ${details['price']} {stars}", 
                    bg='#ecf0f1', fg='#2c3e50', font=('Arial', 10)).pack(side='left', padx=5)
            
            tk.Button(item_frame, text="Add to Order", 
                     command=lambda i=item: self.add_to_order(i),
                     bg='#27ae60', fg='white', font=('Arial', 8)).pack(side='right', padx=5)
        
        # Current orders section
        orders_label = tk.Label(left_panel, text="📋 CURRENT ORDERS", bg='#bdc3c7', fg='#2c3e50', 
                               font=('Arial', 14, 'bold'))
        orders_label.pack(pady=(20, 10))
        
        self.orders_listbox = tk.Listbox(left_panel, bg='#ecf0f1', fg='#2c3e50', 
                                        font=('Arial', 10), height=8)
        self.orders_listbox.pack(fill='x', padx=10)
        
        # Right panel - Customers and Service
        right_panel = tk.Frame(restaurant_frame, bg='#95a5a6', relief='raised', bd=2)
        right_panel.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        customers_label = tk.Label(right_panel, text="👥 WAITING CUSTOMERS", bg='#95a5a6', fg='#2c3e50', 
                                  font=('Arial', 14, 'bold'))
        customers_label.pack(pady=10)
        
        # Customer canvas with images
        self.customer_canvas = tk.Canvas(right_panel, bg='#ecf0f1', height=150)
        self.customer_canvas.pack(fill='x', padx=10, pady=5)
        
        service_frame = tk.Frame(right_panel, bg='#95a5a6')
        service_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(service_frame, text="🍽️ Serve Customer", command=self.serve_customer,
                 bg='#e74c3c', fg='white', font=('Arial', 12, 'bold')).pack(fill='x', pady=2)
        
        tk.Button(service_frame, text="🧹 Clean Tables", command=self.clean_tables,
                 bg='#f39c12', fg='white', font=('Arial', 12, 'bold')).pack(fill='x', pady=2)
        
        # Customer satisfaction display
        sat_frame = tk.Frame(right_panel, bg='#95a5a6')
        sat_frame.pack(fill='x', padx=10, pady=5)
        tk.Label(sat_frame, text="Current Customer Mood:", bg='#95a5a6', 
                font=('Arial', 10)).pack(side='left')
        self.current_sat_label = tk.Label(sat_frame, text="😊", bg='#95a5a6', 
                                        font=('Arial', 14))
        self.current_sat_label.pack(side='right')
    
    def update_customer_display(self):
        """Update the customer canvas with customer images"""
        self.customer_canvas.delete("all")
        
        if not self.customers_waiting:
            self.customer_canvas.create_text(150, 75, text="No customers waiting", 
                                          fill='#7f8c8d', font=('Arial', 12))
            self.current_sat_label.config(text="😴")
            return
        
        # Display up to 6 customers
        for i, customer in enumerate(self.customers_waiting[:6]):
            x_pos = 50 + (i * 100)
            img_idx = hash(customer) % len(self.customer_images)
            self.customer_canvas.create_image(x_pos, 75, image=self.customer_images[img_idx])
            
            # Show satisfaction level
            sat = self.calculate_customer_satisfaction(customer)
            emoji = self.get_satisfaction_emoji(sat)
            self.customer_canvas.create_text(x_pos, 130, text=emoji, font=('Arial', 12))
        
        # Update current satisfaction
        avg_sat = sum(self.calculate_customer_satisfaction(c) for c in self.customers_waiting)
        avg_sat = avg_sat / len(self.customers_waiting) if self.customers_waiting else 75
        self.current_sat_label.config(text=self.get_satisfaction_emoji(avg_sat))
    
    def calculate_customer_satisfaction(self, customer):
        """Calculate satisfaction for a customer (0-100)"""
        base_sat = self.satisfaction
        # Add random variation
        sat = max(0, min(100, base_sat + random.randint(-20, 20)))
        return sat
    
    def get_satisfaction_emoji(self, satisfaction):
        """Get emoji based on satisfaction level"""
        if satisfaction >= 80:
            return "😍"
        elif satisfaction >= 60:
            return "😊"
        elif satisfaction >= 40:
            return "😐"
        elif satisfaction >= 20:
            return "😕"
        else:
            return "😠"
    
    def create_hotel_tab(self):
        hotel_frame = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(hotel_frame, text='🏨 Hotel')
        
        # Reception section
        reception_frame = tk.Frame(hotel_frame, bg='#bdc3c7', relief='raised', bd=2)
        reception_frame.pack(fill='x', padx=10, pady=10)
        
        reception_label = tk.Label(reception_frame, text="🏢 RECEPTION", bg='#bdc3c7', fg='#2c3e50', 
                                  font=('Arial', 14, 'bold'))
        reception_label.pack(pady=10)
        
        # Room status
        rooms_frame = tk.Frame(reception_frame, bg='#bdc3c7')
        rooms_frame.pack(fill='x', padx=10, pady=10)
        
        self.room_labels = {}
        for room_type, details in self.rooms.items():
            room_frame = tk.Frame(rooms_frame, bg='#ecf0f1', relief='raised', bd=1)
            room_frame.pack(fill='x', pady=2)
            
            # Add cleanliness indicator
            clean_emoji = "✨" if details['dirty'] == 0 else "💩"
            
            label_text = f"{room_type.title()} Rooms: {details['occupied']}/{details['total']} {clean_emoji} - ${details['price']}/night"
            self.room_labels[room_type] = tk.Label(room_frame, text=label_text, 
                                                  bg='#ecf0f1', fg='#2c3e50', font=('Arial', 10))
            self.room_labels[room_type].pack(side='left', padx=5)
            
            tk.Button(room_frame, text="Book", 
                     command=lambda rt=room_type: self.book_room(rt),
                     bg='#3498db', fg='white', font=('Arial', 8)).pack(side='right', padx=5)
        
        # Current bookings
        bookings_label = tk.Label(hotel_frame, text="📅 CURRENT BOOKINGS", bg='#ecf0f1', fg='#2c3e50', 
                                 font=('Arial', 14, 'bold'))
        bookings_label.pack(pady=10)
        
        self.bookings_listbox = tk.Listbox(hotel_frame, bg='#bdc3c7', fg='#2c3e50', 
                                          font=('Arial', 10), height=8)
        self.bookings_listbox.pack(fill='x', padx=10)
        
        # Hotel management buttons
        management_frame = tk.Frame(hotel_frame, bg='#ecf0f1')
        management_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(management_frame, text="🔑 Check-in Customer", command=self.checkin_customer,
                 bg='#27ae60', fg='white', font=('Arial', 12, 'bold')).pack(side='left', padx=5, expand=True)
        
        tk.Button(management_frame, text="🚪 Check-out Customer", command=self.checkout_customer,
                 bg='#e74c3c', fg='white', font=('Arial', 12, 'bold')).pack(side='left', padx=5, expand=True)
        
        tk.Button(management_frame, text="🧹 Clean Rooms", command=self.clean_rooms,
                 bg='#f39c12', fg='white', font=('Arial', 12, 'bold')).pack(side='left', padx=5, expand=True)
    
    def create_staff_tab(self):
        staff_frame = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(staff_frame, text='👨‍🍳 Staff Management')
        
        staff_label = tk.Label(staff_frame, text="👥 STAFF MANAGEMENT", bg='#ecf0f1', fg='#2c3e50', 
                              font=('Arial', 16, 'bold'))
        staff_label.pack(pady=20)
        
        self.staff_labels = {}
        for staff_type, count in self.staff.items():
            staff_row = tk.Frame(staff_frame, bg='#bdc3c7', relief='raised', bd=2)
            staff_row.pack(fill='x', padx=20, pady=5)
            
            # Staff icon
            icon = "👨‍🍳" if staff_type == "chefs" else "💁" if staff_type == "waiters" else "🧹" if staff_type == "cleaners" else "💼"
            
            label_text = f"{icon} {staff_type.title()}: {count}"
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
        
        tk.Label(efficiency_frame, text="📊 STAFF EFFICIENCY", bg='#95a5a6', fg='#2c3e50', 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        self.efficiency_text = tk.Text(efficiency_frame, height=6, bg='#ecf0f1', fg='#2c3e50', 
                                      font=('Arial', 10))
        self.efficiency_text.pack(fill='x', padx=10, pady=10)
        
        self.update_efficiency_display()
    
    def create_upgrades_tab(self):
        upgrades_frame = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(upgrades_frame, text='🛠️ Upgrades')
        
        upgrades_label = tk.Label(upgrades_frame, text="✨ BUSINESS UPGRADES ✨", bg='#ecf0f1', fg='#2c3e50', 
                                 font=('Arial', 16, 'bold'))
        upgrades_label.pack(pady=20)
        
        # Room upgrades
        room_upgrades = tk.Frame(upgrades_frame, bg='#bdc3c7', relief='raised', bd=2)
        room_upgrades.pack(fill='x', padx=20, pady=10)
        
        tk.Label(room_upgrades, text="🏨 ROOM UPGRADES", bg='#bdc3c7', fg='#2c3e50', 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        upgrades_list = [
            ("🛏️ Add Single Room", 5000, lambda: self.add_room('single')),
            ("🛏️🛏️ Add Double Room", 8000, lambda: self.add_room('double')),
            ("🏰 Add Suite", 15000, lambda: self.add_room('suite')),
            ("👨‍🍳 Kitchen Equipment", 3000, lambda: self.upgrade_kitchen()),
            ("🪑 Better Furniture", 4000, lambda: self.upgrade_furniture()),
            ("📢 Marketing Campaign", 2000, lambda: self.marketing_campaign()),
            ("🎨 Interior Design", 6000, lambda: self.upgrade_interior()),
            ("🌿 Garden Landscaping", 4500, lambda: self.upgrade_garden())
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
        self.notebook.add(kitchen_frame, text='👨‍🍳 Kitchen')
        
        kitchen_label = tk.Label(kitchen_frame, text="🍳 KITCHEN OPERATIONS 🍲", bg='#ecf0f1', fg='#2c3e50', 
                                font=('Arial', 16, 'bold'))
        kitchen_label.pack(pady=20)
        
        # Cooking queue
        cooking_frame = tk.Frame(kitchen_frame, bg='#bdc3c7', relief='raised', bd=2)
        cooking_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(cooking_frame, text="⏳ COOKING QUEUE", bg='#bdc3c7', fg='#2c3e50', 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        self.cooking_listbox = tk.Listbox(cooking_frame, bg='#ecf0f1', fg='#2c3e50', 
                                         font=('Arial', 10), height=8)
        self.cooking_listbox.pack(fill='x', padx=10, pady=10)
        
        # Kitchen stats
        stats_frame = tk.Frame(kitchen_frame, bg='#95a5a6', relief='raised', bd=2)
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(stats_frame, text="📊 KITCHEN STATISTICS", bg='#95a5a6', fg='#2c3e50', 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        self.kitchen_stats = tk.Text(stats_frame, height=6, bg='#ecf0f1', fg='#2c3e50', 
                                    font=('Arial', 10))
        self.kitchen_stats.pack(fill='x', padx=10, pady=10)
        
        self.update_kitchen_stats()
    
    def create_stats_tab(self):
        stats_frame = tk.Frame(self.notebook, bg='#ecf0f1')
        self.notebook.add(stats_frame, text='📊 Statistics')
        
        stats_label = tk.Label(stats_frame, text="📈 BUSINESS STATISTICS", bg='#ecf0f1', fg='#2c3e50', 
                              font=('Arial', 16, 'bold'))
        stats_label.pack(pady=20)
        
        # Stats display
        self.stats_text = tk.Text(stats_frame, height=15, bg='#bdc3c7', fg='#2c3e50', 
                                 font=('Arial', 10), wrap='word')
        self.stats_text.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.update_stats_display()
    
    def update_stats_display(self):
        """Update the statistics tab with current game stats"""
        self.stats_text.delete(1.0, tk.END)
        
        # Calculate occupancy rate
        total_rooms = sum(room['total'] for room in self.rooms.values())
        occupied_rooms = sum(room['occupied'] for room in self.rooms.values())
        occupancy_rate = (occupied_rooms / total_rooms) * 100 if total_rooms > 0 else 0
        
        # Calculate most popular menu item
        popular_item = max(self.menu.items(), key=lambda x: x[1]['popularity'], default=("None", 0))
        
        stats_text = f"""
        📅 Day {self.day} | 🕒 {self.time_of_day}:00 {'(Night)' if self.is_night else '(Day)'}
        
        💰 Financial Status:
        - Current Funds: ${self.money}
        - Room Revenue: ${sum(room['price'] * room['occupied'] for room in self.rooms.values())}/day
        - Restaurant Revenue: ${sum(order['price'] for order in self.orders)} (pending)
        
        🏨 Hotel Operations:
        - Occupancy Rate: {occupancy_rate:.1f}%
        - Cleanliness: {self.cleanliness}%
        - Dirty Rooms: {sum(room['dirty'] for room in self.rooms.values())}
        
        🍽️ Restaurant Operations:
        - Orders in Progress: {len(self.orders)}
        - Most Popular Item: {popular_item[0]} ({popular_item[1]['popularity']} popularity)
        - Customer Satisfaction: {self.satisfaction}% {self.get_satisfaction_emoji(self.satisfaction)}
        
        👥 Staff:
        - Total Employees: {sum(self.staff.values())}
        - Chefs: {self.staff['chefs']}
        - Waiters: {self.staff['waiters']}
        - Cleaners: {self.staff['cleaners']}
        - Receptionists: {self.staff['receptionists']}
        """
        
        self.stats_text.insert(1.0, stats_text)
    
    def add_to_order(self, item):
        self.sounds['order'].play()
        
        customer_name = f"Customer {random.randint(1, 999)}"
        order_time = time.time()
        order = {
            'customer': customer_name,
            'item': item,
            'time': order_time,
            'status': 'pending',
            'satisfaction': 100  # Starts at 100, decreases over time
        }
        self.orders.append(order)
        self.menu[item]['popularity'] += 1
        self.update_orders_display()
        
        # Add to cooking queue
        cooking_time = self.menu[item]['time']
        self.cooking_listbox.insert(tk.END, f"{item} for {customer_name} - {cooking_time}s")
        
        # Add customer to waiting list
        self.customers_waiting.append(customer_name)
        self.update_customer_display()
        
        # Start cooking in background
        threading.Thread(target=self.cook_order, args=(order,), daemon=True).start()
    
    def cook_order(self, order):
        cook_time = self.menu[order['item']]['time']
        # Reduce time based on chef count
        actual_time = max(1, cook_time - (self.staff['chefs'] * 2))
        
        # Play cooking sound
        self.sounds['cooking'].play()
        
        # Update satisfaction while cooking
        start_time = time.time()
        while time.time() - start_time < actual_time:
            elapsed = time.time() - start_time
            order['satisfaction'] = max(0, 100 - (elapsed / actual_time) * 30)
            time.sleep(0.5)
        
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
        
        # Remove customer from waiting list
        if order['customer'] in self.customers_waiting:
            self.customers_waiting.remove(order['customer'])
        
        # Calculate payment and tip based on satisfaction
        price = self.menu[order['item']]['price']
        tip_multiplier = order['satisfaction'] / 100
        tip = random.randint(0, int(price * tip_multiplier))
        total = price + tip
        
        self.money += total
        self.experience += 10
        self.reputation = min(100, self.reputation + 2)
        self.satisfaction = min(100, self.satisfaction + 5)
        
        self.update_displays()
        self.update_orders_display()
        self.update_customer_display()
        
        self.sounds['money'].play()
        
        messagebox.showinfo("Order Served", 
                          f"Served {order['item']} to {order['customer']}\n"
                          f"Customer Satisfaction: {int(order['satisfaction'])}%\n"
                          f"Payment: ${price}\nTip: ${tip}\nTotal: ${total}")
    
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
            'price': self.rooms[room_type]['price'],
            'dirty': False
        }
        
        self.bookings.append(booking)
        self.rooms[room_type]['occupied'] += 1
        
        self.update_bookings_display()
        self.update_room_labels()
        
        messagebox.showinfo("Booking Confirmed", 
                          f"Booked {room_type} room for {customer_name}\n"
                          f"Check-in: {check_in.strftime('%m/%d')}\n"
                          f"Check-out: {check_out.strftime('%m/%d')}")
    
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
        self.sounds['money'].play()
        
        messagebox.showinfo("Check-in", 
                          f"Checked in {booking['customer']}\n"
                          f"Room: {booking['room_type']}\n"
                          f"Payment: ${payment}")
    
    def checkout_customer(self):
        if not self.bookings:
            messagebox.showinfo("No Bookings", "No bookings to check out!")
            return
        
        booking = self.bookings.pop(0)
        self.rooms[booking['room_type']]['occupied'] -= 1
        self.rooms[booking['room_type']]['dirty'] += 1
        
        # Additional payment for extra days
        days_stayed = (datetime.now() - booking['check_in']).days
        extra_payment = booking['price'] * max(0, days_stayed - 1)
        
        if extra_payment > 0:
            self.money += extra_payment
            self.sounds['money'].play()
            messagebox.showinfo("Check-out", 
                              f"Checked out {booking['customer']}\n"
                              f"Extra days stayed: {days_stayed - 1}\n"
                              f"Extra payment: ${extra_payment}")
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
        self.draw_staff_animations()
    
    def buy_upgrade(self, cost, upgrade_func):
        if self.money < cost:
            messagebox.showwarning("Insufficient Funds", f"Need ${cost} for this upgrade!")
            return
        
        self.money -= cost
        upgrade_func()
        self.update_displays()
        self.sounds['money'].play()
    
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
        self.satisfaction = min(100, self.satisfaction + 15)
        messagebox.showinfo("Furniture Upgraded", "Better furniture installed! Reputation and satisfaction increased!")
    
    def upgrade_interior(self):
        self.reputation += 15
        self.satisfaction = min(100, self.satisfaction + 10)
        messagebox.showinfo("Interior Upgraded", "New interior design! Customers love the new look!")
    
    def upgrade_garden(self):
        self.reputation += 5
        self.satisfaction = min(100, self.satisfaction + 5)
        messagebox.showinfo("Garden Upgraded", "Beautiful garden landscaping! Improves customer experience!")
    
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
        self.satisfaction = min(100, self.satisfaction + 5)
        self.update_displays()
        self.sounds['clean'].play()
        messagebox.showinfo("Cleaning", "Tables cleaned! Cleanliness and satisfaction improved!")
    
    def clean_rooms(self):
        if self.staff['cleaners'] == 0:
            messagebox.showwarning("No Cleaners", "Hire cleaners to clean rooms!")
            return
        
        for room_type in self.rooms:
            if self.rooms[room_type]['dirty'] > 0:
                self.rooms[room_type]['dirty'] = 0
                break
        
        self.cleanliness = min(100, self.cleanliness + 15)
        self.reputation += 2
        self.update_displays()
        self.update_room_labels()
        self.sounds['clean'].play()
        messagebox.showinfo("Cleaning", "Rooms cleaned! Cleanliness improved!")
    
    def update_displays(self):
        self.money_label.config(text=f"💰 ${self.money}")
        self.level_label.config(text=f"🏆 Level {self.level}")
        self.exp_label.config(text=f"📊 EXP: {self.experience}/{self.exp_needed}")
        self.rep_bar['value'] = self.reputation
        self.clean_bar['value'] = self.cleanliness
        self.sat_bar['value'] = self.satisfaction
        
        # Check for level up
        if self.experience >= self.exp_needed:
            self.level_up()
    
    def level_up(self):
        self.level += 1
        self.experience = 0
        self.exp_needed = int(self.exp_needed * 1.5)
        self.sounds['level_up'].play()
        messagebox.showinfo("Level Up!", 
                          f"Congratulations! You reached level {self.level}!\n"
                          f"New upgrades and features unlocked!")
    
    def update_orders_display(self):
        self.orders_listbox.delete(0, tk.END)
        for order in self.orders:
            status = "✓ Ready" if order['status'] == 'ready' else "⏳ Cooking"
            sat = int(order.get('satisfaction', 100))
            self.orders_listbox.insert(tk.END, 
                                     f"{order['item']} for {order['customer']} - {status} ({sat}%)")
    
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
            clean_emoji = "✨" if details['dirty'] == 0 else "💩"
            label_text = f"{room_type.title()} Rooms: {details['occupied']}/{details['total']} {clean_emoji} - ${details['price']}/night"
            label.config(text=label_text)
    
    def update_staff_labels(self):
        for staff_type, label in self.staff_labels.items():
            icon = "👨‍🍳" if staff_type == "chefs" else "💁" if staff_type == "waiters" else "🧹" if staff_type == "cleaners" else "💼"
            label.config(text=f"{icon} {staff_type.title()}: {self.staff[staff_type]}")
    
    def update_efficiency_display(self):
        self.efficiency_text.delete(1.0, tk.END)
        efficiency_text = "📊 STAFF EFFICIENCY REPORT:\n\n"
        
        # Calculate efficiency based on staff count
        chef_efficiency = min(100, self.staff['chefs'] * 25)
        waiter_efficiency = min(100, self.staff['waiters'] * 20)
        cleaner_efficiency = min(100, self.staff['cleaners'] * 30)
        reception_efficiency = min(100, self.staff['receptionists'] * 40)
        
        efficiency_text += f"👨‍🍳 Kitchen Efficiency: {chef_efficiency}% {'⭐' * (chef_efficiency // 20)}\n"
        efficiency_text += f"💁 Service Efficiency: {waiter_efficiency}% {'⭐' * (waiter_efficiency // 20)}\n"
        efficiency_text += f"🧹 Cleanliness Efficiency: {cleaner_efficiency}% {'⭐' * (cleaner_efficiency // 20)}\n"
        efficiency_text += f"💼 Reception Efficiency: {reception_efficiency}% {'⭐' * (reception_efficiency // 20)}\n\n"
        efficiency_text += "Higher efficiency = Faster service & happier customers!"
        
        self.efficiency_text.insert(1.0, efficiency_text)
    
    def update_kitchen_stats(self):
        self.kitchen_stats.delete(1.0, tk.END)
        stats_text = "🍳 KITCHEN STATISTICS:\n\n"
        
        total_orders = len(self.orders)
        ready_orders = len([o for o in self.orders if o['status'] == 'ready'])
        cooking_orders = total_orders - ready_orders
        
        stats_text += f"📋 Total Orders: {total_orders}\n"
        stats_text += f"⏳ Orders Cooking: {cooking_orders}\n"
        stats_text += f"✅ Orders Ready: {ready_orders}\n"
        stats_text += f"👨‍🍳 Kitchen Staff: {self.staff['chefs']} chefs\n\n"
        stats_text += "🍽️ MENU ITEMS:\n"
        
        for item, details in self.menu.items():
            stars = '★' * (details['popularity'] // 20)
            if not stars:
                stars = '☆'
            stats_text += f"- {item}: ${details['price']} (Cook time: {details['time']}s) {stars}\n"
        
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
                    
                    # Simulate satisfaction decay
                    self.satisfaction = max(0, self.satisfaction - 2)
                    
                    # Random chance of new customer if rep is high
                    if self.reputation >= 60 and random.random() < 0.3 and not self.is_night:
                        new_customer = f"Customer {random.randint(1000, 9999)}"
                        self.customers_waiting.append(new_customer)
                        self.update_customer_display()
                    
                    # Update all displays
                    self.root.after(0, self.update_displays)
                    self.root.after(0, self.update_kitchen_stats)
                    self.root.after(0, self.update_stats_display)
                    self.root.after(0, self.draw_staff_animations)
                
                time.sleep(1)
        
        threading.Thread(target=game_loop, daemon=True).start()
    
    def start_day_night_cycle(self):
        def update_cycle():
            # Update time (1 hour every 6 seconds)
            self.time_of_day += 1
            if self.time_of_day >= 24:
                self.time_of_day = 0
                self.day += 1
                self.new_day_events()
            
            # Update day/night state
            self.is_night = self.time_of_day < 6 or self.time_of_day >= 20
            
            # Update display
            self.day_label.config(text=f"Day {self.day} | {self.time_of_day}:00 {'🌙' if self.is_night else '☀️'}")
            self.draw_staff_animations()
            
            # Schedule next update
            self.root.after(6000, update_cycle)
        
        update_cycle()
    
    def new_day_events(self):
        """Handle events that occur at the start of a new day"""
        # Collect room payments
        room_income = sum(room['price'] * room['occupied'] for room in self.rooms.values())
        self.money += room_income
        
        # Pay staff salaries
        staff_costs = sum(self.staff.values()) * 100
        self.money -= staff_costs
        
        # Update displays
        self.update_displays()
        self.update_stats_display()
        
        # Show daily report
        messagebox.showinfo("Daily Report",
                          f"Day {self.day - 1} Report:\n\n"
                          f"💰 Room Income: +${room_income}\n"
                          f"💸 Staff Costs: -${staff_costs}\n"
                          f"🏆 Reputation: {self.reputation}%\n"
                          f"😊 Satisfaction: {self.satisfaction}%")

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelRestaurantManager(root)
    root.mainloop()