import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/refeicao.dart';
import '../models/consumoalimento.dart';
import 'armazenamento_token.dart';
// basicamente chamadas http para  em produção vamos usar https

class RefeicaoService {
  static const String baseurl = 'http://127.0.0.1:8000/api';
 // dando erro 400 ver depois e depurar
  Future<Refeicao> criaRefeicao(Map<String,dynamic> dados)async{
    final token= await ArmazenamentoToken.getAcesso();
    final resposta= await http.post(
      Uri.parse('$baseurl/refeicoes/'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: jsonEncode(dados),
    );
    if (resposta.statusCode == 201) {
      return Refeicao.fromJson(jsonDecode(resposta.body));
    }
    if(resposta.statusCode==400){
       print(" se entrou aqui ta o erro e como ta a resposta ${resposta.statusCode} - ${resposta.body}");
    }
    
    throw Exception('Erro ao criar refeição');
  }
  Future<List<Refeicao>> buscarRefeicao() async {
    final token = await ArmazenamentoToken.getAcesso();
    final resposta = await http.get(
      Uri.parse('$baseurl/refeicoes/'),
      headers: {'Authorization': 'Bearer $token'},
    );
    print("STATUS: ${resposta.statusCode}");
    print("BODY: ${resposta.body}");

    if (resposta.statusCode == 200) {
      final List lista = jsonDecode(resposta.body);
      return lista.map((e) => Refeicao.fromJson(e)).toList();
    } else {
      throw Exception('Erro ao buscar refeição');
    }
  }

  Future<void> atualizarRefeicao(int id, Map<String, dynamic> dados) async {
    final token = await ArmazenamentoToken.getAcesso();
    final resposta = await http.patch(
      Uri.parse('$baseurl/refeicoes/$id/'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: jsonEncode(dados),
    );
    if (resposta.statusCode != 200) {
      throw Exception('Erro ao atualiazar perfil');
    }
  }

  Future<void> deletarRefeicao(int id) async {
    final token = await ArmazenamentoToken.getAcesso();
    final resposta = await http.delete(
      Uri.parse('$baseurl/refeicoes/$id/'),
      headers: {'Authorization': 'Bearer $token'},
    );

    if (resposta.statusCode != 204) {
      throw Exception('Erro ao deletar refeição');
    }
  }

  Future<ConsumoAlimento> adicionarAlimento(ConsumoAlimento consumo) async {
    final token = await ArmazenamentoToken.getAcesso();

    final resposta = await http.post(
      Uri.parse('$baseurl/consumos/'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: jsonEncode(consumo.toJsonCriacao()),
    );

    if (resposta.statusCode == 201) {
      return ConsumoAlimento.fromJson(jsonDecode(resposta.body));
    }

    throw Exception('Erro ao adicionar alimento');
  }
}
