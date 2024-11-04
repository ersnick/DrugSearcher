import 'package:flutter/material.dart';
import 'search_bar.dart';
import 'side_menu.dart';

class MyHomePage extends StatelessWidget {
  final Function(ThemeMode) onThemeChange; // Функция изменения темы

  const MyHomePage({super.key, required this.onThemeChange});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        title: const Text('ЧЕ ЗЫРИШЬ'),
        backgroundColor: Theme.of(context).colorScheme.primary,
        actions: [
          ThemeButton(onThemeChange: onThemeChange), // Передаем функцию изменения темы
        ],
      ),
      body: const App(),
      drawer: const MyDrawer(),
    );
  }
}

class ThemeButton extends StatefulWidget {
  final Function(ThemeMode) onThemeChange; // Функция изменения темы

  const ThemeButton({super.key, required this.onThemeChange});

  @override
  State<ThemeButton> createState() => _ThemeButtonState();
}

class _ThemeButtonState extends State<ThemeButton> {
  bool isDark = false; // Переменная для отслеживания режима

  @override
  Widget build(BuildContext context) {
    return Tooltip(
      message: 'Change brightness mode',
      child: IconButton(
        onPressed: () {
          setState(() {
            isDark = !isDark;
            widget.onThemeChange(isDark ? ThemeMode.dark : ThemeMode.light); // Изменяем themeMode в MyApp
          });
        },
        icon: Icon(
          isDark ? Icons.light_mode : Icons.dark_mode,
        ),
      ),
    );
  }
}

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    return const Padding(
      padding: const EdgeInsets.all(8.0),
      child: SearchBarDrug(),
    );
  }
}