"""
Rail Handbrakes Data - Interactive HTML Visualizations
=======================================================

This script creates interactive HTML visualizations using Plotly for the rail handbrakes dataset.
The visualizations are saved as standalone HTML files that can be opened in any web browser.

Features:
- Interactive charts with zoom, pan, and hover capabilities
- Multiple visualization types (scatter, bar, line, box, heatmap)
- Responsive design that works on different screen sizes
- Export capabilities for sharing and presentations
- Professional styling and layout

Author: Data Analysis Team
Date: May 10, 2026
Dataset: output.xlsx (Rail Handbrakes Data)
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set default template for all plots
pio.templates.default = "plotly_white"

print("="*80)
print("RAIL HANDBRAKES DATA - INTERACTIVE VISUALIZATION GENERATOR")
print("="*80)
print(f"\nStarting analysis at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# ============================================================================
# 1. LOAD DATA
# ============================================================================
print("Step 1: Loading data...")
file_path = 'output.xlsx'
df = pd.read_excel(file_path)
print(f"✓ Data loaded successfully: {df.shape[0]} rows × {df.shape[1]} columns\n")

# Identify column types
numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

print(f"Numerical columns: {len(numerical_cols)}")
print(f"Categorical columns: {len(categorical_cols)}\n")

# ============================================================================
# 2. INTERACTIVE DISTRIBUTION PLOTS
# ============================================================================
print("Step 2: Creating distribution visualizations...")

if len(numerical_cols) > 0:
    # Histograms with distribution curves
    for col in numerical_cols:
        fig = px.histogram(
            df, 
            x=col,
            nbins=30,
            title=f'Interactive Distribution: {col}',
            labels={col: col, 'count': 'Frequency'},
            color_discrete_sequence=['#1f77b4'],
            marginal='box'  # Add box plot on top
        )
        
        fig.update_layout(
            title_font_size=20,
            title_x=0.5,
            showlegend=False,
            hovermode='x unified',
            height=600,
            template='plotly_white'
        )
        
        # Add mean and median lines
        mean_val = df[col].mean()
        median_val = df[col].median()
        
        fig.add_vline(x=mean_val, line_dash="dash", line_color="red", 
                     annotation_text=f"Mean: {mean_val:.2f}", 
                     annotation_position="top")
        fig.add_vline(x=median_val, line_dash="dash", line_color="green",
                     annotation_text=f"Median: {median_val:.2f}",
                     annotation_position="bottom")
        
        filename = f'interactive_distribution_{col.replace(" ", "_")}.html'
        fig.write_html(filename)
        print(f"  ✓ Created: {filename}")

# ============================================================================
# 3. INTERACTIVE BOX PLOTS
# ============================================================================
print("\nStep 3: Creating box plot visualizations...")

if len(numerical_cols) > 0:
    # Create combined box plot
    fig = go.Figure()
    
    for col in numerical_cols:
        fig.add_trace(go.Box(
            y=df[col],
            name=col,
            boxmean='sd',  # Show mean and standard deviation
            marker_color='lightblue',
            line_color='darkblue'
        ))
    
    fig.update_layout(
        title='Interactive Box Plots - All Numerical Variables',
        title_font_size=20,
        title_x=0.5,
        yaxis_title='Value',
        showlegend=True,
        height=600,
        hovermode='closest'
    )
    
    fig.write_html('interactive_boxplots_combined.html')
    print("  ✓ Created: interactive_boxplots_combined.html")

# ============================================================================
# 4. CORRELATION HEATMAP
# ============================================================================
print("\nStep 4: Creating correlation heatmap...")

if len(numerical_cols) > 1:
    correlation_matrix = df[numerical_cols].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=correlation_matrix.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Correlation")
    ))
    
    fig.update_layout(
        title='Interactive Correlation Heatmap',
        title_font_size=20,
        title_x=0.5,
        width=800,
        height=800,
        xaxis_title='Variables',
        yaxis_title='Variables'
    )
    
    fig.write_html('interactive_correlation_heatmap.html')
    print("  ✓ Created: interactive_correlation_heatmap.html")

# ============================================================================
# 5. SCATTER PLOTS (PAIRWISE)
# ============================================================================
print("\nStep 5: Creating scatter plot matrix...")

if len(numerical_cols) >= 2:
    # Create scatter matrix for first 5 numerical columns (to avoid overcrowding)
    cols_to_plot = numerical_cols[:min(5, len(numerical_cols))]
    
    fig = px.scatter_matrix(
        df,
        dimensions=cols_to_plot,
        title='Interactive Scatter Plot Matrix',
        height=900,
        width=900
    )
    
    fig.update_traces(diagonal_visible=False, showupperhalf=False)
    fig.update_layout(
        title_font_size=20,
        title_x=0.5
    )
    
    fig.write_html('interactive_scatter_matrix.html')
    print("  ✓ Created: interactive_scatter_matrix.html")

# ============================================================================
# 6. CATEGORICAL BAR CHARTS
# ============================================================================
print("\nStep 6: Creating categorical visualizations...")

if len(categorical_cols) > 0:
    for col in categorical_cols[:5]:  # Limit to first 5
        if df[col].nunique() <= 30:  # Only if reasonable number of categories
            value_counts = df[col].value_counts().head(20)
            
            fig = go.Figure(data=[
                go.Bar(
                    x=value_counts.index,
                    y=value_counts.values,
                    text=value_counts.values,
                    textposition='auto',
                    marker_color='steelblue',
                    hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
                )
            ])
            
            fig.update_layout(
                title=f'Interactive Distribution: {col}',
                title_font_size=20,
                title_x=0.5,
                xaxis_title=col,
                yaxis_title='Count',
                height=600,
                showlegend=False
            )
            
            filename = f'interactive_bar_{col.replace(" ", "_")}.html'
            fig.write_html(filename)
            print(f"  ✓ Created: {filename}")

# ============================================================================
# 7. TIME SERIES (if date column exists)
# ============================================================================
print("\nStep 7: Checking for time series data...")

date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
if len(date_cols) > 0 and len(numerical_cols) > 0:
    for date_col in date_cols[:1]:  # Use first date column
        for num_col in numerical_cols[:3]:  # Plot first 3 numerical columns
            fig = px.line(
                df.sort_values(date_col),
                x=date_col,
                y=num_col,
                title=f'Time Series: {num_col} over {date_col}',
                markers=True
            )
            
            fig.update_layout(
                title_font_size=20,
                title_x=0.5,
                xaxis_title=date_col,
                yaxis_title=num_col,
                height=600,
                hovermode='x unified'
            )
            
            filename = f'interactive_timeseries_{num_col.replace(" ", "_")}.html'
            fig.write_html(filename)
            print(f"  ✓ Created: {filename}")
else:
    print("  ℹ No datetime columns found for time series analysis")

# ============================================================================
# 8. COMPREHENSIVE DASHBOARD
# ============================================================================
print("\nStep 8: Creating comprehensive dashboard...")

# Create a multi-panel dashboard
fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=(
        'Data Overview',
        'Missing Values',
        'Numerical Summary',
        'Categorical Summary',
        'Data Types',
        'Record Count'
    ),
    specs=[
        [{"type": "table"}, {"type": "bar"}],
        [{"type": "table"}, {"type": "pie"}],
        [{"type": "pie"}, {"type": "indicator"}]
    ],
    vertical_spacing=0.12,
    horizontal_spacing=0.15
)

# Panel 1: Data Overview Table
overview_data = {
    'Metric': ['Total Rows', 'Total Columns', 'Numerical Cols', 'Categorical Cols', 'Missing Values', 'Duplicates'],
    'Value': [
        len(df),
        len(df.columns),
        len(numerical_cols),
        len(categorical_cols),
        df.isnull().sum().sum(),
        df.duplicated().sum()
    ]
}
fig.add_trace(
    go.Table(
        header=dict(values=['<b>Metric</b>', '<b>Value</b>'],
                   fill_color='paleturquoise',
                   align='left'),
        cells=dict(values=[overview_data['Metric'], overview_data['Value']],
                  fill_color='lavender',
                  align='left')
    ),
    row=1, col=1
)

# Panel 2: Missing Values Bar Chart
if df.isnull().sum().sum() > 0:
    missing_data = df.isnull().sum()[df.isnull().sum() > 0].sort_values(ascending=False)
    fig.add_trace(
        go.Bar(x=missing_data.index, y=missing_data.values, marker_color='coral'),
        row=1, col=2
    )
else:
    fig.add_trace(
        go.Bar(x=['No Missing Values'], y=[0], marker_color='lightgreen'),
        row=1, col=2
    )

# Panel 3: Numerical Summary Table
if len(numerical_cols) > 0:
    num_summary = df[numerical_cols].describe().T.reset_index()
    fig.add_trace(
        go.Table(
            header=dict(values=['<b>Column</b>', '<b>Mean</b>', '<b>Std</b>', '<b>Min</b>', '<b>Max</b>'],
                       fill_color='paleturquoise',
                       align='left'),
            cells=dict(values=[
                num_summary['index'],
                num_summary['mean'].round(2),
                num_summary['std'].round(2),
                num_summary['min'].round(2),
                num_summary['max'].round(2)
            ],
            fill_color='lavender',
            align='left')
        ),
        row=2, col=1
    )

# Panel 4: Categorical Distribution Pie
if len(categorical_cols) > 0:
    cat_unique = {col: df[col].nunique() for col in categorical_cols[:5]}
    fig.add_trace(
        go.Pie(labels=list(cat_unique.keys()), values=list(cat_unique.values()),
               marker_colors=px.colors.qualitative.Set3),
        row=2, col=2
    )

# Panel 5: Data Types Pie
dtype_counts = df.dtypes.value_counts()
fig.add_trace(
    go.Pie(labels=[str(x) for x in dtype_counts.index], values=dtype_counts.values,
           marker_colors=px.colors.qualitative.Pastel),
    row=3, col=1
)

# Panel 6: Total Records Indicator
fig.add_trace(
    go.Indicator(
        mode="number+delta",
        value=len(df),
        title={"text": "Total Records"},
        delta={'reference': 0},
        domain={'x': [0, 1], 'y': [0, 1]}
    ),
    row=3, col=2
)

fig.update_layout(
    title_text="Rail Handbrakes Data - Interactive Dashboard",
    title_font_size=24,
    title_x=0.5,
    showlegend=False,
    height=1200,
    width=1400
)

fig.write_html('interactive_dashboard.html')
print("  ✓ Created: interactive_dashboard.html")

# ============================================================================
# 9. 3D SCATTER PLOT (if enough numerical columns)
# ============================================================================
print("\nStep 9: Creating 3D visualizations...")

if len(numerical_cols) >= 3:
    fig = px.scatter_3d(
        df,
        x=numerical_cols[0],
        y=numerical_cols[1],
        z=numerical_cols[2],
        color=categorical_cols[0] if len(categorical_cols) > 0 else None,
        title=f'3D Scatter Plot: {numerical_cols[0]} vs {numerical_cols[1]} vs {numerical_cols[2]}',
        height=800,
        opacity=0.7
    )
    
    fig.update_layout(
        title_font_size=20,
        title_x=0.5,
        scene=dict(
            xaxis_title=numerical_cols[0],
            yaxis_title=numerical_cols[1],
            zaxis_title=numerical_cols[2]
        )
    )
    
    fig.write_html('interactive_3d_scatter.html')
    print("  ✓ Created: interactive_3d_scatter.html")
else:
    print("  ℹ Not enough numerical columns for 3D visualization")

# ============================================================================
# 10. VIOLIN PLOTS
# ============================================================================
print("\nStep 10: Creating violin plots...")

if len(numerical_cols) > 0:
    fig = go.Figure()
    
    for col in numerical_cols:
        fig.add_trace(go.Violin(
            y=df[col],
            name=col,
            box_visible=True,
            meanline_visible=True,
            fillcolor='lightseagreen',
            opacity=0.6,
            x0=col
        ))
    
    fig.update_layout(
        title='Interactive Violin Plots - Distribution Comparison',
        title_font_size=20,
        title_x=0.5,
        yaxis_title='Value',
        showlegend=True,
        height=600,
        violinmode='group'
    )
    
    fig.write_html('interactive_violin_plots.html')
    print("  ✓ Created: interactive_violin_plots.html")

# ============================================================================
# 11. SUNBURST CHART (if multiple categorical columns)
# ============================================================================
print("\nStep 11: Creating hierarchical visualizations...")

if len(categorical_cols) >= 2:
    # Create sunburst for first 2-3 categorical columns
    cols_for_sunburst = categorical_cols[:min(3, len(categorical_cols))]
    
    # Limit categories to avoid overcrowding
    df_sunburst = df.copy()
    for col in cols_for_sunburst:
        top_categories = df_sunburst[col].value_counts().head(10).index
        df_sunburst[col] = df_sunburst[col].apply(lambda x: x if x in top_categories else 'Other')
    
    fig = px.sunburst(
        df_sunburst,
        path=cols_for_sunburst,
        title='Hierarchical Sunburst Chart',
        height=800,
        width=800
    )
    
    fig.update_layout(
        title_font_size=20,
        title_x=0.5
    )
    
    fig.write_html('interactive_sunburst.html')
    print("  ✓ Created: interactive_sunburst.html")
else:
    print("  ℹ Not enough categorical columns for sunburst chart")

# ============================================================================
# 12. MASTER INDEX HTML
# ============================================================================
print("\nStep 12: Creating master index page...")

html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rail Handbrakes Data - Interactive Visualizations</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }}
        h1 {{
            color: #667eea;
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .subtitle {{
            text-align: center;
            color: #666;
            font-size: 1.1em;
            margin-bottom: 40px;
        }}
        .info-box {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            border-left: 5px solid #667eea;
        }}
        .info-box h3 {{
            margin-top: 0;
            color: #667eea;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}
        .card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
            color: white;
        }}
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.2);
        }}
        .card h3 {{
            margin-top: 0;
            font-size: 1.3em;
        }}
        .card p {{
            margin: 10px 0;
            opacity: 0.9;
        }}
        .card a {{
            display: inline-block;
            margin-top: 15px;
            padding: 10px 20px;
            background: white;
            color: #667eea;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            transition: background 0.3s;
        }}
        .card a:hover {{
            background: #f0f0f0;
        }}
        .footer {{
            text-align: center;
            margin-top: 50px;
            padding-top: 20px;
            border-top: 2px solid #eee;
            color: #666;
        }}
        .stats {{
            display: flex;
            justify-content: space-around;
            margin: 30px 0;
            flex-wrap: wrap;
        }}
        .stat-item {{
            text-align: center;
            padding: 15px;
        }}
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚂 Rail Handbrakes Data</h1>
        <p class="subtitle">Interactive Visualizations & Analysis Dashboard</p>
        
        <div class="info-box">
            <h3>📊 Dataset Overview</h3>
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-number">{len(df):,}</div>
                    <div class="stat-label">Total Records</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{len(df.columns)}</div>
                    <div class="stat-label">Columns</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{len(numerical_cols)}</div>
                    <div class="stat-label">Numerical</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{len(categorical_cols)}</div>
                    <div class="stat-label">Categorical</div>
                </div>
            </div>
            <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Source:</strong> output.xlsx</p>
        </div>
        
        <h2 style="color: #667eea; margin-top: 40px;">📈 Available Visualizations</h2>
        
        <div class="grid">
            <div class="card">
                <h3>🎯 Master Dashboard</h3>
                <p>Comprehensive overview with multiple panels showing data quality, statistics, and distributions</p>
                <a href="interactive_dashboard.html">View Dashboard →</a>
            </div>
            
            <div class="card">
                <h3>🔥 Correlation Heatmap</h3>
                <p>Interactive correlation matrix showing relationships between numerical variables</p>
                <a href="interactive_correlation_heatmap.html">View Heatmap →</a>
            </div>
            
            <div class="card">
                <h3>📦 Box Plots</h3>
                <p>Combined box plots for outlier detection and distribution comparison</p>
                <a href="interactive_boxplots_combined.html">View Box Plots →</a>
            </div>
            
            <div class="card">
                <h3>🎻 Violin Plots</h3>
                <p>Distribution shapes with probability density for all numerical variables</p>
                <a href="interactive_violin_plots.html">View Violin Plots →</a>
            </div>
            
            <div class="card">
                <h3>🔍 Scatter Matrix</h3>
                <p>Pairwise scatter plots showing relationships between variables</p>
                <a href="interactive_scatter_matrix.html">View Scatter Matrix →</a>
            </div>
            
            <div class="card">
                <h3>🌐 3D Scatter Plot</h3>
                <p>Three-dimensional visualization for exploring multi-variable relationships</p>
                <a href="interactive_3d_scatter.html">View 3D Plot →</a>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>Rail Handbrakes Data Analysis</strong></p>
            <p>All visualizations are interactive - hover, zoom, pan, and click to explore!</p>
            <p>Generated with Plotly | May 2026</p>
        </div>
    </div>
</body>
</html>
"""

with open('index.html', 'w') as f:
    f.write(html_content)

print("  ✓ Created: index.html (Master Index)")

# ============================================================================
# COMPLETION SUMMARY
# ============================================================================
print("\n" + "="*80)
print("VISUALIZATION GENERATION COMPLETE!")
print("="*80)
print("\n📁 Generated Files:")
print("  • index.html - Master index page with links to all visualizations")
print("  • interactive_dashboard.html - Comprehensive multi-panel dashboard")
print("  • interactive_correlation_heatmap.html - Correlation analysis")
print("  • interactive_boxplots_combined.html - Box plots for outlier detection")
print("  • interactive_violin_plots.html - Distribution shapes")
print("  • interactive_scatter_matrix.html - Pairwise relationships")
print("  • interactive_3d_scatter.html - 3D visualization")
print("  • Plus individual distribution and bar charts for each variable")

print("\n🚀 To view the visualizations:")
print("  1. Open 'index.html' in your web browser")
print("  2. Click on any visualization card to explore")
print("  3. Use interactive features: hover, zoom, pan, click")

print("\n✨ All visualizations are standalone HTML files")
print("   They can be shared, embedded, or presented without any dependencies!")

print("\n" + "="*80)
print(f"Analysis completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)
