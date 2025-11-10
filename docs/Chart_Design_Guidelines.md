# Chart Design & Visualization Guidelines
## KODING with KAGR Case Competition

---

## Professional Color Palette

### Primary Colors (Main Data)
```python
PRIMARY_BLUE = '#1f77b4'      # Main bars/lines
PRIMARY_GREEN = '#2ca02c'     # Positive metrics
PRIMARY_RED = '#d62728'       # Problem areas/alerts
PRIMARY_ORANGE = '#ff7f0e'    # Secondary emphasis
PRIMARY_PURPLE = '#9467bd'    # Tertiary data
```

### Traffic Light System (Performance)
```python
EXCELLENT = '#2E7D32'   # Dark Green (>80% performance)
GOOD = '#66BB6A'        # Light Green (60-80%)
WARNING = '#FFA726'     # Orange (40-60%)
CRITICAL = '#E53935'    # Red (<40%)
```

### Sport-Specific Colors
```python
FOOTBALL = '#8B0000'        # Dark Red
MENS_BASKETBALL = '#FF8C00'  # Dark Orange
WOMENS_BASKETBALL = '#FF69B4' # Hot Pink
BASEBALL = '#4169E1'        # Royal Blue
SOFTBALL = '#FFD700'        # Gold
VOLLEYBALL = '#9370DB'      # Medium Purple
```

---

## Chart Type Best Practices

### 1. Revenue Composition - Improved Donut Chart
**Why:** Donut charts look more modern than pie charts
```python
fig, ax = plt.subplots(figsize=(12, 8))
wedges, texts, autotexts = ax.pie(
    revenue_data,
    labels=labels,
    autopct=lambda pct: f'${pct/100*total_revenue/1e6:.1f}M\n({pct:.1f}%)',
    startangle=90,
    colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'],
    wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2),
    explode=(0.05, 0, 0, 0)
)

# Add center circle for donut effect
centre_circle = plt.Circle((0,0), 0.70, fc='white')
fig.gca().add_artist(centre_circle)

# Add total in center
ax.text(0, 0, f'Total\n${total_revenue/1e6:.1f}M',
        ha='center', va='center', fontsize=20, weight='bold')
```

### 2. Sport Performance - Horizontal Bar Chart with Benchmarks
**Why:** Easier to read sport names, can add benchmark lines
```python
fig, ax = plt.subplots(figsize=(14, 8))

# Sort by revenue
sorted_data = sport_revenue.sort_values(ascending=True)

# Color code by performance
colors = [EXCELLENT if x > 30e6 else GOOD if x > 15e6 else WARNING
          for x in sorted_data.values]

bars = ax.barh(sorted_data.index, sorted_data.values, color=colors,
               edgecolor='black', linewidth=1.5)

# Add value labels at end of bars
for i, (sport, value) in enumerate(sorted_data.items()):
    ax.text(value + 1e6, i, f'${value/1e6:.1f}M',
            va='center', fontsize=11, weight='bold')

# Add benchmark line
benchmark = 20e6
ax.axvline(benchmark, color='red', linestyle='--', linewidth=2,
           label=f'Target: ${benchmark/1e6:.0f}M')

ax.set_xlabel('Annual Revenue (Millions)', fontsize=13, weight='bold')
ax.set_title('Sport Revenue Performance vs. Benchmark',
             fontsize=16, weight='bold', pad=20)
ax.legend(loc='lower right', fontsize=11)
ax.grid(axis='x', alpha=0.3, linestyle='--')
```

### 3. Capacity Utilization - Gauge/Speedometer Style
**Why:** Visual metaphor shows "health" at a glance
```python
from matplotlib.patches import Wedge, Rectangle
import numpy as np

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Capacity Utilization Dashboard', fontsize=18, weight='bold')

for ax, (sport, util_pct) in zip(axes.flat, sport_capacity.items()):
    # Create gauge
    theta1, theta2 = 180, 0

    # Background arc (gray)
    arc = Wedge((0.5, 0.2), 0.3, theta1, theta2, width=0.1,
                facecolor='lightgray', edgecolor='none')
    ax.add_patch(arc)

    # Colored arc based on utilization
    if util_pct >= 80:
        color = EXCELLENT
    elif util_pct >= 60:
        color = GOOD
    elif util_pct >= 40:
        color = WARNING
    else:
        color = CRITICAL

    angle = theta1 - (util_pct / 100) * 180
    arc_filled = Wedge((0.5, 0.2), 0.3, theta1, angle, width=0.1,
                       facecolor=color, edgecolor='none')
    ax.add_patch(arc_filled)

    # Add percentage in center
    ax.text(0.5, 0.3, f'{util_pct:.1f}%', ha='center', va='center',
            fontsize=20, weight='bold')
    ax.text(0.5, 0.05, sport, ha='center', va='center',
            fontsize=12, weight='bold')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.7)
    ax.axis('off')
```

