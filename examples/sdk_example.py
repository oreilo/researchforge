from oreilo_researchforge import ResearchConfig, ResearchEngine
from oreilo_researchforge.export import export_report

config = ResearchConfig(topic="Sustainable packaging industry", questions=[
    "What technologies are emerging?", "What are the major adoption barriers?"], max_pages=6)
report = ResearchEngine(config).run()
export_report(report, "reports/sustainable-packaging.md")
print(f"Sources: {len(report.sources)}; errors: {len(report.errors)}")
