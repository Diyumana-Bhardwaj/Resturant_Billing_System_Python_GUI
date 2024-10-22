import datetime
import pickle
import random
import tkinter as tk
from tkinter import messagebox, ttk

# Function to calculate the total amounts
def calculate_totals(items):
    sub_totals = [item[1] * item[2] for item in items]  # Quantity * Price
    subtotal = sum(sub_totals)
    discount = 0.1 * subtotal
    net_total = subtotal - discount
    gst = 0.09 * net_total
    grand_total = net_total + gst + gst
    return subtotal, discount, net_total, gst, grand_total

# Function to display the invoice
def display_invoice(date, name, cust_id, items, subtotal, discount, net_total, gst, grand_total):
    invoice_text.delete(1.0, tk.END)  # Clear the text box
    invoice_text.insert(tk.END, f"\n\n\t    ADV. Restaurant\n")
    invoice_text.insert(tk.END, "\t   -----------------\n")
    invoice_text.insert(tk.END, f"\nDate: {date}")
    invoice_text.insert(tk.END, f"\nInvoice To: {name}")
    invoice_text.insert(tk.END, f"\nInvoice number: {cust_id}")
    invoice_text.insert(tk.END, "\n---------------------------------------")
    invoice_text.insert(tk.END, "\nItems\t\tQty\t\tTotal")
    invoice_text.insert(tk.END, "\n---------------------------------------\n")
    
    for i in items:
        invoice_text.insert(tk.END, f"{i[0]}\t\t{i[1]}\t\t{i[1] * i[2]:.2f}\n")

    invoice_text.insert(tk.END, "\n---------------------------------------")
    invoice_text.insert(tk.END, f"\nSub Total\t\t\t\t{subtotal:.2f}")
    invoice_text.insert(tk.END, f"\nDiscount @10%\t\t\t\t{discount:.2f}")
    invoice_text.insert(tk.END, "\n\t\t\t\t-------")
    invoice_text.insert(tk.END, f"\nNet Total\t\t\t\t{net_total:.2f}")
    invoice_text.insert(tk.END, f"\nCGST @9%\t\t\t\t{gst:.2f}")
    invoice_text.insert(tk.END, f"\nsGST @9%\t\t\t\t{gst:.2f}")
    invoice_text.insert(tk.END, "\n---------------------------------------")
    invoice_text.insert(tk.END, f"\nGrand Total\t\t\t\t{grand_total:.2f}")
    invoice_text.insert(tk.END, "\n---------------------------------------\n")

# Function to save the invoice data
def save_invoice(date, name, items, cust_id, subtotals):
    summary = [date, name, items, subtotals, cust_id]
    try:
        # Open file in append-binary mode, create if it doesn't exist
        with open('resbilldata', 'ab') as f:
            pickle.dump(summary, f)
        messagebox.showinfo("Success", "Invoice saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save invoice: {str(e)}")

# Function to generate the invoice
def generate_invoice():
    name = name_entry.get()
    if not name:
        messagebox.showwarning("Input Error", "Please enter the customer's name.")
        return

    n_items = int(items_count_entry.get())
    items = []

    for i in range(n_items):
        item = item_entries[i][0].get()
        quantity = int(item_entries[i][1].get())
        price = int(item_entries[i][2].get())
        items.append([item, quantity, price])

    # Calculate totals
    subtotal, discount, net_total, gst, grand_total = calculate_totals(items)

    # Get current date and generate random invoice number
    date = datetime.datetime.now()
    cust_id = random.randint(1111111, 9999999)

    # Display the invoice
    display_invoice(date, name, cust_id, items, subtotal, discount, net_total, gst, grand_total)

    # Ask if user wants to save the invoice
    save_choice = messagebox.askyesno("Save Invoice", "Do you want to save this invoice?")
    if save_choice:
        save_invoice(date, name, items, cust_id, [item[1] * item[2] for item in items])

# Function to dynamically add item entry fields
def add_items_fields():
    try:
        n_items = int(items_count_entry.get())
        for widget in items_frame.winfo_children():
            widget.destroy()  # Clear existing widgets

        global item_entries
        item_entries = []
        
        # Shifted headings by 1 column
        tk.Label(items_frame, text="Item", font=('Arial', 10, 'bold')).grid(row=0, column=1, padx=10, pady=5)
        tk.Label(items_frame, text="Quantity", font=('Arial', 10, 'bold')).grid(row=0, column=2, padx=10, pady=5)
        tk.Label(items_frame, text="Price/Unit", font=('Arial', 10, 'bold')).grid(row=0, column=3, padx=10, pady=5)

        # Add input fields for each item
        for i in range(n_items):
            item_label = tk.Label(items_frame, text=f"Item {i+1}:")
            item_label.grid(row=i+1, column=0)

            item_name_entry = tk.Entry(items_frame)
            item_name_entry.grid(row=i+1, column=1)

            item_quantity_entry = tk.Entry(items_frame)
            item_quantity_entry.grid(row=i+1, column=2)

            item_price_entry = tk.Entry(items_frame)
            item_price_entry.grid(row=i+1, column=3)

            item_entries.append((item_name_entry, item_quantity_entry, item_price_entry))

    except ValueError:
        messagebox.showwarning("Input Error", "Please enter a valid number of items.")

