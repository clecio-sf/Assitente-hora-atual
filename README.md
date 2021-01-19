# Assistente hora atual

Projeto desenvolvido para disciplina Inteligência Artificial, do Curso Superior em Sistemas
de Informação do Instituto Federal de Educação,
Ciência e Tecnologia da Bahia campus Vitória da
Conquista.

O intuito do projeto é o desenvolvimento de um assistente virtual capaz de obedecer a comandos de voz, para assim realizar a busca da hora atual em qualquer local do mundo.
<br><br>

# Tecnologias utilizadas

- ### [Python](https://www.python.org/downloads/)
- ### [Pip](https://pip.pypa.io/en/stable/installing/)
<br>

# Instalação e execução

1. Clonar o repositório

```bash
$ git clone https://github.com/clecio-sf/Assistente-hora-atual.git
```

2. Acessar o diretório

```bash
$ cd Assistente-hora-atual/
```

3. Instalar as dependências do projeto

```bash
$ pip3 install -r requirements.txt
```

4. Realizar o download do banco de dados utilizado

```bash
$ python donwnload.py
```

5. Executar o módulo hora atual

```bash
$ python hora\ atual.py
```

<br>

# Uso do assistente

Para que funcione de forma correta é necessário que o usuário primeiramente diga o nome do assistente, neste caso “Osvaldo”, após isso alguns padrões de comandos devem ser seguidos para que possa ser feita a pesquisa do horário pelo assistente, atualmente as seguintes formas de interação com o assistente são aceitas
<br><br>

| Comando                         | Resultado                                                   |
| ------------------------------- | ----------------------------------------------------------- |
| Osvaldo que horas são agora     | Sem informar um local será retornado a hora local no Brasil |
| Osvaldo que horas são em/no/na  | Passando ao final uma cidade, estado ou país                |
| Osvaldo qual o horário atual    | Sem informar um local será retornado a hora local no Brasil |
| Osvaldo qual o horário em/no/na | Passando ao final uma cidade, estado ou país                |

<br>

# Exemplos

- Osvaldo que horas são agora

- Osvaldo que horas são em São Paulo

- Osvaldo qual o horário atual

- Osvaldo qual o horário em Paris
