import 'dart:convert';//para converter dados tranforma map(dart) em texto json
import 'package:http/http.dart' as http; //biblioteca http(get,post,put,delete)

class AutenticacaoService {
  static const String baseurl='http://192.168.0.103:8000/api';


  Future<String?> cadastrar(String email, String senha) async{
    final resposta=await http.post(
      Uri.parse('$baseurl/cria-usuario/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'email':email,'senha':senha,
      }),
    );
    if(resposta.statusCode==201){
      return null;
    }
    else{
      final data=jsonDecode(resposta.body);
      return data['erro']??'erro desconhecido';

    }
     
  }

}
