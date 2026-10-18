# ⏳ Pomodoro Timer com Persistência em JSON

Uma aplicação de gerenciamento de tempo baseada no método Pomodoro, desenvolvida em Python com interface gráfica Tkinter.
O sistema auxilia no acompanhamento do tempo de estudo e registra automaticamente o progresso diário em um arquivo de dados persistente em formato JSON.

---

## 🚀 Funcionalidades

- **Ciclos Pré-configurados:** 50 minutos de estudo e 10 minutos de pausa para descanso.
- **Interface Gráfica Intuitiva:** Desenvolvida em Tkinter com suporte a temas modernos em estilo dark mode.
- **Controle Completo:** Botões para Iniciar, Pausar e Resetar o temporizador.
- **Persistência de Dados (JSON):** Salvamento automático de cada ciclo concluído com data (`YYYY-MM-DD`), contagem de ciclos e minutos acumulados.
- **Painel de Estatísticas:** Exibição em tempo real do progresso diário e do total de dias registrados no histórico.
- **Alertas Sonoros e Notificações:** Avisos visuais em pop-up e efeito sonoro do sistema ao alternar de fase.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** [Python 3.x](https://www.python.org/)
- **Interface Gráfica:** Tkinter
- **Persistência:** Módulo `json` integrado
- **Manipulação de Datas:** Módulo `datetime` integrado

---

## 📦 Estrutura do Projeto

```text
├── main.py              # Código principal da aplicação
├── historico_estudos.json   # Base de dados em JSON (gerada automaticamente)
└── README.md                # Documentação do repositório
```
## 📄 Formato do Arquivo JSON

- Os dados de progresso são salvos estruturados por data da seguinte forma:
```text
JSON {
    "2026-10-18": {
        "ciclos": 3,
        "minutos_totais": 150
    },
    "2026-10-19": {
        "ciclos": 2,
        "minutos_totais": 100
    }
}
```
## 📄 Licença
- Este projeto é de uso livre e está sob a licença MIT.