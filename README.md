# Travel Distance Calculator

This script automates the process of calculating travel times and distances between multiple pairs of coordinates using Google Maps. It uses Selenium WebDriver to interact with Google Maps and extract route information.

## Prerequisites

- Python 3.x
- Chrome browser installed
- ChromeDriver (matching your Chrome version)

## Installation

1. Clone this repository or download the script
2. Install required packages:
```bash
pip install -r requirements.txt
```

## Input File Format

The script expects an Excel file (`.xlsx`) with the following column structure:

| Origin | x1    | y1     | Destination | x2    | y2     |
|--------|-------|--------|-------------|-------|---------|
| 1      | 43.07 | -83.73 | 1          | 43.02 | -83.69 |

Where:
- `x1`, `y1`: Origin coordinates (latitude, longitude)
- `x2`, `y2`: Destination coordinates (latitude, longitude)

## Usage

1. Place your input Excel file (named `coordinates.xlsx`) in the same directory as the script
2. Run the script:
```bash
python distance_calculator.py
```

## Output

The script generates a CSV file (`coordinates_with_travel_info.csv`) containing all original columns plus two new columns:
- `Travel Time (min)`: Travel time in minutes
- `Total Distance (miles)`: Travel distance in miles

If the script fails to process a particular row, it will mark the values as 'N.A.' and continue with the next row.

## Notes

- The script currently processes a subset of rows (configurable in the code)
- Each request includes appropriate delays to respect Google Maps' service
- Failed requests are handled gracefully and marked as 'N.A.' in the output
- Screenshots are saved for debugging purposes when errors occur

## Limitations

- Depends on Google Maps web interface
- Processing speed is limited by necessary delays between requests
- May require adjustments if Google Maps interface changes 
