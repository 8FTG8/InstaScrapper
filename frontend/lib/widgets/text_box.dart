import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class CustomTextBox extends StatelessWidget {
  final String labelText;
  final String hintText;
  final double height;
  final double width;
  
  const CustomTextBox({
    super.key,
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
        style: textStyle,
        decoration: InputDecoration( // Configura a aparência do campo de texto (rótulos, bordas, dicas, ícones)
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
            color: Colors.black),
          border: OutlineInputBorder( // Cria uma borda completa e personalizável ao redor do campo de texto
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
