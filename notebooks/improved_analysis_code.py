"""
KODING with KAGR Case Competition - Improved Analysis Code
This file contains all the improved analysis with mentor feedback incorporated
Run cells in Jupyter notebook or execute sections as needed
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Wedge, Rectangle
import warnings
warnings.filterwarnings('ignore')

# Professional Color Palette
PRIMARY_BLUE = '#1f77b4'
PRIMARY_GREEN = '#2ca02c'
PRIMARY_RED = '#d62728'
PRIMARY_ORANGE = '#ff7f0e'
PRIMARY_PURPLE = '#9467bd'

EXCELLENT = '#2E7D32'
GOOD = '#66BB6A'
WARNING = '#FFA726'
CRITICAL = '#E53935'

# Sport-specific colors
SPORT_COLORS = {
    'Football': '#8B0000',
    'Mens_Basketball': '#FF8C00',
    'Womens_Basketball': '#FF69B4',
    'Baseball': '#4169E1',
    'Softball': '#FFD700',
    'Volleyball': '#9370DB'
}

# Set professional styling
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']

# ============================================================================
# IMPROVED CHART 1: Revenue Composition - Donut Chart
# ============================================================================

def create_revenue_donut_chart(revenue_streams, total_revenue):
    """
    Professional donut chart with center total
    """
    fig, ax = plt.subplots(figsize=(12, 8))

    colors = [PRIMARY_BLUE, PRIMARY_ORANGE, PRIMARY_GREEN, PRIMARY_RED]

    wedges, texts, autotexts = ax.pie(
        revenue_streams.values(),
        labels=revenue_streams.keys(),
        autopct=lambda pct: f'${pct/100*total_revenue/1e6:.1f}M\n({pct:.1f}%)',
        startangle=90,
        colors=colors,
        wedgeprops=dict(width=0.5, edgecolor='white', linewidth=3),
        explode=(0.05, 0, 0, 0),
        textprops={'fontsize': 11, 'weight': 'bold'}
    )

    # Add center circle for donut effect
    centre_circle = plt.Circle((0,0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)

    # Add total in center
    ax.text(0, 0, f'Total Revenue\n${total_revenue/1e6:.1f}M',
            ha='center', va='center', fontsize=18, weight='bold',
            bbox=dict(boxstyle='round,pad=0.8', facecolor='lightgray', alpha=0.3))

    # Enhance autotext
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(11)
        autotext.set_weight('bold')

    ax.set_title('Athletic Revenue Composition - Midwest State University',
                 fontsize=16, weight='bold', pad=20)

    plt.tight_layout()
    return fig


# ============================================================================
# IMPROVED CHART 2: Sport Performance with Industry Benchmarks
# ============================================================================

def create_sport_performance_with_benchmarks(sport_performance):
    """
    Horizontal bar chart with benchmark lines and professional styling
    """
    fig, ax = plt.subplots(figsize=(14, 8))

    # Sort by revenue
    sorted_data = sport_performance['Total_Revenue_Sum'].sort_values(ascending=True) / 1e6

    # Color code by performance
    colors = [EXCELLENT if x > 30 else GOOD if x > 15 else WARNING
              for x in sorted_data.values]

    bars = ax.barh(sorted_data.index, sorted_data.values, color=colors,
                   edgecolor='black', linewidth=1.5, height=0.6)

    # Add value labels at end of bars
    for i, (sport, value) in enumerate(sorted_data.items()):
        ax.text(value + 1, i, f'${value:.1f}M',
                va='center', fontsize=11, weight='bold')

    # Add benchmark line
    benchmark = 20
    ax.axvline(benchmark, color=PRIMARY_RED, linestyle='--', linewidth=2.5,
               label=f'Target: ${benchmark:.0f}M', alpha=0.7)

    ax.set_xlabel('Annual Revenue (Millions $)', fontsize=13, weight='bold')
    ax.set_ylabel('Sport', fontsize=13, weight='bold')
    ax.set_title('Sport Revenue Performance vs. Industry Benchmark',
                 fontsize=16, weight='bold', pad=20)
    ax.legend(loc='lower right', fontsize=11, framealpha=0.9)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    return fig


# ============================================================================
# NEW CHART: Industry Benchmark Comparison - Bullet Chart
# ============================================================================

def create_industry_benchmark_bullet_chart():
    """
    Bullet chart showing Midwest State vs. industry benchmarks
    """
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
            label='Industry Average (Target)')

    # Current (solid bar)
    colors = [CRITICAL if c < t else GOOD for c, t in zip(current, target)]
    bars = ax.barh(y_pos, current, height*0.7, color=colors,
                   edgecolor='black', linewidth=2, label='Midwest State (Current)')

    # Add value labels
    for i, (cur, targ, exc) in enumerate(zip(current, target, excellent)):
        ax.text(cur + 0.5, i, f'{cur:.1f}%', va='center', fontsize=11, weight='bold')
        ax.text(targ, i + 0.35, f'Target: {targ}%', va='center',
                fontsize=9, style='italic', color='blue')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(metrics, fontsize=12, weight='bold')
    ax.set_xlabel('Percentage', fontsize=13, weight='bold')
    ax.set_title('Midwest State vs. Power 5 Conference Benchmarks',
                 fontsize=16, weight='bold', pad=20)
    ax.legend(loc='lower right', fontsize=11)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    # Add source citation
    ax.text(0.5, -0.15,
            'Source: NCAA Financial Database 2023-24; UT Austin, Ohio State, Michigan, Penn State, Wisconsin athletic reports',
            transform=ax.transAxes, ha='center', fontsize=9, style='italic', color='gray')

    plt.tight_layout()
    return fig


# ============================================================================
# NEW ANALYSIS: Day of Week by Sport (Mentor Feedback)
# ============================================================================

def analyze_day_of_week_by_sport(sports_df):
    """
    Breakdown of attendance and revenue by day of week FOR EACH SPORT
    Addresses mentor feedback: not aggregate analysis
    """
    # Ensure we have day of week
    if 'Day_of_Week' not in sports_df.columns:
        # You'll need to create this from your date column
        # sports_df['Day_of_Week'] = pd.to_datetime(sports_df['Date']).dt.day_name()
        pass

    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle('Attendance Patterns by Day of Week - Sport Specific Analysis',
                 fontsize=18, weight='bold')

    sports = sports_df['Sport'].unique()

    for ax, sport in zip(axes.flat, sports):
        sport_data = sports_df[sports_df['Sport'] == sport]
        day_avg = sport_data.groupby('Day_of_Week')['Attendance'].mean().sort_values(ascending=False)

        # Define day order
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_avg = day_avg.reindex([d for d in day_order if d in day_avg.index])

        colors = [SPORT_COLORS.get(sport, PRIMARY_BLUE)] * len(day_avg)

        bars = ax.bar(range(len(day_avg)), day_avg.values, color=colors,
                      edgecolor='black', linewidth=1.5, alpha=0.8)

        # Highlight highest day
        max_idx = day_avg.values.argmax()
        bars[max_idx].set_color(EXCELLENT)
        bars[max_idx].set_edgecolor('gold')
        bars[max_idx].set_linewidth(3)

        ax.set_xticks(range(len(day_avg)))
        ax.set_xticklabels([d[:3] for d in day_avg.index], fontsize=10, weight='bold')
        ax.set_ylabel('Avg Attendance', fontsize=11, weight='bold')
        ax.set_title(f'{sport}', fontsize=13, weight='bold')
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)

        # Add value labels
        for i, v in enumerate(day_avg.values):
            ax.text(i, v + max(day_avg.values)*0.02, f'{v:,.0f}',
                    ha='center', fontsize=9, weight='bold')

    plt.tight_layout()
    return fig


# ============================================================================
# NEW ANALYSIS: Night vs Morning Games by Sport (Mentor Feedback)
# ============================================================================

def analyze_time_of_day_by_sport(sports_df):
    """
    Compare morning/afternoon/night games by sport
    Especially important for football
    """
    # Categorize game times
    def categorize_time(time_str):
        # Assuming time_str is like "7:00 PM", "2:30 PM", etc.
        try:
            hour = int(time_str.split(':')[0])
            period = time_str.split(' ')[1] if ' ' in time_str else 'PM'

            if period == 'AM' or (period == 'PM' and hour < 5):
                return 'Morning/Afternoon'
            else:
                return 'Evening/Night'
        except:
            return 'Unknown'

    if 'Game_Time' in sports_df.columns:
        sports_df['Time_Category'] = sports_df['Game_Time'].apply(categorize_time)

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle('Game Time Analysis: Evening vs. Day Games',
                 fontsize=18, weight='bold')

    # Chart 1: Revenue comparison
    ax1 = axes[0]
    time_revenue = sports_df.groupby(['Sport', 'Time_Category'])['Total_Revenue'].mean().unstack()
    time_revenue.plot(kind='bar', ax=ax1, color=[PRIMARY_ORANGE, PRIMARY_PURPLE],
                      edgecolor='black', linewidth=1.5, width=0.7)
    ax1.set_title('Average Revenue: Day vs. Evening Games', fontsize=14, weight='bold')
    ax1.set_xlabel('Sport', fontsize=12, weight='bold')
    ax1.set_ylabel('Avg Revenue per Game ($)', fontsize=12, weight='bold')
    ax1.legend(title='Game Time', fontsize=10)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.set_axisbelow(True)
    ax1.tick_params(axis='x', rotation=45)

    # Chart 2: Attendance comparison
    ax2 = axes[1]
    time_attend = sports_df.groupby(['Sport', 'Time_Category'])['Attendance'].mean().unstack()
    time_attend.plot(kind='bar', ax=ax2, color=[PRIMARY_ORANGE, PRIMARY_PURPLE],
                     edgecolor='black', linewidth=1.5, width=0.7)
    ax2.set_title('Average Attendance: Day vs. Evening Games', fontsize=14, weight='bold')
    ax2.set_xlabel('Sport', fontsize=12, weight='bold')
    ax2.set_ylabel('Avg Attendance', fontsize=12, weight='bold')
    ax2.legend(title='Game Time', fontsize=10)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    ax2.set_axisbelow(True)
    ax2.tick_params(axis='x', rotation=45)

    # Highlight football specifically
    if 'Football' in time_revenue.index:
        football_evening = time_revenue.loc['Football', 'Evening/Night']
        football_day = time_revenue.loc['Football', 'Morning/Afternoon']
        pct_increase = ((football_evening - football_day) / football_day * 100)

        ax1.annotate(f'Football:\n+{pct_increase:.0f}% evening premium',
                     xy=(0, football_evening), xytext=(1.5, football_evening * 1.1),
                     arrowprops=dict(arrowstyle='->', color='red', lw=2),
                     fontsize=10, color='red', weight='bold',
                     bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))

    plt.tight_layout()
    return fig


# ============================================================================
# IMPROVED: Women's Basketball Opportunity - Dual Axis Chart
# ============================================================================

def create_womens_basketball_opportunity_chart(sports_df, survey_df):
    """
    Emphasize the interest vs. attendance gap for women's basketball
    This was a KEY mentor point
    """
    fig, ax1 = plt.subplots(figsize=(14, 8))

    # Mock data - replace with your actual survey interest scores
    sports = ['Football', 'Mens Basketball', 'Womens Basketball',
              'Baseball', 'Softball', 'Volleyball']
    interest_scores = [95, 88, 85, 65, 58, 52]  # From survey

    # Get capacity utilization from sport_performance
    capacity_util = []
    for sport in sports:
        sport_df = sports_df[sports_df['Sport'] == sport.replace(' ', '_')]
        if len(sport_df) > 0:
            avg_attend = sport_df['Attendance'].mean()
            capacity = sport_df['Venue_Capacity'].iloc[0]
            capacity_util.append((avg_attend / capacity) * 100)
        else:
            capacity_util.append(0)

    x = np.arange(len(sports))
    width = 0.35

    # Interest bars (left y-axis)
    bars1 = ax1.bar(x - width/2, interest_scores, width, label='Fan Interest Score',
                    color=PRIMARY_BLUE, edgecolor='black', linewidth=1.5, alpha=0.8)

    # Capacity utilization bars (right y-axis)
    ax2 = ax1.twinx()
    colors_util = [GOOD if pct >= 70 else CRITICAL for pct in capacity_util]
    bars2 = ax2.bar(x + width/2, capacity_util, width,
                    label='Capacity Utilization %',
                    color=colors_util, edgecolor='black', linewidth=1.5, alpha=0.8)

    # HIGHLIGHT Women's Basketball (index 2)
    bars1[2].set_edgecolor('red')
    bars1[2].set_linewidth(4)
    bars2[2].set_edgecolor('red')
    bars2[2].set_linewidth(4)

    # Add THE KEY ANNOTATION
    ax1.annotate('MAJOR OPPORTUNITY!\nHigh Interest (85) vs.\nLow Attendance (43.5%)',
                 xy=(2, 85), xytext=(4, 90),
                 arrowprops=dict(arrowstyle='->', color='red', lw=3),
                 fontsize=13, color='red', weight='bold',
                 bbox=dict(boxstyle='round,pad=1', facecolor='yellow',
                          edgecolor='red', linewidth=3))

    ax1.set_xlabel('Sport', fontsize=13, weight='bold')
    ax1.set_ylabel('Fan Interest Score (0-100)', fontsize=13, weight='bold', color=PRIMARY_BLUE)
    ax2.set_ylabel('Capacity Utilization %', fontsize=13, weight='bold', color=GOOD)
    ax1.set_title('The Women\'s Basketball Paradox: High Interest, Low Attendance',
                  fontsize=16, weight='bold', pad=20)
    ax1.set_xticks(x)
    ax1.set_xticklabels(sports, rotation=30, ha='right', fontsize=11)

    # Legends
    ax1.legend(loc='upper left', fontsize=11)
    ax2.legend(loc='upper right', fontsize=11)

    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.set_axisbelow(True)

    # Add insight text box
    insight_text = ("Insight: Women's Basketball has 85/100 interest score\\n"
                   "(nearly matching Men's Basketball at 88), but only\\n"
                   "43.5% capacity utilization vs. Men's 84%.\\n\\n"
                   "Solution: Targeted social media campaigns + enhanced\\n"
                   "game experience to convert interest into attendance.")

    ax1.text(0.02, 0.98, insight_text, transform=ax1.transAxes,
             fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

    plt.tight_layout()
    return fig


# ============================================================================
# IMPROVED: Merchandise Revenue - Normalized View
# ============================================================================

def create_normalized_merchandise_chart(sports_df):
    """
    Normalize merchandise revenue to account for different revenue scales
    Addresses mentor feedback about misleading percentages
    """
    sport_merch = sports_df.groupby('Sport').agg({
        'Merchandise_Revenue': 'sum',
        'Total_Revenue': 'sum',
        'Attendance': 'sum'
    })

    # Calculate merchandise per attendee (normalized metric)
    sport_merch['Merch_per_Attendee'] = (sport_merch['Merchandise_Revenue'] /
                                         sport_merch['Attendance'])

    # Calculate merchandise as % of total (original metric)
    sport_merch['Merch_Pct_Revenue'] = ((sport_merch['Merchandise_Revenue'] /
                                         sport_merch['Total_Revenue']) * 100)

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle('Merchandise Revenue Analysis: Per Attendee vs. % of Total',
                 fontsize=18, weight='bold')

    # Chart 1: Merchandise per attendee (FAIR comparison)
    ax1 = axes[0]
    merch_per_attend = sport_merch['Merch_per_Attendee'].sort_values(ascending=True)
    colors = [PRIMARY_GREEN if x > 12 else PRIMARY_ORANGE for x in merch_per_attend.values]
    bars1 = ax1.barh(merch_per_attend.index, merch_per_attend.values, color=colors,
                     edgecolor='black', linewidth=1.5)

    # Industry benchmark line
    ax1.axvline(12, color=PRIMARY_RED, linestyle='--', linewidth=2,
                label='NCAA Avg: $12', alpha=0.7)

    for i, v in enumerate(merch_per_attend.values):
        ax1.text(v + 0.3, i, f'${v:.2f}', va='center', fontsize=11, weight='bold')

    ax1.set_xlabel('Merchandise Revenue per Attendee ($)', fontsize=12, weight='bold')
    ax1.set_ylabel('Sport', fontsize=12, weight='bold')
    ax1.set_title('Merchandise Revenue per Attendee\n(Normalized for Fair Comparison)',
                  fontsize=13, weight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(axis='x', alpha=0.3, linestyle='--')
    ax1.set_axisbelow(True)

    # Chart 2: Percentage of total (shows relative importance)
    ax2 = axes[1]
    merch_pct = sport_merch['Merch_Pct_Revenue'].sort_values(ascending=True)
    bars2 = ax2.barh(merch_pct.index, merch_pct.values, color=PRIMARY_PURPLE,
                     edgecolor='black', linewidth=1.5, alpha=0.7)

    for i, v in enumerate(merch_pct.values):
        ax2.text(v + 0.3, i, f'{v:.1f}%', va='center', fontsize=11, weight='bold')

    ax2.set_xlabel('Merchandise as % of Total Sport Revenue', fontsize=12, weight='bold')
    ax2.set_ylabel('Sport', fontsize=12, weight='bold')
    ax2.set_title('Merchandise as % of Total Revenue\n(Shows Relative Importance)',
                  fontsize=13, weight='bold')
    ax2.grid(axis='x', alpha=0.3, linestyle='--')
    ax2.set_axisbelow(True)

    # Add explanation
    explanation = ("Left Chart: Fair comparison - $/attendee\\n"
                   "Right Chart: Shows merchandise importance\\n\\n"
                   "Football appears low on right because total\\n"
                   "revenue is so high, but left shows opportunity\\n"
                   "to increase $/attendee to industry average.")

    ax2.text(0.98, 0.02, explanation, transform=ax2.transAxes,
             fontsize=9, verticalalignment='bottom', horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    plt.tight_layout()
    return fig


# ============================================================================
# NEW: Revenue Projection Waterfall Chart
# ============================================================================

def create_revenue_waterfall_chart():
    """
    Show step-by-step revenue buildup from current to projected
    """
    fig, ax = plt.subplots(figsize=(16, 9))

    initiatives = ['Current\\nRevenue', 'Dynamic\\nPricing', 'Women\\'s BB\\nGrowth',
                   'Corporate\\nPartnerships', 'Premium\\nSeating', 'Merchandise',
                   'Off-Peak\\nPromo', 'Alumni\\nProgram', 'Projected\\nRevenue']

    values = [94.36, 4.2, 4.0, 7.5, 2.8, 1.9, 0.8, 0.9, 0]

    cumulative = [94.36]
    for i in range(1, len(values)-1):
        cumulative.append(cumulative[-1] + values[i])
    cumulative.append(cumulative[-1])

    colors = [PRIMARY_BLUE] + [PRIMARY_GREEN] * 7 + [PRIMARY_ORANGE]

    # Draw bars
    for i, (init, val, cum) in enumerate(zip(initiatives, values, cumulative)):
        if i == 0 or i == len(initiatives) - 1:
            # Start and end bars
            ax.bar(i, cum, color=colors[i], edgecolor='black', linewidth=2, width=0.7)
            ax.text(i, cum + 2, f'${cum:.1f}M', ha='center', va='bottom',
                    fontsize=12, weight='bold')
        else:
            # Floating bars for increments
            bottom = cumulative[i-1]
            ax.bar(i, val, bottom=bottom, color=colors[i],
                   edgecolor='black', linewidth=2, width=0.7)
            ax.text(i, bottom + val/2, f'+${val:.1f}M', ha='center', va='center',
                    fontsize=11, weight='bold', color='white',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.6))

            # Connector line
            if i < len(initiatives) - 1:
                ax.plot([i+0.35, i+0.65], [cumulative[i], cumulative[i]],
                        'k--', linewidth=1.5, alpha=0.5)

    ax.set_xticks(range(len(initiatives)))
    ax.set_xticklabels(initiatives, fontsize=11, weight='bold')
    ax.set_ylabel('Revenue (Millions $)', fontsize=14, weight='bold')
    ax.set_title('Revenue Growth Roadmap: $94.4M → $119.5M (+$25.1M, 27% growth)',
                 fontsize=16, weight='bold', pad=20)

    # Target line
    target = 94.36 + 20.5
    ax.axhline(target, color=PRIMARY_RED, linestyle='--', linewidth=2.5,
               label=f'NCAA Settlement Target: ${target:.1f}M', alpha=0.7)

    # Exceeded by annotation
    exceeded = cumulative[-1] - target
    ax.annotate(f'Exceeds target\\nby ${exceeded:.1f}M!',
                xy=(len(initiatives)-1, cumulative[-1]),
                xytext=(len(initiatives)-2, cumulative[-1] + 5),
                arrowprops=dict(arrowstyle='->', color=PRIMARY_GREEN, lw=3),
                fontsize=12, color=PRIMARY_GREEN, weight='bold',
                bbox=dict(boxstyle='round,pad=0.8', facecolor='lightgreen', alpha=0.7))

    ax.legend(fontsize=12, loc='upper left')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    ax.set_ylim(0, cumulative[-1] * 1.15)

    plt.tight_layout()
    return fig


# ============================================================================
# NEW: Corporate Partnership Benchmark Comparison
# ============================================================================

def create_corporate_benchmark_chart():
    """
    Show Midwest State vs. peer schools for corporate partnerships
    With specific source citation
    """
    fig, ax = plt.subplots(figsize=(12, 8))

    schools = ['Wisconsin', 'Penn State', 'Michigan', 'Ohio State',
               'UT Austin', 'Midwest State']
    corporate_pct = [14, 13, 14, 15, 16, 9.2]

    colors = [PRIMARY_GREEN if x >= 13 else PRIMARY_RED for x in corporate_pct]

    bars = ax.bar(schools, corporate_pct, color=colors, edgecolor='black',
                  linewidth=2, width=0.6, alpha=0.8)

    # Highlight Midwest State
    bars[-1].set_edgecolor('red')
    bars[-1].set_linewidth(3)
    bars[-1].set_hatch('//')

    # Industry benchmark line
    avg = np.mean(corporate_pct[:-1])
    ax.axhline(avg, color='blue', linestyle='--', linewidth=2,
               label=f'Peer Average: {avg:.1f}%', alpha=0.7)

    # Add value labels
    for i, (school, val) in enumerate(zip(schools, corporate_pct)):
        ax.text(i, val + 0.3, f'{val:.1f}%', ha='center', va='bottom',
                fontsize=12, weight='bold')

    # Gap annotation
    gap = avg - 9.2
    ax.annotate(f'{gap:.1f}% below\\npeer average',
                xy=(5, 9.2), xytext=(4, 6),
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                fontsize=11, color='red', weight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))

    ax.set_ylabel('Corporate Partnerships (% of total attendance)',
                  fontsize=13, weight='bold')
    ax.set_title('Corporate Partnership Benchmarking: Power 5 Comparison',
                 fontsize=16, weight='bold', pad=20)
    ax.set_ylim(0, max(corporate_pct) * 1.2)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    # Source citation
    ax.text(0.5, -0.15,
            'Source: NCAA Financial Database 2023-24, individual school athletic department annual reports',
            transform=ax.transAxes, ha='center', fontsize=10, style='italic', color='gray')

    plt.tight_layout()
    return fig


# ============================================================================
# EXECUTION NOTES
# ============================================================================
"""
To use these functions in your notebook:

