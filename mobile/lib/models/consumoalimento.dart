class ConsumoAlimento{
  int id,quantidade;
  String nome;
  double calorias,proteinas,carboidratos,gordura;
  
  ConsumoAlimento(
    {
      required this.id, 
      required this.quantidade, 
      required this.nome, 
      required this.calorias,
      required this.proteinas,
      required this.carboidratos,
      required this.gordura,
    }
  );
  factory ConsumoAlimento.fromJson(Map<String, dynamic> json){
       return ConsumoAlimento(
      id: json['id'],
      nome: json['nome'],
      quantidade: json['quantidade'],
      calorias: (json['calorias'] ?? 0).toDouble(),
      proteinas: (json['proteinas'] ?? 0).toDouble(),
      carboidratos: (json['carboidratos'] ?? 0).toDouble(),
      gordura: (json['gordura'] ?? 0).toDouble(),
    );
  }
   
}