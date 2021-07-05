- Move `BaseCase` model somewhere else.
- Place lock on model instance while `execute_run` is happening.
- Move all shared and duplicate code to `utils`.
- Create custom exceptions.
- Better exception handling.
- Check why the original `case_directory_path` in `ai_corona` did not work.
- Prevent `execute_run` from happening a second time (by placing a check).
- Aggregate all the knobs and parameters (e.g. batch size) in a dedicated file.
- Move all validators to `utils`.

| Modality    | Price |
| ----------- | ----- |
| Chest X-Ray | 100   |
| Brain CT    | 300   |
| Chest CT    | 400   |
| Brain MRI   | 500   |

| Size   | Chest X-Ray | CT (any kind) | MRI (any kind) |
| ------ | ----------- | ------------- | -------------- |
| Small  | ~25         | 20 - 50       | 25 - 50        |
| Medium | ~50         | 30 - 100      | 50 - 100       |
| Large  | ~75         | 50 - 120      | 80 - 150       |
