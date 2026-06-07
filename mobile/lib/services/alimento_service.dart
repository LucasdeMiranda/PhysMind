import 'dart:convert';
import 'dart:ui_web';
import 'package:http/http.dart' as http;
import 'armazenamento_token.dart';
import '../models/alimento.dart';

class AlimentoService {
  static const String baseurl='http://127.0.0.1:8000/api'; //'http://192.168.0.103:8000/api';
  Future<List <Alimento>> buscarAlimentos(String subnome) async{
    final token=  await ArmazenamentoToken.getAcesso();
    final resposta= await http.get(
      Uri.parse('$baseurl/alimentos/?search=$subnome'),
      headers: {'Authorization': 'Bearer $token'},
    );
    if(resposta.statusCode==200){
      List lista= jsonDecode(resposta.body);
      return lista.map((e) => Alimento.fromJson(e)).toList();
    }
    else{
       throw Exception('Erro ao buscar refeição');
    }

  }
}