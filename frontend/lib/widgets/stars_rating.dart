import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class StarsRating extends StatelessWidget{
  final String labelText;
  final int index; // Iindica a classificação (1 a 5 estrelas)
  final double starSpacing; // Espaçamento entre as estrelas

  const StarsRating({
    super.key,
    required this.labelText,
    required this.index,
    required this.starSpacing,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Text(
          labelText,
          style: GoogleFonts.workSans(
            fontSize: 18,
            fontWeight: FontWeight.w600,
            letterSpacing: .5,
            color: Color(0xFF0F4655),
          ),
        ),
        const SizedBox(width: 12),
        Row(
          children: List.generate(5, (i) {
            return Padding(
              padding: EdgeInsets.only(right: i < 4 ? starSpacing : 0),
              child: Icon(
                i < index ? Icons.star : Icons.star_border,
                size: 28,
                color: Color(0xFF0F4655),
              ),
            );
          }),
        ),
      ],
    );
  }
}