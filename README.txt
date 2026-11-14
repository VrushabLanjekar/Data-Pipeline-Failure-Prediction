Pipeline Radar - DPFP project + webapp

Live webapp: https://dpfp-pipeline-radar.lovable.app
Lovable editor: https://lovable.dev/projects/6161900c-5ad3-4320-ba64-c87bc753af90
Data source (updated daily 08:00 IST by GitHub Actions): https://vrushablanjekar.github.io/DPFP-Project/data.json
Repo: https://github.com/VrushabLanjekar/DPFP-Project

pipeline-radar-webapp/  React + TypeScript (TanStack Start, Tailwind, shadcn/ui), built in Lovable.
  Run locally:  bun install  (or npm install)  then  bun run dev  (or npm run dev)
  The app has no backend: it reads the public data.json and CSVs from the repo in the browser.
  public/favicon.ico is not included (binary file).

DPFP_PROJECT/  the pipeline, model, notebook, data and automation. Start with README_START_HERE.md.
  venv/ and .git/ are not included. Rebuild the environment with: pip install -r requirements.txt
