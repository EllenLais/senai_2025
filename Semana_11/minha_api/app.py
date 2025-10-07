from flask import Flask, jsonify, request
from flask_cors import CORS

# Cria a instância da aplicação Flask
app = Flask(__name__)

# Habilita o CORS para permitir que a API seja acessada de outras origens
CORS(app)

# PASSO 2: Lista de produtos de exemplo
produtos = [
    {
        'id': 1,
        'nome': 'Notebook Dell',
        'preco': 2500.99,
        'estoque': 10
    },
    {
        'id': 2,
        'nome': 'Mouse Gamer',
        'preco': 150.50,
        'estoque': 25
    },
    {
        'id': 3,
        'nome': 'Teclado Mecânico',
        'preco': 300.00,
        'estoque': 15
    }
]

# PASSO 3: Adaptar as rotas para produtos

# Rota para obter todos os produtos (GET /produtos)
@app.route('/produtos', methods=['GET'])
def obter_produtos():
    return jsonify(produtos)

# Rota para obter um produto por ID (GET /produtos/<id>)
@app.route('/produtos/<int:produto_id>', methods=['GET'])
def obter_produto(produto_id):
    produto = next((p for p in produtos if p['id'] == produto_id), None)
    if produto is None:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    return jsonify(produto)

# Rota para criar um novo produto (POST /produtos)
@app.route('/produtos', methods=['POST'])
def criar_produto():
    # Verifica se a requisição tem JSON e se tem o campo 'nome'
    if not request.json or not 'nome' in request.json:
        return jsonify({'erro': 'A requisição deve ser em JSON e conter um nome'}), 400
    
    # Verifica todos os campos obrigatórios
    campos_obrigatorios = ['nome', 'preco', 'estoque']
    for campo in campos_obrigatorios:
        if campo not in request.json:
            return jsonify({'erro': f'Campo {campo} é obrigatório'}), 400
    
    # Cria o novo produto
    novo_produto = {
        'id': produtos[-1]['id'] + 1 if produtos else 1,
        'nome': request.json['nome'],
        'preco': float(request.json['preco']),
        'estoque': int(request.json['estoque'])
    }
    
    produtos.append(novo_produto)
    return jsonify(novo_produto), 201

# Rota para atualizar um produto (PUT /produtos/<id>)
@app.route('/produtos/<int:produto_id>', methods=['PUT'])
def atualizar_produto(produto_id):
    produto = next((p for p in produtos if p['id'] == produto_id), None)
    if produto is None:
        return jsonify({'erro': 'Produto não encontrado'}), 404

    # Atualiza apenas os campos que foram enviados
    produto['nome'] = request.json.get('nome', produto['nome'])
    produto['preco'] = float(request.json.get('preco', produto['preco']))
    produto['estoque'] = int(request.json.get('estoque', produto['estoque']))
    
    return jsonify(produto)

# Rota para deletar um produto (DELETE /produtos/<id>)
@app.route('/produtos/<int:produto_id>', methods=['DELETE'])
def deletar_produto(produto_id):
    produto_a_remover = next((p for p in produtos if p['id'] == produto_id), None)
    if produto_a_remover is None:
        return jsonify({'erro': 'Produto não encontrado'}), 404

    produtos.remove(produto_a_remover)
    return jsonify({'resultado': 'Produto deletado com sucesso'})

# DESAFIO EXTRA: Rota para comprar um produto
@app.route('/produtos/<int:produto_id>/comprar', methods=['POST'])
def comprar_produto(produto_id):
    produto = next((p for p in produtos if p['id'] == produto_id), None)
    if produto is None:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    
    if produto['estoque'] <= 0:
        return jsonify({'erro': 'Produto fora de estoque'}), 400
    
    # Diminui o estoque em 1 unidade
    produto['estoque'] -= 1
    return jsonify(produto)

# Executa a aplicação
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)