# Function to show all invoices
# Function to show all invoices
def show_all_invoices():
    try:
        # Try opening the file for reading
        with open('resbilldata', 'rb') as f:
            invoice_text.delete(1.0, tk.END)  # Clear the text box
            while True:
                try:
                    invoice = pickle.load(f)
                    subtotal, discount, net_total, gst, grand_total = calculate_totals(invoice[2])
                    display_invoice(invoice[0], invoice[1], invoice[-1], invoice[2], subtotal, discount, net_total, gst, grand_total)
                    invoice_text.insert(tk.END, "\n\n---\n\n")  # Add a separator between invoices
                except EOFError:
                    # End of file reached
                    break
    except FileNotFoundError:
        # Handle if file doesn't exist
        messagebox.showinfo("Info", "No invoices found. The file does not exist.")
    except Exception as e:
        # Catch any other exception
        messagebox.showerror("Error", f"Failed to load invoices: {str(e)}")

# Function to search invoices by invoice number
def search_invoice_by_id():
    user_input = search_entry.get()
    if not user_input.isdigit():
        messagebox.showwarning("Input Error", "Please enter a valid invoice number.")
        return

    try:
        with open('resbilldata', 'rb') as f:
            while True:
                invoice = pickle.load(f)
                if invoice[-1] == int(user_input):
                    subtotal, discount, net_total, gst, grand_total = calculate_totals(invoice[2])
                    display_invoice(invoice[0], invoice[1], invoice[-1], invoice[2], subtotal, discount, net_total, gst, grand_total)
                    return
    except (EOFError, FileNotFoundError):
        messagebox.showinfo("Info", "Invoice not found.")

# Function to search invoices by date
def search_invoice_by_date():
    user_input = date_entry.get()
    if not user_input:
        messagebox.showwarning("Input Error", "Please enter a valid date (YYYY-MM-DD).")
        return

    try:
        search_date = datetime.datetime.strptime(user_input, "%Y-%m-%d").date()
        with open('resbilldata', 'rb') as f:
            found = False
            while True:
                invoice = pickle.load(f)
                if invoice[0].date() == search_date:
                    found = True
                    subtotal, discount, net_total, gst, grand_total = calculate_totals(invoice[2])
                    display_invoice(invoice[0], invoice[1], invoice[-1], invoice[2], subtotal, discount, net_total, gst, grand_total)
                    break
            
            if not found:
                messagebox.showinfo("Info", "No invoices found for this date.")
    except (EOFError, FileNotFoundError):
        messagebox.showinfo("Info", "No invoices found.")
    except ValueError:
        messagebox.showwarning("Input Error", "Please enter a valid date (YYYY-MM-DD).")

# Create the main application window
root = tk.Tk()
root.title("Restaurant Invoice System")
root.geometry("600x600")
root.configure(bg='#C9DABF')  # Set main window background color

# Customer Name
tk.Label(root, text="Customer Name:", bg='#9CA986').pack(pady=5)
name_entry = tk.Entry(root)
name_entry.pack(pady=5)

# Number of Items
tk.Label(root, text="Number of Items:", bg='#9CA986').pack(pady=5)
items_count_entry = tk.Entry(root)
items_count_entry.pack(pady=5)

# Button to add item entry fields
tk.Button(root, text="Add Items", command=add_items_fields, bg='#9CA986').pack(pady=10)

# Frame to hold item entry fields
items_frame = tk.Frame(root)
items_frame.pack(pady=10)

# Text box to display the invoice
invoice_text = tk.Text(root, height=15, width=70)
invoice_text.pack(pady=10)
invoice_text.configure(bg='#9CA986')
# Button to generate the invoice
tk.Button(root, text="Generate Invoice", command=generate_invoice,bg='#9CA986').pack(pady=20)

# Frame for search functionality
search_frame = tk.Frame(root)
search_frame.pack(pady=10)
search_frame.configure(bg='#9CA986')

tk.Label(search_frame, text="Search Invoice by ID:",bg='#9CA986').grid(row=0, column=0)
search_entry = tk.Entry(search_frame)
search_entry.grid(row=0, column=1)
tk.Button(search_frame, text="Search", command=search_invoice_by_id,bg='#9CA986').grid(row=0, column=2)

tk.Label(search_frame, text="Search Invoice by Date (YYYY-MM-DD):",bg='#9CA986').grid(row=1, column=0)
date_entry = tk.Entry(search_frame)
date_entry.grid(row=1, column=1)
tk.Button(search_frame, text="Search", command=search_invoice_by_date,bg='#9CA986').grid(row=1, column=2)

# Button to show all invoices
tk.Button(root, text="Show All Invoices", command=show_all_invoices).pack(pady=10)

# Start the main event loop
root.mainloop()
