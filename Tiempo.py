import customtkinter as ctk
from datetime import datetime
import json
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AppPSP(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Gestión PSP - Control de Calidad Final")
        self.geometry("1250x950")

        self.fases_psp = ["Planificación", "Diseño", "Revisión de Diseño", "Codificación", 
                          "Revisión de Código", "Compilación", "Pruebas", "Post Mortem"]
        
        self.tipos_error = [
            "10 Omission", "20 Repetition", "30 Transcription", "40 Calculation",
            "50 Interfaz", "60 Verificación", "70 Datos", "80 Función", 
            "90 Sistema", "100 Entorno"
        ]
        
        self.registros_tiempo = []
        self.registros_defectos = []
        self.errores_finales = [] # Nueva lista para la Tabla 3

        # Configuración de Scroll
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.scroll_canvas = ctk.CTkScrollableFrame(self)
        self.scroll_canvas.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.scroll_canvas.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.scroll_canvas, text="DASHBOARD DE INGENIERÍA Y CALIDAD PSP", font=("Arial", 26, "bold")).grid(row=0, column=0, pady=15)

        # 1. PANEL DE PROYECTO
        self.frame_proy = ctk.CTkFrame(self.scroll_canvas)
        self.frame_proy.grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        self.entry_proyecto = ctk.CTkEntry(self.frame_proy, width=250, placeholder_text="Nombre del proyecto...")
        self.entry_proyecto.grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkButton(self.frame_proy, text="Recuperar Todo", command=self.cargar_datos).grid(row=0, column=1, padx=5)

        # 2. CONTENEDOR DE ENTRADAS (MENÚ DINÁMICO)
        self.input_container = ctk.CTkFrame(self.scroll_canvas)
        self.input_container.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        
        # 3. TERMINAL DE REGISTROS (LOG DE TEXTO)
        self.txt_display = ctk.CTkTextbox(self.scroll_canvas, width=1150, height=180, font=("Consolas", 12), fg_color="#1a1a1a")
        self.txt_display.grid(row=3, column=0, padx=20, pady=10)

        # 4. PESTAÑAS DE TABLAS
        self.tabview = ctk.CTkTabview(self.scroll_canvas, width=1180, height=600, command=self.al_cambiar_pestana)
        self.tabview.grid(row=4, column=0, padx=20, pady=10)
        
        self.tab1 = self.tabview.add("Tiempo por fase")
        self.tab2 = self.tabview.add("Defectos introducidos")
        self.tab3 = self.tabview.add("Defectos finales")

        self.celdas_t1, self.celdas_t2, self.celdas_t3 = [], [], []
        self.setup_ui_entradas()
        self.crear_tabla_estandar(self.tab1, self.celdas_t1, ["Etapa Desarrollo", "Plan (min)", "Tiempo Real", "Suma Mensual", "% a la Fecha"])
        self.crear_tabla_estandar(self.tab2, self.celdas_t2, ["Etapa Desarrollo", "Meta (U)", "Tiempo Real", "Suma Mensual", "% Avance"])
        self.crear_tabla_estandar(self.tab3, self.celdas_t3, ["Etapa Desarrollo", "Estimación (E)", "Real (E)", "Suma Mensual", "% Calidad"])

    def setup_ui_entradas(self):
        # Panel Tiempo (Pestaña 1)
        self.frame_ui_t = ctk.CTkFrame(self.input_container, fg_color="transparent")
        self.frame_ui_t.grid(row=0, column=0, sticky="ew")
        self.combo_fase_t = ctk.CTkComboBox(self.frame_ui_t, values=self.fases_psp, state="readonly", width=160)
        self.combo_fase_t.set("Planificación"); self.combo_fase_t.grid(row=0, column=0, padx=5, pady=10)
        self.t_ini_t = ctk.CTkEntry(self.frame_ui_t, placeholder_text="Inic HH:MM", width=85); self.t_ini_t.grid(row=0, column=1, padx=5)
        self.t_fin_t = ctk.CTkEntry(self.frame_ui_t, placeholder_text="Fin HH:MM", width=85); self.t_fin_t.grid(row=0, column=2, padx=5)
        self.t_mue_t = ctk.CTkEntry(self.frame_ui_t, placeholder_text="Muerto", width=65); self.t_mue_t.insert(0,"0"); self.t_mue_t.grid(row=0, column=3, padx=5)
        self.t_com_t = ctk.CTkEntry(self.frame_ui_t, placeholder_text="Comentarios Tiempo", width=350); self.t_com_t.grid(row=0, column=4, padx=5)
        ctk.CTkButton(self.frame_ui_t, text="Reg. Tiempo", fg_color="#27AE60", command=self.registrar_tiempo).grid(row=0, column=5, padx=5)

        # Panel Defectos (Pestaña 2)
        self.frame_ui_d = ctk.CTkFrame(self.input_container, fg_color="transparent")
        self.ent_id_d = ctk.CTkEntry(self.frame_ui_d, width=45, state="readonly", fg_color="#34495E"); self.ent_id_d.grid(row=0, column=0, padx=5, pady=10)
        self.actualizar_id_visual()
        self.combo_tipo_err = ctk.CTkComboBox(self.frame_ui_d, values=self.tipos_error, state="readonly", width=160); self.combo_tipo_err.set("10 Omission"); self.combo_tipo_err.grid(row=0, column=1, padx=5)
        self.combo_desc = ctk.CTkComboBox(self.frame_ui_d, values=self.fases_psp, state="readonly", width=150); self.combo_desc.set("Codificación"); self.combo_desc.grid(row=0, column=2, padx=5)
        self.combo_remo = ctk.CTkComboBox(self.frame_ui_d, values=self.fases_psp, state="readonly", width=150); self.combo_remo.set("Pruebas"); self.combo_remo.grid(row=0, column=3, padx=5)
        self.t_ini_d = ctk.CTkEntry(self.frame_ui_d, placeholder_text="Inic HH:MM", width=85); self.t_ini_d.grid(row=0, column=4, padx=5)
        self.t_fin_d = ctk.CTkEntry(self.frame_ui_d, placeholder_text="Fin HH:MM", width=85); self.t_fin_d.grid(row=0, column=5, padx=5)
        self.t_com_d = ctk.CTkEntry(self.frame_ui_d, placeholder_text="Observaciones", width=180); self.t_com_d.grid(row=0, column=6, padx=5)
        ctk.CTkButton(self.frame_ui_d, text="Reg. Defecto", fg_color="#E67E22", command=self.registrar_defecto).grid(row=0, column=7, padx=5)

        # Panel Errores Finales (Pestaña 3)
        self.frame_ui_e = ctk.CTkFrame(self.input_container, fg_color="transparent")
        ctk.CTkLabel(self.frame_ui_e, text="N° Errores:").grid(row=0, column=0, padx=10, pady=10)
        self.ent_num_err = ctk.CTkEntry(self.frame_ui_e, width=80, placeholder_text="0")
        self.ent_num_err.grid(row=0, column=1, padx=5)
        ctk.CTkLabel(self.frame_ui_e, text="Etapa Encontrada:").grid(row=0, column=2, padx=10)
        self.combo_fase_e = ctk.CTkComboBox(self.frame_ui_e, values=self.fases_psp, state="readonly", width=200)
        self.combo_fase_e.set("Pruebas")
        self.combo_fase_e.grid(row=0, column=3, padx=5)
        ctk.CTkButton(self.frame_ui_e, text="Registrar Error Final", fg_color="#C0392B", command=self.registrar_error_final).grid(row=0, column=4, padx=15)

    def actualizar_id_visual(self):
        self.ent_id_d.configure(state="normal")
        self.ent_id_d.delete(0, 'end'); self.ent_id_d.insert(0, str(len(self.registros_defectos) + 1))
        self.ent_id_d.configure(state="readonly")

    def al_cambiar_pestana(self):
        tab = self.tabview.get()
        # Ocultar todos primero
        self.frame_ui_t.grid_remove()
        self.frame_ui_d.grid_remove()
        self.frame_ui_e.grid_remove()
        
        if tab == "Defectos introducidos":
            self.frame_ui_d.grid(row=0, column=0, sticky="ew")
        elif tab == "Defectos finales":
            self.frame_ui_e.grid(row=0, column=0, sticky="ew")
        else:
            self.frame_ui_t.grid(row=0, column=0, sticky="ew")
        self.renderizar_logs()

    def registrar_error_final(self):
        try:
            num = int(self.ent_num_err.get() or 0)
            fase = self.combo_fase_e.get()
            self.errores_finales.append({
                "fecha": datetime.now().strftime("%d/%m/%Y"),
                "mes": datetime.now().strftime("%m"),
                "cantidad": num,
                "fase": fase
            })
            self.ent_num_err.delete(0, 'end')
            self.actualizar_tablas_calculos(); self.renderizar_logs(); self.guardar_datos()
        except: pass

    def registrar_tiempo(self):
        try:
            h_i, m_i = map(int, self.t_ini_t.get().split(':'))
            h_f, m_f = map(int, self.t_fin_t.get().split(':'))
            efec = (h_f*60+m_f) - (h_i*60+m_i) - float(self.t_mue_t.get() or 0)
            self.registros_tiempo.append({
                "fecha": datetime.now().strftime("%d/%m/%Y"), "mes": datetime.now().strftime("%m"),
                "fase": self.combo_fase_t.get(), "inicio": self.t_ini_t.get(), "fin": self.t_fin_t.get(),
                "muerto": float(self.t_mue_t.get() or 0), "efectivo": efec, "com": self.t_com_t.get()
            })
            self.actualizar_tablas_calculos(); self.renderizar_logs(); self.guardar_datos()
        except: pass

    def registrar_defecto(self):
        try:
            h_i, m_i = map(int, self.t_ini_d.get().split(':'))
            h_f, m_f = map(int, self.t_fin_d.get().split(':'))
            efec = (h_f*60+m_f) - (h_i*60+m_i)
            self.registros_defectos.append({
                "fecha": datetime.now().strftime("%d/%m/%Y"), "mes": datetime.now().strftime("%m"),
                "id": len(self.registros_defectos) + 1, "tipo": self.combo_tipo_err.get(),
                "fase": self.combo_desc.get(), "removido": self.combo_remo.get(),
                "inicio": self.t_ini_d.get(), "fin": self.t_fin_d.get(), "efectivo": efec, "com": self.t_com_d.get()
            })
            self.actualizar_id_visual(); self.actualizar_tablas_calculos(); self.renderizar_logs(); self.guardar_datos()
        except: pass

    def renderizar_logs(self):
        self.txt_display.delete("0.0", "end")
        tab = self.tabview.get()
        if tab == "Defectos finales":
            header = f"{'FECHA':<12} | {'CANTIDAD':<10} | {'ETAPA ENCONTRADA':<20}\n"
            self.txt_display.insert("end", header + "-"*50 + "\n")
            for r in self.errores_finales:
                self.txt_display.insert("end", f"{r['fecha']:<12} | {r['cantidad']:<10} | {r['fase']:<20}\n")
        elif tab == "Defectos introducidos":
            header = f"{'ID':<4} | {'TIPO':<16} | {'REMOVIDO EN':<18} | {'DURACIÓN':<8}\n"
            self.txt_display.insert("end", header + "-"*50 + "\n")
            for r in self.registros_defectos:
                self.txt_display.insert("end", f"{r['id']:<4} | {r['tipo']:<16} | {r['removido']:<18} | {r['efectivo']}m\n")
        else:
            header = f"{'FECHA':<12} | {'FASE':<18} | {'MINUTOS':<10}\n"
            self.txt_display.insert("end", header + "-"*45 + "\n")
            for r in self.registros_tiempo:
                self.txt_display.insert("end", f"{r['fecha']:<12} | {r['fase']:<18} | {r['efectivo']}m\n")

    def actualizar_tablas_calculos(self):
        mes_act = datetime.now().strftime("%m")
        t_r1, t_m1 = {}, {}
        t_r2, t_m2 = {}, {}
        t_r3, t_m3 = {}, {}

        for r in self.registros_tiempo:
            f = r['fase']
            t_r1[f] = t_r1.get(f, 0) + r['efectivo']
            if r['mes'] == mes_act: t_m1[f] = t_m1.get(f, 0) + r['efectivo']
        for r in self.registros_defectos:
            f = r['removido']
            t_r2[f] = t_r2.get(f, 0) + r['efectivo']
            if r['mes'] == mes_act: t_m2[f] = t_m2.get(f, 0) + r['efectivo']
        for r in self.errores_finales:
            f = r['fase']
            t_r3[f] = t_r3.get(f, 0) + r['cantidad']
            if r['mes'] == mes_act: t_m3[f] = t_m3.get(f, 0) + r['cantidad']

        for i, fase in enumerate(self.fases_psp):
            # Lógica para Tabla 1, 2 y 3
            for lista, dict_r, dict_m in [(self.celdas_t1, t_r1, t_m1), (self.celdas_t2, t_r2, t_m2), (self.celdas_t3, t_r3, t_m3)]:
                try: p_val = float(lista[i][0].get() or 0)
                except: p_val = 0
                r_val = dict_r.get(fase, 0); m_val = dict_m.get(fase, 0)
                perc = (m_val / p_val * 100) if p_val > 0 else 0
                lista[i][1].configure(text=str(r_val))
                lista[i][2].configure(text=str(m_val))
                lista[i][3].configure(text=f"{perc:.1f}%")

        # Totales Generales Fila 9
        for lista in [self.celdas_t1, self.celdas_t2, self.celdas_t3]:
            s_p = sum([float(lista[k][0].get() or 0) for k in range(8)])
            lista[8][0].configure(text=str(s_p))

    def crear_tabla_estandar(self, tab, celdas, headers):
        f = ctk.CTkFrame(tab); f.pack(padx=10, pady=10, fill="both", expand=True)
        for j, h in enumerate(headers): ctk.CTkLabel(f, text=h, font=("Arial", 11, "bold"), width=180).grid(row=0, column=j)
        for i, fase in enumerate(self.fases_psp + ["TOTAL GENERAL"]):
            ctk.CTkLabel(f, text=fase, fg_color="#34495E", width=180).grid(row=i+1, column=0, padx=1, pady=1)
            row = []
            if i < 8:
                e = ctk.CTkEntry(f, width=180, justify="center"); e.insert(0, "0"); e.grid(row=i+1, column=1)
                e.bind("<FocusOut>", lambda ev, ent=e: self.bloquear(ent)); row.append(e)
            else:
                l = ctk.CTkLabel(f, text="0", width=180, fg_color="#1F618D"); l.grid(row=i+1, column=1); row.append(l)
            for j in range(2, 5):
                l = ctk.CTkLabel(f, text="0", width=180, fg_color="#2C3E50"); l.grid(row=i+1, column=j); row.append(l)
            celdas.append(row)

    def bloquear(self, entry):
        try:
            if float(entry.get() or 0) != 0:
                entry.configure(state="readonly", fg_color="#566573")
            self.actualizar_tablas_calculos(); self.guardar_datos()
        except: pass

    def guardar_datos(self):
        nom = self.entry_proyecto.get() or "proyecto"
        p1 = [self.celdas_t1[i][0].get() for i in range(8)]
        p2 = [self.celdas_t2[i][0].get() for i in range(8)]
        p3 = [self.celdas_t3[i][0].get() for i in range(8)]
        data = {"t": self.registros_tiempo, "d": self.registros_defectos, "e": self.errores_finales, "p1": p1, "p2": p2, "p3": p3}
        with open(f"{nom}.json", "w") as f: json.dump(data, f, indent=4)

    def cargar_datos(self):
        nom = self.entry_proyecto.get()
        if os.path.exists(f"{nom}.json"):
            with open(f"{nom}.json", "r") as f:
                data = json.load(f)
                self.registros_tiempo = data.get("t", []); self.registros_defectos = data.get("d", [])
                self.errores_finales = data.get("e", [])
                for lista, key in [(self.celdas_t1, "p1"), (self.celdas_t2, "p2"), (self.celdas_t3, "p3")]:
                    planes = data.get(key, ["0"]*8)
                    for i, v in enumerate(planes):
                        lista[i][0].configure(state="normal")
                        lista[i][0].delete(0, 'end'); lista[i][0].insert(0, v)
                        if float(v) != 0: lista[i][0].configure(state="readonly", fg_color="#566573")
            self.actualizar_tablas_calculos(); self.renderizar_logs()

if __name__ == "__main__":
    AppPSP().mainloop()