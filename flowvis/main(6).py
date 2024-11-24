from conexao_bd import conexao_fechar, conexao_abrir

def usuarioListar(con):
    cursor = con.cursor()
    sql = "SELECT * FROM usuarios"
    # Criando o cursor com a opção de retorno como dicionário   
    cursor = con.cursor(dictionary=True)
    cursor.execute(sql)

    for (registro) in cursor:
        print(registro['usuario_nome'] + " - "+ registro['usuario_email'])

    cursor.close()
    #con.commit()    #mesma coisa q editar e não salvar


def usuarioInserir(con, usuario_nome, usuario_user, usuario_email, usuario_senha):
     cursor = con.cursor()
     sql = "INSERT INTO usuarios (usuario_nome, usuario_user, usuario_email, usuario_senha) VALUES (%s, %s, %s, %s)"
     cursor.execute(sql, (usuario_nome, usuario_user, usuario_email, usuario_senha))
     con.commit() 
     cursor.close()
        

def main():
    con = conexao_abrir("localhost", "root", "admin", "flowvis")
    
    usuarioInserir(con, "rodrigo", "rodrigobaesa","rodrigobaesa@gmail.com", "senha123")
    usuarioListar(con)

    conexao_fechar(con)

if __name__ == "__main__":
	main()
     