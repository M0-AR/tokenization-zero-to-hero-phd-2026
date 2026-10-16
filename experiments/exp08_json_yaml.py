"""EXP-08: JSON vs YAML density (video claim: YAML wins token economy)."""
import tiktoken

obj_json = '{"name": "tokphd", "langs": ["en", "ko", "ar"], "n": 12345, "ok": true}'
obj_yaml = 'name: tokphd\nlangs:\n- en\n- ko\n- ar\nn: 12345\nok: true\n'
for enc_name in ["gpt2", "cl100k_base", "o200k_base"]:
    enc = tiktoken.get_encoding(enc_name)
    j, y = len(enc.encode(obj_json)), len(enc.encode(obj_yaml))
    print(f"{enc_name}: json={j} yaml={y} saving={(j-y)/j*100:.1f}%")
print("EXP-08 OK")
