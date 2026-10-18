import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import date


class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer Pomodoro 50/10 + Estatísticas")
        self.root.geometry("380x480")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        # Configuração do JSON
        self.DATA_FILE = "historico_estudos.json"

        # Tempos em segundos (50 min estudo / 10 min descanso)
        self.WORK_TIME = 50 * 60
        self.REST_TIME = 10 * 60

        self.current_time = self.WORK_TIME
        self.is_work_phase = True
        self.is_running = False
        self.timer_id = None

        self.setup_ui()
        self.update_stats_label()

    def setup_ui(self):
        # Título da Fase
        self.label_status = tk.Label(
            self.root,
            text="Foco no Estudo! 📚",
            font=("Helvetica", 16, "bold"),
            fg="#a6e3a1",
            bg="#1e1e2e"
        )
        self.label_status.pack(pady=(25, 5))

        # Relógio
        self.label_timer = tk.Label(
            self.root,
            text="50:00",
            font=("Helvetica", 48, "bold"),
            fg="#cdd6f4",
            bg="#1e1e2e"
        )
        self.label_timer.pack(pady=15)

        # Botões
        frame_buttons = tk.Frame(self.root, bg="#1e1e2e")
        frame_buttons.pack(pady=15)

        self.btn_start = tk.Button(
            frame_buttons,
            text="Iniciar",
            font=("Helvetica", 11, "bold"),
            bg="#a6e3a1",
            fg="#11111b",
            width=8,
            command=self.start_timer
        )
        self.btn_start.grid(row=0, column=0, padx=5)

        self.btn_pause = tk.Button(
            frame_buttons,
            text="Pausar",
            font=("Helvetica", 11, "bold"),
            bg="#f9e2af",
            fg="#11111b",
            width=8,
            state=tk.DISABLED,
            command=self.pause_timer
        )
        self.btn_pause.grid(row=0, column=1, padx=5)

        self.btn_reset = tk.Button(
            frame_buttons,
            text="Resetar",
            font=("Helvetica", 11, "bold"),
            bg="#f38ba8",
            fg="#11111b",
            width=8,
            command=self.reset_timer
        )
        self.btn_reset.grid(row=0, column=2, padx=5)

        # Painel de Estatísticas / Medição
        frame_stats = tk.LabelFrame(
            self.root,
            text="📊 Progresso de Estudos",
            font=("Helvetica", 10, "bold"),
            fg="#89b4fa",
            bg="#181825",
            bd=1,
            padx=15,
            pady=10
        )
        frame_stats.pack(fill="x", padx=20, pady=(10, 0))

        self.label_stats_today = tk.Label(
            frame_stats,
            text="Hoje: 0 min (0 ciclos)",
            font=("Helvetica", 10),
            fg="#cdd6f4",
            bg="#181825",
            anchor="w"
        )
        self.label_stats_today.pack(fill="x", pady=2)

        self.label_stats_total = tk.Label(
            frame_stats,
            text="Total geral: 0 dias estudados",
            font=("Helvetica", 10),
            fg="#cdd6f4",
            bg="#181825",
            anchor="w"
        )
        self.label_stats_total.pack(fill="x", pady=2)

    # --- LÓGICA DO JSON / PERSISTÊNCIA ---
    def load_data(self):
        if not os.path.exists(self.DATA_FILE):
            return {}
        try:
            with open(self.DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def save_completed_session(self):
        data = self.load_data()
        today_str = str(date.today())
        minutos_estudo = self.WORK_TIME // 60

        if today_str not in data:
            data[today_str] = {
                "ciclos": 1,
                "minutos_totais": minutos_estudo
            }
        else:
            data[today_str]["ciclos"] += 1
            data[today_str]["minutos_totais"] += minutos_estudo

        with open(self.DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        self.update_stats_label()

    def update_stats_label(self):
        data = self.load_data()
        today_str = str(date.today())

        dias_estudados = len(data)
        minutos_hoje = data.get(today_str, {}).get("minutos_totais", 0)
        ciclos_hoje = data.get(today_str, {}).get("ciclos", 0)

        self.label_stats_today.config(text=f"Hoje: {minutos_hoje} min ({ciclos_hoje} ciclos)")
        self.label_stats_total.config(text=f"Total: {dias_estudados} dia(s) registrado(s)")

    # --- CONTROLE DO TIMER ---
    def update_clock(self):
        minutes, seconds = divmod(self.current_time, 60)
        self.label_timer.config(text=f"{minutes:02d}:{seconds:02d}")

        if self.current_time > 0:
            self.current_time -= 1
            self.timer_id = self.root.after(1000, self.update_clock)
        else:
            self.switch_phase()

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.btn_start.config(state=tk.DISABLED)
            self.btn_pause.config(state=tk.NORMAL)
            self.update_clock()

    def pause_timer(self):
        if self.is_running:
            self.is_running = False
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
            self.btn_start.config(state=tk.NORMAL)
            self.btn_pause.config(state=tk.DISABLED)

    def reset_timer(self):
        self.pause_timer()
        self.is_work_phase = True
        self.current_time = self.WORK_TIME
        self.label_status.config(text="Foco no Estudo! 📚", fg="#a6e3a1")
        minutes, seconds = divmod(self.current_time, 60)
        self.label_timer.config(text=f"{minutes:02d}:{seconds:02d}")

    def switch_phase(self):
        self.root.bell()
        if self.is_work_phase:
            # Salvamos no JSON assim que o tempo de estudo encerra
            self.save_completed_session()

            self.is_work_phase = False
            self.current_time = self.REST_TIME
            self.label_status.config(text="Pausa para Descanso! ☕", fg="#89b4fa")
            messagebox.showinfo("Pomodoro", "Excelente! Sessão concluída e registrada. Desconecte por 10 minutos.")
        else:
            self.is_work_phase = True
            self.current_time = self.WORK_TIME
            self.label_status.config(text="Foco no Estudo! 📚", fg="#a6e3a1")
            messagebox.showinfo("Pomodoro", "Pausa terminada! De volta ao estudo.")

        self.update_clock()


if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()