class Usuario {
  String nome='',objetivo='',tipousuario='',sexo='';
  int idade=0,altura=0;
  double cintura=0.0,pescoco=0.0;

  Usuario.fromJson(Map<String,dynamic> json){
    nome=json['nome']??'';
    idade = json['idade'] ?? 0;
    tipousuario = json['tipo_usuario'] ?? '';
    sexo= json['sexo'];
    objetivo=json['objetivo'];
    cintura= json['cintura']?.toDouble();
    pescoco= json['pescoco']?.toDouble();
  }
  
    Map<String, dynamic> toJson() {
    return {
      'nome': nome,
      'idade': idade,
      'altura': altura,
      'tipo_usuario': tipousuario,
      'sexo': sexo,
      'objetivo': objetivo,
      'cintura': cintura,
      'pescoco': pescoco,
    }..removeWhere((key, value) => value == '' || value == 0 || value == 0.0,); // esse remove so manda o que foi prenchido 
  }
}