### 4. Customer Segments - Stacked Area Chart (Trend Over Time)
**Why:** Shows composition AND growth over time
```python
fig, ax = plt.subplots(figsize=(14, 8))

# Assuming you have data by season/year
ax.stackplot(seasons, students, alumni, local_fans, corporate, families,
             labels=['Students', 'Alumni', 'Local Fans', 'Corporate', 'Families'],
             colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
             alpha=0.8)

ax.set_xlabel('Season', fontsize=13, weight='bold')
ax.set_ylabel('Attendance', fontsize=13, weight='bold')
ax.set_title('Customer Segment Evolution (2022-2024)',
             fontsize=16, weight='bold', pad=20)
ax.legend(loc='upper left', fontsize=11, framealpha=0.9)
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Add annotation for corporate gap
ax.annotate('Corporate Below\nIndustry Benchmark',
            xy=(2023, corporate_2023), xytext=(2023.5, corporate_2023 + 50000),
            arrowprops=dict(arrowstyle='->', color='red', lw=2),
            fontsize=11, color='red', weight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))
```

### 5. Women's Basketball Opportunity - Dual Y-Axis Chart
**Why:** Shows interest AND attendance on same chart to emphasize gap
```python
fig, ax1 = plt.subplots(figsize=(12, 7))

sports = ['Football', 'Mens_BB', 'Womens_BB', 'Baseball', 'Softball', 'Volleyball']
interest = [95, 88, 85, 65, 58, 52]  # Survey interest scores
attendance_pct = [87, 84, 43, 67, 59, 71]  # Capacity utilization

x = np.arange(len(sports))
width = 0.35

# Interest bars
bars1 = ax1.bar(x - width/2, interest, width, label='Fan Interest Score',
                color='#1f77b4', edgecolor='black', linewidth=1.5)

# Attendance on second y-axis
ax2 = ax1.twinx()
bars2 = ax2.bar(x + width/2, attendance_pct, width,
                label='Capacity Utilization %',
                color=['#2ca02c' if pct >= 70 else '#d62728' for pct in attendance_pct],
                edgecolor='black', linewidth=1.5)

# Highlight Women's Basketball
ax1.patches[2].set_edgecolor('red')
ax1.patches[2].set_linewidth(3)
ax2.patches[2].set_edgecolor('red')
ax2.patches[2].set_linewidth(3)

# Add annotation
ax1.annotate('MAJOR OPPORTUNITY\nHigh Interest, Low Attendance',
             xy=(2, 85), xytext=(3.5, 90),
             arrowprops=dict(arrowstyle='->', color='red', lw=3),
             fontsize=12, color='red', weight='bold',
             bbox=dict(boxstyle='round,pad=0.8', facecolor='yellow',
                      edgecolor='red', linewidth=2))

ax1.set_xlabel('Sport', fontsize=13, weight='bold')
ax1.set_ylabel('Fan Interest Score (0-100)', fontsize=12, weight='bold', color='#1f77b4')
ax2.set_ylabel('Capacity Utilization %', fontsize=12, weight='bold', color='#2ca02c')
ax1.set_title('Interest vs. Attendance Gap Analysis', fontsize=16, weight='bold', pad=20)
ax1.set_xticks(x)
ax1.set_xticklabels(sports, rotation=45, ha='right')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
ax1.grid(axis='y', alpha=0.3, linestyle='--')
```

