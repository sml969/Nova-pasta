from kivy.app import App
import os
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from cryptography.fernet import Fernet
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout

class Tela1(Screen):
    def __init__(self, **kwargs):
        super(Tela1, self).__init__(**kwargs)
        layout = FloatLayout()

        btn = Button(text="Ir para Tela 2", size_hint=(None, None), size=(500, 80), pos_hint={"center_x": 0.5, "center_y": 0.6})
        btn.bind(on_release=self.mudar_para_tela2)
        layout.add_widget(btn)

        btn_funcao1 = Button(text="Gerar Chave", size_hint=(None, None), size=(500, 80), pos_hint={"center_x": 0.5, "center_y": 0.4})
        btn_funcao1.bind(on_release=self.gerar_chave)
        layout.add_widget(btn_funcao1)

        self.add_widget(layout)

    def mudar_para_tela2(self, *args):
        self.manager.current = 'tela2'

    def gerar_chave(self, instance):
        chave = Fernet.generate_key()
        with open("chave.key", "wb") as chave_arquivo:
            chave_arquivo.write(chave)
        label = Label(text="Chave gerada com sucesso!", size_hint=(None, None), size=(500, 50), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.add_widget(label)

    def carregar_chave(self):
        return open("chave.key", "rb").read()

class Tela2(Screen):
    def __init__(self, **kwargs):
        super(Tela2, self).__init__(**kwargs)
        layout = FloatLayout()

        btn = Button(text="Ir para Tela 3", size_hint=(None, None), size=(500, 80), pos_hint={"center_x": 0.5, "center_y": 0.7})
        btn.bind(on_release=self.mudar_para_tela3)
        layout.add_widget(btn)

        label = Label(text="Digite o nome do arquivo abaixo:", size_hint=(None, None), size=(250, 50), pos_hint={"center_x": 0.5, "center_y": 0.5})
        layout.add_widget(label)

        self.text_input = TextInput(hint_text="Digite aqui", multiline=False, size_hint=(None, None), size=(500, 50), pos_hint={"center_x": 0.5, "center_y": 0.4})
        layout.add_widget(self.text_input)

        self.result_label = Label(text="", size_hint=(None, None), size=(500, 50), pos_hint={"center_x": 0.5, "center_y": 0.2})
        layout.add_widget(self.result_label)

        self.text_input.bind(text=self.atualizar_texto)

        btn_funcao2 = Button(text="Criptografar Arquivo", size_hint=(None, None), size=(500, 80), pos_hint={"center_x": 0.5, "center_y": 0.2})
        btn_funcao2.bind(on_release=self.criptografar_arquivo)
        layout.add_widget(btn_funcao2)

        self.add_widget(layout)

    def atualizar_texto(self, instance, value):
        self.result_label.text = f"Você digitou: {value}"

    def carregar_chave(self):
        return open("chave.key", "rb").read()

    def criptografar_arquivo(self, instance):
        nome_arquivo = self.text_input.text
        if not os.path.exists(nome_arquivo):
            self.result_label.text = "Arquivo não encontrado."
            return

        chave = self.carregar_chave()
        f = Fernet(chave)

        with open(nome_arquivo, "rb") as arquivo:
            dados = arquivo.read()

        dados_criptografados = f.encrypt(dados)

        with open(nome_arquivo, "wb") as arquivo:
            arquivo.write(dados_criptografados)

        self.result_label.text = f"{nome_arquivo} criptografado com sucesso."

    def mudar_para_tela3(self, *args):
        self.manager.current = 'tela3'

class Tela3(Screen):
    def __init__(self, **kwargs):
        super(Tela3, self).__init__(**kwargs)
        layout = FloatLayout()

        label = Label(text="Digite o nome do arquivo abaixo:", size_hint=(None, None), size=(500, 50), pos_hint={"center_x": 0.5, "center_y": 0.6})
        layout.add_widget(label)

        self.text_input = TextInput(hint_text="Digite aqui", multiline=False, size_hint=(None, None), size=(500, 50), pos_hint={"center_x": 0.5, "center_y": 0.5})
        layout.add_widget(self.text_input)

        btn_funcao3 = Button(text="Descriptografar Arquivo", size_hint=(None, None), size=(500, 80), pos_hint={"center_x": 0.5, "center_y": 0.3})
        btn_funcao3.bind(on_release=self.descriptografar_arquivo)
        layout.add_widget(btn_funcao3)

        self.result_label = Label(text="", size_hint=(None, None), size=(500, 50), pos_hint={"center_x": 0.5, "center_y": 0.5})
        layout.add_widget(self.result_label)

        self.add_widget(layout)

    def carregar_chave(self):
        return open("chave.key", "rb").read()

    def descriptografar_arquivo(self, instance):
        nome_arquivo = self.text_input.text
        if not os.path.exists(nome_arquivo):
            self.result_label.text = "Arquivo não encontrado."
            return

        chave = self.carregar_chave()
        f = Fernet(chave)

        with open(nome_arquivo, "rb") as arquivo:
            dados_criptografados = arquivo.read()

        dados = f.decrypt(dados_criptografados)

        with open(nome_arquivo, "wb") as arquivo:
            arquivo.write(dados)

        self.result_label.text = f"{nome_arquivo} descriptografado com sucesso."

    def mudar_para_tela4(self, *args):
        self.manager.current = 'tela4'

class Tela4(Screen):
    def __init__(self, **kwargs):
        super(Tela4, self).__init__(**kwargs)
        layout = FloatLayout()

        btn = Button(text="Fechar", size_hint=(None, None), size=(250, 80), pos_hint={"center_x": 0.5, "center_y": 0.9})
        btn.bind(on_release=self.mudar_para_tela1)
        layout.add_widget(btn)

    def mudar_para_tela1(self, *args):
        self.manager.current = 'tela1'

class GerenciadorTelas(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Tela1(name='tela1'))
        sm.add_widget(Tela2(name='tela2'))
        sm.add_widget(Tela3(name='tela3'))
        sm.add_widget(Tela4(name='tela4'))
        return sm

if __name__ == '__main__':
    GerenciadorTelas().run()
