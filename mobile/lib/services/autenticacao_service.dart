import 'dart:convert';//para converter dados tranforma map(dart) em texto json
import 'package:http/http.dart' as http; //biblioteca http(get,post,put,delete) implemnta o cliente abri conexão tcp cria requisição http envia headers e recebe resposta

class AutenticacaoService {
  static const String baseurl='http://192.168.0.103:8000/api';//ip do meu django necessario para acessar e validar 
  //static faz pertencer a classe toda não so o objeto
  //cost não muda
  Future<String?> cadastrar(String email, String senha) async{
    // no futuro vai devolver uma string(o erro no caso) ou null
    //async tranforma em assincrona e permite usar await e sempre retorna futre
    final resposta=await http.post(//cria uma requisição http
      Uri.parse('$baseurl/cria-usuario/'),
      headers: {'Content-Type': 'application/json'},//diz que é json 
      body: jsonEncode({
        'email':email,'senha':senha,//corpo do http
      }),
    );
    if(resposta.statusCode==201 ||resposta.statusCode==200){
      return null;//cadastro correu certo
    }

    else{
      final data=jsonDecode(resposta.body);//catura o erro
      return data['erro']??'erro desconhecido';

    }
     
  }

}
