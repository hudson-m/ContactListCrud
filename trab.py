import pyodbc
from flask import Flask

app = Flask(__name__)

@app.route("/api/getContatos")
def read(conn):
    print("Read")
    cursor = conn.cursor()
    cursor.execute('''SELECT 
                        nome,
                        dataNascimento,
                        regiao,
                        ddd,
                        t.numero,
                        rua,
                        e.numero,
                        complemento,
                        CEP,
                        cidade,
                        estado 
                        FROM Pessoa p 
                        INNER JOIN Telefone t ON p.idPessoa = t.fkPessoa 
                        INNER JOIN Endereco e ON e.fkPessoa = p.idPessoa;''')
    for row in cursor:
        print(f'row = {row}')
    print()

@app.route("/create")
def create(conn,nome,dataNascimento,regiao,ddd,numero,rua,numeroEndereco,complemento,cep,cidade,estado):
    print("Create")
    cursor = conn.cursor()
    cursor.execute(
        'insert into Pessoa(nome,dataNascimento) values (?,?)',
        (nome, dataNascimento)
    )
    cursor.execute(
        'insert into Telefone(regiao,ddd,numero,fkPessoa) values (?,?,?,(SELECT top(1) idPessoa FROM Pessoa Order by idPessoa desc))',
        (regiao, ddd, numero)
    )
    cursor.execute(
        'insert into Endereco(rua,numero,complemento,CEP,cidade,estado,fkPessoa) values (?,?,?,?,?,?,(SELECT top(1) idPessoa FROM Pessoa Order by idPessoa desc))',
        (rua, numeroEndereco, complemento, cep,cidade,estado)
    )
    conn.commit()
    read(conn)

@app.route("/update")
def update(conn):
    print("Update")
    cursor = conn.cursor()
    cursor.execute(
        'insert into Pessoa(nome,dataNascimento) values (?,?)',
        ('batatao', '10/10/1915')
    )
    cursor.execute(
        'insert into Telefone(regiao,ddd,numero) values (?,?,?)',
        (55, 42, 999999989)
    )
    cursor.execute(
        'insert into Endereco(rua,numero,complemento,CEP,cidade,estado) values (?,?,?,?,?,?)',
        ('rua batatao', 1234, 'num sei', 12345678, 'curitiba', 'parana')
    )
    conn.commit()
    read(conn)

@app.route("/delete")
def delete(conn):
    print("Delete")
    cursor = conn.cursor()
    cursor.execute(
        'delete from Pessoa where nome = ?;',
        ('batatao')
    )
    conn.commit()
    read(conn)


def createTable(conn):
    print("Create Tables")
    cursor = conn.cursor()
    cursor.execute(
        '''DROP TABLE IF EXISTS dbo.Pessoa 
            CREATE TABLE dbo.Pessoa
            (
            idPessoa		INT IDENTITY PRIMARY KEY,
            nome			VARCHAR(255),
            dataNascimento DATE
            );'''

        '''DROP TABLE IF EXISTS dbo.Telefone
            CREATE TABLE dbo.Telefone
            (
            idTelefone INT NOT NULL IDENTITY PRIMARY KEY, 
            regiao		int NOT NULL, 
            ddd		int NOT NULL, 
            numero		int NOT NULL,
            fkPessoa	int FOREIGN KEY REFERENCES Pessoa(idPessoa)  
            ON DELETE CASCADE ON UPDATE CASCADE
            );'''

        '''DROP TABLE IF EXISTS dbo.Endereco 
            CREATE TABLE dbo.Endereco
            (
            idEndereco  INT NOT NULL IDENTITY PRIMARY KEY, 
            rua		 VARCHAR(MAX) NOT NULL, 
            numero		 VARCHAR(MAX) NOT NULL, 
            complemento VARCHAR(MAX), 
            CEP		 int NOT NULL, 
            cidade		 VARCHAR(MAX) NOT NULL, 
            estado		 VARCHAR(MAX) NOT NULL,
            fkPessoa	int FOREIGN KEY REFERENCES Pessoa(idPessoa)  
            ON DELETE CASCADE ON UPDATE CASCADE
            );'''
    )
    conn.commit()


conn = pyodbc.connect(
    "Driver={SQL Server Native Client 11.0};"
    "Server=.\MSSQLSERVER2;"
    "Database=trab;"
    "Trusted_Connection=yes;", autocommit=True
)

#createTable(conn)
#read(conn)
#create(conn)
#update(conn)
#delete(conn)

conn.close()
