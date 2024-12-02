import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

// CLASSE DE CRIAÇÃO DO CHECKBOX
class CheckBox extends StatefulWidget {
  final String label;
  final bool enable;

  const CheckBox({
    super.key,
    required this.label,
    required this.enable,
  });

  @override
  _CheckBoxState createState() => _CheckBoxState();

}

// CLASSE DO ESTADO DO CHECKBOX
class _CheckBoxState extends State<CheckBox> {
  late bool enable;

  @override
  void initState() { // Inicializa o estado com o valor recebido do widget pai
    super.initState();
    enable = widget.enable;
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        GestureDetector(
          onTap: () {
            setState(() {
              enable = !enable; // Altera o estado ao clicar
            });
          },
          child: Container(
            width: 20,
            height: 20,
            decoration: BoxDecoration(
              color: enable ? Color(0xFF0F4655) : Colors.transparent,
              border: Border.all(
                color: enable ? Color(0xFF0F4655) : Color(0xFF6195A4),
                width: 2,
              ),
              borderRadius: BorderRadius.circular(2),
            ),
            child: enable ? Icon(Icons.check, size: 16, color: Colors.white) : null,
          ),
        ),
        const SizedBox(width: 6),
        Text(
          widget.label,
          style: GoogleFonts.workSans(
            fontSize: 18,
            fontWeight: FontWeight.w600,
            letterSpacing: 0.5,
            color: enable ? Color(0xFF0F4655) : Color(0xFF6195A4),
          ),
        ),
      ],
    );
  }
}