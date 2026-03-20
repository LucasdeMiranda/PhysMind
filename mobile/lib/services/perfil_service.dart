import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/perfil.dart';
import 'armazenamento_token.dart';

class PerfilService {
  static const String baseurl= 'http://127.0.0.1:8000/api';//'http://192.168.0.103:8000/api';
  Future<Perfil> buscarPerfil() async{
  final token= await ArmazenamentoToken.getAcesso();
  final resposta=await http.get(
   Uri.parse('$baseurl/perfil/'),
   headers:{
    'Authorization':'Bearer $token',
   }
  );

  if(resposta.statusCode==200){
    return Perfil.fromJson(jsonDecode(resposta.body));
  }
  else{
    throw Exception('Erro ao buscar perfil');
  }
  }

  Future<void> atulizarPerfil(Map<String,dynamic> dados) async{
    final token= await ArmazenamentoToken.getAcesso();
    final resposta= await http.patch(
      Uri.parse('$baseurl/perfil/'),
       headers:{
    'Authorization':'Bearer $token',
    'Content-Type':'application/json',
   },
   body: jsonEncode(dados),
    );
    if(resposta.statusCode!=200){
      throw Exception('Erro ao atualiazar perfil');
    }
  }
}