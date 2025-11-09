"""
Lab 4: Statistical Analysis
Descriptive Statistics and Probability Distributions
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import norm, binom, poisson, expon

# -------------------------------
# Data Loading
# -------------------------------
import os

def load_data(filename):
    """Load CSV from the same folder as this script."""
    dir_path = os.path.dirname(os.path.abspath(__file__))  # Python dosyasının bulunduğu klasör
    file_path = os.path.join(dir_path, filename)           # Dosya yolu oluştur
    return pd.read_csv(file_path)

# -------------------------------
# Descriptive Statistics
# -------------------------------
def calculate_descriptive_stats(data, column):  # Function to calculate descriptive statistics for a specified column in a DataFrame.
    col = data[column].dropna()                 # Drop missing values from the specified column
    mean = col.mean()                           
    median = col.median()
    mode_val = col.mode()[0]                    # Take the first mode if multiple exist.
    std = col.std()
    var = col.var()
    rng = col.max() - col.min()                 # Calculate the range (max - min) of the column.
    q1 = col.quantile(0.25)
    q2 = col.quantile(0.5)
    q3 = col.quantile(0.75)                     # Calculate the first quartile (Q1), median (Q2), and third quartile (Q3)
    iqr = q3 - q1                               # Calculate the interquartile range (IQR = Q3 - Q1).
    skew = col.skew()                           # Calculate skewness to measure the asymmetry of the distribution.
    kurt = col.kurtosis()                       # Calculate kurtosis to measure the flatness / sharpness of the distribution.
    
    print(f"=== Descriptive Statistics for {column} ===")
    print(f"mean: {mean:.2f}")
    print(f"median: {median:.2f}")
    print(f"mode: {mode_val:.2f}")
    print(f"std: {std:.2f}")
    print(f"variance: {var:.2f}")
    print(f"range: {rng:.2f}")
    print(f"IQR: {iqr:.2f}")
    print(f"skewness: {skew:.2f}")
    print(f"kurtosis: {kurt:.2f}")
    print(f"min: {col.min():.2f}")
    print(f"Q1: {q1:.2f}")
    print(f"Q2: {q2:.2f}")
    print(f"Q3: {q3:.2f}")
    print(f"max: {col.max():.2f}\n")
    
    return mean, std, q1, q2, q3                # Return key statistics for further use

# -------------------------------
# Distribution Plot
# -------------------------------
def plot_distribution(data, column):
    col = data[column].dropna()
    mean, median, mode_val = col.mean(), col.median(), col.mode()[0]
    
    plt.figure(figsize=(8,5))
    plt.hist(col, bins=30, density=True, color='skyblue', alpha=0.7, edgecolor='black')
    # Plot histogram of data: 30 intervals, 70% opacity for better visibility with overlays
    plt.axvline(mean, color='red', linestyle='--', label='Mean')
    plt.axvline(median, color='green', linestyle='-.', label='Median')  # Add vertical axis line for median
    plt.axvline(mode_val, color='orange', linestyle=':', label='Mode')
    plt.title(f'{column} Distribution')
    plt.xlabel(column)
    plt.ylabel('Density')
    plt.legend()
    plt.show()

# -------------------------------
# Distribution Fitting
# -------------------------------
def plot_distribution_fitting(data, column, fitted_dist):
    col = data[column].dropna()
    plt.figure(figsize=(8,5))
    plt.hist(col, bins=30, density=True, color='skyblue', alpha=0.7, edgecolor='black')
    x = np.linspace(col.min(), col.max(), 100)                                                   # Generate 100 evenly spaced values within data range
    plt.plot(x, norm.pdf(x, fitted_dist[0], fitted_dist[1]), 'r--', lw=2, label='Fitted Normal') # Overlay fitted normal distribution curve
                                                                                                 # fitted_dist[0] = mean, fitted_dist[1] = standard deviation 
    plt.title(f'{column} Distribution with Fitted Normal')
    plt.xlabel(column)
    plt.ylabel('Density')
    plt.legend()
    plt.show()

# -------------------------------
# Material Comparison Boxplot
# -------------------------------
def plot_material_comparison(data, column='yield_strength_mpa', group_column='material_type'):
    plt.figure(figsize=(8,5))
    sns.boxplot(x=group_column, y=column, hue=group_column, data=data, palette='Set2', dodge=False, legend=False)
    # hue = which variable to use for coloring. Each group gets a different color.
    # dodge = whether boxes should be side by side or stacked. False stacks them, True puts them side by side.
    plt.title('Material Strength Comparison')
    plt.xlabel(group_column)
    plt.ylabel(column)
    plt.show()

# -------------------------------
# Probability Distributions Plot
# -------------------------------
def plot_probability_distributions():
    # --------------------
    # Binomial Scenario
    # --------------------
    n_bin = 100
    p_bin = 0.05
    x_bin = np.arange(0, 16)  # 0-15 defekt için
    y_bin = binom.pmf(x_bin, n_bin, p_bin)

    # --------------------
    # Poisson Scenario
    # --------------------
    lambda_pois = 10          # Average rate of events (e.g., 10 trucks per hour)
    x_pois = np.arange(0, 25) # Possible number of events (0 to 24 trucks)
    y_pois = poisson.pmf(x_pois, lambda_pois) # Probability for each number of events

    # --------------------
    # Normal Scenario
    # --------------------
    mu_norm = 250             # Mean of the distribution (average steel strength)
    sigma_norm = 15           # Standard deviation (spread of steel strength)
    x_norm = np.linspace(200, 300, 400) # 400 points from 200 to 300 for plotting
    y_norm = norm.pdf(x_norm, mu_norm, sigma_norm) # PDF values for each x

    # --------------------
    # Exponential Scenario
    # --------------------
    mean_exp = 1000            # Mean lifetime of a component (1000 hours)
    x_exp = np.linspace(0, 3000, 400) # 400 points from 0 to 3000 hours for plotting
    y_exp = expon.pdf(x_exp, scale=mean_exp) # PDF values for each x

    # 2x2 subplot
    fig, axs = plt.subplots(2, 2, figsize=(14,10))

    # Binomial
    axs[0,0].bar(x_bin, y_bin, color='skyblue', edgecolor='black')
    axs[0,0].bar(3, binom.pmf(3, n_bin, p_bin), color='orange', label='Exactly 3 defective')
    axs[0,0].bar(x_bin[x_bin<=5], y_bin[x_bin<=5], color='green', alpha=0.5, label='≤ 5 defective')
    axs[0,0].set_title('Binomial Distribution', pad=15)
    axs[0,0].set_xlabel('Number of Defective Components', labelpad=10)
    axs[0,0].set_ylabel('Probability', labelpad=10)
    axs[0,0].legend()

    # Poisson
    axs[0,1].bar(x_pois, y_pois, color='lightgreen', edgecolor='black')
    axs[0,1].bar(8, poisson.pmf(8, lambda_pois), color='orange', label='Exactly 8 trucks')
    axs[0,1].bar(x_pois[x_pois>15], y_pois[x_pois>15], color='red', alpha=0.5, label='> 15 trucks')
    axs[0,1].set_title('Poisson Distribution', pad=15)
    axs[0,1].set_xlabel('Number of Trucks', labelpad=10)
    axs[0,1].set_ylabel('Probability', labelpad=10)
    axs[0,1].legend()

    # Normal
    axs[1,0].plot(x_norm, y_norm, color='orange')
    axs[1,0].fill_between(x_norm, 0, y_norm, where=(x_norm>280), color='red', alpha=0.3, label='> 280 MPa')
    axs[1,0].set_title('Normal Distribution', pad=15)
    axs[1,0].set_xlabel('Yield Strength (MPa)', labelpad=10)
    axs[1,0].set_ylabel('Density', labelpad=10)
    axs[1,0].legend()

    # Exponential
    axs[1,1].plot(x_exp, y_exp, color='purple')
    axs[1,1].fill_between(x_exp, 0, y_exp, where=(x_exp<500), color='red', alpha=0.3, label='Failure < 500h')
    axs[1,1].fill_between(x_exp, 0, y_exp, where=(x_exp>1500), color='green', alpha=0.3, label='Survive > 1500h')
    axs[1,1].set_title('Exponential Distribution', pad=15)
    axs[1,1].set_xlabel('Lifetime (hours)', labelpad=10)
    axs[1,1].set_ylabel('Density', labelpad=10)
    axs[1,1].legend()

    plt.tight_layout(pad=3.0)
    plt.show()

    # --------------------
    # Probability Calculations 
    # --------------------
    prob_bin_3 = binom.pmf(3, n_bin, p_bin)
    prob_bin_le5 = binom.cdf(5, n_bin, p_bin)
    prob_pois_8 = poisson.pmf(8, lambda_pois)
    prob_pois_gt15 = 1 - poisson.cdf(15, lambda_pois)
    prob_norm_gt280 = 1 - norm.cdf(280, mu_norm, sigma_norm)
    percentile_95_norm = norm.ppf(0.95, mu_norm, sigma_norm)
    prob_exp_lt500 = expon.cdf(500, scale=mean_exp) # Calculate the probability that the component fails before 500 hours
                                                    # expon.cdf(x, scale=mean_exp) gives P(X <= x), i.e., the probability that lifetime X is less than or equal to x
    prob_exp_gt1500 = 1 - expon.cdf(1500, scale=mean_exp) # Calculate the probability that the component survives beyond 1500 hours
                                                          # expon.cdf(1500, scale=mean_exp) gives P(X <= 1500), so subtracting from 1 gives P(X > 1500)

    # Printing the probabilities
    print(f"Binomial: P(X=3) = {prob_bin_3:.3f}")
    print(f"Binomial: P(X≤5) = {prob_bin_le5:.3f}")
    print(f"Poisson: P(X=8) = {prob_pois_8:.3f}")
    print(f"Poisson: P(X>15) = {prob_pois_gt15:.3f}")
    print(f"Normal: P(X>280) = {prob_norm_gt280:.3f}")
    print(f"Normal: 95th percentile = {percentile_95_norm:.3f}")
    print(f"Exponential: P(X<500) = {prob_exp_lt500:.3f}")
    print(f"Exponential: P(X>1500) = {prob_exp_gt1500:.3f}")

# -------------------------------
# Statistical Summary Dashboard
# -------------------------------
def plot_statistical_dashboard(concrete_data):
    col = concrete_data['strength_mpa'].dropna()
    fig, axs = plt.subplots(2,2, figsize=(12,8))        # Create a 2x2 grid of subplots
    
    # Histogram
    axs[0,0].hist(col, bins=20, color='skyblue', edgecolor='black')
    axs[0,0].set_title('Histogram')
    
    # Boxplot
    # Calculate quartiles
    q1 = col.quantile(0.25)
    median = col.median()
    q3 = col.quantile(0.75)

    # Draw boxplot
    sns.boxplot(y=col, ax=axs[0,1], color='lightblue')

    # Add Q1, Median, Q3 as text
    axs[0,1].text(0, q1, f"Q1 = {q1:.2f}", color='blue')
    axs[0,1].text(0, median, f"Median = {median:.2f}", color='green')
    axs[0,1].text(0, q3, f"Q3 = {q3:.2f}", color='red')

    # QQ-plot (Quantile-Quantile plot)
    # QQ-plot: Compare data quantiles with a theoretical normal distribution
    # If points lie approximately on a straight line, the data is normally distributed
    stats.probplot(col, dist="norm", plot=axs[1,0])
    axs[1,0].set_title('QQ Plot')
    
    # Density
    # used to visualize the probability density of the data
    # the peak shows where the data is most concentrated
    sns.kdeplot(col, ax=axs[1,1], color='green') # KDE provides a smooth, continuous approximation of the probability density function
    axs[1,1].set_title('Density Plot')
    
    plt.tight_layout()
    plt.show()

# -------------------------------
# Bayes Theorem Application
# -------------------------------
def bayes_structural_damage():

    # Given
    P_damage = 0.05
    P_no_damage = 1 - P_damage
    sensitivity = 0.95                                                  # Test sensitivity: P(Test positive | Damage)
    specificity = 0.90                                                  # Test specificity: P(Test negative | No damage)
    false_positive = 1 - specificity                                    

    # Bayes Calculation
    P_positive = sensitivity*P_damage + false_positive*P_no_damage      # Total probability of a positive test
    P_damage_given_positive = (sensitivity*P_damage) / P_positive       # Bayes' theorem: P(Damage | Positive test)
    print(f"P(Damage | Positive Test) = {P_damage_given_positive:.3f}")

    # Probability Tree Görselleştirme
    fig, ax = plt.subplots(figsize=(10,6))
    # Root
    ax.text(0.1, 0.9, "Structure", fontsize=12, ha='center')

    # Branches
    ax.text(0.3, 0.8, "Damage\n0.05", fontsize=10, ha='center')
    ax.text(0.3, 0.6, "No Damage\n0.95", fontsize=10, ha='center')

    # Outcomes for Damage
    ax.text(0.55, 0.85, "Positive\n0.95", fontsize=10, ha='center')
    ax.text(0.55, 0.75, "Negative\n0.05", fontsize=10, ha='center')

    # Outcomes for No Damage (geniş aralık verdik)
    ax.text(0.55, 0.58, "Positive\n0.10", fontsize=10, ha='center')
    ax.text(0.55, 0.48, "Negative\n0.90", fontsize=10, ha='center')

    # Oklar
    # Root -> Damage / No Damage
    ax.annotate("", xy=(0.25,0.805), xytext=(0.12,0.9), arrowprops=dict(arrowstyle="->"))
    ax.annotate("", xy=(0.25,0.605), xytext=(0.12,0.9), arrowprops=dict(arrowstyle="->"))

    # Damage -> Positive / Negative
    ax.annotate("", xy=(0.50,0.85), xytext=(0.32,0.8), arrowprops=dict(arrowstyle="->"))
    ax.annotate("", xy=(0.50,0.75), xytext=(0.32,0.8), arrowprops=dict(arrowstyle="->"))

    # No Damage -> Positive / Negative
    ax.annotate("", xy=(0.50,0.58), xytext=(0.32,0.6), arrowprops=dict(arrowstyle="->"))
    ax.annotate("", xy=(0.50,0.48), xytext=(0.32,0.6), arrowprops=dict(arrowstyle="->"))
    
    ax.axis('off')    # Hide axis for cleaner visualization
    plt.title("Probability Tree: Structural Damage Detection")
    plt.show()

# -------------------------------
# Report File
# -------------------------------
def create_statistical_report(mean,std,q1,q2,q3,file='lab4_statistical_report.txt'):
    with open(file,'w') as f:                          # Open the file in write mode (overwrites if it already exists)
        f.write("Lab 4 Statistical Report\n")
        f.write("=======================\n")
        f.write(f"Mean: {mean:.2f}\nStd: {std:.2f}\n") # Write mean and standard deviation
        f.write(f"Q1: {q1:.2f}, Q2: {q2:.2f}, Q3: {q3:.2f}\n") # Write quartiles
    print(f"Report saved to {file}")

# -------------------------------
# Main Execution
# -------------------------------
def main():
    # Load datasets
    concrete_data = load_data("concrete_strength.csv")
    material_data = load_data("material_properties.csv")
    structural_data = load_data("structural_loads.csv")
    
    # 1. Concrete Strength Analysis
    mean, std, q1, q2, q3 = calculate_descriptive_stats(concrete_data, 'strength_mpa')
    plot_distribution(concrete_data, 'strength_mpa')
    plot_distribution_fitting(concrete_data, 'strength_mpa', (mean,std))
    
    # 2. Material Comparison
    plot_material_comparison(material_data)
    
    # 3. Probability Distributions
    plot_probability_distributions()          # Visualize Binomial, Poisson, Normal, and Exponential distributions
    
    # 4. Statistical Dashboard
    plot_statistical_dashboard(concrete_data) # Combine histogram, boxplot, QQ-plot, and KDE into one dashboard

    # 5. Bayes Theorem Application
    bayes_structural_damage()
       
    # 6. Create Report
    create_statistical_report(mean,std,q1,q2,q3) # Save key statistics to a text file

if __name__=="__main__": # Run the main function
    main()
