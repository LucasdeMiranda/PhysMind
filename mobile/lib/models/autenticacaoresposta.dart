class Autenticacaoresposta {
  final String status;
  final String? tipoUsuario;//se existe retorna se não retorna null
  final String acesso;
  final String refresh;
  Autenticacaoresposta({
   required this.status,this.tipoUsuario, required this.acesso, required this.refresh,
  });

  factory Autenticacaoresposta.fromJson(Map<String,dynamic>json){//converte pra json basicamente tudo a gente tem que converter pra json
  //e eu pensando que não ia ter que mexer mais com isso era ruim demais nisso.
    return Autenticacaoresposta(status: json['status'],tipoUsuario: json['tipo_usuario'], acesso: json['access'],refresh: json['refresh'],);
  }
}
