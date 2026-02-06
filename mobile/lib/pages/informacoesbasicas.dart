import 'package:flutter/material.dart';
import '../models/perfil.dart';   
 

class Informacoesbasicas extends StatefulWidget {
  const Informacoesbasicas({super.key});

@override//sobrescrever um metódo de uma classe 
  State<Informacoesbasicas> createState() => _InformacoesbasicasState(); 
}
 
 class _InformacoesbasicasState extends State<Informacoesbasicas>{
    final PageController _pageController=PageController();
    int pagatual=0;
    int totalpaginas=8;
    final  Perfil _perfil=Perfil();

    void Paginas(){
      if(pagatual<totalpaginas-1){
        
      }
    }
     
    
  }