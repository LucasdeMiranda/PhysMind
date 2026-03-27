 import 'package:flutter/material.dart';
 import '../services/perfil_service.dart';

 class Homeusuariocomum extends StatelessWidget{
  @override
  const Homeusuariocomum({super.key});

  Widget _Meta (){
   final cor=Theme.of(context).colorScheme;
   return Container(
    padding: const EdgeInsets.all(16),
    decoration: BoxDecoration(
       color:  cor.surface,
       borderRadius: BorderRadius.circular(16),
       

    ),
    child:Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          "Meta Diária", style: TextStyle(fontSize: 18,fontWeight: FontWeight.bold),
          
        ),
        IconButton(onPressed: () {}, icon: const Icon(Icons.edit)),
      ],
      
    ),
      
   )
  }
  Widget  build(BuildContext context){
    return Scaffold(
     
    );
  }
 } 