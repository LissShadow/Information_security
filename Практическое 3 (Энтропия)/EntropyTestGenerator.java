import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class EntropyTestGenerator {

    public static void main(String[] args) {
        // Папка для тестовых файлов
        File outputDir = new File("entropy_tests");
        if (!outputDir.exists()) {
            outputDir.mkdir();
        }

        // 1. Файл с одним повторяющимся символом
        generateAndAnalyze(
                new File(outputDir, "single_char.txt"),
                "Один символ ('X')",
                () -> 'X');

        // 2. Файл из случайных 0 и 1
        generateAndAnalyze(
                new File(outputDir, "random_bits.txt"),
                "Случайные биты (0 и 1)",
                () -> (char) ('0' + new Random().nextInt(2)));

        // 3. Файл из случайных байтов (0–255)
        generateAndAnalyze(
                new File(outputDir, "random_bytes.txt"),
                "Случайные байты (0–255)",
                () -> (char) (new Random().nextInt(256)));

        // 4. Файл из случайных букв a–z
        generateAndAnalyze(
                new File(outputDir, "random_letters.txt"),
                "Случайные буквы (a–z)",
                () -> (char) ('a' + new Random().nextInt(26)));
    }

    // Генерирует файл, заполняет его по supplier, затем анализирует
    private static void generateAndAnalyze(File file, String description, CharSupplier charSupplier) {
        final int FILE_SIZE = 10_000;

        try (FileOutputStream fos = new FileOutputStream(file);
                OutputStreamWriter osw = new OutputStreamWriter(fos, StandardCharsets.UTF_8)) {

            for (int i = 0; i < FILE_SIZE; i++) {
                osw.write(charSupplier.getAsChar());
            }
        } catch (IOException e) {
            System.err.println("Ошибка при создании файла " + file.getName() + ": " + e.getMessage());
            return;
        }

        analyzeFile(file);
    }

    // Анализирует файл: читает, считает частоты, вычисляет энтропию
    private static void analyzeFile(File file) {
        Map<Character, Integer> freqMap = new TreeMap<>();
        int total = 0;

        try (BufferedReader br = new BufferedReader(
                new InputStreamReader(
                        new FileInputStream(file),
                        StandardCharsets.UTF_8))) {

            int code;
            while ((code = br.read()) != -1) {
                char ch = (char) code;
                freqMap.put(ch, freqMap.getOrDefault(ch, 0) + 1);
                total++;
            }
        } catch (IOException e) {
            System.err.println("Ошибка при чтении файла " + file.getName() + ": " + e.getMessage());
            return;
        }

        if (total == 0) {
            System.out.println("Файл " + file.getName() + " пуст.");
            return;
        }

        // Вывод заголовка
        System.out.println("\n=== АНАЛИЗ ФАЙЛА: " + file.getName() + " ===");
        System.out.println("Описание: " + getDescription(file.getName()));
        System.out.println("Размер: " + total + " символов");

        // Выводим частоты (ограничим до 20 строк для читаемости)
        System.out.println("\nЧастоты символов (первые 20):");
        int count = 0;
        for (Map.Entry<Character, Integer> entry : freqMap.entrySet()) {
            if (count >= 20)
                break;
            char ch = entry.getKey();
            int freq = entry.getValue();
            String repr = getCharRepresentation(ch);
            System.out.printf("  %-12s : %d\n", repr, freq);
            count++;
        }
        if (freqMap.size() > 20) {
            System.out.println("  ... и ещё " + (freqMap.size() - 20) + " символов");
        }

        // Вычисление энтропии
        double entropy = 0.0;
        for (int freq : freqMap.values()) {
            double p = (double) freq / total;
            entropy -= p * Math.log(p) / Math.log(2); // log2(p)
        }

        System.out.printf("\nЭнтропия: %.4f бит/символ\n", entropy);
        System.out.println(new String(new char[50]).replace("\0", "-"));
    }

    // Возвращает описание типа файла по имени (классический switch)
    private static String getDescription(String filename) {
        if ("single_char.txt".equals(filename)) {
            return "Один повторяющийся символ ('X')";
        } else if ("random_bits.txt".equals(filename)) {
            return "Случайные биты: 0 и 1";
        } else if ("random_bytes.txt".equals(filename)) {
            return "Случайные байты: 0–255 (как символы)";
        } else if ("random_letters.txt".equals(filename)) {
            return "Случайные строчные буквы: a–z";
        } else {
            return "Неизвестный тип";
        }
    }

    // Представление символа для вывода (классический switch)
    private static String getCharRepresentation(char ch) {
        switch (ch) {
            case '\n':
                return "\\n";
            case '\r':
                return "\\r";
            case '\t':
                return "\\t";
            case ' ':
                return "' '";
            default:
                if (ch < 32 || ch > 126) {
                    return String.format("0x%02X", (int) ch);
                } else {
                    return String.valueOf(ch);
                }
        }
    }

    // Интерфейс для генерации символа
    @FunctionalInterface
    private interface CharSupplier {
        char getAsChar();
    }
}
