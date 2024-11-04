import 'package:flutter/material.dart';
import 'presentation/home_page.dart';


void main() {
  runApp(const MyApp());
}
class MyApp extends StatefulWidget { // Делаем MyApp StatefulWidget
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  ThemeMode _themeMode = ThemeMode.system; // Состояние для themeMode

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      locale: const Locale('ru', 'RU'),
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: const ColorScheme.light(
          brightness:  Brightness.light,
          primary: Color(0xff33568A),
          // secondary: Color(0xff6200EE),
        ),
      ),
      darkTheme: ThemeData(
        useMaterial3: true,
        colorScheme: const ColorScheme.dark(
          brightness:  Brightness.dark,
          primary: Color(0xff33568A),
          // secondary: Color(0xff6200EE),
        ),
      ),
      themeMode: _themeMode, // Используем _themeMode
      //home: MedicinePage(medicineName: 'Парацетамол'),
      home: MyHomePage(onThemeChange: _changeTheme), // Передаем функцию изменения темы
    );
  }

  void _changeTheme(ThemeMode newThemeMode) {
    setState(() { // Обновляем состояние
      _themeMode = newThemeMode;
    });
  }
}




