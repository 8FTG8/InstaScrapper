import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class CustomTextBox extends StatelessWidget {
  final TextEditingController controller;
  final GlobalKey<FormState> formKey;
  final String labelText;
  final String hintText;
  final double height;
  final double width;
  
  const CustomTextBox({
    super.key,
    required this.controller,
    required this.formKey,
    required this.labelText,
    required this.hintText,
    required this.height,
    required this.width,
  });

  @override
  Widget build(BuildContext context) {
    final textStyle = GoogleFonts.workSans(
      fontSize: 18,
      fontWeight: FontWeight.w500,
      color: Colors.black
    );

    return SizedBox(
      height: height,
      width: width,
      child: TextFormField(
        controller: controller,
        style: textStyle,
        validator: (value) => validateInstagram(value ?? ''),
        onFieldSubmitted: (value) {
          if (formKey.currentState?.validate() ?? false) {
            print("Campo válido: $value");
          } else {
            print('Campo inválido');
          }
        },
        decoration: InputDecoration(
          labelText: labelText,
          labelStyle: GoogleFonts.workSans(
            fontSize: 16,
            fontWeight: FontWeight.w600,
            letterSpacing: .5,
            color: Color(0xFF0F4655),
            ),
          hintText: hintText,
          hintStyle: GoogleFonts.workSans(
            fontSize: 16,
            fontWeight: FontWeight.w500,
            color: Colors.black,
            ),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: BorderSide(
              width: 5.0,
              color: Color(0xFF0F4655),
            ),
          ),
        ),
      ),
    );
  }
}

// FUNÇÃO DE VALIDAÇÕES: USERNAME + PROFILE LINK
String? validateInstagram(String value) {
  final regExp = RegExp( // Regex para validar link de perfil ou nome de usuário
    //r'^(https?:\/\/)?(www\.)?instagram\.com\/[a-zA-Z0-9._]{1,30}\/?(\?[\w=&]+)?$',
    r'^(https?:\/\/)?(www\.)?instagram\.com\/[a-zA-Z0-9._]{1,30}\/?(\?[\w=&]+)?$|^[a-zA-Z0-9._]{1,30}$',

  );

  if (value.isEmpty) {
    return 'Este campo é obrigatório.';
  } else if (!regExp.hasMatch(value)) {
    return 'Insira um link ou nome de perfil válido!';
  }
  return null; // Válido
}