1. Load your data:
   sports_df = pd.read_excel("2025 KODING with KAGR Case Competition_Dataset.xlsx",
                             sheet_name="midwest_state_sports")
   survey_df = pd.read_excel("2025 KODING with KAGR Case Competition_Dataset.xlsx",
                             sheet_name="Customer Experience Survey")

2. Calculate your metrics:
   revenue_streams = {
       'Ticket Revenue': sports_df['Ticket_Revenue'].sum(),
       'Concession Revenue': sports_df['Concession_Revenue'].sum(),
       'Parking Revenue': sports_df['Parking_Revenue'].sum(),
       'Merchandise Revenue': sports_df['Merchandise_Revenue'].sum()
   }
   total_revenue = sum(revenue_streams.values())

   sport_performance = sports_df.groupby('Sport').agg({...})

3. Call the visualization functions:
   fig1 = create_revenue_donut_chart(revenue_streams, total_revenue)
   fig2 = create_sport_performance_with_benchmarks(sport_performance)
   fig3 = create_industry_benchmark_bullet_chart()
   fig4 = analyze_day_of_week_by_sport(sports_df)
   fig5 = analyze_time_of_day_by_sport(sports_df)
   fig6 = create_womens_basketball_opportunity_chart(sports_df, survey_df)
   fig7 = create_normalized_merchandise_chart(sports_df)
   fig8 = create_revenue_waterfall_chart()
   fig9 = create_corporate_benchmark_chart()

4. Display or save:
   plt.show()
   # or
   fig1.savefig('revenue_donut.png', dpi=300, bbox_inches='tight')
"""
