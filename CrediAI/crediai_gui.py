import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# (Lista Python paa armazenar informações) ---
clients_db_list = []
client_id_counter = 1


# Lógica de Negócio

def create_client(full_name, document_id, income_str):
    global client_id_counter

    if not full_name or not document_id or not income_str:
        messagebox.showerror("Erro", "Todos os campos de cadastro são obrigatórios.")
        return None

    try:
        income = float(income_str)
    except ValueError:
        messagebox.showerror("Erro", "O valor da Renda deve ser um número (ex: 3500.50).")
        return None

    if any(c['document_id'] == document_id for c in clients_db_list):
        messagebox.showwarning("Aviso", f"Cliente com documento {document_id} já existe.")
        return None

    new_client_data = {
        "id": client_id_counter,
        "full_name": full_name,
        "document_id": document_id,
        "income": income
    }

    clients_db_list.append(new_client_data)

    success_msg = f"[SUCESSO] Cliente '{full_name}' (ID: {client_id_counter}) cadastrado."
    client_id_counter += 1

    return success_msg


def analyze_client_credit(client_id_str):
    try:
        client_id = int(client_id_str)
    except ValueError:
        messagebox.showerror("Erro", "O ID do cliente deve ser um número inteiro.")
        return None

    client_to_analyze = next((c for c in clients_db_list if c['id'] == client_id), None)

    if client_to_analyze is None:
        messagebox.showwarning("Aviso", f"Cliente com ID {client_id} não foi encontrado.")
        return None

    client_income = client_to_analyze.get('income', 0)
    score, risk, report = 0, "", ""

    if client_income >= 10000:
        score, risk, report = 950, "MUITO BAIXO", "Cliente com alta renda comprovada."
    elif client_income >= 5000:
        score, risk, report = 720, "BAIXO", "Cliente com boa renda."
    elif client_income >= 2000:
        score, risk, report = 510, "MÉDIO", "Renda moderada, analisar outras variáveis."
    else:
        score, risk, report = 300, "ALTO RISCO", "Renda abaixo do mínimo para análise."

    analysis_report = f"""
--- Análise de Crédito (ID: {client_to_analyze['id']}) ---
Cliente: {client_to_analyze['full_name']}
Score: {score}
Nível de Risco: {risk}
Resumo: {report}
-------------------------------------
"""
    return analysis_report


# Funções da Interface

def gui_handle_register():
    name = entry_name.get()
    doc = entry_document.get()
    income = entry_income.get()

    message = create_client(name, doc, income)

    if message:
        entry_name.delete(0, tk.END)
        entry_document.delete(0, tk.END)
        entry_income.delete(0, tk.END)
        log_to_console(message)


def gui_handle_analyze():
    client_id = entry_analyze_id.get()
    report = analyze_client_credit(client_id)

    if report:
        entry_analyze_id.delete(0, tk.END)
        log_to_console(report)


def log_to_console(message):
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, message + "\n")
    output_text.see(tk.END)
    output_text.config(state=tk.DISABLED)


# Interface Gráfica da aplicação

root = tk.Tk()
root.title("Protótipo CrediAI - Testes")
root.geometry("550x500")

main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

# Cadastro
frame_register = ttk.LabelFrame(main_frame, text="1. Cadastrar Novo Cliente")
frame_register.pack(fill=tk.X, padx=5, pady=5)


frame_register.columnconfigure(1, weight=1)  # Faz a coluna 1 (entradas) expandir

ttk.Label(frame_register, text="Nome Completo:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
entry_name = ttk.Entry(frame_register, width=40)
entry_name.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=3)

ttk.Label(frame_register, text="Documento (CPF):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
entry_document = ttk.Entry(frame_register, width=40)
entry_document.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=3)

ttk.Label(frame_register, text="Renda (R$):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=3)
entry_income = ttk.Entry(frame_register, width=40)
entry_income.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=3)

btn_register = ttk.Button(frame_register, text="Cadastrar Cliente", command=gui_handle_register)
btn_register.grid(row=3, column=1, sticky=tk.E, padx=5, pady=10)

# Análise do score
frame_analyze = ttk.LabelFrame(main_frame, text="2. Analisar Crédito")
frame_analyze.pack(fill=tk.X, padx=5, pady=5)


frame_analyze.columnconfigure(2, weight=1)

ttk.Label(frame_analyze, text="ID do Cliente:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
entry_analyze_id = ttk.Entry(frame_analyze, width=10)
entry_analyze_id.grid(row=0, column=1, sticky=tk.W, padx=5, pady=3)

btn_analyze = ttk.Button(frame_analyze, text="Analisar Crédito", command=gui_handle_analyze)
btn_analyze.grid(row=0, column=2, sticky=tk.E, padx=10, pady=10)

# LOGS com observações
frame_output = ttk.LabelFrame(main_frame, text="Console de Resultados")
frame_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

output_text = tk.Text(frame_output, height=10, state=tk.DISABLED, wrap=tk.WORD, background="#f0f0f0")
output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

if __name__ == "__main__":
    root.mainloop()