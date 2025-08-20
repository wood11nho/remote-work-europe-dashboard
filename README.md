# 📈 Remote Work in Europe Dashboard

An interactive Streamlit dashboard analyzing remote work adoption trends across European countries from 2022 to 2024, with a special focus on Romania's position and household internet access as a key enabler.

## 🚀 Features

- **Interactive Dumbbell Chart**: Compare 2022 vs 2024 remote work percentages across European countries
- **Choropleth Map**: Visualize household internet access levels across Europe
- **Romania Focus**: Dedicated KPI section highlighting Romania's performance vs EU average
- **Dynamic Sorting**: Sort countries by remote work adoption, growth, or alphabetically
- **Rich Tooltips**: Comprehensive hover information with trends and additional metrics

## 📊 Key Insights

- Finland leads Europe in remote work adoption (84.54% in 2024)
- Romania ranks 29th with 34.88% remote work adoption in 2024
- Strong correlation between internet access and remote work capabilities
- Most European countries showed positive growth in remote work from 2022-2024

## 🛠️ Technologies Used

- **Python 3.8+**
- **Streamlit** - Web application framework
- **Plotly** - Interactive visualizations
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computations

## 📁 Project Structure

```
├── app.py                              # Main Streamlit application
├── romania_remote_work_prepared_data.csv  # Processed dataset
├── Remote_work_in_Romania.csv          # Raw remote work data
├── Households - level of internet access.csv  # Raw internet access data
├── explore_data.ipynb                  # Data exploration and preprocessing
├── requirements.txt                    # Python dependencies
└── README.md                          # Project documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/remote-work-europe-dashboard.git
cd remote-work-europe-dashboard
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:
```bash
streamlit run app.py
```

4. Open your browser to `http://localhost:8501`

## 📈 Data Sources

- **Remote Work Data**: European Union statistics on enterprises conducting remote meetings
- **Internet Access Data**: Household internet access statistics across European countries
- **Time Period**: 2022-2024 comparison data
- **Geographic Coverage**: 27 EU countries plus additional European nations

## 🎯 Dashboard Sections

### 1. Key Performance Indicators (KPIs)
- Romania's remote work percentage (2024)
- Romania vs EU average comparison
- Romania's internet access statistics

### 2. Evolution of Remote Work
- Interactive dumbbell chart showing 2022 vs 2024 comparison
- Color-coded growth indicators
- Multiple sorting options

### 3. Supporting Context Map
- Choropleth visualization of internet access levels
- Toggle between current levels and growth rates

### 4. Data Explorer
- Full dataset view with all countries and metrics

## 📝 Data Processing

The data preprocessing workflow is documented in `explore_data.ipynb`:

1. Load raw CSV files
2. Clean and standardize column names
3. Handle missing values and data types
4. Create derived metrics (growth rates, trends)
5. Add ISO country codes for mapping
6. Export processed dataset

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Elias-Valeriu Stoica**
- LinkedIn: [Elias-Valeriu Stoica](https://www.linkedin.com/in/elias-valeriu-stoica-462872229/)

## 🙏 Acknowledgments

- Data sources: European Union statistical offices
- Romanian Data Tribe community for project inspiration
- Streamlit and Plotly teams for excellent visualization tools

---
*Built with ❤️ for data-driven insights into Europe's remote work landscape*