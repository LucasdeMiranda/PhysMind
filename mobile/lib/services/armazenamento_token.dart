import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';//biblioteca pra salvar dados criptografados no celular

class ArmazenamentoToken {
  static const _armazenamento = FlutterSecureStorage();
  static Future<void> salvar({required String acesso, refresh}) async { // o _ é pra que somente esse arquivo acesse essa variável
    await _armazenamento.write(key: 'access', value: acesso);
    await _armazenamento.write(key: 'refresh', value: refresh);
  //async deixa usar await pr esperar pra depois continuar
  //static é usado para vc acessar a classe inteira não precisa acessar um objeto especifico e const é pra não mudar o valor
  }

  static Future<String?> getAcesso() async {// o future garante que espere a resposta da função e avisa
    return _armazenamento.read(key: 'access');
  }

  static Future<void> limpar() async {
    await _armazenamento.deleteAll();
    
  }
}