### 6. Revenue Projection - Waterfall Chart
**Why:** Shows how you get from $94M to $120M step by step
```python
from matplotlib.patches import Rectangle

fig, ax = plt.subplots(figsize=(16, 8))

initiatives = ['Current\nRevenue', 'Dynamic\nPricing', 'Women\'s BB\nGrowth',
               'Corporate\nPartnerships', 'Premium\nSeating', 'Merchandise',
               'Off-Peak\nPromo', 'Alumni\nProgram', 'Projected\nRevenue']
values = [94.36, 4.2, 4.0, 7.5, 2.8, 1.9, 0.8, 0.9, 0]  # Last is calculated

cumulative = [94.36]
for i in range(1, len(values)-1):
    cumulative.append(cumulative[-1] + values[i])
cumulative.append(cumulative[-1])  # Final total

colors = ['#1f77b4'] + ['#2ca02c'] * 7 + ['#ff7f0e']

# Draw bars
for i, (init, val, cum) in enumerate(zip(initiatives, values, cumulative)):
    if i == 0 or i == len(initiatives) - 1:
        # Start and end bars go from 0
        ax.bar(i, cum, color=colors[i], edgecolor='black', linewidth=2)
        ax.text(i, cum + 2, f'${cum:.1f}M', ha='center', fontsize=11, weight='bold')
    else:
        # Floating bars for increments
        bottom = cumulative[i-1]
        ax.bar(i, val, bottom=bottom, color=colors[i], edgecolor='black', linewidth=2)
        ax.text(i, bottom + val/2, f'+${val:.1f}M', ha='center', va='center',
                fontsize=10, weight='bold', color='white')
        # Connector line
        ax.plot([i-0.5, i-0.5], [cumulative[i-1], cumulative[i]],
                'k--', linewidth=1, alpha=0.5)

ax.set_xticks(range(len(initiatives)))
ax.set_xticklabels(initiatives, fontsize=11, weight='bold')
ax.set_ylabel('Revenue (Millions)', fontsize=13, weight='bold')
ax.set_title('Revenue Growth Waterfall: Current to Projected ($94M → $119.5M)',
             fontsize=16, weight='bold', pad=20)
ax.axhline(94.36 + 20.5, color='red', linestyle='--', linewidth=2,
           label='NCAA Settlement Target: $114.86M')
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3, linestyle='--')
```

### 7. Industry Benchmark Comparison - Bullet Chart
**Why:** Shows performance vs. target vs. excellent performance
```python
fig, ax = plt.subplots(figsize=(12, 10))

metrics = ['Corporate\nPartnerships %', 'Capacity\nUtilization',
           'Merchandise\nRevenue %', 'Premium\nSeating %']
current = [9.2, 68.5, 12.5, 8]
target = [15, 75, 15, 18]
excellent = [18, 85, 18, 22]

y_pos = np.arange(len(metrics))
height = 0.5

# Excellent range (background)
ax.barh(y_pos, excellent, height, color='lightgray', alpha=0.3,
        label='Industry Leader')

# Target (darker background)
ax.barh(y_pos, target, height, color='lightblue', alpha=0.5,
        label='Industry Average')

# Current (solid bar)
colors = ['#d62728' if c < t else '#2ca02c' for c, t in zip(current, target)]
bars = ax.barh(y_pos, current, height*0.7, color=colors,
               edgecolor='black', linewidth=2, label='Midwest State')

# Add value labels
for i, (cur, targ, exc) in enumerate(zip(current, target, excellent)):
    ax.text(cur + 0.5, i, f'{cur:.1f}%', va='center', fontsize=11, weight='bold')
    ax.text(targ, i + 0.35, f'Target: {targ}%', va='center',
            fontsize=9, style='italic', color='blue')

ax.set_yticks(y_pos)
ax.set_yticklabels(metrics, fontsize=12, weight='bold')
ax.set_xlabel('Percentage', fontsize=13, weight='bold')
ax.set_title('Midwest State vs. Industry Benchmarks',
             fontsize=16, weight='bold', pad=20)
ax.legend(loc='lower right', fontsize=11)
ax.grid(axis='x', alpha=0.3, linestyle='--')
```

---

## General Styling Guidelines

### Font Hierarchy
```python
TITLE_SIZE = 16        # Main chart title
SUBTITLE_SIZE = 13     # Axis labels
LABEL_SIZE = 11        # Data labels
ANNOTATION_SIZE = 10   # Annotations

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
```

### Grid and Background
```python
# Light grid on y-axis only for bar charts
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.8)
ax.set_axisbelow(True)  # Grid behind bars

# Remove top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
```

### Annotations Best Practices
- Use arrows sparingly (only for major insights)
- Yellow background with red border for critical findings
- Place annotations outside data area when possible
- Use bold text for emphasis

### Color Coding Consistency
- 🟢 Green = Good/Above target
- 🟡 Orange = Warning/Room for improvement
- 🔴 Red = Problem/Below target
- 🔵 Blue = Neutral/Current state

---

## Mobile/Projection Friendly
- Minimum font size: 10pt
- High contrast colors (avoid pastels)
- Test at 1920x1080 resolution
- Export as PNG at 300 DPI for presentations

---

## Data-Ink Ratio
**Maximize data, minimize decoration:**
- Remove chart junk (unnecessary 3D effects, gradients)
- Use direct labeling instead of legends when possible
- Eliminate redundant grid lines
- Remove chart borders

---

## Accessibility
- Don't rely solely on color (use patterns/labels too)
- Color-blind friendly palettes
- Alt text for all charts in documentation
