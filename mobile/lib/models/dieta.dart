class Dieta {
   int calorias=0;
   double proteinas=0.0,carboidratos=0.0,gordura=0.0;
  Dieta();
  Dieta.fromJson(Map<String,dynamic>json){
  calorias=json['calorias']?.toInt();
  proteinas=json['proteinas']?.toDouble();
  carboidratos=json['carboidratos']?.toDouble();
  gordura=json['gordura']?.toDouble();
  }
  Map<String,dynamic> toJson(){
    return{
      'calorias':calorias,
      'proteinas':proteinas,
      'carboidratos':carboidratos,
      'gordura':gordura,
    }..removeWhere((key, value) => value == '' || value == 0 || value == 0.0,);
  }
}