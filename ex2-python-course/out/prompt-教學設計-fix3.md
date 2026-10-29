# 教學設計 Agent：修正單（第 3 輪，N-2）
只改 `curriculum.md`。第 3、5 堂起手式加防呆：`if len(sys.argv) < 2 or not sys.argv[1].strip(): print('用法：python lesson3.py "$TMP"（TMP 不可為空）'); sys.exit(2)`，並在小活動說明「看到 IndexError 代表忘了加 "$TMP"」。練習仍恰好三題。完成後建立 `out/教學設計-fix3.done`。
