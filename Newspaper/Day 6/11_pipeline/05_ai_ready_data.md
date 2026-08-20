# 11.5 AI-ready data

Một dataset sẵn sàng cho AI phải có:

- timestamp và sampling contract rõ;
- không còn reserved marker ngoài policy;
- missing/outlier đã được xử lý hoặc gắn cờ;
- feature scale nhất quán;
- tensor shape và target horizon rõ;
- train/validation/test không leakage;
- metadata về mọi transform;
- quality report và provenance.

## Acceptance checks

```text
schema valid
→ temporal order valid
→ finite values
→ expected shape
→ target aligned
→ no future-derived feature
→ reproducible parameters
```

“AI-ready” không có nghĩa mọi giá trị đều là observation thật. Nó nghĩa model có thể nhận input với semantics, shape, scale và provenance được kiểm soát.