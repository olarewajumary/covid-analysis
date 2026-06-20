import matplotlib.pyplot as plt
import seaborn as sns

def plot_top_cases(df, output_path='output/top_cases.png'):
    latest = df.groupby('location')['total_cases'].max().reset_index()
    top10 = latest.sort_values('total_cases', ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=top10, x='total_cases', y='location', ax=ax, palette='Reds_r')

    ax.set_title('Top 10 Countries by Total COVID-19 Cases')
    ax.set_xlabel('Total Cases')
    ax.set_ylabel('')
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x/1e6:.1f}M'))

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Saved: {output_path}")

def plot_global_trend(df, output_path='output/global_trend.png'):
    global_trend = df.groupby('date')['new_cases'].sum().reset_index()
    global_trend['7day_avg'] = global_trend['new_cases'].rolling(7).mean()

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.fill_between(global_trend['date'], global_trend['new_cases'], alpha=0.3, color='steelblue')
    ax.plot(global_trend['date'], global_trend['7day_avg'], color='steelblue', linewidth=2)

    ax.set_title('Global COVID-19 New Cases Over Time')
    ax.set_xlabel('')
    ax.set_ylabel('New Cases')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x/1e6:.1f}M'))

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Saved: {output_path}")

def plot_death_rate(df, output_path='output/death_rate.png'):
    latest = df.groupby('location')['total_deaths_per_million'].max().reset_index()
    top10 = latest.sort_values('total_deaths_per_million', ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=top10, x='total_deaths_per_million', y='location', ax=ax, palette='OrRd_r')

    ax.set_title('Top 10 Countries by COVID-19 Deaths per Million')
    ax.set_xlabel('Deaths per Million')
    ax.set_ylabel('')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Saved: {output_path}")

def plot_vaccination_rollout(df, output_path='output/vaccination_rollout.png'):
    vax = df.groupby(['date', 'continent'])['people_vaccinated_per_hundred'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(14, 6))
    for continent in vax['continent'].unique():
        data = vax[vax['continent'] == continent]
        ax.plot(data['date'], data['people_vaccinated_per_hundred'], label=continent, linewidth=2)

    ax.set_title('COVID-19 Vaccination Rollout by Continent')
    ax.set_xlabel('')
    ax.set_ylabel('% Population Vaccinated')
    ax.legend(loc='upper left')
    ax.set_ylim(0, 100)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Saved: {output_path}")

def plot_gdp_vs_vaccination(df, output_path='output/gdp_vs_vaccination.png'):
    latest = df.groupby('location').agg(
        gdp=('gdp_per_capita', 'max'),
        vax_rate=('people_fully_vaccinated_per_hundred', 'max'),
        continent=('continent', 'first')
    ).reset_index().dropna()

    fig, ax = plt.subplots(figsize=(12, 7))
    continents = latest['continent'].unique()
    colors = sns.color_palette('tab10', len(continents))

    for i, continent in enumerate(continents):
        data = latest[latest['continent'] == continent]
        ax.scatter(data['gdp'], data['vax_rate'], label=continent, color=colors[i], alpha=0.7, s=60)

    ax.set_title('GDP per Capita vs Full Vaccination Rate by Country')
    ax.set_xlabel('GDP per Capita (USD)')
    ax.set_ylabel('% Fully Vaccinated')
    ax.legend(title='Continent')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Saved: {output_path}")

def plot_cases_by_continent(df, output_path='output/cases_by_continent.png'):
    latest = df.groupby(['location', 'continent'])['total_cases_per_million'].max().reset_index()
    continent_avg = latest.groupby('continent')['total_cases_per_million'].mean().reset_index()
    continent_avg = continent_avg.sort_values('total_cases_per_million', ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=continent_avg, x='continent', y='total_cases_per_million', ax=ax, palette='Blues_r')

    ax.set_title('Average COVID-19 Cases per Million by Continent')
    ax.set_xlabel('')
    ax.set_ylabel('Cases per Million')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x/1e3:.0f}K'))

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Saved: {output_path}")

