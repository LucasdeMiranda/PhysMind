import 'dart:convert';//para converter dados tranforma map(dart) em texto json
import 'package:http/http.dart' as http; //biblioteca http(get,post,put,delete) implemnta o cliente abri conexão tcp cria requisição http envia headers e recebe resposta
import '../models/autenticacaoresposta.dart';
import 'armazenamento_token.dart';

class AutenticacaoService {
  static const String baseurl='http://192.168.0.103:8000/api';//ip do meu django necessario para acessar e validar 
  //static faz pertencer a classe toda não so o objeto
  //cost não muda
  Future<Autenticacaoresposta> cadastrar(String email, String senha) async{
    // no futuro vai devolver uma string(o erro no caso) ou null
    //async tranforma em assincrona e permite usar await e sempre retorna futre
    final resposta=await http.post(//cria uma requisição http
      Uri.parse('$baseurl/cria-usuario/'),
      headers: {'Content-Type': 'application/json'},//diz que é json 
      body: jsonEncode({
        'email':email,'senha':senha,//corpo do http
      }),
    );
     final data = jsonDecode(resposta.body);//pra pegar o status se existe ou não
    if(resposta.statusCode==201 ||resposta.statusCode==200){
      final auth= Autenticacaoresposta.fromJson(data);

      await ArmazenamentoToken.salvar(acesso: auth.acesso, refresh: auth.refresh,);
      //return Autenticacaoresposta.fromJson(data);//cadastro correu certo (novo ou existente)
      return auth;
    }

    else{
      throw Exception(data['erro'] ?? 'Erro desconhecido');

    }
     
  }

}
