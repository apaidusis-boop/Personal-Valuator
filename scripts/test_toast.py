"""Teste de notificação Windows Toast.

Mostra uma toast simulando um fato relevante. Clicar abre YouTube
(só para validar que o fluxo "notificação clicável → browser" funciona).

Uso:
    python scripts/test_toast.py
"""
from win11toast import toast

toast(
    "🔴 Fato Relevante — ITSA4",
    "Simulação: Itaúsa anuncia nova aquisição. Clica para abrir (teste: YouTube).",
    on_click="https://www.youtube.com",
    button={"activationType": "protocol", "arguments": "https://www.youtube.com", "content": "Abrir"},
    duration="long",
    app_id="Investment Intelligence",
)
print("[ok] toast enviada — verifica o canto inferior direito do ecrã")
