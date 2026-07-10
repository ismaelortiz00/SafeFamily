from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.graphics import Color, Rectangle, Ellipse, Line, RoundedRectangle
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, IconLeftWidget, OneLineListItem, TwoLineListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.selectioncontrol import MDSwitch, MDCheckbox
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.widget import Widget
import random, math

from kivy.utils import platform

if platform != "android":
    Window.size = (375, 667)
# ══════════════════════════════════════════════
#  COLORES GLOBALES
# ══════════════════════════════════════════════
BLANCO         = (1.00, 1.00, 1.00, 1.0)
BLANCO_SUAVE   = (1.00, 1.00, 1.00, 1.0)   # puro blanco
CYAN_CLARO     = (1.00, 1.00, 1.00, 1.0)   # blanco (antes era cian, poco visible)
VIOLETA_CLARO  = (1.00, 1.00, 1.00, 1.0)   # blanco (títulos)
AMARILLO_CLARO = (1.00, 0.95, 0.55, 1.0)   # se mantiene (Premium)
VERDE_CLARO    = (0.70, 1.00, 0.85, 1.0)   # se mantiene (confirmaciones)
ROJO_CLARO     = (1.00, 0.65, 0.65, 1.0)   # se mantiene (errores)
GRIS_CLARO     = (0.90, 0.90, 0.95, 1.0)   # casi blanco (textos secundarios)

# ── Forzar colores blancos en MDTextField globalmente ──
from kivy.metrics import dp
from kivymd.uix.textfield import MDTextField as _MDTFBase

_orig_init = _MDTFBase.__init__
def _tf_init(self, **kw):
    kw.setdefault("text_color_normal",   [1, 1, 1, 1])
    kw.setdefault("text_color_focus",    [1, 1, 1, 1])
    kw.setdefault("hint_text_color_normal",  [0.75, 0.75, 0.85, 1])
    kw.setdefault("hint_text_color_focus",   [0.88, 0.72, 1.00, 1])
    kw.setdefault("line_color_normal",   [0.55, 0.30, 1.0, 0.6])
    kw.setdefault("line_color_focus",    [0.88, 0.72, 1.00, 1])
    _orig_init(self, **kw)
_MDTFBase.__init__ = _tf_init

PLAN_ORDEN = {None: 0, "silver": 1, "gold": 2, "platinum": 3}
PLAN_LABEL = {None: "Gratuito", "silver": "🥈 Silver", "gold": "🥇 Gold", "platinum": "💎 Platinum"}
PLAN_COLOR = {None: CYAN_CLARO, "silver": GRIS_CLARO, "gold": AMARILLO_CLARO, "platinum": VIOLETA_CLARO}

OPCIONES = [
    ("account-cog",           "Mi Perfil",            None,       "perfil"),
    ("cog-outline",           "Configuración",         None,       "config"),
    ("account-multiple-plus", "Agregar Miembro",       "silver",   "agregar"),
    ("map-marker-radius",     "Zonas Seguras",         "gold",     "zonas"),
    ("chart-line",            "Historial de Rutas",    "gold",     "historial"),
    ("shield-lock",           "Modo Privado",          "platinum", "privado"),
    ("palette-outline",       "Personalizar Interfaz", "platinum", "personalizar"),
    ("bell-ring-outline",     "Alertas Avanzadas",     "platinum", "alertas"),
    ("help-circle-outline",   "Ayuda & Soporte",       None,       "ayuda"),
    ("logout",                "Cerrar Sesión",         None,       "logout"),
]

# Datos en memoria (simula base de datos)
APP_STATE = {
    "nombre_usuario": "Admin",
    "avatar": "account",
    "notificaciones": True,
    "gps": True,
    "modo_privado": False,
    "miembros": [
        {"nombre": "Matias", "lugar": "En casa",      "correo": "matias@mail.com"},
        {"nombre": "Ismael", "lugar": "Trabajo",      "correo": "ismael@mail.com"},
        {"nombre": "Kevin",  "lugar": "Universidad",  "correo": "kevin@mail.com"},
    ],
    "zonas": [
        {"nombre": "Casa",    "coords": "-0.1807, -78.4678"},
        {"nombre": "Trabajo", "coords": "-0.1950, -78.5010"},
    ],
    "historial": [
        {"fecha": "Hoy 08:12",  "ruta": "Casa → Universidad"},
        {"fecha": "Ayer 17:45", "ruta": "Trabajo → Casa"},
        {"fecha": "Lun 09:00",  "ruta": "Casa → Trabajo"},
        {"fecha": "Dom 14:30",  "ruta": "Casa → Centro Comercial"},
    ],
    "alertas": {
        "salida_zona": True,
        "velocidad": False,
        "bateria": True,
        "checkin": False,
    }
}

AVATARES = ["account", "account-cowboy-hat", "robot", "cat", "dog",
            "alien", "ninja", "emoticon-cool", "star-face", "glasses"]


# ══════════════════════════════════════════════
#  HELPERS VISUALES
# ══════════════════════════════════════════════
def titulo_pantalla(texto):
    return MDLabel(text=texto, halign="center", font_style="H6", bold=True,
                   theme_text_color="Custom", text_color=VIOLETA_CLARO,
                   size_hint_y=None, height=44)

def separador():
    s = MDBoxLayout(size_hint_y=None, height=1)
    with s.canvas:
        Color(0.55, 0.30, 1.0, 0.25)
        Rectangle(pos=s.pos, size=s.size)
    return s

def card_oscura(height=None):
    kw = dict(radius=[12]*4, md_bg_color=[0.08, 0.06, 0.20, 1], elevation=3, padding=14)
    if height: kw["size_hint"] = (1, None); kw["height"] = height
    else:       kw["size_hint"] = (1, None); kw["height"] = 70
    return MDCard(**kw)


# ══════════════════════════════════════════════
#  BURBUJAS + FONDO
# ══════════════════════════════════════════════
class Burbuja(Widget):
    COLORES = [(0.40,0.85,1.0),(0.65,0.35,1.0),(0.25,0.95,0.70),(0.95,0.40,1.0),(0.35,0.65,1.0)]
    def __init__(self, w=375, h=667, **kwargs):
        super().__init__(**kwargs)
        self.w_p=w; self.h_p=h
        self.radio=random.randint(10,32); self.vel_x=random.uniform(-0.4,0.4)
        self.vel_y=random.uniform(0.3,0.75); alpha=random.uniform(0.06,0.18)
        r,g,b=random.choice(self.COLORES); d=self.radio*2
        self.size_hint=(None,None); self.size=(d,d)
        self.pos=(random.randint(0,max(1,w-d)),random.randint(-d,h))
        with self.canvas:
            Color(r,g,b,alpha); self.c=Ellipse(pos=self.pos,size=self.size)
            Color(r,g,b,alpha*2.5); self.b=Line(ellipse=(self.pos[0],self.pos[1],d,d),width=1.1)
        self._ev=Clock.schedule_interval(self._mv,1/30)
    def _mv(self,dt):
        d=self.radio*2; nx=self.x+self.vel_x; ny=self.y+self.vel_y
        if nx<0 or nx+d>self.w_p: self.vel_x*=-1; nx=max(0,min(nx,self.w_p-d))
        if ny>self.h_p+d: ny=-d; nx=random.randint(0,max(1,self.w_p-d))
        self.pos=(nx,ny); self.c.pos=self.pos; self.b.ellipse=(nx,ny,d,d)
    def detener(self): self._ev.cancel()

class FondoBurbujas(Widget):
    def __init__(self,**kwargs):
        super().__init__(**kwargs); self.size_hint=(1,1); self._bb=[]
        with self.canvas:
            Color(0.04,0.04,0.11,1); self._bg=Rectangle(pos=self.pos,size=self.size)
            Color(0.18,0.06,0.42,0.18); self._vl=Rectangle(pos=self.pos,size=self.size)
        self.bind(pos=self._s,size=self._s); Clock.schedule_once(self._cr,0.05)
    def _s(self,*a):
        self._bg.pos=self.pos; self._bg.size=self.size
        self._vl.pos=self.pos; self._vl.size=self.size
    def _cr(self,dt):
        w,h=Window.size
        for _ in range(15): b=Burbuja(w=w,h=h); self.add_widget(b); self._bb.append(b)


# ══════════════════════════════════════════════
#  RUEDA GIRATORIA
# ══════════════════════════════════════════════
class RuedaGiratoria(Widget):
    def __init__(self,radio=28,**kwargs):
        super().__init__(**kwargs); self.radio=radio; self.angulo=0
        self.size_hint=(None,None); self.size=(radio*2+10,radio*2+10)
        self._d(); Clock.schedule_interval(self._r,1/30)
    def _d(self):
        self.canvas.clear(); cx=self.x+self.width/2; cy=self.y+self.height/2; r=self.radio
        with self.canvas:
            Color(0.55,0.95,1.0,0.85); Line(circle=(cx,cy,r),width=2.5)
            Color(0.75,0.50,1.0,0.60); Line(circle=(cx,cy,r*0.60),width=1.5)
            for i in range(8):
                a=math.radians(self.angulo+i*45)
                Color(0.55,0.95,1.0,0.9 if i%2==0 else 0.4)
                Line(points=[cx+math.cos(a)*r*0.25,cy+math.sin(a)*r*0.25,
                              cx+math.cos(a)*r*0.95,cy+math.sin(a)*r*0.95],width=1.4)
            Color(1,1,1,0.9); Ellipse(pos=(cx-4,cy-4),size=(8,8))
    def _r(self,dt): self.angulo=(self.angulo+1.5)%360; self._d()
    def on_pos(self,*a): self._d()
    def on_size(self,*a): self._d()


