# Slick2Vessel
### author@ LELE

Segment SAR images to get candidate oil slicks , assign slicks to candidate vessels with AIS data.

Work in this folder only. Jupyter Lab should be started from `F:\jupyter` (or this directory). Open notebooks under `notebooks/`.

## Layout

- `notebooks/` — experiments and analysis notebooks
- `src/` — reusable Python modules imported by notebooks, csv operation
- `data/` — local data (not committed by default)

## Daily git

```powershell
cd F:\jupyter\Slick2Vessel
git pull
# edit in Jupyter Lab, save notebooks
git add .
git status
git commit -m "Describe the change"
git push
```
