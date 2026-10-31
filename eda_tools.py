import pandas as pd
import plotly.express as px
from IPython.display import HTML, display


def profile_data(
    df: pd.DataFrame,
    target_num: str = None,
    target_cat: str = None,
    show_raw_info: bool = False,
):
    """
    Universal EDA & Data Health Profile for any Tabular Dataset.
    Works seamlessly in VS Code Interactive (# %%), Jupyter Notebooks, and Google Colab.

    Parameters:
    -----------
    df : pd.DataFrame
        The dataset to inspect.
    target_num : str, optional
        Specific numerical column to plot histogram for (auto-selected if None).
    target_cat : str, optional
        Specific categorical column to plot bar chart for (auto-selected if None).
    show_raw_info : bool, optional
        If True, also outputs pandas' raw df.info() console text (default: False).
    """
    if df is None or df.empty:
        display(
            HTML(
                "<p style='color:red;font-weight:bold'>⚠️ Error: Provided DataFrame is empty.</p>"
            )
        )
        return

    # --- 1. Dataset Dimensions & Memory Health ---
    rows, cols = df.shape
    duplicates = int(df.duplicated().sum())
    total_cells = rows * cols
    missing_cells = int(df.isna().sum().sum())
    missing_cell_pct = (
        round((missing_cells / total_cells) * 100, 2) if total_cells > 0 else 0
    )
    mem_mb = df.memory_usage(deep=True).sum() / (1024**2)
    mem_str = f"{mem_mb:.2f} MB" if mem_mb >= 1 else f"{mem_mb * 1024:.1f} KB"

    # Dtype breakdown counts
    numeric = df.select_dtypes(include="number")
    categorical = df.select_dtypes(include=["object", "category", "string"])
    datetimes = df.select_dtypes(include=["datetime", "datetimetz"])
    booleans = df.select_dtypes(include="bool")

    # Header Card
    html = f"""<div style='font-family:Arial, sans-serif;background:#111c2b;color:white;padding:20px;border-radius:12px;margin-bottom:15px'>
    <div style='display:flex;justify-content:space-between;align-items:center'>
        <div>
            <h2 style='margin:0;font-size:22px'>📊 DATA HEALTH CHECK</h2>
            <p style='color:#94a3b8;margin:4px 0 0 0;font-size:13px'>Automated Exploratory Profiler</p>
        </div>
        <div style='background:#1e293b;padding:6px 14px;border-radius:6px;font-size:12px;color:#38bdf8'>RAM: {
        mem_str
    }</div>
    </div>
    <div style='display:flex;gap:12px;flex-wrap:wrap;margin-top:14px'>
    {
        "".join(
            f"<div style='background:#1e293b;padding:12px 18px;border-radius:8px;min-width:120px'><b style='font-size:22px;color:#f8fafc'>{v:,}</b><br><span style='color:#94a3b8;font-size:12px'>{name}</span></div>"
            for name, v in [
                ("Rows", rows),
                ("Columns", cols),
                ("Duplicate Rows", duplicates),
                ("Missing Cells", missing_cells),
            ]
        )
    }
    <div style='background:#1e293b;padding:12px 18px;border-radius:8px;min-width:120px'><b style='font-size:22px;color:#f8fafc'>{
        missing_cell_pct
    }%</b><br><span style='color:#94a3b8;font-size:12px'>Missing Overall</span></div>
    </div>
    <div style='margin-top:12px;font-size:12px;color:#cbd5e1'>
        Types: <b style='color:#38bdf8'>{
        len(numeric.columns)
    }</b> Numeric | <b style='color:#38bdf8'>{
        len(categorical.columns)
    }</b> Text/Categorical | <b style='color:#38bdf8'>{
        len(booleans.columns)
    }</b> Boolean | <b style='color:#38bdf8'>{len(datetimes.columns)}</b> Datetime
    </div>
    </div>"""
    display(HTML(html))

    # --- 2. Enhanced df.info() Schema & Dtype Table ---
    display(
        HTML(
            "<h3 style='margin-bottom:4px'>📋 Column Schema & Data Types (Enhanced df.info)</h3>"
        )
    )
    sample_vals = []
    for col in df.columns:
        valid_series = df[col].dropna()
        sample_vals.append(valid_series.iloc[0] if not valid_series.empty else "N/A")

    schema_df = pd.DataFrame(
        {
            "Data Type": df.dtypes.astype(str),
            "Non-Null Count": df.notna().sum(),
            "Null Count": df.isna().sum(),
            "Null %": (df.isna().mean() * 100).round(2),
            "Unique Count": df.nunique(),
            "Sample Value": sample_vals,
        },
        index=df.columns,
    )

    try:
        display(
            schema_df.style.background_gradient(
                cmap="YlOrRd", subset=["Null %"]
            ).format(
                {
                    "Non-Null Count": "{:,}",
                    "Null Count": "{:,}",
                    "Null %": "{:.2f}%",
                    "Unique Count": "{:,}",
                }
            )
        )
    except Exception:
        display(schema_df)

    if show_raw_info:
        display(
            HTML(
                "<details><summary style='cursor:pointer;color:#38bdf8;margin:8px 0'><b>Show Raw df.info() Output</b></summary>"
            )
        )
        df.info()
        display(HTML("</details>"))

    # --- 3. Smart Alerts / Red Flags (Crucial for Feature Engineering) ---
    alerts = []
    constant_cols = [c for c in df.columns if df[c].nunique(dropna=False) == 1]
    if constant_cols:
        alerts.append(
            f"⚠️ <b>Constant Columns (zero variance):</b> {constant_cols} — Consider dropping these."
        )

    # Detect date-like strings that should probably be converted to datetime
    unparsed_dates = [
        c
        for c in categorical.columns
        if any(w in c.lower() for w in ["time", "date", "timestamp"])
    ]
    if unparsed_dates:
        alerts.append(
            f"💡 <b>Potential Datetime Columns stored as 'object':</b> {unparsed_dates} — Convert with <code>pd.to_datetime()</code>."
        )

    # High cardinality columns (potential IDs / UUIDs)
    high_card_cols = [
        c for c in categorical.columns if df[c].nunique() > (0.8 * rows) and rows > 50
    ]
    if high_card_cols:
        alerts.append(
            f"🔑 <b>High Cardinality / Identifier Columns:</b> {high_card_cols}"
        )

    if alerts:
        display(
            HTML(f"""<div style='background:#1e293b;border-left:4px solid #f59e0b;padding:12px 16px;border-radius:6px;margin:12px 0;font-size:13px;color:#e2e8f0;line-height:1.6'>
        {"<br>".join(alerts)}
        </div>""")
        )

    # --- 4. Datetime Overview (if parsed) ---
    if not datetimes.empty:
        display(HTML("<h3 style='margin-bottom:4px'>📅 Datetime Range</h3>"))
        dt_summary = pd.DataFrame(
            {
                "Earliest": [df[col].min() for col in datetimes.columns],
                "Latest": [df[col].max() for col in datetimes.columns],
                "Span (Days)": [
                    (df[col].max() - df[col].min()).days for col in datetimes.columns
                ],
                "Unique Dates": [df[col].nunique() for col in datetimes.columns],
            },
            index=datetimes.columns,
        )
        display(dt_summary)

    # --- 5. Numerical Summary & Distribution ---
    if not numeric.empty:
        display(HTML("<h3 style='margin-bottom:4px'>📈 Numerical Summary</h3>"))
        display(
            numeric.describe().T[["count", "mean", "std", "min", "50%", "max"]].round(2)
        )

        num_col = target_num if target_num in numeric.columns else None
        if not num_col:
            candidates = [
                c
                for c in numeric.columns
                if not c.lower().endswith(("_id", "_uuid", "id", "uuid"))
                and df[c].nunique() > 1
            ]
            num_col = candidates[0] if candidates else numeric.columns[0]

        if num_col:
            plot_data = df[num_col].dropna()
            if len(plot_data) > 30000:
                plot_data = plot_data.sample(30000, random_state=42)
                sub_title = f"{num_col} (sampled 30k rows)"
            else:
                sub_title = num_col

            fig = px.histogram(
                plot_data,
                x=num_col,
                nbins=35,
                title=f"Distribution: {sub_title}",
                color_discrete_sequence=["#14b8a6"],
                template="plotly_dark",
            )
            fig.update_layout(height=320, margin=dict(l=30, r=20, t=50, b=20))
            fig.show()

    # --- 6. Categorical Summary & Top Categories ---
    if not categorical.empty:
        display(HTML("<h3 style='margin-bottom:4px'>🏷️ Categorical Summary</h3>"))

        cat_col = target_cat if target_cat in categorical.columns else None
        if not cat_col:
            meaningful = [
                c
                for c in categorical.columns
                if 1 < df[c].nunique() <= 60
                and not c.lower().endswith(("_id", "_uuid"))
            ]
            cat_col = meaningful[0] if meaningful else categorical.columns[0]

        if cat_col:
            top_counts = (
                df[cat_col]
                .fillna("Missing")
                .astype(str)
                .value_counts()
                .head(10)
                .reset_index()
            )
            top_counts.columns = ["category_value", "frequency"]
            fig = px.bar(
                top_counts,
                x="category_value",
                y="frequency",
                title=f"Top Categories in '{cat_col}' (Cardinality: {df[cat_col].nunique():,})",
                color="frequency",
                color_continuous_scale="Teal",
                template="plotly_dark",
            )
            fig.update_layout(
                height=320, margin=dict(l=30, r=20, t=50, b=20), showlegend=False
            )
            fig.show()

    # --- 7. First Rows Preview ---
    display(HTML("<h3 style='margin-bottom:4px'>👀 Raw Data Snapshot</h3>"))
    display(df.head(5))
    print(f"ℹ️ Profile complete: {cols} features inspected.")
