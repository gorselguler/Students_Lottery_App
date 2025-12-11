import tkinter as tk
from tkinter import messagebox
import random
import json

class LotteryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lottery Draw System")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        self.students = []
        self.load_data()
        
        # Header
        header = tk.Frame(self.root, bg='#34495e', height=70)
        header.pack(fill=tk.X)
        
        title = tk.Label(header, text="🎲 LOTTERY DRAW SYSTEM", 
                        font=('Arial', 20, 'bold'), 
                        bg='#34495e', fg='#ecf0f1')
        title.pack(pady=20)
        
        # Content
        content = tk.Frame(self.root, bg='#2c3e50')
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        left_panel = tk.Frame(content, bg='#34495e', width=350)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        form_title = tk.Label(left_panel, text="Add New Participant",
                             font=('Arial', 14, 'bold'),
                             bg='#34495e', fg='#ecf0f1')
        form_title.pack(pady=15)
        
        # name pls
        self.create_input(left_panel, "Name Surname:", "name_entry")
        
        # Adress
        self.create_input(left_panel, "Adress:", "address_entry")
        
        # Phone entry
        self.create_input(left_panel, "Phone:", "phone_entry")
        
        # Buttons
        btn_frame = tk.Frame(left_panel, bg='#34495e')
        btn_frame.pack(pady=20)
        
        add_btn = tk.Button(btn_frame, text="Add", 
                           command=self.add_student,
                           bg='#27ae60', fg='white',
                           font=('Arial', 12, 'bold'),
                           width=12, height=2,
                           cursor='hand2')
        add_btn.pack(pady=5)
        
        delete_btn = tk.Button(btn_frame, text="Delete Selected",
                              command=self.delete_student,
                              bg='#e74c3c', fg='white',
                              font=('Arial', 11),
                              width=12,
                              cursor='hand2')
        delete_btn.pack(pady=5)
        
        clear_btn = tk.Button(btn_frame, text="Clear All",
                             command=self.clear_all,
                             bg='#95a5a6', fg='white',
                             font=('Arial', 11),
                             width=12,
                             cursor='hand2')
        clear_btn.pack(pady=5)
        
        self.count_label = tk.Label(left_panel, 
                                    text="Total: 0 participants",
                                    font=('Arial', 11, 'bold'),
                                    bg='#34495e', fg='#3498db')
        self.count_label.pack(pady=10)
        
        right_panel = tk.Frame(content, bg='#34495e')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        list_title = tk.Label(right_panel, text="Participants List",
                             font=('Arial', 14, 'bold'),
                             bg='#34495e', fg='#ecf0f1')
        list_title.pack(pady=15)
        
        list_frame = tk.Frame(right_panel, bg='#34495e')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(list_frame,
                                  font=('Courier', 10),
                                  bg='#2c3e50', fg='#ecf0f1',
                                  selectbackground='#3498db',
                                  yscrollcommand=scrollbar.set)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        lottery_btn = tk.Button(right_panel, text="🎲 DRAW LOTTERY",
                               command=self.draw_lottery,
                               bg='#3498db', fg='white',
                               font=('Arial', 16, 'bold'),
                               height=2,
                               cursor='hand2')
        lottery_btn.pack(fill=tk.X, padx=10, pady=15)
        
        winner_frame = tk.Frame(right_panel, bg='#2c3e50')
        winner_frame.pack(fill=tk.X, padx=10, pady=(0, 15))
        
        winner_title = tk.Label(winner_frame, text="🏆 WINNER 🏆",
                               font=('Arial', 13, 'bold'),
                               bg='#2c3e50', fg='#f39c12')
        winner_title.pack(pady=10)
        
        self.winner_label = tk.Label(winner_frame, 
                                     text="No lottery drawn yet",
                                     font=('Arial', 11),
                                     bg='#2c3e50', fg='#ecf0f1',
                                     wraplength=350,
                                     justify=tk.LEFT)
        self.winner_label.pack(pady=10)
        
        self.update_list()
    
    def create_input(self, parent, label_text, entry_name):
        frame = tk.Frame(parent, bg='#34495e')
        frame.pack(fill=tk.X, padx=15, pady=8)
        
        label = tk.Label(frame, text=label_text,
                        font=('Arial', 10, 'bold'),
                        bg='#34495e', fg='#ecf0f1',
                        width=12, anchor='w')
        label.pack(side=tk.LEFT)
        
        entry = tk.Entry(frame, font=('Arial', 10),
                        bg='#2c3e50', fg='#ecf0f1',
                        insertbackground='white')
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        setattr(self, entry_name, entry)
    
    def add_student(self):
        name = self.name_entry.get().strip()
        address = self.address_entry.get().strip()
        phone = self.phone_entry.get().strip()
        
        if not name or not address or not phone:
            messagebox.showwarning("Warning", "Please fill all fields!")
            return
        
        student = {
            "name": name,
            "address": address,
            "phone": phone
        }
        
        self.students.append(student)
        self.save_data()
        self.update_list()
        
        self.name_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        
        messagebox.showinfo("Success", f"{name} added successfully!")
    
    def update_list(self):
        self.listbox.delete(0, tk.END)
        
        for i, student in enumerate(self.students, 1):
            text = f"{i}. {student['name']} - {student['phone']}"
            self.listbox.insert(tk.END, text)
        
        self.count_label.config(text=f"Total: {len(self.students)} participants")
    
    def delete_student(self):
        selection = self.listbox.curselection()
        
        if not selection:
            messagebox.showwarning("Warning", "Please select a participant to delete!")
            return
        
        index = selection[0]
        name = self.students[index]['name']
        
        if messagebox.askyesno("Confirm", f"Delete {name}?"):
            self.students.pop(index)
            self.save_data()
            self.update_list()
    
    def clear_all(self):
        if not self.students:
            messagebox.showinfo("Info", "The list is already empty!")
            return
        
        if messagebox.askyesno("Confirm", "Delete all participants?"):
            self.students = []
            self.save_data()
            self.update_list()
            self.winner_label.config(text="No lottery drawn yet")
    
    def draw_lottery(self):
        if not self.students:
            messagebox.showwarning("Warning", "Add participants before drawing!")
            return
        
        self.winner_label.config(text="🎲 Drawing... 🎲")
        self.root.update()
        
        for i in range(10):
            temp = random.choice(self.students)
            self.winner_label.config(text=f"🎲 {temp['name']} 🎲")
            self.root.update()
            self.root.after(100)
        
        winner = random.choice(self.students)
        
        winner_text = f"🏆 {winner['name']} 🏆\n\n"
        winner_text += f"📍 {winner['address']}\n"
        winner_text += f"📞 {winner['phone']}"
        
        self.winner_label.config(text=winner_text)
        
        messagebox.showinfo("🎉 Winner!", 
                          f"Congratulations!\n\n{winner['name']}\n{winner['address']}\n{winner['phone']}")
    
    def save_data(self):
        with open('students.json', 'w', encoding='utf-8') as f:
            json.dump(self.students, f, ensure_ascii=False, indent=2)
    
    def load_data(self):
        try:
            with open('students.json', 'r', encoding='utf-8') as f:
                self.students = json.load(f)
        except FileNotFoundError:
            self.students = []


if __name__ == "__main__":
    root = tk.Tk()
    app = LotteryApp(root)
    root.mainloop()