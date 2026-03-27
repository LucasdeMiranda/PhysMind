import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/dieta.dart';
import 'armazenamento_token.dart';

class PerfilService {
  static const String baseurl= 'http://127.0.0.1:8000/api';//'http://192.168.0.103:8000/api';
  Future<Dieta> buscarDietaAtiva() async{
  final token= await ArmazenamentoToken.getAcesso();
  final resposta=await http.get(
   Uri.parse('$baseurl/dieta/'),
   headers:{
    'Authorization':'Bearer $token',
   }
  );

  if(resposta.statusCode==200){
    return Dieta.fromJson(jsonDecode(resposta.body));
  }
  else{
    throw Exception('Erro ao buscar dieta');
  }
  }

  Future<void> atualizarDietaAtiva (Map<String,dynamic> dados) async{
    final token= await ArmazenamentoToken.getAcesso();
    final resposta= await http.patch(
      Uri.parse('$baseurl/dieta/'),
       headers:{
    'Authorization':'Bearer $token',
    'Content-Type':'application/json',
   },
   body: jsonEncode(dados),
    );
    if(resposta.statusCode!=200){
      throw Exception('Erro ao atualiazar dieta');
    }
  }
}