# ══════════════════════════════════════════════
#  QR
# ══════════════════════════════════════════════
class CuadroQRVisual(Widget):
    """QR vectorial con línea de escáner animada."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (180, 180)
        self.pos_hint = {"center_x": 0.5}
        self._scan_y = 0      # posición relativa 0..1 de la línea
        self._scan_dir = 1
        self._ev = None
        with self.canvas:
            # Fondo blanco del QR
            Color(1, 1, 1, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)
            # Esquinas (patrón QR)
            Color(0.06, 0.04, 0.18, 1)
            self.tl  = Rectangle(size=(50, 50))
            self.tr  = Rectangle(size=(50, 50))
            self.bl  = Rectangle(size=(50, 50))
            self.ct  = Rectangle(size=(28, 28))
            # Puntos de datos simulados (fila de cuadraditos)
            Color(0.06, 0.04, 0.18, 0.55)
            self._dots = []
            for i in range(6):
                d = Rectangle(size=(8, 8))
                self._dots.append(d)
            # Línea de escaneo neón
            Color(0.30, 0.90, 0.60, 0.85)
            self._linea = Line(points=[0, 0, 1, 0], width=2.2)
            # Brillo sobre la línea
            Color(0.30, 0.90, 0.60, 0.25)
            self._brillo = Rectangle(pos=(0, 0), size=(180, 6))
        self.bind(pos=self._layout, size=self._layout)
        Clock.schedule_once(lambda dt: self._start_anim(), 0.1)

    def _layout(self, *a):
        x, y = self.pos; w, h = self.size
        self.bg.pos  = self.pos; self.bg.size = self.size
        self.tl.pos  = (x + 10,     y + h - 60)
        self.tr.pos  = (x + w - 60, y + h - 60)
        self.bl.pos  = (x + 10,     y + 10)
        self.ct.pos  = (x + w/2 - 14, y + h/2 - 14)
        # Puntos de datos en filas
        for i, d in enumerate(self._dots):
            d.pos = (x + 68 + i * 14, y + h/2 + 20)
        self._update_scan()

    def _update_scan(self):
        x, y = self.pos; w, h = self.size
        sy = y + 12 + self._scan_y * (h - 24)
        self._linea.points = [x + 8, sy, x + w - 8, sy]
        self._brillo.pos   = (x + 8, sy - 3)
        self._brillo.size  = (w - 16, 6)

    def _start_anim(self):
        self._ev = Clock.schedule_interval(self._tick, 1/30)

    def _tick(self, dt):
        self._scan_y += self._scan_dir * 0.015
        if self._scan_y >= 1: self._scan_dir = -1
        if self._scan_y <= 0: self._scan_dir = 1
        self._update_scan()

    def detener(self):
        if self._ev: self._ev.cancel()


# ══════════════════════════════════════════════
#  DRAWER FILA
# ══════════════════════════════════════════════
class FilaOpcion(MDBoxLayout):
    def __init__(self,icono,texto,plan_req,accion,bloqueado,on_tap,**kw):
        super().__init__(orientation="horizontal",size_hint_y=None,height=54,
                         padding=[16,0,12,0],spacing=14,**kw)
        self._tap=on_tap; self._ac=accion; self._bl=bloqueado; self._pr=plan_req
        with self.canvas.before:
            Color(1,1,1,0.03); self._bg=Rectangle(pos=self.pos,size=self.size)
        self.bind(pos=lambda i,v:(setattr(self._bg,"pos",v)),
                  size=lambda i,v:(setattr(self._bg,"size",v)))
        self.add_widget(MDIconButton(
            icon="lock-outline" if bloqueado else icono,
            theme_text_color="Custom",
            text_color=list(GRIS_CLARO if bloqueado else CYAN_CLARO),
            size_hint=(None,None),size=(36,36),pos_hint={"center_y":0.5}))
        col=MDBoxLayout(orientation="vertical",spacing=0,size_hint_y=None,height=54,
                        pos_hint={"center_y":0.5})
        col.add_widget(MDLabel(text=texto,font_style="Body1",theme_text_color="Custom",
                               text_color=list(GRIS_CLARO if bloqueado else BLANCO_SUAVE),
                               size_hint_y=None,height=30,valign="center"))
        if bloqueado:
            col.add_widget(MDLabel(text=f"Requiere {PLAN_LABEL[plan_req]}",font_style="Caption",
                                   theme_text_color="Custom",text_color=list(PLAN_COLOR[plan_req]),
                                   size_hint_y=None,height=18))
        self.add_widget(col)
    def on_touch_down(self,touch):
        if self.collide_point(*touch.pos): self._tap(self._ac,self._bl,self._pr); return True
        return super().on_touch_down(touch)


# ══════════════════════════════════════════════
#  DRAWER MENU
# ══════════════════════════════════════════════
class DrawerMenu(MDFloatLayout):
    ANCHO=270
    def __init__(self,pantalla,**kw):
        super().__init__(**kw); self.pantalla=pantalla; self.abierto=False
        self.size_hint=(None,None); self.size=(self.ANCHO,Window.height)
        self.x=-self.ANCHO; self.y=0
        with self.canvas.before:
            Color(0.05,0.03,0.16,0.97)
            self._bg=RoundedRectangle(pos=self.pos,size=self.size,
                                      radius=[(0,0),(16,16),(16,16),(0,0)])
            Color(0.55,0.30,1.0,0.50)
            self._bd=Line(points=[self.x+self.ANCHO,self.y,
                                  self.x+self.ANCHO,self.y+Window.height],width=1.5)
        self.bind(pos=self._sb,size=self._sb)
        self._int=MDBoxLayout(orientation="vertical",size_hint=(None,None),
                              size=(self.ANCHO,Window.height),pos=(0,0))
        self.add_widget(self._int); self._poblar()

    def _sb(self,*a):
        self._bg.pos=self.pos; self._bg.size=self.size
        self._bd.points=[self.x+self.ANCHO,self.y,self.x+self.ANCHO,self.y+Window.height]
        self._int.pos=self.pos; self._int.size=(self.ANCHO,Window.height)

    def _poblar(self):
        self._int.clear_widgets()
        app=MDApp.get_running_app(); plan=getattr(app,"plan_usuario",None)
        nivel=PLAN_ORDEN.get(plan,0)
        # Header
        hdr=MDBoxLayout(orientation="vertical",size_hint_y=None,height=100,
                        padding=[18,18,10,8],spacing=2)
        with hdr.canvas.before:
            Color(0.08,0.05,0.22,1); self._hbg=Rectangle(pos=hdr.pos,size=hdr.size)
        hdr.bind(pos=lambda i,v:setattr(self._hbg,"pos",v),
                 size=lambda i,v:setattr(self._hbg,"size",v))
        hdr.add_widget(MDLabel(text="☰  SafeFamily",font_style="H6",bold=True,
                               theme_text_color="Custom",text_color=VIOLETA_CLARO,
                               size_hint_y=None,height=34))
        hdr.add_widget(MDLabel(text=f"Plan: {PLAN_LABEL.get(plan,'Gratuito')}",
                               font_style="Caption",theme_text_color="Custom",
                               text_color=list(PLAN_COLOR.get(plan,CYAN_CLARO)),
                               size_hint_y=None,height=22))
        self._int.add_widget(hdr); self._int.add_widget(separador())
        scroll=MDScrollView(size_hint=(1,1))
        lista=MDBoxLayout(orientation="vertical",adaptive_height=True)
        for icono,texto,plan_req,accion in OPCIONES:
            bl=plan_req is not None and nivel<PLAN_ORDEN.get(plan_req,0)
            lista.add_widget(FilaOpcion(icono=icono,texto=texto,plan_req=plan_req,
                                        accion=accion,bloqueado=bl,on_tap=self._exec))
            lista.add_widget(separador())
        scroll.add_widget(lista); self._int.add_widget(scroll)

    def _exec(self,accion,bloqueado,plan_req):
        if bloqueado:
            dlg=MDDialog(title="🔒 Función Premium",
                         text=f"Requiere plan {PLAN_LABEL[plan_req]}.\n¿Mejorar ahora?",
                         buttons=[
                             MDRaisedButton(text="VER PLANES",md_bg_color=[0.45,0.20,0.90,1],
                                            text_color=list(BLANCO),
                                            on_release=lambda x:(dlg.dismiss(),self.cerrar(),
                                                Clock.schedule_once(lambda dt:self._nav("premium"),0.25))),
                             MDFlatButton(text="AHORA NO",theme_text_color="Custom",
                                         text_color=list(GRIS_CLARO),
                                         on_release=lambda x:dlg.dismiss())])
            dlg.open(); return
        self.cerrar()
        if accion=="logout":
            Clock.schedule_once(lambda dt:self._nav("login","right"),0.25)
        elif accion=="premium":
            Clock.schedule_once(lambda dt:self._nav("premium"),0.25)
        else:
            Clock.schedule_once(lambda dt:self._nav(accion),0.25)

    def _nav(self,dest,direction="left"):
        sm=self.pantalla.manager
        if dest in ("login","registro","principal","premium","mapa","chat",
                    "perfil","config","agregar","zonas","historial",
                    "privado","personalizar","alertas","ayuda"):
            sm.transition=SlideTransition(direction=direction)
            sm.current=dest

    def abrir(self):
        if self.abierto: return
        self._poblar(); self.size=(self.ANCHO,Window.height); self.abierto=True
        Animation(x=0,duration=0.22,t="out_quad").start(self)

    def cerrar(self):
        if not self.abierto: return
        def _fin(a,w): w.abierto=False
        an=Animation(x=-self.ANCHO,duration=0.18,t="in_quad"); an.bind(on_complete=_fin); an.start(self)

    def on_touch_down(self,touch):
        if self.abierto and not self.collide_point(*touch.pos): self.cerrar(); return True
        return super().on_touch_down(touch)


# ══════════════════════════════════════════════
#  PANTALLA BASE (fondo + toolbar)
# ══════════════════════════════════════════════
class PantallaBase(Screen):
    def _build(self, titulo, dest_back="principal"):
        self.add_widget(FondoBurbujas())
        self._lay = MDBoxLayout(orientation="vertical")
        self._lay.add_widget(MDTopAppBar(
            title=titulo, md_bg_color=[0.08,0.05,0.20,1],
            specific_text_color=list(VIOLETA_CLARO),
            left_action_items=[["arrow-left",lambda x:self._back(dest_back)]]))
        self._scroll = MDScrollView(size_hint=(1,1))
        self._body   = MDBoxLayout(orientation="vertical",adaptive_height=True,
                                   padding=20,spacing=15)
        self._scroll.add_widget(self._body)
        self._lay.add_widget(self._scroll)
        self.add_widget(self._lay)

    def _back(self,dest):
        self.manager.transition=SlideTransition(direction="right"); self.manager.current=dest

    def _toast(self,msg):
        dlg=MDDialog(text=msg,buttons=[MDFlatButton(text="OK",
                     theme_text_color="Custom",text_color=VIOLETA_CLARO,
                     on_release=lambda x:dlg.dismiss())])
        dlg.open()


# ══════════════════════════════════════════════
#  PANTALLA MI PERFIL
# ══════════════════════════════════════════════
class PantallaPerfil(PantallaBase):
    def __init__(self,**kw):
        super().__init__(**kw)
        self._build("👤 Mi Perfil")

    def on_pre_enter(self):
        self._body.clear_widgets()
        app=MDApp.get_running_app()

        # Avatar selector
        self._body.add_widget(titulo_pantalla("Selecciona tu Avatar"))
        grid=MDBoxLayout(spacing=8,size_hint_y=None,height=60,padding=[0,0,0,0])
        for av in AVATARES:
            btn=MDIconButton(icon=av,theme_text_color="Custom",
                             text_color=list(CYAN_CLARO if av==APP_STATE["avatar"] else GRIS_CLARO),
                             size_hint=(None,None),size=(44,44))
            btn.bind(on_release=lambda x,a=av:self._set_avatar(a))
            grid.add_widget(btn)
        sv=MDScrollView(size_hint=(1,None),height=64); sv.add_widget(grid)
        self._body.add_widget(sv)

        # Nombre
        self._body.add_widget(separador())
        self._body.add_widget(titulo_pantalla("Tu Nombre"))
        self.campo_nombre=MDTextField(text=APP_STATE["nombre_usuario"],
                                      hint_text="Nombre de usuario",multiline=False)
        self._body.add_widget(self.campo_nombre)

        # Plan
        self._body.add_widget(separador())
        plan=getattr(app,"plan_usuario",None)
        card=card_oscura(80)
        cl=MDBoxLayout(orientation="vertical",spacing=4)
        cl.add_widget(MDLabel(text="Plan Activo",font_style="Caption",
                              theme_text_color="Custom",text_color=GRIS_CLARO,
                              size_hint_y=None,height=20))
        cl.add_widget(MDLabel(text=PLAN_LABEL.get(plan,"Gratuito"),font_style="H6",bold=True,
                              theme_text_color="Custom",text_color=list(PLAN_COLOR.get(plan,CYAN_CLARO)),
                              size_hint_y=None,height=30))
        card.add_widget(cl); self._body.add_widget(card)

        # Guardar
        self._body.add_widget(MDRaisedButton(
            text="💾  GUARDAR CAMBIOS",md_bg_color=[0.45,0.20,0.90,1],
            text_color=list(BLANCO),size_hint_x=1,
            on_release=self._guardar))

    def _set_avatar(self,av):
        APP_STATE["avatar"]=av
        MDApp.get_running_app().avatar_seleccionado=av
        self.on_pre_enter()

    def _guardar(self,obj):
        APP_STATE["nombre_usuario"]=self.campo_nombre.text or "Admin"
        self._toast(f"✅ Perfil actualizado\nNombre: {APP_STATE['nombre_usuario']}\nAvatar: {APP_STATE['avatar']}")


# ══════════════════════════════════════════════
#  PANTALLA CONFIGURACIÓN
# ══════════════════════════════════════════════
class PantallaConfig(PantallaBase):
    def __init__(self,**kw):
        super().__init__(**kw); self._build("⚙️ Configuración")

    def on_pre_enter(self):
        self._body.clear_widgets()

        for titulo,clave,desc in [
            ("🔔 Notificaciones","notificaciones","Recibir alertas y mensajes"),
            ("📡 GPS Activo","gps","Compartir ubicación en tiempo real"),
        ]:
            self._body.add_widget(separador())
            fila=MDBoxLayout(orientation="horizontal",size_hint_y=None,height=64,
                             spacing=10,padding=[0,8,0,8])
            col=MDBoxLayout(orientation="vertical",spacing=2)
            col.add_widget(MDLabel(text=titulo,font_style="Body1",bold=True,
                                   theme_text_color="Custom",text_color=BLANCO_SUAVE,
                                   size_hint_y=None,height=24))
            col.add_widget(MDLabel(text=desc,font_style="Caption",
                                   theme_text_color="Custom",text_color=GRIS_CLARO,
                                   size_hint_y=None,height=18))
            sw=MDSwitch(active=APP_STATE[clave],size_hint=(None,None),size=(60,36),
                        pos_hint={"center_y":0.5})
            _c=clave
            sw.bind(active=lambda inst,val,c=_c:APP_STATE.update({c:val}))
            fila.add_widget(col); fila.add_widget(sw)
            self._body.add_widget(fila)

        self._body.add_widget(separador())
        self._body.add_widget(titulo_pantalla("🌐 Idioma"))
        for idioma in ["Español","English","Português"]:
            btn=MDRaisedButton(text=idioma,size_hint_x=1,
                               md_bg_color=[0.15,0.08,0.35,1],text_color=list(BLANCO_SUAVE),
                               on_release=lambda x,i=idioma:self._toast(f"Idioma seleccionado: {i}"))
            self._body.add_widget(btn)

        self._body.add_widget(separador())
        self._body.add_widget(MDRaisedButton(
            text="🗑️  BORRAR CACHÉ",md_bg_color=[0.40,0.08,0.08,1],
            text_color=list(ROJO_CLARO),size_hint_x=1,
            on_release=lambda x:self._toast("✅ Caché borrada correctamente")))


# ══════════════════════════════════════════════
#  PANTALLA AGREGAR MIEMBRO
# ══════════════════════════════════════════════
class PantallaAgregarMiembro(PantallaBase):
    def __init__(self,**kw):
        super().__init__(**kw); self._build("👥 Agregar Miembro")

    def on_pre_enter(self):
        self._body.clear_widgets()

        # Miembros actuales
        self._body.add_widget(titulo_pantalla("Miembros del Grupo"))
        self._lista_widget=MDBoxLayout(orientation="vertical",adaptive_height=True,spacing=6)
        self._refrescar_lista()
        self._body.add_widget(self._lista_widget)

        self._body.add_widget(separador())
        self._body.add_widget(titulo_pantalla("Invitar Nuevo Miembro"))

        self.campo_nombre=MDTextField(hint_text="Nombre del miembro",multiline=False)
        self.campo_correo=MDTextField(hint_text="Correo electrónico",multiline=False)
        self.campo_lugar =MDTextField(hint_text="Ubicación inicial (ej: Casa)",multiline=False)
        self._body.add_widget(self.campo_nombre)
        self._body.add_widget(self.campo_correo)
        self._body.add_widget(self.campo_lugar)

        self._body.add_widget(MDRaisedButton(
            text="➕  AGREGAR MIEMBRO",md_bg_color=[0.15,0.55,0.35,1],
            text_color=list(VERDE_CLARO),size_hint_x=1,on_release=self._agregar))

    def _refrescar_lista(self):
        self._lista_widget.clear_widgets()
        for m in APP_STATE["miembros"]:
            card=card_oscura(72)
            row=MDBoxLayout(orientation="horizontal",spacing=10)
            row.add_widget(MDIconButton(icon="account-circle",theme_text_color="Custom",
                                        text_color=list(CYAN_CLARO),size_hint=(None,None),size=(40,40)))
            col=MDBoxLayout(orientation="vertical",spacing=2)
            col.add_widget(MDLabel(text=m["nombre"],font_style="Body1",bold=True,
                                   theme_text_color="Custom",text_color=BLANCO_SUAVE,
                                   size_hint_y=None,height=24))
            col.add_widget(MDLabel(text=f"📍 {m['lugar']}  |  {m['correo']}",
                                   font_style="Caption",theme_text_color="Custom",
                                   text_color=GRIS_CLARO,size_hint_y=None,height=18))
            row.add_widget(col)
            _n=m["nombre"]
            row.add_widget(MDIconButton(icon="delete-outline",theme_text_color="Custom",
                                        text_color=list(ROJO_CLARO),size_hint=(None,None),size=(36,36),
                                        on_release=lambda x,n=_n:self._eliminar(n)))
            card.add_widget(row); self._lista_widget.add_widget(card)

    def _agregar(self,obj):
        n=self.campo_nombre.text.strip(); c=self.campo_correo.text.strip()
        l=self.campo_lugar.text.strip() or "Desconocida"
        if not n or not c: self._toast("⚠️ Nombre y correo son obligatorios"); return
        APP_STATE["miembros"].append({"nombre":n,"lugar":l,"correo":c})
        self.campo_nombre.text=""; self.campo_correo.text=""; self.campo_lugar.text=""
        self._refrescar_lista(); self._toast(f"✅ {n} agregado al grupo")

    def _eliminar(self,nombre):
        APP_STATE["miembros"]=[m for m in APP_STATE["miembros"] if m["nombre"]!=nombre]
        self._refrescar_lista(); self._toast(f"🗑️ {nombre} eliminado del grupo")


# ══════════════════════════════════════════════
#  PANTALLA ZONAS SEGURAS
# ══════════════════════════════════════════════
class PantallaZonas(PantallaBase):
    def __init__(self,**kw):
        super().__init__(**kw); self._build("📍 Zonas Seguras")

    def on_pre_enter(self):
        self._body.clear_widgets()
        self._body.add_widget(titulo_pantalla("Zonas Registradas"))
        self._lista=MDBoxLayout(orientation="vertical",adaptive_height=True,spacing=6)
        self._refrescar()
        self._body.add_widget(self._lista)
        self._body.add_widget(separador())
        self._body.add_widget(titulo_pantalla("Nueva Zona"))
        self.c_nombre=MDTextField(hint_text="Nombre de la zona",multiline=False)
        self.c_lat   =MDTextField(hint_text="Latitud (ej: -0.1807)",multiline=False)
        self.c_lon   =MDTextField(hint_text="Longitud (ej: -78.4678)",multiline=False)
        self._body.add_widget(self.c_nombre); self._body.add_widget(self.c_lat)
        self._body.add_widget(self.c_lon)
        self._body.add_widget(MDRaisedButton(
            text="📌  AGREGAR ZONA",md_bg_color=[0.10,0.40,0.65,1],
            text_color=list(CYAN_CLARO),size_hint_x=1,on_release=self._agregar))

    def _refrescar(self):
        self._lista.clear_widgets()
        for z in APP_STATE["zonas"]:
            card=card_oscura(72)
            row=MDBoxLayout(orientation="horizontal",spacing=10)
            row.add_widget(MDIconButton(icon="map-marker",theme_text_color="Custom",
                                        text_color=list(VERDE_CLARO),size_hint=(None,None),size=(40,40)))
            col=MDBoxLayout(orientation="vertical",spacing=2)
            col.add_widget(MDLabel(text=z["nombre"],font_style="Body1",bold=True,
                                   theme_text_color="Custom",text_color=BLANCO_SUAVE,
                                   size_hint_y=None,height=24))
            col.add_widget(MDLabel(text=f"📡 {z['coords']}",font_style="Caption",
                                   theme_text_color="Custom",text_color=GRIS_CLARO,
                                   size_hint_y=None,height=18))
            row.add_widget(col)
            _n=z["nombre"]
            row.add_widget(MDIconButton(icon="delete-outline",theme_text_color="Custom",
                                        text_color=list(ROJO_CLARO),size_hint=(None,None),size=(36,36),
                                        on_release=lambda x,n=_n:self._eliminar(n)))
            card.add_widget(row); self._lista.add_widget(card)

    def _agregar(self,obj):
        n=self.c_nombre.text.strip(); lat=self.c_lat.text.strip(); lon=self.c_lon.text.strip()
        if not n or not lat or not lon: self._toast("⚠️ Completa todos los campos"); return
        APP_STATE["zonas"].append({"nombre":n,"coords":f"{lat}, {lon}"})
        self.c_nombre.text=""; self.c_lat.text=""; self.c_lon.text=""
        self._refrescar(); self._toast(f"✅ Zona '{n}' agregada")

    def _eliminar(self,nombre):
        APP_STATE["zonas"]=[z for z in APP_STATE["zonas"] if z["nombre"]!=nombre]
        self._refrescar(); self._toast(f"🗑️ Zona '{nombre}' eliminada")


# ══════════════════════════════════════════════
#  PANTALLA HISTORIAL
# ══════════════════════════════════════════════
class PantallaHistorial(PantallaBase):
    def __init__(self,**kw):
        super().__init__(**kw); self._build("📈 Historial de Rutas")

    def on_pre_enter(self):
        self._body.clear_widgets()
        self._body.add_widget(titulo_pantalla("Últimas Rutas Registradas"))
        for h in APP_STATE["historial"]:
            card=card_oscura(80)
            col=MDBoxLayout(orientation="vertical",spacing=4)
            col.add_widget(MDLabel(text=h["ruta"],font_style="Body1",bold=True,
                                   theme_text_color="Custom",text_color=CYAN_CLARO,
                                   size_hint_y=None,height=26))
            col.add_widget(MDLabel(text=f"🕐 {h['fecha']}",font_style="Caption",
                                   theme_text_color="Custom",text_color=GRIS_CLARO,
                                   size_hint_y=None,height=18))
            card.add_widget(col); self._body.add_widget(card)
        self._body.add_widget(separador())
        self._body.add_widget(MDRaisedButton(
            text="🗑️  LIMPIAR HISTORIAL",md_bg_color=[0.40,0.08,0.08,1],
            text_color=list(ROJO_CLARO),size_hint_x=1,on_release=self._limpiar))

    def _limpiar(self,obj):
        APP_STATE["historial"].clear(); self.on_pre_enter()
        self._toast("✅ Historial limpiado")


# ══════════════════════════════════════════════
#  PANTALLA MODO PRIVADO
# ══════════════════════════════════════════════
class PantallaPrivado(PantallaBase):
    def __init__(self,**kw):
        super().__init__(**kw); self._build("🛡️ Modo Privado")

    def on_pre_enter(self):
        self._body.clear_widgets()
        activo=APP_STATE["modo_privado"]
        color=ROJO_CLARO if activo else VERDE_CLARO
        estado="ACTIVO 🔴" if activo else "INACTIVO 🟢"

        card=MDCard(size_hint=(1,None),height=120,radius=[16]*4,
                    md_bg_color=[0.18,0.05,0.05,1] if activo else [0.05,0.18,0.10,1],
                    elevation=5,padding=18)
        col=MDBoxLayout(orientation="vertical",spacing=6)
        col.add_widget(MDLabel(text="Estado del Modo Privado",font_style="Caption",
                               theme_text_color="Custom",text_color=GRIS_CLARO,
                               size_hint_y=None,height=20))
        col.add_widget(MDLabel(text=estado,font_style="H5",bold=True,
                               theme_text_color="Custom",text_color=list(color),
                               size_hint_y=None,height=40))
        card.add_widget(col); self._body.add_widget(card)

        self._body.add_widget(MDLabel(
            text="Cuando está activo, tu ubicación es invisible\npara todos los miembros del grupo.",
            halign="center",theme_text_color="Custom",text_color=BLANCO_SUAVE,
            size_hint_y=None,height=50))

        lbl="🔴  DESACTIVAR MODO PRIVADO" if activo else "🛡️  ACTIVAR MODO PRIVADO"
        bg=[0.60,0.08,0.10,1] if activo else [0.10,0.45,0.25,1]
        self._body.add_widget(MDRaisedButton(
            text=lbl,md_bg_color=bg,text_color=list(BLANCO),
            size_hint_x=1,on_release=self._toggle))

    def _toggle(self,obj):
        APP_STATE["modo_privado"]=not APP_STATE["modo_privado"]
        self.on_pre_enter()


# ══════════════════════════════════════════════
#  PANTALLA PERSONALIZAR
# ══════════════════════════════════════════════
class PantallaPersonalizar(PantallaBase):
    def __init__(self,**kw):
        super().__init__(**kw); self._build("🎨 Personalizar Interfaz")

    def on_pre_enter(self):
        self._body.clear_widgets()
        self._body.add_widget(titulo_pantalla("Color de Acento"))
        colores=[
            ("Violeta",  [0.45,0.20,0.90,1]),
            ("Cian",     [0.10,0.70,0.90,1]),
            ("Verde",    [0.10,0.65,0.35,1]),
            ("Dorado",   [0.75,0.55,0.05,1]),
            ("Magenta",  [0.80,0.15,0.60,1]),
        ]
        grid=MDBoxLayout(spacing=10,size_hint_y=None,height=50)
        for nombre,color in colores:
            btn=MDRaisedButton(text=nombre,md_bg_color=color,text_color=list(BLANCO),
                               size_hint_x=1,
                               on_release=lambda x,c=color,n=nombre:self._toast(f"✅ Color '{n}' aplicado"))
            grid.add_widget(btn)
        self._body.add_widget(grid)

        self._body.add_widget(separador())
        self._body.add_widget(titulo_pantalla("Tamaño de Fuente"))
        tam=MDBoxLayout(spacing=10,size_hint_y=None,height=50)
        for t in ["Pequeño","Normal","Grande"]:
            tam.add_widget(MDRaisedButton(text=t,md_bg_color=[0.15,0.08,0.35,1],
                                          text_color=list(BLANCO_SUAVE),size_hint_x=1,
                                          on_release=lambda x,s=t:self._toast(f"Fuente: {s}")))
        self._body.add_widget(tam)

        self._body.add_widget(separador())
        self._body.add_widget(titulo_pantalla("Tema"))
        temas=MDBoxLayout(spacing=10,size_hint_y=None,height=50)
        for tm,bg in [("Oscuro",[0.05,0.03,0.15,1]),("Medianoche",[0.00,0.05,0.20,1]),("Cosmos",[0.10,0.02,0.25,1])]:
            temas.add_widget(MDRaisedButton(text=tm,md_bg_color=bg,text_color=list(BLANCO_SUAVE),
                                             size_hint_x=1,
                                             on_release=lambda x,t=tm:self._toast(f"Tema '{t}' aplicado")))
        self._body.add_widget(temas)


# ══════════════════════════════════════════════
#  PANTALLA ALERTAS AVANZADAS
# ══════════════════════════════════════════════
class PantallaAlertas(PantallaBase):
    def __init__(self,**kw):
        super().__init__(**kw); self._build("🔔 Alertas Avanzadas")

    def on_pre_enter(self):
        self._body.clear_widgets()
        self._body.add_widget(titulo_pantalla("Configura tus Alertas"))
        alertas_cfg=[
            ("salida_zona",  "🚧 Salida de zona segura","Alerta cuando alguien sale de una zona definida"),
            ("velocidad",    "🚗 Velocidad inusual",     "Alerta si detecta movimiento a alta velocidad"),
            ("bateria",      "🔋 Batería baja",          "Avisa cuando la batería baja del 20%"),
            ("checkin",      "📍 Check-in automático",  "Notifica llegada a zonas frecuentes"),
        ]
        for clave,titulo,desc in alertas_cfg:
            self._body.add_widget(separador())
            fila=MDBoxLayout(orientation="horizontal",size_hint_y=None,height=68,
                             spacing=10,padding=[0,8,0,8])
            col=MDBoxLayout(orientation="vertical",spacing=2)
            col.add_widget(MDLabel(text=titulo,font_style="Body1",bold=True,
                                   theme_text_color="Custom",text_color=BLANCO_SUAVE,
                                   size_hint_y=None,height=24))
            col.add_widget(MDLabel(text=desc,font_style="Caption",
                                   theme_text_color="Custom",text_color=GRIS_CLARO,
                                   size_hint_y=None,height=18))
            sw=MDSwitch(active=APP_STATE["alertas"][clave],
                        size_hint=(None,None),size=(60,36),pos_hint={"center_y":0.5})
            _c=clave
            sw.bind(active=lambda inst,val,c=_c:(APP_STATE["alertas"].update({c:val}),
                                                  self._toast(f"{'✅ Activado' if val else '🔕 Desactivado'}: {c}")))
            fila.add_widget(col); fila.add_widget(sw)
            self._body.add_widget(fila)

        self._body.add_widget(separador())
        self._body.add_widget(MDRaisedButton(
            text="💾  GUARDAR ALERTAS",md_bg_color=[0.45,0.20,0.90,1],
            text_color=list(BLANCO),size_hint_x=1,
            on_release=lambda x:self._toast("✅ Configuración de alertas guardada")))


# ══════════════════════════════════════════════
#  PANTALLA AYUDA
# ══════════════════════════════════════════════
class PantallaAyuda(PantallaBase):
    def __init__(self,**kw):
        super().__init__(**kw); self._build("❓ Ayuda & Soporte")

    def on_pre_enter(self):
        self._body.clear_widgets()
        faqs=[
            ("¿Cómo agrego un miembro?","Ve al menú ☰ → Agregar Miembro (plan Silver requerido). Ingresa nombre y correo."),
            ("¿Cómo funciona el GPS?","El GPS se activa en Configuración. Comparte tu ubicación en tiempo real con el grupo."),
            ("¿Qué es el Modo Privado?","Oculta tu ubicación temporalmente. Requiere plan Platinum."),
            ("¿Cómo cambio mi plan?","Desde el menú ☰ → Ver Planes o desde el botón ⭐ Premium en la pantalla principal."),
            ("¿Dónde veo las rutas?","En el menú ☰ → Historial de Rutas (requiere plan Gold)."),
        ]
        for preg,resp in faqs:
            card=MDCard(size_hint=(1,None),height=110,radius=[12]*4,
                        md_bg_color=[0.08,0.06,0.20,1],elevation=3,padding=14)
            col=MDBoxLayout(orientation="vertical",spacing=6)
            col.add_widget(MDLabel(text=f"❓ {preg}",font_style="Body1",bold=True,
                                   theme_text_color="Custom",text_color=VIOLETA_CLARO,
                                   size_hint_y=None,height=28))
            col.add_widget(MDLabel(text=resp,font_style="Caption",
                                   theme_text_color="Custom",text_color=BLANCO_SUAVE,
                                   size_hint_y=None,height=48))
            card.add_widget(col); self._body.add_widget(card)

        self._body.add_widget(separador())
        self._body.add_widget(titulo_pantalla("Contacto"))
        for ico,txt in [("email","soporte@safefamily.app"),
                         ("whatsapp","+593 99 000 0000"),
                         ("information","Versión 1.0.0")]:
            fila=MDBoxLayout(orientation="horizontal",spacing=10,size_hint_y=None,height=44)
            fila.add_widget(MDIconButton(icon=ico,theme_text_color="Custom",
                                         text_color=list(CYAN_CLARO),size_hint=(None,None),size=(36,36)))
            fila.add_widget(MDLabel(text=txt,theme_text_color="Custom",text_color=BLANCO_SUAVE,
                                    size_hint_y=None,height=44,valign="center"))
            self._body.add_widget(fila)


# ══════════════════════════════════════════════
#  PANTALLAS ORIGINALES
# ══════════════════════════════════════════════
class PantallaLogin(Screen):
    def __init__(self,**kw):
        super().__init__(**kw); self.add_widget(FondoBurbujas())
        lay=MDBoxLayout(orientation="vertical",padding=30,spacing=15,
                        pos_hint={"center_x":0.5,"center_y":0.5},size_hint=(0.9,0.85))
        lay.add_widget(MDLabel(text="SafeFamily",halign="center",font_style="H4",bold=True,
                               theme_text_color="Custom",text_color=VIOLETA_CLARO,
                               size_hint_y=None,height=40))
        lay.add_widget(MDLabel(text="Inicia sesión para continuar",halign="center",
                               theme_text_color="Custom",text_color=BLANCO_SUAVE,
                               size_hint_y=None,height=25))
        self.usuario=MDTextField(hint_text="Usuario o Correo",icon_right="account",multiline=False)
        self.contrasena=MDTextField(hint_text="Contraseña",icon_right="key",password=True,multiline=False)
        lay.add_widget(self.usuario); lay.add_widget(self.contrasena)
        self.err=MDLabel(text="",halign="center",theme_text_color="Custom",
                         text_color=ROJO_CLARO,size_hint_y=None,height=25)
        lay.add_widget(self.err)
        lay.add_widget(MDRaisedButton(text="INGRESAR",pos_hint={"center_x":0.5},size_hint_x=0.8,
                                      md_bg_color=[0.45,0.20,0.90,1],text_color=BLANCO,
                                      on_release=self._login))
        lay.add_widget(MDFlatButton(text="¿No tienes cuenta? Regístrate aquí",
                                    pos_hint={"center_x":0.5},theme_text_color="Custom",
                                    text_color=CYAN_CLARO,on_release=self._reg))
        self.add_widget(lay)
    def _login(self,o):
        if self.usuario.text=="admin" and self.contrasena.text=="1234":
            self.err.text=""; self.usuario.text=""; self.contrasena.text=""
            self.manager.transition=SlideTransition(direction="left"); self.manager.current="principal"
        else: self.err.text="Usuario o contraseña incorrectos"
    def _reg(self,o):
        self.manager.transition=SlideTransition(direction="left"); self.manager.current="registro"

class PantallaRegistro(Screen):
    def __init__(self,**kw):
        super().__init__(**kw); self.add_widget(FondoBurbujas())
        lay=MDBoxLayout(orientation="vertical",padding=30,spacing=20,
                        pos_hint={"center_x":0.5,"center_y":0.5},size_hint=(0.9,0.8))
        lay.add_widget(MDLabel(text="Crear Cuenta",halign="center",font_style="H4",bold=True,
                               theme_text_color="Custom",text_color=VIOLETA_CLARO,
                               size_hint_y=None,height=40))
        self.nu=MDTextField(hint_text="Nombre de Usuario",icon_right="account-plus",multiline=False)
        self.nc=MDTextField(hint_text="Contraseña",icon_right="lock-plus",password=True,multiline=False)
        lay.add_widget(self.nu); lay.add_widget(self.nc)
        lay.add_widget(MDRaisedButton(text="REGISTRAR",pos_hint={"center_x":0.5},size_hint_x=0.8,
                                      md_bg_color=[0.45,0.20,0.90,1],text_color=BLANCO,
                                      on_release=lambda o:self._ir("login")))
        lay.add_widget(MDFlatButton(text="Volver al Login",pos_hint={"center_x":0.5},
                                    theme_text_color="Custom",text_color=CYAN_CLARO,
                                    on_release=lambda o:self._ir("login")))
        self.add_widget(lay)
    def _ir(self,d):
        self.manager.transition=SlideTransition(direction="right"); self.manager.current=d

class Principal(Screen):
    def __init__(self,**kw):
        super().__init__(**kw); self.dialog=None
        self.add_widget(FondoBurbujas())
        self._float=MDFloatLayout(size_hint=(1,1),pos_hint={"x":0,"y":0})
        main=MDBoxLayout(orientation="vertical",size_hint=(1,1),pos_hint={"x":0,"y":0})
        self.toolbar=MDTopAppBar(title="SafeFamily",pos_hint={"top":1},
                                 md_bg_color=[0.08,0.05,0.20,1],
                                 specific_text_color=list(VIOLETA_CLARO),
                                 left_action_items=[["menu",lambda x:self._drawer.abrir()]],
                                 right_action_items=[["bell",lambda x:None]])
        main.add_widget(self.toolbar)
        scroll=MDScrollView(); body=MDBoxLayout(orientation="vertical",padding=20,spacing=15,adaptive_height=True)
        mapa_card=MDCard(size_hint=(1,None),height=140,radius=[20]*4,
                         md_bg_color=[0.10,0.07,0.25,1],elevation=4)
        ca=MDFloatLayout()
        self.ml=MDLabel(text="MAPA SAFEFAMILY",theme_text_color="Custom",text_color=CYAN_CLARO,
                        font_style="H6",size_hint=(None,None),size=(200,50),
                        pos_hint={"center_x":0.5,"center_y":0.5},halign="center")
        ca.add_widget(self.ml); mapa_card.add_widget(ca)
        an=(Animation(pos_hint={"center_x":0.75},duration=2,t="in_out_sine")+
            Animation(pos_hint={"center_x":0.25},duration=2,t="in_out_sine"))
        an.repeat=True; an.start(self.ml); body.add_widget(mapa_card)
        # Lista de miembros con tarjetas oscuras (texto blanco visible)
        miembros_box=MDBoxLayout(orientation="vertical",adaptive_height=True,spacing=4)
        self.items_miembros=[]
        for nombre,lugar in [("Matias","En casa"),("Ismael","Trabajo"),("Kevin","Universidad")]:
            card=MDCard(size_hint=(1,None),height=62,radius=[12]*4,
                        md_bg_color=[0.10,0.07,0.26,1],elevation=2,padding=[12,0,12,0])
            fila=MDBoxLayout(orientation="horizontal",spacing=12)
            self._ico=MDIconButton(icon="account",theme_text_color="Custom",
                                   text_color=list(CYAN_CLARO),
                                   size_hint=(None,None),size=(40,40),
                                   pos_hint={"center_y":0.5})
            col=MDBoxLayout(orientation="vertical",spacing=2,pos_hint={"center_y":0.5})
            col.add_widget(MDLabel(text=nombre,font_style="Body1",bold=True,
                                   theme_text_color="Custom",text_color=list(BLANCO),
                                   size_hint_y=None,height=26))
            col.add_widget(MDLabel(text=f"📍 {lugar}",font_style="Caption",
                                   theme_text_color="Custom",text_color=list(GRIS_CLARO),
                                   size_hint_y=None,height=18))
            fila.add_widget(self._ico); fila.add_widget(col)
            card.add_widget(fila)
            _n=nombre
            card.bind(on_release=lambda x,n=_n:self._chat(n))
            self.items_miembros.append(self._ico)
            miembros_box.add_widget(card)
        body.add_widget(miembros_box)
        bts=MDBoxLayout(spacing=10,size_hint_y=None,height=50)
        bts.add_widget(MDRaisedButton(text="Ver mapa",md_bg_color=[0.15,0.08,0.40,1],text_color=BLANCO,on_release=lambda o:self._ir("mapa")))
        bts.add_widget(MDRaisedButton(text="Chat General",md_bg_color=[0.10,0.35,0.70,1],text_color=BLANCO,on_release=lambda o:self._chat("General")))
        bts.add_widget(MDRaisedButton(text="⭐ Premium",md_bg_color=[0.55,0.40,0.00,1],text_color=AMARILLO_CLARO,on_release=lambda o:self._ir("premium")))
        body.add_widget(bts)
        body.add_widget(MDRaisedButton(text="EMERGENCIA",md_bg_color=[0.75,0.08,0.15,1],text_color=BLANCO,size_hint=(1,None),height=50,on_release=self._emergencia))
        body.add_widget(MDRaisedButton(text="CERRAR SESIÓN",md_bg_color=[0.15,0.15,0.30,1],text_color=BLANCO_SUAVE,size_hint=(1,None),height=50,on_release=lambda o:self._ir("login","right")))
        scroll.add_widget(body); main.add_widget(scroll); self._float.add_widget(main)
        self._rueda=RuedaGiratoria(radio=28); self._float.add_widget(self._rueda)
        self._drawer=DrawerMenu(pantalla=self); self._float.add_widget(self._drawer)
        self.add_widget(self._float)

    def on_pre_enter(self):
        pass  # avatares manejados en las cards directamente
    def on_enter(self):
        self._rueda.pos=(8,Window.height-56-self._rueda.height-8)
    def _ir(self,d,direction="left"):
        self.manager.transition=SlideTransition(direction=direction); self.manager.current=d
    def _chat(self,n):
        self._ir("chat"); pc=self.manager.get_screen("chat")
        pc.cargar_chat(n)
        Clock.schedule_once(lambda dt:setattr(pc.escribir,"focus",True),0.2)
    def _emergencia(self,obj):
        self._ov=MDFloatLayout(size_hint=(1,1),pos_hint={"x":0,"y":0})
        with self._ov.canvas.before:
            Color(0,0,0,0.60); Rectangle(pos=(0,0),size=Window.size)
        card=MDCard(size_hint=(None,None),size=(300,350),
                    pos_hint={"center_x":0.5,"center_y":0.5},
                    md_bg_color=[0.05,0.03,0.16,1],radius=[20]*4,padding=16)
        col=MDBoxLayout(orientation="vertical",spacing=10)
        col.add_widget(MDLabel(
            text="🚨  ¿Qué emergencia tienes?",halign="center",
            font_style="H6",bold=True,theme_text_color="Custom",
            text_color=list(BLANCO),size_hint_y=None,height=36))
        for txt,color,ent in [
            ("📞  POLICÍA",      [0.10,0.20,0.85,1],"Policía"),
            ("🔥  BOMBEROS",     [0.85,0.42,0.00,1],"Bomberos"),
            ("🚑  AMBULANCIA",   [0.10,0.62,0.18,1],"Médicos"),
            ("⚠️  ENVIAR ALERTA",[0.72,0.06,0.14,1],None),
        ]:
            cb=(lambda x,e=ent:self._llamada(e)) if ent else self._alerta
            col.add_widget(MDRaisedButton(text=txt,md_bg_color=color,
                text_color=list(BLANCO),size_hint_x=1,elevation=4,on_release=cb))
        col.add_widget(MDFlatButton(text="✕  CANCELAR",size_hint_x=1,
            theme_text_color="Custom",text_color=list(GRIS_CLARO),
            on_release=lambda x:self._qov()))
        card.add_widget(col); self._ov.add_widget(card)
        self._float.add_widget(self._ov)

    def _qov(self):
        if hasattr(self,"_ov") and self._ov.parent:
            self._float.remove_widget(self._ov)

    def _llamada(self,e):
        self._qov()
        ov=MDFloatLayout(size_hint=(1,1),pos_hint={"x":0,"y":0})
        with ov.canvas.before:
            Color(0,0,0,0.60); Rectangle(pos=(0,0),size=Window.size)
        card=MDCard(size_hint=(None,None),size=(290,160),
                    pos_hint={"center_x":0.5,"center_y":0.5},
                    md_bg_color=[0.05,0.03,0.16,1],radius=[20]*4,padding=16)
        col=MDBoxLayout(orientation="vertical",spacing=8)
        col.add_widget(MDLabel(text=f"📞  Llamando a {e}...",halign="center",
            font_style="H6",bold=True,theme_text_color="Custom",
            text_color=list(BLANCO),size_hint_y=None,height=34))
        col.add_widget(MDLabel(text="La ayuda está en camino.",halign="center",
            font_style="Caption",theme_text_color="Custom",
            text_color=list(GRIS_CLARO),size_hint_y=None,height=22))
        col.add_widget(MDRaisedButton(text="📵  COLGAR",
            md_bg_color=[0.72,0.06,0.14,1],text_color=list(BLANCO),
            size_hint_x=1,on_release=lambda x:self._float.remove_widget(ov)))
        card.add_widget(col); ov.add_widget(card); self._float.add_widget(ov)

    def _alerta(self,obj):
        self._qov()
        ov=MDFloatLayout(size_hint=(1,1),pos_hint={"x":0,"y":0})
        with ov.canvas.before:
            Color(0,0,0,0.60); Rectangle(pos=(0,0),size=Window.size)
        card=MDCard(size_hint=(None,None),size=(290,180),
                    pos_hint={"center_x":0.5,"center_y":0.5},
                    md_bg_color=[0.05,0.03,0.16,1],radius=[20]*4,padding=16)
        col=MDBoxLayout(orientation="vertical",spacing=8)
        col.add_widget(MDLabel(text="⚠️  ALERTA ENVIADA",halign="center",
            font_style="H6",bold=True,theme_text_color="Custom",
            text_color=list(AMARILLO_CLARO),size_hint_y=None,height=34))
        col.add_widget(MDLabel(
            text="📍 Lat: -0.1807  |  Lon: -78.4678\nTu grupo ha sido notificado.",
            halign="center",font_style="Body2",theme_text_color="Custom",
            text_color=list(BLANCO),size_hint_y=None,height=44))
        col.add_widget(MDRaisedButton(text="✓  CERRAR",
            md_bg_color=[0.25,0.12,0.55,1],text_color=list(BLANCO),
            size_hint_x=1,on_release=lambda x:self._float.remove_widget(ov)))
        card.add_widget(col); ov.add_widget(card); self._float.add_widget(ov)

class PantallaPlanes(Screen):
    def __init__(self,**kw):
        super().__init__(**kw); self.dialog=None; self.add_widget(FondoBurbujas())
        lay=MDBoxLayout(orientation="vertical")
        lay.add_widget(MDTopAppBar(title="SafeFamily Premium",md_bg_color=[0.08,0.05,0.20,1],
                                   specific_text_color=list(VIOLETA_CLARO),
                                   left_action_items=[["arrow-left",lambda x:self._v()]]))
        scroll=MDScrollView(); cont=MDBoxLayout(orientation="vertical",padding=20,spacing=15,adaptive_height=True)
        cont.add_widget(MDLabel(text="⭐ Mejora tu plan",halign="center",font_style="H5",bold=True,theme_text_color="Custom",text_color=VIOLETA_CLARO,size_hint_y=None,height=40))
        for nombre,precio,bens,bg,tc,pk in [
            ("🥈 Silver","$2.99/mes","• Hasta 5 miembros\n• Agregar Miembro\n• Invitaciones",[0.13,0.13,0.32,1],CYAN_CLARO,"silver"),
            ("🥇 Gold","$5.99/mes","• Todo Silver\n• GPS + Zonas + Historial",[0.22,0.16,0.04,1],AMARILLO_CLARO,"gold"),
            ("💎 Platinum","$9.99/mes","• TODO + Privado + Alertas + Personalizar",[0.16,0.07,0.38,1],VIOLETA_CLARO,"platinum"),
        ]:
            card=MDCard(size_hint=(1,None),height=185,radius=[15]*4,md_bg_color=bg,elevation=5,padding=12)
            cl=MDBoxLayout(orientation="vertical",spacing=5)
            cl.add_widget(MDLabel(text=nombre,font_style="H6",bold=True,theme_text_color="Custom",text_color=list(tc),size_hint_y=None,height=25))
            cl.add_widget(MDLabel(text=precio,font_style="Subtitle2",theme_text_color="Custom",text_color=list(tc),size_hint_y=None,height=20))
            cl.add_widget(MDLabel(text=bens,theme_text_color="Custom",text_color=list(tc),size_hint_y=None,height=55,font_style="Caption"))
            cl.add_widget(MDRaisedButton(text="Elegir este plan",md_bg_color=[0.45,0.20,0.90,0.90],text_color=list(BLANCO),size_hint_x=1,on_release=lambda x,n=nombre,pk=pk:self._pago(n,pk)))
            card.add_widget(cl); cont.add_widget(card)
        scroll.add_widget(cont); lay.add_widget(scroll); self.add_widget(lay)
    def _v(self):
        self.manager.transition=SlideTransition(direction="right"); self.manager.current="principal"
    def _pago(self, nombre, pk):
        nl = nombre.replace("🥈 ","").replace("🥇 ","").replace("💎 ","")
        self._ov_pago = MDFloatLayout(size_hint=(1,1), pos_hint={"x":0,"y":0})
        with self._ov_pago.canvas.before:
            Color(0,0,0,0.60); Rectangle(pos=(0,0), size=Window.size)
        card = MDCard(size_hint=(None,None), size=(300,310),
                      pos_hint={"center_x":0.5,"center_y":0.5},
                      md_bg_color=[0.05,0.03,0.16,1], radius=[20]*4, padding=16)
        col = MDBoxLayout(orientation="vertical", spacing=12)
        col.add_widget(MDLabel(
            text=f"💳  Pagar · {nl}", halign="center",
            font_style="H6", bold=True,
            theme_text_color="Custom", text_color=list(BLANCO),
            size_hint_y=None, height=36))
        for et, bg in [
            ("💳  Tarjeta de Crédito", [0.28,0.12,0.78,1]),
            ("📱  PayPal",             [0.00,0.38,0.82,1]),
            ("🔳  Código QR",          [0.08,0.52,0.42,1]),
        ]:
            col.add_widget(MDRaisedButton(
                text=et, md_bg_color=bg, text_color=list(BLANCO),
                size_hint_x=1, elevation=4,
                on_release=lambda x,m=et,p=nl,k=pk: self._redir(m,p,k)))
        col.add_widget(MDFlatButton(
            text="✕  CANCELAR", size_hint_x=1,
            theme_text_color="Custom", text_color=list(GRIS_CLARO),
            on_release=lambda x: self._qov_pago()))
        card.add_widget(col)
        self._ov_pago.add_widget(card)
        # Añadirlo al layout raíz de la pantalla
        self.children[0].add_widget(self._ov_pago)

    def _qov_pago(self):
        if hasattr(self,"_ov_pago") and self._ov_pago.parent:
            self._ov_pago.parent.remove_widget(self._ov_pago)

    def _redir(self, m, p, pk):
        self._qov_pago()
        if "QR" in m:
            self._qr = CuadroQRVisual()
            ov = MDFloatLayout(size_hint=(1,1), pos_hint={"x":0,"y":0})
            with ov.canvas.before:
                Color(0,0,0,0.60); Rectangle(pos=(0,0), size=Window.size)
            card = MDCard(size_hint=(None,None), size=(300,380),
                          pos_hint={"center_x":0.5,"center_y":0.5},
                          md_bg_color=[0.05,0.03,0.16,1], radius=[20]*4, padding=16)
            col = MDBoxLayout(orientation="vertical", spacing=10)
            col.add_widget(MDLabel(
                text="🔳  Escanea para pagar", halign="center",
                font_style="H6", bold=True,
                theme_text_color="Custom", text_color=list(VERDE_CLARO),
                size_hint_y=None, height=34))
            col.add_widget(self._qr)
            col.add_widget(MDLabel(
                text="Usa la app de tu banco para confirmar.",
                halign="center", font_style="Caption",
                theme_text_color="Custom", text_color=list(BLANCO),
                size_hint_y=None, height=26))
            col.add_widget(MDRaisedButton(
                text="✔  COMPLETÉ MI PAGO",
                md_bg_color=[0.10,0.60,0.38,1], text_color=list(BLANCO),
                size_hint_x=1,
                on_release=lambda x: (self._qr.detener(),
                                      ov.parent.remove_widget(ov) if ov.parent else None,
                                      self._proc("QR", p, pk))))
            col.add_widget(MDFlatButton(
                text="✕  ATRÁS", size_hint_x=1,
                theme_text_color="Custom", text_color=list(GRIS_CLARO),
                on_release=lambda x: (self._qr.detener(),
                                      ov.parent.remove_widget(ov) if ov.parent else None)))
            card.add_widget(col); ov.add_widget(card)
            self.children[0].add_widget(ov)
        else:
            self._proc(m, p, pk)

    def _proc(self, m, p, pk):
        MDApp.get_running_app().plan_usuario = pk
        ov = MDFloatLayout(size_hint=(1,1), pos_hint={"x":0,"y":0})
        with ov.canvas.before:
            Color(0,0,0,0.60); Rectangle(pos=(0,0), size=Window.size)
        card = MDCard(size_hint=(None,None), size=(290,170),
                      pos_hint={"center_x":0.5,"center_y":0.5},
                      md_bg_color=[0.05,0.03,0.16,1], radius=[20]*4, padding=16)
        col = MDBoxLayout(orientation="vertical", spacing=10)
        col.add_widget(MDLabel(
            text="✅  Plan Activado", halign="center",
            font_style="H6", bold=True,
            theme_text_color="Custom", text_color=list(VERDE_CLARO),
            size_hint_y=None, height=34))
        col.add_widget(MDLabel(
            text=f"¡Plan {p} activado!\nYa puedes usar sus funciones.",
            halign="center", font_style="Body2",
            theme_text_color="Custom", text_color=list(BLANCO),
            size_hint_y=None, height=44))
        col.add_widget(MDRaisedButton(
            text="CONTINUAR", md_bg_color=[0.25,0.12,0.55,1],
            text_color=list(BLANCO), size_hint_x=1,
            on_release=lambda x: (ov.parent.remove_widget(ov) if ov.parent else None,
                                  self._v())))
        card.add_widget(col); ov.add_widget(card)
        self.children[0].add_widget(ov)

class PantallaMapa(Screen):
    def __init__(self,**kw):
        super().__init__(**kw); self.add_widget(FondoBurbujas())
        lay=MDBoxLayout(orientation="vertical")
        lay.add_widget(MDTopAppBar(title="Mapa",md_bg_color=[0.08,0.05,0.20,1],specific_text_color=list(VIOLETA_CLARO),left_action_items=[["arrow-left",lambda x:self._v()]]))
        lay.add_widget(MDLabel(text="Mapa en desarrollo",halign="center",theme_text_color="Custom",text_color=BLANCO_SUAVE))
        self.add_widget(lay)
    def _v(self):
        self.manager.transition=SlideTransition(direction="right"); self.manager.current="principal"

class PantallaChat(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.usuario_actual = ""

        # Fondo con burbujas
        self.add_widget(FondoBurbujas())

        lay = MDBoxLayout(orientation="vertical")

        # Toolbar con nombre del chat
        self.toolbar = MDTopAppBar(
            title="Chat",
            md_bg_color=[0.06, 0.04, 0.18, 1],
            specific_text_color=list(BLANCO),
            left_action_items=[["arrow-left", lambda x: self._v()]])
        lay.add_widget(self.toolbar)

        # Área de mensajes
        self.scroll = MDScrollView(size_hint=(1, 1))
        self.msgs = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            padding=[10, 10, 10, 10],
            spacing=8)
        self.scroll.add_widget(self.msgs)
        lay.add_widget(self.scroll)

        # Barra de escritura estilo WhatsApp
        barra = MDBoxLayout(size_hint_y=None, height=58,
                            padding=[8, 6, 8, 6], spacing=8)
        with barra.canvas.before:
            Color(0.06, 0.04, 0.18, 1)
            self._bb = Rectangle(pos=barra.pos, size=barra.size)
        barra.bind(pos=lambda i, v: setattr(self._bb, "pos", v),
                   size=lambda i, v: setattr(self._bb, "size", v))

        self.escribir = MDTextField(
            hint_text="Escribe un mensaje...",
            multiline=False, size_hint_x=0.80)

        btn_env = MDRaisedButton(
            text="➤", md_bg_color=[0.45, 0.20, 0.90, 1],
            text_color=list(BLANCO), size_hint=(0.20, 1),
            on_release=self._env)

        barra.add_widget(self.escribir)
        barra.add_widget(btn_env)
        lay.add_widget(barra)
        self.add_widget(lay)

    def cargar_chat(self, nombre):
        """Carga el historial guardado de este chat."""
        self.usuario_actual = nombre
        self.toolbar.title = f"Chat · {nombre}"
        self.msgs.clear_widgets()

        # Inicializar historial si no existe
        if nombre not in APP_STATE.get("chats", {}):
            if "chats" not in APP_STATE:
                APP_STATE["chats"] = {}
            APP_STATE["chats"][nombre] = []

        # Re-renderizar mensajes guardados
        for msg in APP_STATE["chats"][nombre]:
            self._render_burbuja(msg["texto"], msg["es_mio"])

        # Scroll al final
        Clock.schedule_once(lambda dt: setattr(self.scroll, "scroll_y", 0), 0.2)

    def _render_burbuja(self, txt, es_mio):
        """Dibuja una burbuja en pantalla sin guardar en estado."""
        bg_mio  = [0.32, 0.10, 0.72, 1]   # violeta — mensajes propios
        bg_otro = [0.10, 0.09, 0.28, 1]   # azul oscuro — mensajes recibidos

        bg = bg_mio if es_mio else bg_otro

        # Ancho máximo de la burbuja en px
        ancho_burbuja = Window.width * 0.72

        # Altura dinámica según texto
        chars  = len(txt)
        lineas = max(1, -(-chars // 28))
        h_txt  = lineas * 22 + 4
        h_fila = h_txt + 28   # padding vertical

        fila = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None, height=h_fila,
            padding=[4, 4, 4, 4])

        burbuja = MDBoxLayout(
            orientation="vertical",
            size_hint=(None, 1),
            width=ancho_burbuja,
            padding=[14, 8, 14, 8])

        # Canvas: fondo redondeado propio por burbuja
        _br = []
        _radius = [(16,16),(16,16),(4,16),(16,16)] if es_mio \
                  else [(16,16),(16,16),(16,16),(4,16)]
        with burbuja.canvas.before:
            Color(*bg)
            rr = RoundedRectangle(pos=burbuja.pos,
                                  size=burbuja.size,
                                  radius=_radius)
            _br.append(rr)

        burbuja.bind(
            pos=lambda  inst, val, r=_br: setattr(r[0], "pos",  val),
            size=lambda inst, val, r=_br: setattr(r[0], "size", val))

        # Hora simulada
        from datetime import datetime
        hora = datetime.now().strftime("%H:%M")

        # Texto del mensaje
        burbuja.add_widget(MDLabel(
            text=txt,
            font_style="Body2",
            theme_text_color="Custom",
            text_color=list(BLANCO),
            size_hint_y=None,
            height=h_txt,
            text_size=(ancho_burbuja - 28, None)))

        # Hora debajo
        burbuja.add_widget(MDLabel(
            text=hora,
            font_style="Caption",
            theme_text_color="Custom",
            text_color=(0.75, 0.75, 0.85, 0.80),
            size_hint_y=None, height=16,
            halign="right"))

        esp = Widget(size_hint_x=1)   # empuja la burbuja al lado correcto

        if es_mio:
            fila.add_widget(esp)
            fila.add_widget(burbuja)
        else:
            fila.add_widget(burbuja)
            fila.add_widget(esp)

        self.msgs.add_widget(fila)

    def _env(self, *args):
        txt = self.escribir.text.strip()
        if not txt:
            return
        nombre = self.usuario_actual

        # Guardar en APP_STATE para persistencia
        if "chats" not in APP_STATE:
            APP_STATE["chats"] = {}
        if nombre not in APP_STATE["chats"]:
            APP_STATE["chats"][nombre] = []
        APP_STATE["chats"][nombre].append({"texto": txt, "es_mio": True})

        # Renderizar burbuja
        self._render_burbuja(txt, True)
        self.escribir.text = ""

        # Scroll al último mensaje
        Clock.schedule_once(lambda dt: setattr(self.scroll, "scroll_y", 0), 0.1)

    def _v(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "principal"

    def _v(self):
        self.manager.transition=SlideTransition(direction="right")
        self.manager.current="principal"

# ══════════════════════════════════════════════
#  APP
# ══════════════════════════════════════════════
class SafeFamilyApp(MDApp):
    avatar_seleccionado="account"
    plan_usuario=None

    def build(self):
        self.theme_cls.primary_palette="DeepPurple"
        sm=ScreenManager()
        sm.add_widget(PantallaLogin(name="login"))
        sm.add_widget(PantallaRegistro(name="registro"))
        sm.add_widget(Principal(name="principal"))
        sm.add_widget(PantallaPlanes(name="premium"))
        sm.add_widget(PantallaMapa(name="mapa"))
        sm.add_widget(PantallaChat(name="chat"))
        sm.add_widget(PantallaPerfil(name="perfil"))
        sm.add_widget(PantallaConfig(name="config"))
        sm.add_widget(PantallaAgregarMiembro(name="agregar"))
        sm.add_widget(PantallaZonas(name="zonas"))
        sm.add_widget(PantallaHistorial(name="historial"))
        sm.add_widget(PantallaPrivado(name="privado"))
        sm.add_widget(PantallaPersonalizar(name="personalizar"))
        sm.add_widget(PantallaAlertas(name="alertas"))
        sm.add_widget(PantallaAyuda(name="ayuda"))
        sm.current="login"
        return sm

if __name__ == "__main__":
    SafeFamilyApp().run()
