import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class CustomDateBox extends StatelessWidget {
  final String labelText;
  final String hintText;
  final double height;
  final double width;
  final TextEditingController controller;
  final VoidCallback onClickIcon;

  const CustomDateBox({
    super.key,
    required this.labelText,
    required this.hintText,
    required this.height,
    required this.width,
    required this.controller,
    required this.onClickIcon,
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
        readOnly: true,
        style: textStyle,
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
            color: Colors.black
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

// FUNÇÃO PARA EXIBIR O CALENDÁRIO
Future<void> selectDate(BuildContext context, TextEditingController controller) async {
  final DateTime? pickedDate = await showDatePicker(
    context: context,
    initialDate: DateTime.now(),
    firstDate: DateTime(2015), // Data mínima permitida
    lastDate: DateTime(2030), // Data máxima permitida
  );

  if (pickedDate !=null) {
    controller.text = "${pickedDate.day}/${pickedDate.month}/${pickedDate.year}";
  }
}

// FUNÇÃO PARA FORMATAR A DATA
String formatDate(DateTime date) {
  return  "${date.day.toString().padLeft(2, '0')}/"
          "${date.month.toString().padLeft(2, '0')}/"
          "${date.year}";
}