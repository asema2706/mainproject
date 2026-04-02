import 'dart:io';
import 'dart:math';
import 'package:characters/characters.dart';

enum Mood {
  happy,
  excited,
  calm,
  sad,
  angry,
  surprised,
}

extension MoodDetails on Mood {
  String get emoji {
    switch (this) {
      case Mood.happy:
        return '\u{1F600}'; // 😀  широкая улыбка
      case Mood.excited:
        return '\u{1F60E}'; // 😎  крутой, взволнованный
      case Mood.calm:
        return '\u{1F60C}'; // 😌  облегчение, спокойствие
      case Mood.sad:
        return '\u{1F622}'; // 😢 слеза, грусть
      case Mood.angry:
        return '\u{1F621}'; // 😡 злость
      case Mood.surprised:
        return '\u{1F632}'; // 😲 удивление
    }
  }

  /// Текстовое описание настроения на русском
  String get description {
    switch (this) {
      case Mood.happy:
        return 'радостный';
      case Mood.excited:
        return 'взволнованный';
      case Mood.calm:
        return 'спокойный';
      case Mood.sad:
        return 'грустный';
      case Mood.angry:
        return 'злой';
      case Mood.surprised:
        return 'удивлённый';
    }
  }

  /// Уровень энергии от 1 до 10
  int get energy {
    switch (this) {
      case Mood.happy:
        return 8;
      case Mood.excited:
        return 9;
      case Mood.calm:
        return 5;
      case Mood.sad:
        return 3;
      case Mood.angry:
        return 7;
      case Mood.surprised:
        return 6;
    }
  }
}

String codePointToUnicode(int codePoint) {
  final hex = codePoint.toRadixString(16).toUpperCase().padLeft(4, '0');
  return 'U+$hex';
}

void main() {

  stdout.write('Введите ваше имя: ');
  final name = stdin.readLineSync(encoding: systemEncoding)?.trim() ?? 'Пользователь';

  print('');
  print('Генерируем случайное настроение...');
  print('');

  final random = Random();
  final mood = Mood.values[random.nextInt(Mood.values.length)];

  print(
    'Привет, $name! '
    'Твое настроение: ${mood.emoji} ${mood.description} '
    '(энергия: ${mood.energy}/10)',
  );
  print('');

  final emojiCodePoint = mood.emoji.runes.first;
  print('Юникод вашего эмодзи: ${codePointToUnicode(emojiCodePoint)}');
  print('');

  stdout.write('Хотите просмотреть сложные эмодзи? (да/нет): ');
  final answer = stdin.readLineSync(encoding: systemEncoding)?.toLowerCase().trim() ?? 'нет';

  if (answer == 'да' || answer == 'yes') {
    print('');
    stdout.write('Введите комбинацию эмодзи: ');
    final emojiStr = stdin.readLineSync(encoding: systemEncoding) ?? '';

    print('');
    print('Анализ строки "$emojiStr":');
    print('- 16-битных единиц: ${emojiStr.length}');
    print('- Кодовых точек: ${emojiStr.runes.length}');
    print('- Реальных символов: ${emojiStr.characters.length}');
    print('');

    print('Подробный вывод юникода:');
    int index = 1;
    for (final codePoint in emojiStr.runes) {
      final char = String.fromCharCode(codePoint);
      print('Символ $index: $char → ${codePointToUnicode(codePoint)}');
      index++;
    }
  }

  print('');
  print('Спасибо, приходите снова!');
}