def plot_reproduction_rate(df, output_path='output/reproduction_rate.png'):
    r_trend = df.groupby('date')['reproduction_rate'].mean().reset_index()
    r_trend['7day_avg'] = r_trend['reproduction_rate'].rolling(7).mean()

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(r_trend['date'], r_trend['7day_avg'], color='darkorange', linewidth=2)
    ax.axhline(y=1, color='red', linestyle='--', linewidth=1.5, label='R = 1 threshold')

    ax.set_title('Global COVID-19 Reproduction Rate Over Time')
    ax.set_xlabel('')
    ax.set_ylabel('Reproduction Rate (R)')
    ax.legend()

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Saved: {output_path}")

def plot_icu_patients(df, output_path='output/icu_patients.png'):
    peak_icu = df.groupby('location')['icu_patients_per_million'].max().reset_index()
    peak_icu = peak_icu.dropna()
    top10 = peak_icu.sort_values('icu_patients_per_million', ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=top10, x='icu_patients_per_million', y='location', ax=ax, palette='Purples_r')

    ax.set_title('Top 10 Countries by Peak ICU Patients per Million')
    ax.set_xlabel('ICU Patients per Million')
    ax.set_ylabel('')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Saved: {output_path}")

def plot_age_vs_deaths(df, output_path='output/age_vs_deaths.png'):
    latest = df.groupby('location').agg(
        median_age=('median_age', 'max'),
        death_rate=('total_deaths_per_million', 'max'),
        continent=('continent', 'first')
    ).reset_index().dropna()

    fig, ax = plt.subplots(figsize=(12, 7))
    continents = latest['continent'].unique()
    colors = sns.color_palette('tab10', len(continents))

    for i, continent in enumerate(continents):
        data = latest[latest['continent'] == continent]
        ax.scatter(data['median_age'], data['death_rate'], label=continent, color=colors[i], alpha=0.7, s=60)

    ax.set_title('Median Age vs COVID-19 Deaths per Million')
    ax.set_xlabel('Median Age')
    ax.set_ylabel('Deaths per Million')
    ax.legend(title='Continent')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Saved: {output_path}")

def plot_africa_vs_europe(df, output_path='output/africa_vs_europe.png'):
    continents = ['Africa', 'Europe']
    filtered = df[df['continent'].isin(continents)]
    trend = filtered.groupby(['date', 'continent'])['new_cases_per_million'].mean().reset_index()

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    for i, continent in enumerate(continents):
        data = trend[trend['continent'] == continent]
        data = data.copy()
        data['7day_avg'] = data['new_cases_per_million'].rolling(7).mean()
        color = 'steelblue' if continent == 'Europe' else 'darkorange'
        axes[i].fill_between(data['date'], data['new_cases_per_million'], alpha=0.3, color=color)
        axes[i].plot(data['date'], data['7day_avg'], color=color, linewidth=2)
        axes[i].set_title(f'New Cases per Million — {continent}')
        axes[i].set_xlabel('')
        axes[i].set_ylabel('New Cases per Million')

    plt.suptitle('Africa vs Europe: COVID-19 New Cases per Million', fontsize=14)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Saved: {output_path}")

import plotly.express as px

def plot_interactive_vaccinations(df, output_path='output/interactive_vaccinations.html'):
    fig = px.choropleth(
        df,
        locations='iso_code',
        color='people_fully_vaccinated_per_hundred',
        hover_name='location',
        animation_frame=df['date'].dt.year.astype(str),
        color_continuous_scale='Blues',
        title='Global Full Vaccination Rate Over Time',
        labels={'people_fully_vaccinated_per_hundred': '% Fully Vaccinated'}
    )

    fig.update_layout(
        geo=dict(showframe=False, showcoastlines=True),
        coloraxis_colorbar=dict(title='% Vaccinated')
    )

    fig.write_html(output_path)
    print(f"Saved: {output_path}")