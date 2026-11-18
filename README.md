# FnV Availability Dashboard

Live page: `https://<your-github-username>.github.io/<repo-name>/`

## Daily update (about 1 minute)
1. Put the new Excel file in the `data/` folder (same 3 sheets: Raw data, Assortment, Store class breakup).
   The newest committed file is used; old files can stay or be deleted.
2. GitHub Desktop → Commit → Push.
3. GitHub rebuilds `data.json` (Actions tab, ~30 s). Open dashboards update themselves within a minute and show an "updated" toast.

## Cluster managers
Edit `config/cluster_managers.csv` (Store ID,Manager) and push. Stores not listed there use the Excel sheet's COM column.

## One-time setup
- Repo → Settings → Pages → Deploy from a branch → `main` / root.
- Repo → Settings → Actions → General → Workflow permissions → Read and write permissions.

## Run locally
`python build_data.py` then `python -m http.server 8000` and open http://localhost:8000
