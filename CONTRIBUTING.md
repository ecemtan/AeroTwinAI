# Katkı Kuralları (Git, Branch, Pull Request)

## Dallar

- `main` her zaman çalışır durumdadır. **Doğrudan `main`'e push yapılmaz.**
- Her iş kendi dalında yapılır:

| Önek | Kullanım | Örnek |
|---|---|---|
| `feature/` | Yeni özellik | `feature/backend-simulation-runs` |
| `fix/` | Hata düzeltme | `fix/frontend-health-error` |
| `docs/` | Yalnızca doküman | `docs/setup-openvsp` |
| `test/` | Yalnızca test | `test/simulation-turn-scenario` |

```powershell
git switch main
git pull
git switch -c feature/<alan>-<konu>
```

Dalınızı güncel tutmak için `git merge main` kullanın. `rebase` ve force push yapmayın.

## Commit mesajları

Biçim: `<tür>(<alan>): <kısa açıklama>`. Türler: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`.

```text
feat(backend): add POST /api/simulation/runs
test(simulation): cover coordinated turn heading change
```

Küçük ve anlamlı commit'ler atın. Oluşturulan dosyalar (`node_modules`, `dist`,
`data/runs`, `.venv`) ve gizli bilgiler (`.env`, anahtarlar) commit'lenmez.

## Pull request

1. PR açmadan önce yerelde çalıştırın:
   ```powershell
   .\.venv\Scripts\python.exe -m pytest
   cd frontend; npm run lint; npm run build; cd ..
   ```
2. PR şablonunu doldurun (`.github/pull_request_template.md`).
3. En az **bir** onay gerekir; `core/`, `aircraft/` veya API sözleşmesi değişiyorsa onay **proje liderinden** gelmelidir.
4. CI (GitHub Actions) yeşil olmadan birleştirme yapılmaz.
5. Birleştirme yöntemi: **Squash and merge**. Birleştirmeden sonra dal silinir.

## Kod kuralları

- Python: tip ipuçları, SI birimleri, birimi alan adında belirtin (`altitude_m`). Dönüşümler `core/units.py` ile yapılır.
- TypeScript: `strict` derleme; `frontend/src/api/types.ts` backend modelleriyle uyumlu tutulur.
- Her yeni davranış bir test ile gelir.
- Mühendislik verisi kaynaksız eklenmez (bkz. `aircraft/c172/README.md`).
