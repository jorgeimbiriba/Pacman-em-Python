Projeto Final para a Matéria de Lógica de Programação Avançada (LPA) - 2025

# Pac-Man (Pygame)

Este é um jogo simples do clássico Pac-Man desenvolvido em Python utilizando a biblioteca Pygame. O objetivo é comer todas as pílulas espalhadas pelo labirinto enquanto desvia dos fantasmas. Coma as pílulas de poder para ter a chance de comer os fantasmas por um curto período!

## Funcionalidades Atuais

* Movimento do Pac-Man com animação de boca.
* Consumo de pílulas e pílulas de poder.
* Sistema de pontuação.
* Fantasmas com comportamento de perseguição (Chase) e dispersão (Scatter).
* Fantasmas ficam assustados e vulneráveis após o Pac-Man comer uma pílula de poder.
* Mecânica de teletransporte através de túneis laterais.
* Sistema de vidas e Game Over.
* Reinício de nível ao coletar todas as pílulas ou ao perder uma vida.
* Lançamento sequencial de fantasmas da casa.

## Como Rodar o Jogo

Você pode rodar este jogo de duas maneiras principais:

### Opção 1: Rodar via Terminal (Recomendado para Usuários Finais)

Esta é a forma mais comum para quem não usa um ambiente de desenvolvimento integrado (IDE).

1.  **Instale o Python:**
    * Vá para o site oficial do Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)
    * Baixe e execute o instalador para o seu sistema operacional (Windows, macOS, Linux).
    * **IMPORTANTE (para Windows):** Durante a instalação, certifique-se de marcar a opção "Add Python to PATH" ou "Adicionar Python ao PATH". Isso facilita a execução de comandos Python no terminal.

2.  **Instale a Biblioteca Pygame:**
    * Abra o seu terminal ou Prompt de Comando (no Windows, procure por "cmd" no menu Iniciar).
    * Digite o seguinte comando e pressione `Enter`:
        ```bash
        pip install pygame
        ```
    * Aguarde a conclusão da instalação.

3.  **Baixe o Código do Jogo:**
    * Baixe o arquivo `pacman.py` para o seu computador. Você pode fazer isso clonando este repositório ou baixando o arquivo individualmente.

4.  **Execute o Jogo:**
    * No terminal ou Prompt de Comando, navegue até a pasta onde você salvou o arquivo `pacman.py` usando o comando `cd`. Por exemplo, se você salvou na pasta `Downloads`:
        ```bash
        cd Downloads
        ```
    * Depois de navegar para a pasta correta, execute o jogo com o seguinte comando:
        ```bash
        python pacman.py
        ```
    * O jogo Pac-Man deverá ser iniciado em uma nova janela.

### Opção 2: Rodar via PyCharm (Recomendado para Desenvolvedores)

Se você tem o PyCharm (ou outra IDE Python) instalado, você pode rodar o jogo diretamente de lá.

1.  **Clone o Repositório ou Abra o Projeto:**
    * Abra o PyCharm.
    * Se você clonou o repositório, vá em `File > Open` e selecione a pasta do projeto.
    * Se você tem o arquivo `pacman.py` isolado, crie um novo projeto (`File > New Project`), e adicione o `pacman.py` a ele.

2.  **Instale o Pygame no Ambiente do Projeto:**
    * No PyCharm, vá em `File > Settings` (ou `PyCharm > Preferences` no macOS).
    * Navegue até `Project: [Seu_Nome_do_Projeto] > Python Interpreter`.
    * Clique no botão `+` (Install) no canto superior direito.
    * Procure por `pygame`, selecione-o e clique em `Install Package`.
    * Aguarde a instalação e clique em `OK`.

3.  **Execute o Arquivo:**
    * Abra o arquivo `pacman.py` no editor do PyCharm.
    * Clique com o botão direito em qualquer lugar do código e selecione `Run 'pacman'`.
    * Alternativamente, clique no botão verde de "play" na barra superior.

## Controles

* **Setas do Teclado (↑, ↓, ←, →):** Mover o Pac-Man.
* **ENTER (no Game Over):** Reiniciar o jogo.

---
